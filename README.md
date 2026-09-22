# AG Cyberraum: Workshopmaterialien

Alle Teilnehmermaterialien des Workshops sind jetzt freigegeben. Ihr findet
hier die Aufgaben, Starter und Referenzlösungen, die CAI-Laufzeit sowie die
Folien und Materialien zur Nachbereitung.

## Materialien

- [Aufgabenblatt](Challenges/Aufgabenblatt.md) und [druckbare Aufgabenblätter](Challenges/Druck/)
- [Eigener ReAct-Agent](Agent/README.md), [Slot-2-Referenz](Agent/slot2_reference_agent.py), [minimale Slot-3-Lösung](Agent/slot3_solution_minimal.py) und [erweiterter Slot-3-Referenzagent](Agent/slot3_reference_agent.py)
- [CAI-Laufzeit](CAI-Laufzeit.md) und [Compose-Konfiguration](runtime/compose.yml)
- LLM-Cheatsheet als [Markdown](LLM-Dienst-Cheatsheet.md) oder [PDF](LLM-Dienst-Cheatsheet.pdf)
- [Alle sieben Foliensätze](Slides/)
- [Vertiefungsmaterial](Background/Vertiefungsmaterial.md) und [Hintergrundberichte](Background/)
- Slot 6: [Erstbericht](Challenges/Slot-6-Incident-Response-Neuentwurf/01-Erstbericht-Analyseagent.md), [Analyseausgabe](Challenges/Slot-6-Incident-Response-Neuentwurf/02-Analyseausgabe-Agent.md) und [Rohereignisse mit Laufzeitaudit](Challenges/Slot-6-Incident-Response-Neuentwurf/03-Rohereignisse.md)

## Aktualisieren

Speichert eure Änderungen im Editor und führt dann im Repository aus:

```sh
git pull --ff-only
```

Die Abschlussfreigabe enthält auch Aktualisierungen an bereits ausgegebenen
Agentendateien. Wenn Git wegen eigener Änderungen den Pull ablehnt, sichert
eure Arbeit zunächst mit einem lokalen Commit oder `git stash`. Lokale Commits
müssen gegebenenfalls mit dem aktuellen Remote-Stand zusammengeführt werden;
eigene Änderungen werden nicht mit `git reset` oder `git checkout` verworfen.
Wendet euch bei Fragen an die Lehrenden.

## Vor dem Workshop: Laufzeit über Compose vorbereiten

Die technische Freigabe enthält das Aufgabenblatt, `Agent/requirements.txt`,
`Agent/.env.example`, `CAI-Laufzeit.md` und `runtime/`. Folgt vor dem Workshop
dem Abschnitt „Technische Vorbereitung“ in `Challenges/Aufgabenblatt.md`.
Zum Laden der Images führt ihr in der Wurzel des Teilnehmer-Repositories aus:

```sh
git pull --ff-only
docker compose --env-file runtime/workshop.defaults.env -f runtime/compose.yml pull
```

Compose lädt die in der Konfiguration festgelegten Images aus Docker Hub.
Das CAI-Image ist öffentlich und unterstützt `linux/amd64` sowie
`linux/arm64`; Docker wählt die passende Variante. Ein Docker-Hub-Login
ist für den öffentlichen Download nicht erforderlich. Für den lokalen
Starttest legt ihr `Agent/.env` aus der Vorlage an. Den Team-Key tragt ihr
zu Beginn des Workshops dort ein; danach prüft ihr auch den Modellzugang.
Dieselbe Datei wird später für den eigenen Agenten verwendet. Eine separate
`runtime/workshop.env` ist nicht nötig.

Falls ein Download nicht möglich ist, erhaltet ihr ein zur Rechnerarchitektur
passendes Docker-Archiv und die Importanleitung von den Lehrenden.

## Einstieg

Das vollständige Aufgabenblatt liegt in `Challenges/Aufgabenblatt.md`. Die
Vorbereitung und Startbefehle für den eigenen Agenten stehen zusätzlich in
`Agent/README.md`.

Die vorbereitete CAI-Laufzeit wird in Slot 4 verwendet. Git liefert die
Compose-Dateien und die Startanleitung; Compose lädt die Images aus der
Registry. Ein bereitgestelltes Docker-Archiv dient als Offline-Fallback.

Für Slot 6 liegen Erstbericht, Analyseausgabe und Rohereignisse samt
Laufzeitaudit vollständig unter
`Challenges/Slot-6-Incident-Response-Neuentwurf/`. Öffnet die im jeweiligen
Aufgabenteil verlinkte Datei.

Wechselt für die Python-Aufgaben in das Verzeichnis `Agent`:

```sh
cd Agent
```

Zugangsdaten gehören ausschließlich in `Agent/.env`. Die Datei wird von
Git ignoriert und darf nicht committet oder weitergegeben werden.
