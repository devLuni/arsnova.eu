# 2C am Stichtag 6. November 2026

## 1. Fragestellung und vorab festgelegte Kriterien

- V640 und V1024 wiederholen S6/S100 × A/B auf dem neuen Anwendungscode. Hypothese: Die kompaktere Ausgabevorgabe senkt den Tokenbedarf und die Fallbackquote bei 640. Für einen technisch erfolgreichen Einzelauftrag muss eine vollständige generierte, vom Backend akzeptierte Kurzfassung mit erlaubten Quellen vorliegen. Ein betriebliches `ready` allein reicht nicht.
- E-Long verlängert alle 100 Referenztexte mit fünf Wiederholungen derselben Rückfrage. Hypothese: Die Zahl ausgewählter Fragen, gekürzte Texte oder die Laufzeit reagieren auf Kontextdruck. E-Meta vergleicht Vollkontext mit ausgewählten Texten, IDs, Stimmen und Status; S6-B ohne diese Zusatzfelder ist der Referenzfall. Hypothese: Stimmen und Status allein garantieren keine richtige Deutung.
- E-Ground prüft zusätzlich künstlich eingespielte, bekannte Aussagen am Validierungspfad. Geprüft werden unbekannte, fehlende, gemischte und gültige, aber semantisch unpassende Belege, erfundene Kennzahlen, unbelegte Lernstandsbehauptungen und die falsche Deutung von PENDING. Diese Kontrollen zählen separat von der Inferenz.
- SLI: vollständiges JSON, Anteil ausgelieferter generativer Antworten, Anteil zulässiger Verweise, 2A-Rubrik D1–D5, tatsächlich übergebene Fragen, Token, Zeit bis zum ersten Textfragment und Komponentenzeit. Technisches Versuchsziel: vollständige, verwendbare Ausgabe für jede gewertete Wiederholung und null unerlaubte ausgelieferte IDs. Historische Prüfschwellen aus 2A: ≥ 8/10 bei 9 von 10 Ausgaben, volle Punkte für D2/D3/D5, keine erfundenen Zahlen oder Lernstandsbehauptungen, ≥ 95 % innerhalb von 90 s und eine Gegenprobe ab 100 Fragen. Das Zeitkriterium wird zusätzlich für generativ akzeptierte Antworten ausgewiesen. Für die Belastung gilt der historische Zeitabbruch. Die Auswertung trennt fachliche Qualität vom Aufwand.

## 2. Umgebung

Upstream `1d71bd9583954d5304e3d56ee2cc716196190a65` ist der letzte First-Parent-Commit von main vor dem 07.11.2026 00:00 MEZ. Die historische Anwendung lief auf `87c39334619fbcb0c5782b061da1ba0df0ba3142`. Forschungsbranch `codex/2c-stichtag-20261106`, HEAD nach Rebase `e0c8e0546c5f71c882cc03d2b3b764d62e22a354`. Die drei Forschungspatches sind laut `git range-diff` identisch. Die Forschungserweiterungen liegen außerhalb des Anwendungsexports. Hardware, SHA-256, Laufzeitparameter und Quellprüfsummen werden in jeder Serie gespeichert. Qwen3-4B-Instruct-2507 Q4_K_M, lokales llama.cpp, Radeon RX 9070 XT, WSL, 4 CPU-Kerne als Containerquote, 8 GiB RAM-Limit, 8.192 Kontexttoken. Die Serverdatei hat denselben SHA-256 wie am 4. November. In allen drei neuen Serien wurden außerdem CPU, Modell-Digest, Node-Version, Containerquoten, WSL-Kernel und Betriebssystem mit dem historischen Manifest abgeglichen. Die einzige Inferenzverbindung ist Loopback im Container mit deaktiviertem externen Netz. Kein Browser, keine Datenbank, kein Redis und keine gemeinsame Warteschlange.

## 3. Messplan

Historische Snapshots direkt aus dem 640er-Messarchiv laden und durch das Stichtagsschema validieren. In jedem Lauf die tatsächliche Summary-Vorbereitung und den Runtime-Adapter des Stichtags verwenden. A behält den Anwendungsprompt. B ersetzt die Nutzlast durch dieselben ausgewählten Texte und IDs, beschränkt die neue Ausgabegrammatik und die abschließende Quellenbindung auf die in B zulässigen IDs. E-Meta-B fügt Status und Stimmen hinzu. Bei 1.024 nur das Ausgabe-Limit anheben, die Quellenauswahl behält die Reserve von 640. Die vier Requests beider Vergleichsserien müssen nach Entfernen von max_tokens paarweise übereinstimmen.

Je Vergleichsserie zwei Warm-ups und fünf Wiederholungen je Zelle, wechselnde Reihenfolge wie historisch. Für die beiden Erweiterungen enthält die Abgabe zwölf gewertete Läufe: zwei Szenarien × zwei Eingaben × drei Wiederholungen bei 1.024 Token. Die Messwerte stammen aus der ursprünglichen, bereits aufgewärmten Serie. Deren gemeinsame Warm-ups sind im gekürzten Archiv nicht enthalten. Bei einer neuen Messung verwendet der Runner zum Aufwärmen einmal `meta6-A` und einmal `meta6-B`. Die kürzere Abfolge kann die Laufzeiten beeinflussen. Vor jeder Anfrage KV-Slot löschen. Seed 456, Temperatur 0. Serien nacheinander auf derselben GPU. Ursprüngliche Läufe beider Budgets dauerten zusammen knapp sechs Minuten. Der erste reine Pack-Test von E-Long scheiterte bei acht Zusätzen an der Schemaobergrenze von 500 Zeichen. Vor dem ersten Inferenzlauf wurde die Erweiterung auf fünf Zusätze begrenzt; die historischen Fixtures blieben unberührt. Abbruch bei Pilot-Transportfehler oder Überschreiten des 12-Minuten-Studienlimits pro Serie. Fehler und Ersatzantworten bleiben erhalten.

## 4–6. Durchführung, Bewertung und Entscheidung

Jeder Einzelbeleg enthält die rohe Modellantwort, die Adapterentscheidung und die gebundene Hostausgabe. Pro Anfrage sind Konfiguration, Snapshot und Request über Serie, Szenario, Arm und Hash zuordenbar. Die Auswertung zählt Warm-ups separat, berichtet Mediane und Spannweiten und prüft die vorab formulierten Hypothesen. Wiederholungen derselben Eingabe liefern keine unabhängigen Themenstichproben. Die Interpretation und die vier Evidenzstufen stehen im [Verzeichnis der Testfälle](../README.md).

### Wiederholen

Aus dem Verzeichnis `docs/didaktik/referate/2c-tokenbudget` in der neuen Forschungsarbeitskopie ausführen. Ein bereits verifiziertes GPU-Testverzeichnis mit dem historischen Modell und Server wird benötigt. Ein frisches, absolutes Arbeitsverzeichnis vermeidet Kollisionen mit abgeschlossenen Läufen. `setup` benötigt Zugriff auf die Linux-Paketquellen. Die Inferenz und die Kontrollen laufen offline.

```bash
export GPU_DIR=/home/lena/Projects/arsnova.eu/tmp/wsl-gpu-validation
export STUDY_WORK=$(mktemp -d)
bash version_comparison/versuch.sh setup
bash version_comparison/versuch.sh pack 640
bash version_comparison/versuch.sh pack erweitert
bash version_comparison/versuch.sh measure 640
bash version_comparison/versuch.sh measure 1024
bash version_comparison/versuch.sh measure erweitert
bash version_comparison/versuch.sh kontrollen
```

Die Rohantworten liegen danach in `$STUDY_WORK/measure-*`, die Prüfung der Validierungsstufen in `$STUDY_WORK/kontrollen`. `versuch.sh` legt Messverzeichnisse nur neu an. Das bereits gespeicherte 2C-Material lässt sich ohne Inferenz neu auswerten:

```bash
pruefung=$(mktemp -d)
python3 version_comparison/auswerten.py --ausgabe "$pruefung"
diff -ru version_comparison/tabellen "$pruefung"
sha256sum -c version_comparison/SHA256SUMS
```

Für eine neue Archivserie zuerst die Rohdaten im eigenen Versuchsverzeichnis aufbewahren. Die Aktion `--archivieren "$STUDY_WORK"` ist zum erstmaligen Erstellen der drei JSONL-Archive in einer Studienkopie vorgesehen; vorhandene Archive lassen sich damit nicht überschreiben. Neue Inhalte benötigen eine eigene dokumentierte Rubrikbewertung.

Bei der Rubrik verglichen wir jeden unterschiedlichen ausgelieferten Wortlaut mit seinen Quellen. D1 zählt Elemente mit direktem Fragenbeleg; für D2–D5 sind Begründungen nach Inhaltshash hinterlegt. Eine Folge von einzelnen Originalfragen erhält keine Punkte für eine ausdrückliche thematische Gruppierung. Die Einordnung ist KI-gestützt; eine verblindete menschliche Zweitbewertung fehlt.

Beide November-Baselines beendeten jeweils 22 Aufrufe einschließlich Warm-ups. Der äußere Shell-Aufruf meldete nach Abschluss der zweiten Serie einen Lesefehler, weil sein Startskript während der Laufzeit um den separaten Kontrollbefehl ergänzt wurde. Die beiden internen Vitest-Protokolle bestätigen jeweils den abgeschlossenen Test. Alle 44 Einzeldateien, die Abschlussfelder der Servermanifeste und die vier Request-Paare wurden geprüft. Das gemountete Messskript und der Python-Server blieben während der Modellläufe unverändert. Der aktualisierte Shell-Aufruf besteht die Syntaxprüfung.
