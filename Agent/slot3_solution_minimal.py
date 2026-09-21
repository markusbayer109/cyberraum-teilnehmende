"""Minimale Pflichtlösung für Slot 3.

Die vier TODOs aus ``slot3_agent.py`` sind gelöst. Optionale Verbesserungen an
Prompt, Zustand und Fehlerbehandlung enthält erst ``slot3_reference_agent.py``.
"""

import json
import os
import sys
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from dotenv import load_dotenv
from llm_provider import resolve_model_route

load_dotenv()

TARGET_BASE_URL = os.getenv("TARGET_BASE_URL", "http://127.0.0.1:3000")
MAX_STEPS = 10
MAX_MODEL_ATTEMPTS = 3

SYSTEM_PROMPT = """
Du bist ein einfacher Web-Agent in einer isolierten Workshop-Umgebung.
Arbeite schrittweise auf das Ziel hin. Nutze nur relative Pfade der Zielanwendung.

Antworte immer mit genau einem JSON-Objekt in einem dieser Formate:

{"type": "http_get", "reason": "kurze Begründung", "path": "/pfad"}
{"type": "http_post", "reason": "kurze Begründung", "path": "/pfad", "json_body": {"name": "wert"}}
{"type": "finish", "reason": "kurze Begründung", "answer": "deine Antwort"}
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
            parse_action(model_output)
            return model_output
        except (
            requests.RequestException,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ) as error:
            print(
                f"Modellanfrage über {route.provider} fehlgeschlagen "
                f"({attempt}/{MAX_MODEL_ATTEMPTS}): "
                f"{error}"
            )

    return json.dumps(
        {
            "type": "finish",
            "reason": "Das Modell hat dreimal keine gültige Aktion geliefert.",
            "answer": "Keine gültige Modellantwort erhalten. Bitte erneut versuchen.",
        },
        ensure_ascii=False,
    )


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
    if action.get("type") not in {"http_get", "http_post", "finish"}:
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


def target_url(path: str) -> str:
    """Erzeugt eine URL innerhalb der festgelegten Zielanwendung."""
    parsed_path = urlparse(path)
    if parsed_path.scheme or parsed_path.netloc or not path.startswith("/"):
        raise ValueError("Werkzeuge akzeptieren nur relative Pfade wie '/'.")
    return urljoin(f"{TARGET_BASE_URL.rstrip('/')}/", path.lstrip("/"))


def response_observation(response: requests.Response) -> str:
    """Bereitet eine HTTP-Antwort für den nächsten ReAct-Schritt auf."""
    observation = {
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", "unbekannt"),
        "body": response.text[:4000],
    }
    return json.dumps(observation, ensure_ascii=False)


def http_get(path: str) -> str:
    """Ruft einen relativen Pfad der Zielanwendung ab."""
    response = requests.get(target_url(path), timeout=10, allow_redirects=False)
    return response_observation(response)


def http_post(path: str, json_body: dict[str, Any]) -> str:
    """Sendet JSON-Daten an einen relativen Pfad der Zielanwendung."""
    response = requests.post(
        target_url(path),
        json=json_body,
        timeout=10,
        allow_redirects=False,
    )
    return response_observation(response)


def execute_action(action: dict[str, Any]) -> str:
    """Leitet eine Modellaktion an das passende Werkzeug weiter."""
    if action["type"] == "http_get":
        return http_get(action["path"])
    if action["type"] == "http_post":
        return http_post(action["path"], action["json_body"])
    raise ValueError(f"Unbekannte Aktion: {action['type']}")


def run_agent(goal: str) -> str:
    """Führt die ReAct-Schleife bis zum Ergebnis oder Schrittlimit aus."""
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Ziel: {goal}\n" "Erste Observation: Noch keine Webseite abgerufen."
            ),
        },
    ]

    for step in range(1, MAX_STEPS + 1):
        print(f"\n--- Schritt {step}/{MAX_STEPS} ---")

        model_output = call_model(messages)
        print(f"Modell: {model_output}")
        action = parse_action(model_output)

        if action["type"] == "finish":
            return action["answer"]

        observation = execute_action(action)
        print(f"Observation: {observation}")

        messages.append({"role": "assistant", "content": model_output})
        messages.append({"role": "user", "content": f"Neue Observation: {observation}"})

    raise RuntimeError(f"Schrittlimit von {MAX_STEPS} erreicht.")


if __name__ == "__main__":
    default_goal = "Rufe die Startseite der Zielanwendung ab, nenne ihren Anwendungstitel und beende den Lauf."
    selected_goal = " ".join(sys.argv[1:]).strip() or default_goal

    try:
        result = run_agent(selected_goal)
        print(f"\nErgebnis: {result}")
    except (
        KeyError,
        NotImplementedError,
        requests.RequestException,
        RuntimeError,
        TypeError,
        ValueError,
    ) as error:
        print(f"\nFehler: {error}")
