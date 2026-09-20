# CAI-Laufzeit für Slot 4

CAI wird als vorgebautes Dockerimage der workshop-eigenen Implementierung
bereitgestellt. Installiert während des Workshops weder CAI noch dessen
Python-Abhängigkeiten auf eurem Host.

Compose liest die öffentliche Datei `runtime/workshop.defaults.env` für
Image-Digest und Laufzeitlimits. Für Modellaufrufe lädt es zusätzlich die
Datei `Agent/.env` mit dem teambezogenen LiteLLM-Schlüssel
und der Modellkonfiguration. Standardmäßig wird das für JSON-Antworten und native
Werkzeugaufrufe geprüfte Modell `GLM-5.2-AWQ-INT4` über
`https://llm-service.ai.tu-darmstadt.de/v1` verwendet. Der Modellname bleibt
über `LITELLM_MODEL` in `Agent/.env` änderbar. Nur diese private Datei enthält
Zugangsdaten und gehört nicht in Git. Eine zusätzliche `runtime/workshop.env`
wird nicht benötigt.

## Über Compose laden und prüfen

Die Lehrenden pushen die Runtime-Dateien zur technischen Vorbereitung vor
dem Workshop. Führt in der Wurzel des Teilnehmer-Repositories aus:

```sh
git pull --ff-only
docker compose --env-file runtime/workshop.defaults.env -f runtime/compose.yml pull
```

Compose lädt CAI und Juice Shop anhand der Image-Referenzen in der
Konfiguration. Separate `docker pull`-Befehle sind dafür nicht nötig. Beim
späteren Start laden auch `up` beziehungsweise `run` ein fehlendes Image
automatisch nach, weil `pull_policy: missing` gesetzt ist. Mit dem expliziten
Compose-Pull und dem Bereitschaftstest erfolgt dieser Schritt schon vor
Slot 4.

Für die folgenden Startbefehle muss `Agent/.env` vorhanden sein. Legt sie
einmalig aus der bereits in dieser Freigabe enthaltenen Vorlage an:

```sh
cp -n Agent/.env.example Agent/.env
```

Unter Windows PowerShell:

```powershell
if (!(Test-Path Agent/.env)) { Copy-Item Agent/.env.example Agent/.env }
```

Eine bereits ausgefüllte Datei bleibt erhalten. Den Team-Key tragt ihr zu
Beginn des Workshops bei `LITELLM_API_KEY` ein. Compose liest zuerst die
öffentliche Laufzeitkonfiguration, dann `Agent/.env`; deren Werte haben
Vorrang. `LLM_PROVIDER` steuert die Anbieterwahl für Eigenbau und CAI.
Nur der Modell-Gateway erhält die echten API-Schlüssel. CAI erhält weiterhin
den internen Platzhalter `workshop-client` und die Gateway-Adresse.
Eine alte `runtime/workshop.env` wird bei diesen Befehlen nicht eingelesen.

Prüft vorab den lokalen Start. Dieser Test benötigt noch keinen Team-Key:

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml up -d --wait juice-shop browser-gateway model-gateway
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml run --rm cai --version
```

Nach Eintragen des Team-Keys den Modell-Gateway neu erzeugen und den
Modellzugang prüfen. Die Lehrenden führen diesen vollständigen Test vor
der Freigabe auf einem zweiten Rechner aus:

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml up -d --wait --force-recreate model-gateway
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml exec model-gateway curl --fail --silent http://127.0.0.1:8080/readyz
```

Nach einem Vorabtest die Dienste wieder stoppen, damit Port `3000` für
die Juice-Shop-Übung in Slot 1 frei ist:

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml stop
```

## Im Workshop starten

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml up -d juice-shop browser-gateway model-gateway
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml run --rm cai
```

Juice Shop ist im Browser über den fest verdrahteten Browser-Gateway unter
`http://127.0.0.1:3000` erreichbar. Der eigentliche Juice-Shop-Container bleibt
im internen Zielnetz. Innerhalb von CAI lautet seine Adresse weiterhin
`http://juice-shop:3000`.

Ein direkter Start mit dem vorgesehenen Profil ist ebenfalls möglich:

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml run --rm -e CAI_AGENT_TYPE=one_tool_agent cai
```

## Docker-Archiv statt Image-Download

Bei fehlendem Registry-Zugang geben die Lehrenden ein geprüftes Archiv für
`amd64` oder `arm64` aus. Beispiel für `amd64`:

```sh
docker load -i cyberraum-images-2026-09-amd64.tar
```

Das Archiv enthält CAI und Juice Shop. Für dieses Archiv in
`Agent/.env` zusätzlich die lokale Image-Referenz eintragen:

```dotenv
CAI_IMAGE=cyberraum-cai:offline-2026-09
```

Anschließend die normalen Startbefehle verwenden. Die importierten Images
werden mit `pull_policy: missing` lokal verwendet; keinen zusätzlichen
`docker compose pull` ausführen. Der lokale Tag stammt aus dem von den
Lehrenden anhand des Registry-Digests vorbereiteten Archiv. Der Modellzugang
benötigt weiterhin eine Verbindung zum TU-Dienst.

## Plan 2 bei Ausfall des TU-Dienstes

OpenRouter wird nicht automatisch verwendet. Nur wenn die Lehrenden den
Ausfall des TU-LiteLLM-Dienstes bestätigen, werden in `Agent/.env`
die folgenden Werte gesetzt:

```dotenv
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=hier-plan-2-key-eintragen
OPENROUTER_MODEL=hier-getestetes-openrouter-modell-eintragen
```

Danach wird nur der Modell-Gateway neu erzeugt und CAI erneut gestartet:

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml up -d --force-recreate model-gateway
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml run --rm cai
```

Für die Rückkehr zum Normalbetrieb wird `LLM_PROVIDER=litellm` gesetzt und
der Gateway erneut erzeugt. Der Wechsel ist absichtlich manuell, damit keine
Workshopdaten unbemerkt an einen anderen Anbieter übertragen werden.

## Lauf zurücksetzen

Eine frische Juice-Shop-Instanz wird ohne Datenübernahme neu erzeugt:

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml rm -sf juice-shop
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml up -d juice-shop
```

CAI-Protokolle und temporäre Arbeitsdateien liegen in benannten Docker-Volumes,
nicht in einem Host-Mount. Die Lehrenden exportieren benötigte Protokolle vor
dem vollständigen Löschen der Laufzeit. Anschließend entfernt dieser Befehl
Container, Netzwerke und Volumes:

```sh
docker compose --env-file runtime/workshop.defaults.env --env-file Agent/.env -f runtime/compose.yml down -v
```

## Technische Begrenzung

Der CAI-Container läuft ohne Root-Rechte, zusätzliche Linux-Capabilities,
Docker-Socket oder Host-Mount. Seine beiden internen Netze erlauben nur den
Zugriff auf Juice Shop und den Modell-Gatewaydienst. Der Browser-Gateway
veröffentlicht ausschließlich den fest eingestellten Juice-Shop-Dienst auf
`127.0.0.1`; er akzeptiert kein `CONNECT` und keine frei wählbaren Upstreamziele.
Der Modell-Gateway leitet ausschließlich die OpenAI-kompatiblen Routen
`/v1/models` und `/v1/chat/completions` an den fest konfigurierten Modellendpunkt
weiter. Im Normalbetrieb ist dies der TU-LiteLLM-Dienst. OpenRouter ist
ausschließlich der manuelle Plan 2.

Maßgeblich ist der festgehaltene Registry-Digest. Beim Docker-Archiv
dokumentieren die Lehrenden zusätzlich Plattform, Image-ID und
Archivprüfsumme; der lokale Offline-Tag allein belegt den getesteten Stand
nicht.
