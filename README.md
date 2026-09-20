# AG Cyberraum: Workshopmaterialien

Dieses Repository erhält Code und Arbeitsmaterialien schrittweise passend zum
Workshopablauf. Die Lehrenden nennen jeweils den Zeitpunkt für die nächste
Freigabe.

## Aktualisieren

Speichert eure Änderungen im Editor und führt dann im Repository aus:

```sh
git pull --ff-only
```

Jede Freigabe fügt nur neue Dateien hinzu. Eure bereits bearbeiteten
Starterdateien werden nicht überschrieben. Erstellt bis zur letzten Freigabe
keine lokalen Git-Commits. Falls ein Pull abgelehnt wird, verwendet weder
`git reset` noch `git checkout`, sondern bittet die Lehrenden um Unterstützung.

Bei einem Ausfall der Git-Bereitstellung erhaltet ihr dieselben Freigaben als
kleine ZIP-Dateien. Entpackt immer nur die aktuell genannte Datei in dieses
Arbeitsverzeichnis.

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
Vorbereitung ist darin bereits vor dem Workshop beschrieben. `Agent/README.md`
und der erste Startercode kommen zu Beginn von Slot 2 hinzu.

Die vorbereitete CAI-Laufzeit wird in Slot 4 verwendet. Git liefert die
Compose-Dateien und die Startanleitung; Compose lädt die Images aus der
Registry. Ein bereitgestelltes Docker-Archiv dient als Offline-Fallback.

In Slot 6 kommen zu Beginn von Aufgabe 1, 2 und 3 jeweils der Erstbericht,
die Analyseausgabe und die Rohereignisse samt Laufzeitaudit hinzu. Ruft nach
jeder angekündigten Freigabe den aktuellen Stand ab und öffnet die in der
jeweiligen Aufgabe verlinkte Datei unter
`Challenges/Slot-6-Incident-Response-Neuentwurf/`.

Wechselt für die Python-Aufgaben in das Verzeichnis `Agent`:

```sh
cd Agent
```

Zugangsdaten gehören ausschließlich in `Agent/.env`. Die Datei wird von
Git ignoriert und darf nicht committet oder weitergegeben werden.
