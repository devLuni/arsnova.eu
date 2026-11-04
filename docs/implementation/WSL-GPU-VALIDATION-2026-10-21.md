# Moderationskompass: GPU-Kompatibilitätstest für Q&A-Zusammenfassungen unter WSL

**Testdatum:** 21.10.2026 · **Git-Commit des Projekts:** `9e3acea8f1c8260e9212c2ba26a44d5fc1ce92e0`

**Ergebnis: bestanden.** Auf dem Testrechner lief Qwen unter WSL mit allen 37 Modellschichten auf der AMD Radeon RX 9070 XT. Das Modell fasste drei eigens formulierte Fragen in 1,318 Sekunden zusammen, nachdem der Server betriebsbereit war. Ein separater Rechentest lieferte auf der GPU dieselben Ergebnisse wie auf der CPU. Dafür waren weder neue Windows-Software noch Änderungen am Grafiktreiber nötig.

## Ziel und Umfang

Die Hochschulaufgabe »Generative Summarization under Source and Token Budget Constraints« untersucht, welchen Mehrwert eine generierte Zusammenfassung bietet, wenn die Zahl der Quellen und die Zahl der verfügbaren Token begrenzt sind. Gegenstand ist die Zusammenfassung der **offenen Fragen aus dem Q&A-Bereich**, die der Moderationskompass der moderierenden Person anzeigt.

Vor dem Vergleich mit der bestehenden Zusammenfassung war eine technische Frage zu klären: Kann die lokale Inferenzsoftware das Sprachmodell tatsächlich auf der Grafikkarte ausführen? Für diesen Test kamen ausschließlich erfundene Fragen zum Einsatz. Er misst weder die Leistung der vollständigen Anwendung noch die allgemeine Qualität der Zusammenfassungen und erlaubt keine Aussage zur DSGVO-Konformität.

Das Startskript der [bestehenden LLM-Laufzeitumgebung](../features/open-weight-llm-runtime.md) setzt `--n-gpu-layers 0`. Damit läuft dort keine Modellschicht auf der GPU, auch wenn WSL mehr Arbeitsspeicher erhält. Der Versuch nutzte deshalb eine separate GPU-Laufzeitumgebung. Anwendungskonfiguration, CPU-Laufzeitumgebung, Modellmanifest und Windows-Grafiktreiber blieben unverändert.

## Testumgebung

| Merkmal                                          | Wert                                                                                         | Nachweis                                                                 |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Grafikkarte                                      | AMD Radeon RX 9070 XT, 16 GB Grafikspeicher                                                  | Von ROCm und HIP als RX 9070 XT mit Architektur `gfx1201` erkannt        |
| Physischer Arbeitsspeicher                       | 32 GB                                                                                        | Angabe zum Testrechner                                                   |
| Windows                                          | Version 26H2, Build 26300.9711                                                               | Angabe zum Testrechner                                                   |
| Grafiktreiber                                    | 32.0.31041.1004 vom 17.08.2026                                                               | Angabe zum Testrechner; laut AMD entspricht die Version Adrenalin 26.8.1 |
| Weitere Grafikkarten                             | Keine aufgeführt                                                                             | Im Windows-Geräte-Manager geprüft                                        |
| WSL-Distribution                                 | Ubuntu 26.04.1 LTS, `resolute`                                                               | `/etc/os-release`                                                        |
| WSL-Kernel                                       | `6.18.54.1-microsoft-standard-WSL2`                                                          | `uname -r`                                                               |
| Für WSL verfügbarer Speicher                     | Rund 19 GiB RAM und 4 GiB Auslagerungsspeicher (Swap)                                        | `free -h`                                                                |
| Sichtbare logische Prozessoren                   | 16                                                                                           | `nproc`                                                                  |
| Freier Speicherplatz im Arbeitsverzeichnis       | Rund 954 GiB vor Testbeginn                                                                  | `df -h`                                                                  |
| Docker-Server                                    | 29.8.2, x86_64, Docker Desktop (containerisiert)                                             | Abfrage des Docker-Servers                                               |
| ROCm-Werkzeuge auf dem WSL-System vor Testbeginn | Weder `rocminfo` noch `hipcc` gefunden; keine Standardinstallation unter `/opt/rocm` erkannt | Suche nach Programmen und Installationsverzeichnis                       |

Alle neu hinzugekommenen Werkzeuge liefen in Linux-Containern oder lagen im WSL-Dateisystem. Die Container nutzten die bereits vorhandene Docker-Desktop-Engine; eine zusätzliche Installation unter Windows war nicht erforderlich.

## Auswahl der Versionen

Zum Einsatz kamen **ROCm 7.14.1 und ROCDXG 1.2.1**. AMD nennt Ubuntu 26.04 für diesen Installationsweg und stellt ROCDXG als fertiges Paket bereit. Nur für den hier vermiedenen Eigenbau von ROCDXG sieht die Anleitung ein Windows SDK vor. Die unten dokumentierten Messungen belegen, dass die getestete Kombination auf diesem Rechner funktioniert. Sie sind keine allgemeine Freigabe für andere Treiber oder Laufzeitumgebungen.

Für ROCm 7.2 gab es einen positiven Erfahrungsbericht mit derselben GPU und demselben Treiber. Die veröffentlichte WSL-Kompatibilitätstabelle nennt jedoch nur Ubuntu 22.04 und 24.04. Für den Rechner mit Ubuntu 26.04 wurde deshalb ein passender Paketstand gewählt, ohne Paketquellen unterschiedlicher Ubuntu-Versionen zu mischen.

Ein Fehlerbericht zu ROCm 10.1 beschreibt Zeitüberschreitungen bei derselben Kombination aus GPU und Treiber. In der Diskussion wird das Zusammenspiel einer integrierten und einer dedizierten GPU als mögliche Ursache genannt. Auf dem Testrechner war nur eine Grafikkarte aufgeführt. Der Bericht ist daher nur eingeschränkt übertragbar und ersetzt den lokalen Test nicht.

Verwendet wurde das im Projekt festgelegte Modell **Qwen3-4B-Instruct-2507 in der Quantisierung Q4_K_M**:

- Modellmanifest: `docker/open-weight-llm/model-manifest.json`.
- Modellquelle: `unsloth/Qwen3-4B-Instruct-2507-GGUF`, Revision `a06e946bb6b655725eafa393f4a9745d460374c9`.
- Datei: `Qwen3-4B-Instruct-2507-Q4_K_M.gguf`.
- Erwartete Größe: 2.497.281.120 Byte.
- Erwartete SHA-256-Prüfsumme: `3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597`.
- llama.cpp-Version: `b10524`, entsprechend der Laufzeitumgebung der Anwendung.

Der llama.cpp-Tag `b10524` verweist auf den Commit `9ee9fc04c136ef2ae729bfc60d18961b23c13ddf`. Das heruntergeladene Quellarchiv hatte die SHA-256-Prüfsumme `99df023cc0122cf26f6cde2befc79b0c3807f58e3d61c5fe40b9290a222ae8a3`. Da das Archiv keine Git-Metadaten enthält, meldete CMake den Commit als unbekannt. Die auf den Commit festgelegte Downloadadresse und die Prüfsumme identifizieren den verwendeten Quellstand.

## Durchführung und Ergebnisse

### 1. Ausgangszustand erfassen

Vor der Installation wurden Betriebssystem, verfügbare Ressourcen, vorhandene Werkzeuge und Git-Stand erfasst. Dazu dienten unter anderem diese Befehle:

```bash
git status --short
git rev-parse HEAD
uname -r
cat /etc/os-release
free -h
df -h /home/lena/Projects/arsnova.eu /tmp
nproc
command -v rocminfo
command -v hipcc
ls -ld /opt/rocm*
```

**Ergebnis:** Zu Beginn gab es keine lokalen Änderungen im Repository. Die ermittelten Systemwerte stehen in der Tabelle oben. Weder die beiden ROCm-Befehle noch CMake oder die C++-Build-Werkzeuge waren bei der ersten Suche auffindbar. Für die Kompilierung wurde eine eigene Build-Umgebung eingerichtet.

### 2. Sichtbarkeit der GPU im WSL-System prüfen

Im normalen WSL-Terminal war die GPU-Gerätedatei `/dev/dxg` sichtbar, in der eingeschränkten Ausführungsumgebung des Agenten (Sandbox) dagegen nicht. Um diese Einschränkung von einem Hardwareproblem zu unterscheiden, erfolgte nach Freigabe eine rein lesende Prüfung außerhalb der Sandbox:

```bash
ls -l /dev/dxg /usr/lib/wsl/lib/libdxcore.so
docker version --format '{{.Server.Version}}'
docker info --format 'OS={{.OperatingSystem}} Kernel={{.KernelVersion}} Architecture={{.Architecture}} Root={{.DockerRootDir}}'
```

**Ergebnis:** `/dev/dxg` war als zeichenorientierte Gerätedatei mit den Gerätenummern `10, 258` und den Zugriffsrechten `crw-rw-rw-` vorhanden. Die Bibliothek `libdxcore.so` war lesbar. Der Docker-Server meldete Version `29.8.2`. Die fehlende Sichtbarkeit in der Sandbox ließ also keinen Rückschluss auf die Verfügbarkeit der GPU in WSL zu.

### 3. Zugriff aus einem Linux-Container prüfen

Vor dem Download der größeren ROCm-Pakete und des Modells wurde geprüft, ob ein Container sowohl die GPU-Gerätedatei als auch die DXCore-Bibliothek sehen kann. So konnten die Versuchsabhängigkeiten vom WSL-System und von der bestehenden Laufzeitumgebung der Anwendung getrennt bleiben.

```bash
docker run --rm --network none --cpus 2 --memory 512m --pids-limit 64 \
  --cap-drop ALL --security-opt no-new-privileges \
  --device /dev/dxg \
  --mount type=bind,src=/usr/lib/wsl/lib/libdxcore.so,dst=/usr/lib/libdxcore.so,readonly \
  ubuntu:26.04 ls -l /dev/dxg /usr/lib/libdxcore.so
```

**Ergebnis:** Der Befehl endete mit Exit-Code `0`. Die Gerätedatei und die schreibgeschützt eingebundene Bibliothek waren sichtbar. Docker entfernte den temporären Container automatisch. Das heruntergeladene Ubuntu-Image blieb lokal verfügbar. Docker meldete dafür folgenden Prüfwert (Digest):

```text
sha256:c098726dd9b9733f3e885f8de0ef375206a311b0a317eadc40d347b1115fb944
```

Dieser Schritt belegte nur die Weitergabe des Geräts an den Container. Ob die GPU korrekt rechnete und ob llama.cpp Modellschichten auf ihr ausführte, wurde in den Schritten 6 und 8 getrennt geprüft.

### 4. Paketversionen und Prüfsummen ermitteln

Zur Identifikation der verwendeten Software wurden die offiziellen GitHub-Metadaten für ROCDXG `v1.2.1` sowie die Build-Anleitung für llama.cpp `b10524` abgerufen. Die Metadaten nennen für das ROCDXG-Paket folgende Werte:

```text
rocdxg-roct_1.2.1_amd64.deb
size: 184644 bytes
sha256: 7889eef45a1132ed2dde88d8ea1356bf791ec9c05802a18940bc81b970e850e0
```

Die Freigabe für die Linux-Downloads und Tests erfolgte, nachdem feststand, dass die vorhandene Docker-Desktop-Engine weiterverwendet wird. Die Freigabe war nötig, weil die Sandbox den Zugriff auf Docker, Netzwerk und GPU einschränkte. Sie betraf die Ausführung von Linux-Befehlen außerhalb der Sandbox. Unter Windows wurde weder Software installiert noch der Treiber aktualisiert.

### 5. Separate ROCm-Umgebung aufbauen

Das [Dockerfile des Versuchs](../../scripts/experiments/wsl-gpu/Dockerfile) installiert die Ubuntu-26.04-Pakete für ROCm in Version `7.14.1-0`, das BLAS-Paket für `gfx1201`, die Linux-Build-Werkzeuge und ROCDXG `1.2.1`. So blieben die Pakete des WSL-Systems und die CPU-Vergleichskonfiguration der Anwendung unverändert. Vor der Installation stimmte die SHA-256-Prüfsumme von ROCDXG mit dem veröffentlichten Wert überein. Die gewählten AMD-Pakete verwenden `/opt/rocm/core-7.14`; ältere Pfadangaben nach dem Muster `/opt/rocm-*` passen hier nicht.

```bash
mkdir -p tmp/wsl-gpu-validation
docker build --progress plain --tag arsnova-wsl-gpu-sdk:7.14.1 \
  scripts/experiments/wsl-gpu \
  > tmp/wsl-gpu-validation/sdk-build.log 2>&1
```

**Ergebnis:** Das Image wurde erfolgreich erstellt (Exit-Code `0`). Image-ID: `sha256:3b042558e40a421654e88940420bfd8674e24509b92d9bd2b268cf8a0bf1440c`. Die ROCm-Versionen sind festgelegt. Weitere Ubuntu-Abhängigkeiten löst `apt` beim Bau des Images auf; ihre Paketstände können sich bei einem späteren Neubau unterscheiden.

### 6. GPU erkennen und Rechenergebnis prüfen

Der [HIP-Test](../../scripts/experiments/wsl-gpu/hip-smoke.cpp) prüft mehr als die Geräteerkennung: Er reserviert drei Puffer von je 1 MiB, überträgt die Eingabedaten auf die GPU und berechnet dort `out[i] = a[i] + 2 * b[i]`. Anschließend kopiert er die Ergebnisse zurück und vergleicht jeden Wert mit dem auf der CPU berechneten Referenzwert. Erkennt der Test mehrere GPUs oder eine andere als die erwartete GPU-Familie, bricht er vor der Berechnung ab.

Die Befehle sind im Stammverzeichnis des Repositorys auszuführen. `1000:1000` bezeichnet die Benutzer- und Gruppen-ID auf dem Testrechner. Auf einem anderen System sind die IDs des dortigen WSL-Benutzerkontos einzusetzen.

```bash
docker run --rm --name arsnova-wsl-gpu-hip-check --user 1000:1000 \
  --network none --cpus 4 --memory 8g --memory-swap 8g --pids-limit 256 \
  --cap-drop ALL --security-opt no-new-privileges --device /dev/dxg \
  --mount type=bind,src=/usr/lib/wsl/lib/libdxcore.so,dst=/usr/lib/libdxcore.so,readonly \
  --mount type=bind,src="$PWD/scripts/experiments/wsl-gpu",dst=/experiment,readonly \
  --mount type=bind,src="$PWD/tmp/wsl-gpu-validation",dst=/work \
  arsnova-wsl-gpu-sdk:7.14.1 bash -c '
    set -eu
    timeout --kill-after=5s 30s rocminfo > /work/rocminfo.log 2>&1
    timeout --kill-after=5s 120s hipcc --offload-arch=gfx1201 -O2 \
      /experiment/hip-smoke.cpp -o /work/hip-smoke > /work/hip-build.log 2>&1
    timeout --kill-after=5s 30s /work/hip-smoke > /work/hip-result.log 2>&1
    cat /work/hip-result.log
  '
```

**Ergebnis:** Geräteabfrage, Kompilierung und Rechentest waren erfolgreich (Exit-Code `0`). Alle 262.144 GPU-Ergebnisse stimmten mit der CPU-Referenz überein. Originalausgabe:

```text
HIP devices: 1
GPU: AMD Radeon RX 9070 XT; architecture: gfx1201; VRAM: 16974905344 bytes
Allocated 3 MiB; copying input to GPU.
Launching GPU kernel.
PASS: all 262144 GPU results match the CPU reference.
```

**Fehlersuche:** Beim ersten Versuch konnte der Container `rocminfo.log` nicht schreiben (`Permission denied`). Der Prozess lief als `root`, hatte aber alle zusätzlichen Linux-Berechtigungen (Capabilities) abgegeben. Damit fehlte ihm der Schreibzugriff auf das eingebundene Verzeichnis des WSL-Benutzerkontos. Mit `--user 1000:1000` gelang der Zugriff, ohne die Verzeichnisrechte zu ändern. Der fehlgeschlagene Versuch hatte weder die GPU abgefragt noch eine Berechnung gestartet.

### 7. llama.cpp mit GPU-Unterstützung kompilieren und das Modell prüfen

Das bestehende Anwendungs-Image deaktiviert die Ausführung von Modellschichten auf der GPU. Für den Kompatibilitätstest wurde deshalb **dieselbe llama.cpp-Version** mit HIP-Unterstützung kompiliert. Die Implementierung der Zusammenfassung blieb dabei unverändert. Der folgende Download bezieht sich auf den oben angegebenen Commit:

```bash
curl --fail --location --retry 2 \
  https://codeload.github.com/ggml-org/llama.cpp/tar.gz/9ee9fc04c136ef2ae729bfc60d18961b23c13ddf \
  --output tmp/wsl-gpu-validation/llama-source.tar.gz
mkdir -p tmp/wsl-gpu-validation/llama.cpp
tar -xzf tmp/wsl-gpu-validation/llama-source.tar.gz --strip-components=1 \
  -C tmp/wsl-gpu-validation/llama.cpp
docker run --rm --name arsnova-wsl-gpu-build --user 1000:1000 \
  --network none --cpus 4 --memory 8g --memory-swap 8g --pids-limit 256 \
  --cap-drop ALL --security-opt no-new-privileges \
  --mount type=bind,src="$PWD/tmp/wsl-gpu-validation",dst=/work \
  arsnova-wsl-gpu-sdk:7.14.1 bash -c '
    set -eu
    export HIPCXX=/opt/rocm/core-7.14/lib/llvm/bin/clang
    timeout --kill-after=5s 90s cmake -S /work/llama.cpp \
      -B /work/llama.cpp/build -G Ninja -DGGML_HIP=ON \
      -DGPU_TARGETS=gfx1201 -DCMAKE_BUILD_TYPE=Release \
      -DGGML_NATIVE=OFF -DLLAMA_CURL=ON > /work/llama-configure.log 2>&1
    timeout --kill-after=10s 900s cmake --build /work/llama.cpp/build \
      --target llama-server --parallel 4 > /work/llama-build.log 2>&1
  '
```

CMake fand HIP, hipBLAS und Clang `23.0.0`. Es wies darauf hin, dass `LLAMA_CURL` in dieser Version veraltet ist und ignoriert wird.

**Ergebnis:** Alle 471 Build-Schritte liefen erfolgreich durch (Exit-Code `0`). Für Kompilierung und Linken mit höchstens vier CPU-Kernen erfasste Ninja rund 576 Sekunden (9 Minuten und 36 Sekunden). Die Zeit für die Erstellung des Images, den Download des Quellcodes und die CMake-Konfiguration ist darin nicht enthalten. Diese einmaligen Einrichtungszeiten fallen nicht bei jeder Zusammenfassung an.

Der separate Download der öffentlich zugänglichen Modelldatei dauerte rund 57 Sekunden. Dateigröße (2.497.281.120 Byte) und SHA-256-Prüfsumme stimmten mit dem Modellmanifest überein. Download und Prüfung lassen sich ohne Hugging-Face-Konto wiederholen:

```bash
curl --fail --location --retry 2 --max-time 900 \
  --output tmp/wsl-gpu-validation/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
  https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF/resolve/a06e946bb6b655725eafa393f4a9745d460374c9/Qwen3-4B-Instruct-2507-Q4_K_M.gguf
python3 - <<'CHECK_MODEL'
import hashlib, json
from pathlib import Path
manifest = json.loads(Path('docker/open-weight-llm/model-manifest.json').read_text())
model = Path('tmp/wsl-gpu-validation') / manifest['filename']
assert model.stat().st_size == manifest['sizeBytes']
with model.open('rb') as stream:
    assert hashlib.file_digest(stream, 'sha256').hexdigest() == manifest['sha256']
print('PASS: model size and SHA-256 match the manifest')
CHECK_MODEL
```

### 8. Zusammenfassung für die Moderation aus Testfragen erzeugen

Das [Inferenzskript](../../scripts/experiments/wsl-gpu/run-inference.py) sendet drei erfundene deutschsprachige Fragen an einen lokalen llama.cpp-Server. Zwei betreffen die Steigung einer Geraden, eine die Invertierbarkeit einer Matrix. Der Auftrag lautet, die Fragen in höchstens zwei kurzen Aussagen zusammenzufassen und jeweils die Kennungen der zugehörigen Quellen anzugeben. Das Kontextfenster umfasst 4.096 Token; für die Ausgabe stehen höchstens 192 Token zur Verfügung. Der Server bearbeitet eine Anfrage gleichzeitig, nutzt vier CPU-Threads und soll alle Modellschichten auf die GPU laden.

Das Skript prüft mit einem eigenen JSON-Schema die **Struktur der Antwort** und die Gültigkeit der Quellenkennungen. Außerdem prüft es, ob die Generierung regulär endet und ob das Serverprotokoll auf die GPU geladene Modellschichten ausweist. Ob eine Aussage die referenzierten Fragen inhaltlich korrekt wiedergibt, muss ein Mensch beurteilen. Das vollständige Antwortschema der Anwendung, die Authentifizierung der moderierenden Person, die Warteschlange, das Ausweichverhalten bei Fehlern und die Benutzeroberfläche sind nicht Teil dieses Tests.

Nach erfolgreicher Kompilierung und Prüfung der Modelldatei lässt sich der Test so ausführen:

```bash
docker run --rm --name arsnova-wsl-gpu-inference --user 1000:1000 \
  --network none --cpus 4 --memory 8g --memory-swap 8g --pids-limit 256 \
  --cap-drop ALL --security-opt no-new-privileges --device /dev/dxg \
  --mount type=bind,src=/usr/lib/wsl/lib/libdxcore.so,dst=/usr/lib/libdxcore.so,readonly \
  --mount type=bind,src="$PWD/scripts/experiments/wsl-gpu",dst=/experiment,readonly \
  --mount type=bind,src="$PWD/tmp/wsl-gpu-validation",dst=/work \
  arsnova-wsl-gpu-sdk:7.14.1 \
  timeout --kill-after=10s 180s python3 /experiment/run-inference.py \
    --server /work/llama.cpp/build/bin/llama-server \
    --model /work/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
    --output /work/inference-02
```

Für jeden Lauf ist ein neues Ausgabeverzeichnis zu wählen. Das Skript überschreibt keine früheren Ergebnisse. Es legt `request.json`, `response.json`, `result.json` und `server.log` ab. Der zufällig erzeugte lokale API-Schlüssel steht nicht im Ergebnisbericht. Nach dem Test beendet das Skript den Server; es bleibt kein Modelldienst aktiv.

**Ergebnis:** Der abschließende Testlauf (`inference-02`) war erfolgreich (Exit-Code `0`). Im Serverprotokoll stehen die Meldungen `using device ROCm0 (AMD Radeon RX 9070 XT)` und `offloaded 37/37 layers to GPU`. Flash Attention war aktiviert. Der Server lud die Modelldatei lokal. Die Anfrage lief ausschließlich über die Loopback-Schnittstelle innerhalb des Containers.

| Messgröße                                                    | Erster Lauf: Standardprotokoll                   | Zweiter Lauf: mit GPU-Protokolldaten |
| ------------------------------------------------------------ | ------------------------------------------------ | ------------------------------------ |
| Testergebnis                                                 | Nicht bestanden: Nachweis für GPU-Nutzung fehlte | Bestanden                            |
| Serverstart bis zur gemeldeten Betriebsbereitschaft          | 7,038 s                                          | 4,771 s                              |
| Dauer der HTTP-Anfrage für die Zusammenfassung               | 1,444 s                                          | 1,318 s                              |
| Eingabe- / Ausgabetoken                                      | 173 / 85                                         | 173 / 85                             |
| Aus dem Cache übernommene Eingabetoken                       | 0                                                | 0                                    |
| Vom Server gemeldete Ausgaberate                             | 64,94 Token/s                                    | 69,63 Token/s                        |
| Laut Protokoll auf die GPU geladene Modellschichten          | Nicht protokolliert                              | 37 von 37                            |
| Maximaler residenter Arbeitsspeicher des Kindprozesses (RSS) | 2.823.084 KiB                                    | 2.823.364 KiB                        |

Das sind zwei Einzelmessungen. In beiden Läufen wurde der Server neu gestartet. Beim zweiten Lauf könnten bereits im Betriebssystem zwischengespeicherte Dateien und die vorherige Initialisierung der GPU die Zeiten beeinflusst haben. Außerdem änderte sich der Protokollumfang. Aus dem Zeitunterschied lässt sich deshalb keine Verbesserung der Modell- oder Hardwareleistung ableiten. Der RSS-Wert beschreibt den vom Prozess belegten physischen Arbeitsspeicher; er misst weder den Grafikspeicher noch den Speicherverbrauch des Gesamtsystems.

Im zweiten Lauf meldete der Server GPU-Puffer von 2.375,91 MiB für die Modellgewichte, 576,00 MiB für den KV-Cache und 19,75 MiB für Berechnungen. Zusammen sind das rund **2,90 GiB**. Diese Summe ist kein gemessener Spitzenwert für den Grafikspeicher: Zusätzlicher Speicherbedarf der Laufzeitumgebung und anderer Prozesse ist nicht enthalten. Im Protokoll steht außerdem ein CPU-seitig eingeblendeter Modellpuffer von 304,28 MiB.

Beide Läufe lieferten denselben Inhalt:

```json
{
  "statements": [
    {
      "text": "Wie berechnet man die Steigung einer Geraden? Was bedeutet die Steigung m in y = mx + b?",
      "sourceIds": ["q1", "q2"]
    },
    {
      "text": "Wann ist eine Matrix invertierbar?",
      "sourceIds": ["q3"]
    }
  ]
}
```

**Inhaltliche Beobachtung:** Das Modell ordnete die beiden Fragen zur Steigung richtig einander zu (`q1`, `q2`) und führte die Matrixfrage separat auf (`q3`). Die Quellenkennungen stimmen; neue Tatsachenbehauptungen kamen in diesem Beispiel nicht hinzu. Allerdings wiederholte das Modell die Fragen nahezu wörtlich. Der Test belegt damit die technische Machbarkeit. Ob die Moderation einen Mehrwert erhält, muss anhand weiterer Fragen und unterschiedlicher Formulierungen des Modellauftrags (Prompts) bewertet werden.

**Fehlersuche:** Schon im ersten Lauf erzeugte das Modell eine Antwort, die alle JSON-Prüfungen bestand. Das Skript meldete dennoch einen Fehlschlag, weil der Nachweis über die auf der GPU ausgeführten Schichten fehlte. llama.cpp `b10524` gibt die betreffenden Bibliotheksmeldungen erst auf der Protokollstufe »Trace« aus; die Standardstufe `3` blendet sie aus. Mit `--log-verbosity 4` wurden Gerät, Modellschichten und Puffer sichtbar. Modell, Prompt, Ausgabelimit und GPU-Einstellungen blieben für den zweiten Lauf gleich. Beide Ergebnisverzeichnisse blieben lokal erhalten, sodass sich auch der erste Versuch nachvollziehen lässt.

## Ressourcen und lokale Dateien

Für die Kompilierung von llama.cpp und die GPU-Tests standen den Containern jeweils höchstens vier CPU-Kerne und 8 GiB Arbeitsspeicher zur Verfügung. Bei diesem Speicherlimit erlaubt `--memory-swap 8g` keinen zusätzlichen Auslagerungsspeicher. Diese Grenzen beschränken weder die Auslastung der GPU noch reservieren sie eine feste Menge Grafikspeicher. Für die Erstellung des Docker-Images selbst galten diese Containerlimits nicht. Die vorhandene WSL-Speicherzuweisung reichte für die Tests aus. Weder Übertaktung noch eine Änderung des Windows-Treibers, eine Anpassung der `.wslconfig` oder ein WSL-Neustart waren erforderlich.

Modell, kompilierte Dateien und Rohprotokolle liegen unter `tmp/wsl-gpu-validation/`. Git ignoriert dieses Verzeichnis; für die Versionsverwaltung sind nur der Quellcode des Versuchs und dieser Bericht vorgesehen. Docker hält das SDK-Image, das Ubuntu-Basisimage und das Linux-Node-Image für die Formatprüfung lokal zur Wiederverwendung bereit. Die Testcontainer wurden durch `--rm` nach jedem Lauf entfernt. Die Inferenz lief mit `--network none`, lokaler Loopback-Verbindung und ohne veröffentlichten Port. Externer Netzwerkzugriff war nur zum Herunterladen öffentlich verfügbarer Software und Modelldaten erforderlich.

## Bedeutung für die Hochschulaufgabe

**Entscheidung:** Für die ersten Versuche mit einer rein LLM-basierten Q&A-Zusammenfassung genügt der lokale Rechner. Qwen lief mit dem vorhandenen Treiber und der bestehenden WSL-Ressourcenzuweisung auf der GPU. Ein kostenpflichtiger externer Server ist für dieses Experiment nicht erforderlich.

Die bestehende Anwendung bleibt die Vergleichsbasis. Bei einer späteren Anbindung über den vorhandenen Adapter für Zusammenfassungen sind die Berechtigungsprüfung für die Moderation, die Prüfung der Quellen und das Ausweichverhalten bei Fehlern beizubehalten. Für die HTTP-Anfrage im Testskript galt eine Frist von 60 Sekunden. Die Anwendung setzt in `apps/backend/src/lib/qaSummaryConfig.ts` standardmäßig eine Verarbeitungsfrist von 8 Sekunden. Eine einzelne Modellanfrage von 1,318 Sekunden belegt nicht, dass die vollständige Anwendung diese Frist auch bei längerem Kontext einhält. Wartezeit in der Warteschlange kann die Wartezeit für die Moderation zusätzlich verlängern.

Der Kompatibilitätstest liefert weder einen Anwendungsbenchmark noch ein allgemeines Qualitätsurteil oder einen Nachweis der DSGVO-Konformität. Für die weitere Untersuchung braucht es einen festen Korpus von Fragen und wiederholte Durchläufe mit dem bisherigen und dem generativen Verfahren. In getrennten Versuchsreihen lässt sich untersuchen, was sich ändert, wenn weniger Quellen zugelassen werden oder das Tokenbudget sinkt (Ablationsstudien). Die Zusammenfassungen sind anhand eines festgelegten Bewertungsrasters von Menschen zu beurteilen. Für die Moderation zählt die Zeit vom Auslösen der Anfrage bis zum Vorliegen der fertigen Zusammenfassung. Modelldownload, Kompilierung, Serverstart und Dauer der einzelnen Anfrage sind getrennt auszuweisen.

## Prüfungen zum Versuchsprotokoll vom 21.10.2026

- Der relative Verweis auf die Laufzeitdokumentation und der Pfad zum Modellmanifest führten zu vorhandenen Dateien im Repository.
- `git diff --no-index --check /dev/null docs/implementation/WSL-GPU-VALIDATION-2026-10-21.md` meldete nach dem Entfernen überzähliger Leerzeichen keine Formatfehler. Die Datei war neu und noch nicht in Git erfasst; deshalb erfolgte der Vergleich mit `/dev/null`. Der Exit-Code `1` des Dateivergleichs kennzeichnet hier unterschiedliche Inhalte.
- Die Formatierung mit Prettier `3.9.6` und die abschließende Prüfung mit `npx --yes prettier@3.9.6 --check docs/implementation/WSL-GPU-VALIDATION-2026-10-21.md` waren im temporären Linux-Container `node:24-bookworm-slim` erfolgreich (Prüfung: Exit-Code `0`). Das Windows-Programm `npm` kam nicht zum Einsatz.
- Die Python-Syntaxprüfung von `run-inference.py` mit `ast.parse` und die Prüfung aller acht Bash-Befehlsblöcke mit `bash -n` waren erfolgreich.
- Der Bau des Docker-Images, die HIP-Kompilierung, der GPU-Rechentest, die Kompilierung von llama.cpp, die Prüfung der Modelldatei und der abschließende Inferenztest waren erfolgreich. Der erste Inferenztest scheiterte ausschließlich am fehlenden Protokollnachweis für die GPU-Nutzung (siehe Schritt 8).
- Anwendungstests und Produktionsbuild wurden nicht ausgeführt. Anwendungscode und Bereitstellungskonfiguration blieben unverändert.

## Quellen

- [AMD: Versionshinweise zu Adrenalin 26.8.1](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-8-1.html).
- [AMD: Installationsanleitung für ROCm 7.14.1](https://rocm.docs.amd.com/en/docs-7.14.1/install/rocm.html).
- [AMD: WSL-Kompatibilität von ROCDXG](https://github.com/ROCm/librocdxg/blob/develop/README.md#wsl-compatibility-matrix).
- [ROCDXG: Veröffentlichung der Version 1.2.1](https://github.com/ROCm/librocdxg/releases/tag/v1.2.1).
- [ROCm 7.2: WSL-Kompatibilitätstabelle](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html).
- [ROCm: Fehlerbericht Nr. 13291](https://github.com/ROCm/rocm-systems/issues/13291) (Erfahrungsberichte; keine Kompatibilitätszusage).
- [llama.cpp b10524: Anleitung zur Kompilierung mit HIP](https://github.com/ggml-org/llama.cpp/blob/b10524/docs/build.md#hip).
