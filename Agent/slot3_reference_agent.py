"""Erweiterter gemeinsamer Referenzagent nach Slot 3.

Der Agent unterstützt lesende GET-Anfragen, JSON-POST-Anfragen und ein
kontrolliertes Ende. Er hält den HTTP-Sitzungszustand, erzeugt strukturierte
Observations und gibt Aktions- oder Werkzeugfehler an die Schleife zurück.
Neben der Pflichtlösung enthält er die optionalen Verbesserungen aus dem
Aufgabenblatt. Die reine Pflichtlösung steht in ``slot3_solution_minimal.py``.
"""

import argparse
import json
import os
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from dotenv import load_dotenv
from llm_provider import resolve_model_route

load_dotenv()

DEFAULT_TARGET_BASE_URL = os.getenv(
    "TARGET_BASE_URL",
    "http://127.0.0.1:3000",
)
ALLOWED_TARGET_HOSTS = {"127.0.0.1", "localhost"}
ALLOWED_TARGET_PORT = 3000
MAX_STEPS = 10
MAX_BODY_CHARS = 4000
MAX_MODEL_ATTEMPTS = 3

TARGET_SESSION = requests.Session()

SYSTEM_PROMPT = """
Du bist ein einfacher Web-Agent in einer isolierten Workshop-Umgebung.
Arbeite schrittweise auf das Ziel hin. Nutze nur relative Pfade der
bereitgestellten Zielanwendung.

Antworte immer mit genau einem JSON-Objekt in einem dieser Formate:

{"type": "http_get", "reason": "kurze Begründung", "path": "/pfad"}
{"type": "http_post", "reason": "kurze Begründung", "path": "/pfad", "json_body": {"name": "wert"}}
{"type": "finish", "reason": "kurze Begründung", "answer": "deine Antwort"}

Nutze http_get, um Seiten oder Ressourcen zu untersuchen. Nutze http_post für
JSON-Anfragen. Prüfe Statuscode und Antwortinhalt. Wiederhole eine erfolglose
Aktion nicht unverändert. Nutze finish erst, wenn eine Observation den Erfolg
belegt. Gib keinen Text vor oder nach dem JSON-Objekt aus.
""".strip()


def call_model(messages: list[dict[str, str]]) -> str:
    """Ruft das Modell primär über LiteLLM auf."""
    route = resolve_model_route()

    for attempt in range(1, MAX_MODEL_ATTEMPTS + 1):
        try:
            response = requests.post(
                route.chat_completions_url,
                headers=route.headers,
                json={
                    "model": route.model,
                    "messages": messages,
                    "response_format": {"type": "json_object"},
                    "temperature": 0,
                },
                timeout=60,
            )
            response.raise_for_status()
            model_output = response.json()["choices"][0]["message"]["content"]
            if not isinstance(model_output, str):
                raise TypeError("Die Modellantwort ist kein Text.")
            return model_output
        except (
            requests.RequestException,
            KeyError,
            IndexError,
            TypeError,
        ) as error:
            print(
                f"Modellanfrage über {route.provider} fehlgeschlagen "
                f"({attempt}/{MAX_MODEL_ATTEMPTS}): "
                f"{error}"
            )

    raise RuntimeError("Das Modell konnte dreimal nicht aufgerufen werden.")


def parse_action(model_output: str) -> dict[str, Any]:
    """Prüft die Modellantwort und gibt eine ausführbare Aktion zurück."""
    if not isinstance(model_output, str):
        raise ValueError("Die Modellantwort ist leer oder kein Text.")

    try:
        action = json.loads(model_output)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Modellantwort ist kein gültiges JSON: {model_output}"
        ) from error

    if not isinstance(action, dict):
        raise ValueError("Die Modellantwort muss ein JSON-Objekt sein.")
    if action.get("type") not in {"http_get", "finish", "http_post"}:
        raise ValueError("'type' muss 'http_get', 'http_post' oder 'finish' sein.")
    if not isinstance(action.get("reason"), str) or not action["reason"].strip():
        raise ValueError("Die Aktion benötigt eine kurze 'reason'.")
    if action["type"] == "http_get" and not isinstance(action.get("path"), str):
        raise ValueError("http_get benötigt einen 'path'.")
    if action["type"] == "http_post":
        if not isinstance(action.get("path"), str):
            raise ValueError("http_post benötigt einen 'path'.")
        if not isinstance(action.get("json_body"), dict):
            raise ValueError("http_post benötigt ein 'json_body' als JSON-Objekt.")
    if action["type"] == "finish" and not isinstance(action.get("answer"), str):
        raise ValueError("finish benötigt eine 'answer'.")

    return action


def validate_target_base_url(value: str) -> str:
    """Prüft die explizit freigegebene lokale Workshop-Zieladresse."""
    parsed = urlparse(value)

    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError("Die Zieladresse enthält keinen gültigen Port.") from error

    if parsed.scheme != "http":
        raise ValueError("Die Zieladresse muss das Schema 'http' verwenden.")
    if parsed.username or parsed.password:
        raise ValueError("Die Zieladresse darf keine Zugangsdaten enthalten.")
    if parsed.hostname not in ALLOWED_TARGET_HOSTS:
        raise ValueError(
            "Als Zielhost sind nur '127.0.0.1' und 'localhost' erlaubt."
        )
    if port != ALLOWED_TARGET_PORT:
        raise ValueError("Als Zielport ist nur Port 3000 erlaubt.")
    if (
        parsed.path not in {"", "/"}
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "Die Zieladresse muss eine Basisadresse ohne Pfad, Parameter oder "
            "Fragment sein."
        )

    return f"http://{parsed.hostname}:{port}"


def target_url(target_base_url: str, path: str) -> str:
    """Erzeugt eine URL innerhalb der festgelegten Zielanwendung."""
    parsed_path = urlparse(path)
    if parsed_path.scheme or parsed_path.netloc or not path.startswith("/"):
        raise ValueError("Werkzeuge akzeptieren nur relative Pfade wie '/'.")
    return urljoin(f"{target_base_url.rstrip('/')}/", path.lstrip("/"))


def response_observation(
    method: str,
    path: str,
    response: requests.Response,
) -> str:
    """Bereitet Anfrage und Antwort für den nächsten ReAct-Schritt auf."""
    observation = {
        "tool": "http",
        "request": {
            "method": method,
            "path": path,
        },
        "response": {
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", "unbekannt"),
            "body": response.text[:MAX_BODY_CHARS],
            "truncated": len(response.text) > MAX_BODY_CHARS,
        },
    }
    return json.dumps(observation, ensure_ascii=False)


def http_get(target_base_url: str, path: str) -> str:
    """Ruft einen relativen Pfad der Zielanwendung ab."""
    response = TARGET_SESSION.get(
        target_url(target_base_url, path),
        timeout=10,
        allow_redirects=False,
    )
    return response_observation("GET", path, response)


def http_post(
    target_base_url: str,
    path: str,
    json_body: dict[str, Any],
) -> str:
    """Sendet JSON-Daten an einen relativen Pfad der Zielanwendung."""
    response = TARGET_SESSION.post(
        target_url(target_base_url, path),
        json=json_body,
        timeout=10,
        allow_redirects=False,
    )
    return response_observation("POST", path, response)


def execute_action(action: dict[str, Any], target_base_url: str) -> str:
    """Leitet eine Modellaktion an das passende Werkzeug weiter."""
    if action["type"] == "http_get":
        return http_get(target_base_url, action["path"])
    if action["type"] == "http_post":
        return http_post(target_base_url, action["path"], action["json_body"])
    raise ValueError(f"Unbekannte Werkzeugaktion: {action['type']}")


def action_key(action: dict[str, Any]) -> str:
    """Erzeugt eine vergleichbare Darstellung eines Werkzeugaufrufs."""
    relevant_fields = {
        "type": action["type"],
        "path": action["path"],
    }
    if action["type"] == "http_post":
        relevant_fields["json_body"] = action["json_body"]
    return json.dumps(relevant_fields, ensure_ascii=False, sort_keys=True)


def error_observation(error_type: str, message: str) -> str:
    """Formatiert einen Fehler als neue Observation für das Modell."""
    return json.dumps(
        {
            "type": error_type,
            "message": message,
            "instruction": "Korrigiere die Aktion im nächsten Schritt.",
        },
        ensure_ascii=False,
    )


def store_step(
    messages: list[dict[str, str]],
    model_output: str,
    observation: str,
) -> None:
    """Speichert Modellausgabe und Observation im ReAct-Zustand."""
    messages.append({"role": "assistant", "content": model_output})
    messages.append({"role": "user", "content": f"Neue Observation: {observation}"})


def run_agent(goal: str, target_base_url: str) -> str:
    """Führt die ReAct-Schleife bis zum Ergebnis oder Schrittlimit aus."""
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Freigegebene Zielanwendung: {target_base_url}\n"
                f"Ziel: {goal}\n"
                "Erste Observation: Noch keine Webseite abgerufen."
            ),
        },
    ]
    previous_action_key: str | None = None

    print(f"Freigegebene Zielanwendung: {target_base_url}")

    for step in range(1, MAX_STEPS + 1):
        print(f"\n--- Schritt {step}/{MAX_STEPS} ---")
        model_output = call_model(messages)
        print(f"Modell: {model_output}")

        try:
            action = parse_action(model_output)
        except ValueError as error:
            observation = error_observation("action_error", str(error))
            print(f"Observation: {observation}")
            store_step(messages, model_output, observation)
            continue

        if action["type"] == "finish":
            return action["answer"]

        current_action_key = action_key(action)
        if current_action_key == previous_action_key:
            observation = error_observation(
                "repeated_action",
                "Derselbe Werkzeugaufruf wurde unmittelbar zuvor ausgeführt.",
            )
            print(f"Observation: {observation}")
            store_step(messages, model_output, observation)
            continue

        try:
            observation = execute_action(action, target_base_url)
        except (KeyError, requests.RequestException, TypeError, ValueError) as error:
            observation = error_observation("tool_error", str(error))
        else:
            previous_action_key = current_action_key

        print(f"Observation: {observation}")
        store_step(messages, model_output, observation)

    raise RuntimeError(f"Schrittlimit von {MAX_STEPS} erreicht.")


def parse_cli_args() -> argparse.Namespace:
    """Trennt die freigegebene Zieladresse vom natürlichsprachlichen Ziel."""
    parser = argparse.ArgumentParser(
        description="Einfacher Web-Agent für die lokale Workshop-Umgebung."
    )
    parser.add_argument(
        "--target",
        default=DEFAULT_TARGET_BASE_URL,
        metavar="URL",
        help=(
            "Freigegebene Basisadresse der lokalen Zielanwendung "
            "(Standard: %(default)s)."
        ),
    )
    parser.add_argument(
        "goal",
        nargs="*",
        help="Natürlichsprachliche Beschreibung des Ziels.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    default_goal = (
        "Melde dich ohne das tatsächliche Administratorpasswort an. Beende den "
        "Lauf erst, wenn die Antwort das Administratorkonto und den erfolgreichen "
        "Login anhand der HTTP-Antwort belegt."
    )
    args = parse_cli_args()
    selected_goal = " ".join(args.goal).strip() or default_goal

    try:
        selected_target = validate_target_base_url(args.target)
        result = run_agent(selected_goal, selected_target)
        print(f"\nErgebnis: {result}")
    except (
        KeyError,
        requests.RequestException,
        RuntimeError,
        TypeError,
        ValueError,
    ) as error:
        print(f"\nFehler: {error}")
