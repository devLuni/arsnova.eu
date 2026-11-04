# 2C – So funktionieren die Tests der Q&A-Kurzfassung

Die Tests schicken synthetische Fragen an das lokale Modell Qwen und prüfen, welche Kurzfassung das arsnova-Backend für die Lehrperson zurückgibt. Zwei Dinge werden getrennt variiert: welche Informationen Qwen erhält und wie lang seine Antwort werden darf. Die Messwerte stehen in den [Testergebnissen](test_results.md).

Der eigentliche Test steht in [qa-kurzfassung-tokenbudget.test.ts](qa-kurzfassung-tokenbudget.test.ts). Zum Ausführen im WSL-Terminal dient [qa-tests-ausfuehren.sh](qa-tests-ausfuehren.sh). Die Startbefehle stehen weiter unten.

## Was bekommt Qwen zu sehen?

1. **Testdaten.** S6 enthält sechs Fragen aus dem Referenzdatensatz von arsnova. S100 ergänzt 94 künstliche Fragen zu denselben drei Anliegen (Regression üben, Prüfungsstoff klären, Anwesenheit klären).
2. **Auswahl durch arsnova.** Der Backend-Code wählt Fragen und Quellen aus, die zusammen in das Eingabebudget passen. In beiden Datensätzen bleiben dieselben **drei Fragetexte** übrig. Qwen bekommt also auch bei S100 nur drei Texte zu lesen.
3. **Zwei Eingabevarianten.** In **A** erhält Qwen diese Fragen mit den ausgewählten Registerdaten, etwa Quellen-IDs, Stimmen, Status, Thema und Lernziel. In **B** erhält es dieselben Texte in derselben Reihenfolge mit ihren IDs. Die Metadaten fallen weg. Der Test füllt den freien Platz nicht mit weiteren Fragen auf.
4. **Prüfung der Antwort.** Das Backend prüft das JSON, das erwartete Antwortformat und die Quellen-IDs. Kann es die Modellantwort nicht verwenden, gibt es vorhandene Belege als Ersatz zurück (extraktiver Fallback). Der Test speichert sowohl den Modelltext als auch die vom Backend zurückgegebene Kurzfassung.

## Welche Tests laufen?

| Test                                | Was wird geprüft?                                                                                                                                                                                                                            |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend und Quellenbindung          | Vier vorhandene Testsuiten prüfen Kontextaufbau, Auswahl, Warteschlange und Modellclient. Drei zusätzliche Kontrollen testen unbekannte IDs, gemischte IDs und eine sachlich falsche Aussage mit gültiger ID.                                |
| Hauptversuch mit 640 Ausgabetoken   | S6 und S100 durchlaufen jeweils A und B. Gemessen werden Eingabe- und Ausgabetoken, Zeit für die Verarbeitung der Eingabe, Zeit bis zum ersten Textfragment und Zeit bis zum fertigen Backend-Ergebnis.                                      |
| Folgeversuch mit 1.024 Ausgabetoken | Dieselben vier gespeicherten Modellanfragen werden erneut gesendet. Nur die Ausgabegrenze steigt. Der Vergleich ordnet jeder Wiederholung den entsprechenden 640er-Lauf zu und prüft Eingabegleichheit, Antwortgültigkeit und Zeitdifferenz. |

Je Serie laufen zwei Aufwärmanfragen und anschließend 20 gewertete Anfragen (vier Bedingungen × fünf Wiederholungen). Qwen3-4B-Instruct-2507 Q4_K_M läuft unter WSL auf der Radeon RX 9070 XT mit einem Slot, Seed 456 und Temperatur 0. Vor jeder Anfrage leert der Test den Slot. Das Modellfenster umfasst 8.192 Token. Die ursprüngliche Auswahl reserviert 640 für die Antwort und 128 als Sicherheitsmarge. Der Folgeversuch verwendet diese bereits ausgewählten Eingaben. Gemessen wird die Backend-Komponente ab der Fragenauswahl bis zum geprüften Ergebnis. Die äußere Warteschlange und der Browser liegen außerhalb der Zeitmessung.

## Testergebnisse ohne GPU nachprüfen

Im Verzeichnis dieser README ausführen. Python ab 3.11 genügt. Die Befehle berechnen die Tabellen in einem temporären Verzeichnis neu. Wenn die Werte mit den gespeicherten Ergebnissen übereinstimmen, geben die beiden Vergleiche nichts aus.

```bash
sha256sum -c messdaten-640/SHA256SUMS
(cd ausgabelimit-1024 && sha256sum -c SHA256SUMS)
pruefung=$(mktemp -d)
python3 messlaeufe-auswerten.py --out "$pruefung/640"
diff -u messdaten-640/einzelmessungen.csv "$pruefung/640/einzelmessungen.csv"
python3 ausgabelimit-1024/ausgabelimits-vergleichen.py --pairs "$pruefung/laufpaare-640-1024.csv"
diff -u ausgabelimit-1024/laufpaare-640-1024.csv "$pruefung/laufpaare-640-1024.csv"
```

## Tests auf der GPU wiederholen

Voraussetzungen sind WSL mit GPU-Zugriff, Docker, das lokale SDK-Image, der kompilierte Modellserver und die geprüfte Modelldatei. Die Schritte zur Einrichtung stehen im [GPU-Kompatibilitätstest](../../../implementation/WSL-GPU-VALIDATION-2026-10-21.md). Die folgenden Blöcke im selben WSL-Terminal aus dem Projektstamm ausführen.

**1. Release vorbereiten.** `setup` entpackt den [getesteten Stand v1.3.0](https://github.com/kqc-real/arsnova.eu/tree/87c39334619fbcb0c5782b061da1ba0df0ba3142), installiert die Abhängigkeiten und startet die vier Backend-Testsuiten. `pack` prüft anschließend die Testdaten und die Quellenbindung. Auf dem bereits eingerichteten Testrechner kann das vorhandene Release wiederverwendet werden.

```bash
study="$PWD/docs/didaktik/referate/2c-tokenbudget"
mkdir -p "$PWD/tmp/topic2c"
work=$(mktemp -d "$PWD/tmp/topic2c/testserie.XXXXXX")
export OUT="$work/640"
if [[ -x "$PWD/tmp/topic2c/release/.study-node/node" ]]; then
  export TOPIC2C_SCRATCH="$PWD/tmp/topic2c"
else
  export TOPIC2C_SCRATCH="$work/quelle"
  bash "$study/qa-tests-ausfuehren.sh" setup
  bash "$study/qa-tests-ausfuehren.sh" pack
fi
```

**2. Hauptversuch starten.** Die [Testdatei](qa-kurzfassung-tokenbudget.test.ts) baut die Eingaben auf und ruft den Release-Adapter auf. Der [Runner](qa-tests-ausfuehren.sh) startet den lokalen Modellserver ohne externes Netz. Einzelne Antworten stehen unter `$OUT`, z. B. in `R1-S6-A.json`. `rawContent` enthält den ursprünglichen Modelltext, `bound` das geprüfte Backend-Ergebnis.

```bash
bash "$study/qa-tests-ausfuehren.sh" measure
python3 "$study/messlaeufe-auswerten.py" --runs "$OUT" --out "$work/auswertung-640"
```

**3. Folgeversuch starten.** Das [Vorbereitungsskript](ausgabelimit-1024/1024-token-test-vorbereiten.py) erzeugt die Testdatei aus den archivierten Anfragen des dokumentierten 640er-Laufs. Der [Paarvergleich](ausgabelimit-1024/ausgabelimits-vergleichen.py) vergleicht mit dieser festen Referenz. Nach Schritt 1 kann der Folgeversuch auch einzeln laufen.

```bash
export OUT="$work/1024"
python3 "$study/ausgabelimit-1024/1024-token-test-vorbereiten.py" "$work/harness"
bash "$work/harness/qa-tests-ausfuehren.sh" measure
python3 "$study/messlaeufe-auswerten.py" --runs "$OUT" --out "$work/auswertung-1024"
python3 "$study/ausgabelimit-1024/ausgabelimits-vergleichen.py" --archive "$work/auswertung-1024/messarchiv.jsonl" --pairs "$work/laufpaare-640-1024.csv"
```

## Bezug zu 2A

Die 2C-Inhaltsbewertung verwendet die fünf Kriterien der 2A-Gruppe. Deren eigene Versuche zum Regelkompass und zur extraktiven Kurzfassung sind im 2A-Repository getrennt dokumentiert. [Testdokumentation 2A](https://github.com/XarotDev/arsnova.eu/blob/3fc9f5ceffc769804e2a085d95f4608d3f1cd788/docs/didaktik/referate/2a-regelbasierte-extraktive-referenz/README.md) · [Bewertungsrubrik](https://github.com/XarotDev/arsnova.eu/blob/3fc9f5ceffc769804e2a085d95f4608d3f1cd788/docs/didaktik/referate/2a-regelbasierte-extraktive-referenz/evidence/E4/rubrik.md) · [Testergebnisse 2A](https://github.com/XarotDev/arsnova.eu/blob/3fc9f5ceffc769804e2a085d95f4608d3f1cd788/docs/didaktik/referate/2a-regelbasierte-extraktive-referenz/evidence/E4/bewertung-a657798e.md)
