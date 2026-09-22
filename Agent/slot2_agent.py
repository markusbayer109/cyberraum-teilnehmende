"""Starter-Scaffold für eine minimale ReAct-Schleife.

Die fünf TODOs in ``run_agent`` sollen in Aufgabe 2 ergänzt werden. Alle technischen
Hilfsfunktionen sind bereits vorgegeben, damit der Kontrollfluss sichtbar bleibt.
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
    """Prüft, ob die Modellantwort einem der zwei Aktionsformate entspricht."""
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
    if action.get("type") not in {"http_get", "finish"}:
        raise ValueError("'type' muss 'http_get' oder 'finish' sein.")
    if not isinstance(action.get("reason"), str) or not action["reason"].strip():
        raise ValueError("Die Aktion benötigt eine kurze 'reason'.")
    if action["type"] == "http_get" and not isinstance(action.get("path"), str):
        raise ValueError("http_get benötigt einen 'path'.")
    if action["type"] == "finish" and not isinstance(action.get("answer"), str):
        raise ValueError("finish benötigt eine 'answer'.")

    return action


def http_get(path: str) -> str:
    """Ruft einen relativen Pfad der festgelegten Zielanwendung ab."""
    parsed_path = urlparse(path)
    if parsed_path.scheme or parsed_path.netloc or not path.startswith("/"):
        raise ValueError("Das Werkzeug akzeptiert nur relative Pfade wie '/'.")

    url = urljoin(f"{TARGET_BASE_URL.rstrip('/')}/", path.lstrip("/"))
    response = requests.get(url, timeout=10, allow_redirects=False)

    observation = {
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", "unbekannt"),
        "body": response.text[:4000],
    }
    return json.dumps(observation, ensure_ascii=False)


def run_agent(goal: str) -> str:
    """Führt die ReAct-Schleife bis zum Ergebnis oder Schrittlimit aus."""

    # TODO 1: Query-Schritt: Lege den Zustand als Nachrichtenliste an.
    # Er soll den SYSTEM_PROMPT und eine User-Nachricht mit Ziel und erster
    # Observation enthalten. Erste Observation: "Noch keine Webseite abgerufen."
    #
    # Nachrichtenformat (Chat Completions, so erwarten es OpenAI und LiteLLM):
    # ``messages`` ist eine Liste. Jedes Element ist ein Dict mit genau den
    # Schlüsseln "role" und "content" (beide Strings). Es gibt drei Rollen:
    #   - "system":    Grundregeln und Antwortformat, hier der SYSTEM_PROMPT.
    #   - "user":      Eingaben an das Modell, hier das Ziel und später jede
    #                  neue Observation.
    #   - "assistant": die Antworten des Modells, in TODO 5 zurückgeschrieben.
    # Die ReAct-"Observation" ist KEINE eigene Rolle. Sie wird als "user"-
    # Nachricht in den Verlauf gelegt (siehe TODO 5). Genau diese Liste geht
    # unverändert an ``call_model`` und damit an das Modell.
    #
    # Aufbau (Platzhalter, nur zur Form, nicht die Lösung):
    #   messages = [
    #       {"role": "system", "content": "<Grundregeln>"},
    #       {"role": "user", "content": "<erste Eingabe>"},
    #   ]
    # Nach einem Schritt kommen in TODO 5 hinzu:
    #       {"role": "assistant", "content": "<Modellantwort als JSON-String>"},
    #       {"role": "user", "content": "<nächste Observation>"},
    messages: list[dict[str, str]] = []

    for step in range(1, MAX_STEPS + 1):
        print(f"\n--- Schritt {step}/{MAX_STEPS} ---")

        # TODO 2: Setze den ReAct-Schritt "Thought" um. Nutze eine geeignete
        # Hilfsfunktion.
        model_output = ""
        print(f"Modell: {model_output}")

        # TODO 3: Parse die Modellantwort mit einer geeigneten Funktion.
        # Implementiere was laut ReAct dann gemacht werden soll.
        action: dict[str, Any] = {}

        # TODO 4: Setze den ReAct-Schritt "Tool" mit Action und Observation um.
        # Nutze die passende Hilfsfunktion, um die Action auszuführen und
        # die Observation zu erzeugen.
        observation = ""

        # TODO 5: Speichere zuerst die Modellantwort als assistant-Nachricht und
        # danach die neue Observation als user-Nachricht im Zustand messages.

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
