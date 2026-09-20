---
title: "Starter-Scaffold: Minimaler ReAct-Agent"
date: 2026-08-07
tags:
  - workshop
  - cyberraum
  - agent
---

# Minimaler ReAct-Agent

Dieses Gerüst zeigt den Agentenkern ohne Agenten-Framework. Das Modell wird
standardmäßig über den LiteLLM-Dienst der TU Darmstadt aufgerufen. In Slot 2
ergänzt ihr nur die fünf markierten TODOs in `slot2_agent.py`:

1. Zustand mit Ziel und erster Observation anlegen.
2. Modell mit dem bisherigen Zustand aufrufen.
3. Aktion oder Ende auswerten.
4. Das lesende HTTP-Werkzeug aufrufen.
5. Aktion und neue Observation im Zustand speichern.

Das Aktionsformat, der LiteLLM-Zugriff, das HTTP-Werkzeug, die Ausgabe und das
Schrittlimit sind bereits implementiert. In Slot 3 könnt ihr diese Basis um
weitere HTTP-Methoden und Werkzeuge erweitern.

Die Dateien werden im Workshop schrittweise bereitgestellt. Ruft zu den von den
Lehrenden genannten Zeitpunkten im Teilnehmer-Repository `git pull --ff-only`
auf. Spätere Freigaben fügen nur neue Dateien hinzu und überschreiben euren
bearbeiteten Stand nicht.

## Vorbereitung

Voraussetzung ist Python 3.10 oder neuer. Legt eine virtuelle Umgebung an und installiert die zwei Abhängigkeiten.

Unter macOS und Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Unter Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Falls noch keine `.env` aus der technischen Vorbereitung vorhanden ist,
kopiert `.env.example` nach `.env`. Tragt den bereitgestellten
LiteLLM-Key sowie die URL eurer isolierten Juice-Shop-Instanz ein. Als
Standardmodell ist `GLM-5.2-AWQ-INT4` vorkonfiguriert. Ein anderes verfügbares
Modell kann mit `LITELLM_MODEL` gewählt werden, ohne den Python-Code zu ändern.

```sh
cp -n .env.example .env
```

Der API-Key bleibt ausschließlich in `.env`. Diese Datei wird von Git ignoriert.

## Start

Führt nach dem Ergänzen der ReAct-Schleife zuerst einen kurzen technischen Smoke-Test aus:

```sh
python slot2_agent.py "Rufe die Startseite der Zielanwendung ab, nenne ihren Anwendungstitel und beende den Lauf."
```

Wenn Modellausgabe, GET-Werkzeug, Observation und `finish` erkennbar sind, startet den eigentlichen Warm-up:

```sh
python slot2_agent.py "Untersuche zunächst das öffentlich erreichbare, aber nicht verlinkte Dateiverzeichnis. Finde dort das vertrauliche Dokument, rufe es ab, nenne seinen Pfad und belege den Fund anhand der HTTP-Antwort. Beende den Lauf erst, wenn das Dokument tatsächlich abgerufen wurde."
```

Ohne übergebenen Zieltext ruft `slot2_agent.py` die Startseite als technischen
Smoke-Test ab. Der Lauf endet spätestens nach zehn Schritten.

## Bereitgestellte Code-Stände

| Zeitpunkt | Datei | Zweck |
| --- | --- | --- |
| Beginn Slot 2 | `slot2_agent.py` | Starter mit fünf TODOs |
| spätestens nach 25 Minuten Implementierung | `slot2_reference_agent.py` | reine Referenzschleife für blockierte Teams und den Warm-up |
| Beginn Slot 3 | `slot3_agent.py` | gemeinsamer Checkpoint mit fertiger Schleife und vier neuen POST-TODOs |
| Ende Slot 3 | `slot3_solution_minimal.py` | reine Pflichtlösung der vier POST-TODOs |
| Ende Slot 3 | `slot3_reference_agent.py` | erweiterter gemeinsamer Referenzstand für Slot 4 |

Die eigene Lösung bleibt jeweils unter ihrem ursprünglichen Dateinamen
erhalten. Die Referenzdateien werden nur zum Vergleichen oder als gemeinsamer
Ausgangspunkt verwendet.

Der Referenzagent trennt die freigegebene Zieladresse vom natürlichsprachlichen
Ziel. Die lokale Workshop-Instanz kann beim Start explizit angegeben werden:

```sh
python slot3_reference_agent.py --target http://127.0.0.1:3000 "<Ziel>"
```

Die Zieladresse wird vor dem Lauf auf `http`, `127.0.0.1` beziehungsweise
`localhost` und Port `3000` begrenzt. Modellaktionen enthalten weiterhin nur
relative Pfade innerhalb dieser Basisadresse.

## Slot 4: CAI selbst ausführen

In Slot 4 gibt es keinen zusätzlich vorbereiteten Python-Agenten. Die
Teilnehmenden starten anhand des
[[../Challenges/Aufgabenblatt|Aufgabenblatts]] die echte CAI-CLI, untersuchen
die vorhandenen Agentenprofile und wählen `one_tool_agent` selbst aus.

Die CAI-Laufzeit wird aus der workshop-eigenen Implementierung als
vorbereitetes Dockerimage bereitgestellt. Während des Slots wird kein Paket
aus dem Internet installiert. Maßgeblich ist der von den Lehrenden angegebene
Image-Digest, nicht ein beweglicher Tag.

Die Compose-Laufzeit startet CAI ohne Root-Rechte, Host-Mounts und
Docker-Socket. Interne Docker-Netze beschränken den Zugriff auf die isolierte
Juice-Shop-Instanz und einen zielgebundenen Gateway zum vorgesehenen
LiteLLM-Endpunkt. Compose verwendet dieselbe `Agent/.env` wie der Eigenbau
für API-Schlüssel, `LLM_PROVIDER` und Modell. Die öffentliche
`runtime/workshop.defaults.env` enthält nur Image-Referenzen und Laufzeitlimits.
Die konkreten Startbefehle stehen in `CAI-Laufzeit.md`.

## Plan 2: OpenRouter nur bei Ausfall des TU-Dienstes

OpenRouter ist vorbereitet, aber nicht automatisch aktiv. Nur wenn die
Lehrenden den Ausfall des TU-LiteLLM-Dienstes bestätigen, werden in `.env`
`LLM_PROVIDER=openrouter`, `OPENROUTER_API_KEY` und `OPENROUTER_MODEL` gesetzt.
Die Agenten wechseln nicht selbstständig den Anbieter. Dadurch bleibt sichtbar,
an welchen Dienst Workshopdaten gesendet werden.

## Aktionsformat

Das Modell darf genau eine der folgenden Antworten als JSON liefern:

```json
{
  "type": "http_get",
  "reason": "Auf der Startseite steht wahrscheinlich der Anwendungstitel.",
  "path": "/"
}
```

oder:

```json
{
  "type": "finish",
  "reason": "Der Titel ist in der letzten Observation sichtbar.",
  "answer": "Der Anwendungstitel lautet ..."
}
```

`reason` ist eine kurze, nach außen gegebene Handlungsbegründung. Es ist keine vollständige interne Gedankenkette.

## Wenn etwas nicht funktioniert

- `LITELLM_API_KEY fehlt`: Prüft, ob `.env` existiert und der ausgegebene TU-Key eingetragen ist.
- Modell nicht gefunden: Prüft `LITELLM_MODEL`; der Workshopstandard ist `GLM-5.2-AWQ-INT4`.
- OpenRouter-Fehler im Plan-2-Betrieb: Prüft `OPENROUTER_API_KEY` und `OPENROUTER_MODEL`.
- HTTP-Fehler: Prüft, ob eure Juice-Shop-Instanz läuft und `TARGET_BASE_URL` stimmt.
- Ungültiges Aktionsformat: Seht euch die ausgegebene Modellantwort an. Das Modell muss eines der beiden JSON-Formate verwenden.
