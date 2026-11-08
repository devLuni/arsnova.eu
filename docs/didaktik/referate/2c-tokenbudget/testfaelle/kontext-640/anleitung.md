# Hauptversuch · Kontext und Kurzfassung bei 640 Token

S6 enthält sechs Referenzfragen. S100 ergänzt 94 synthetische Fragen zu den gleichen drei Anliegen: Regression üben, Prüfungsstoff klären und Anwesenheitspflicht klären. Beide Git-Stände erhalten dieselben zwei Datensätze.

1. Das Backend wählt Quellen aus dem jeweiligen Snapshot aus. In A bekommt Qwen diese Fragen mit den ausgewählten Registerdaten, etwa Stimmen und Themen. In B bekommt es dieselben Fragen in derselben Reihenfolge, nur mit Text und ID.
2. Qwen generiert das JSON mit höchstens 640 Ausgabetoken. Das Kontextfenster des Versuchs umfasst 8.192 Token. Für jede der vier Kombinationen gibt es fünf Messungen. Vorher läuft je ein Warm-up mit S100-A und S100-B.
3. Der Test speichert die rohe Modellantwort und die geprüfte Hostausgabe. Wenn die Anwendung die Modellantwort verwirft, liefert sie einen Ersatz aus vorhandenen Quellen. Ein Status `ready` kann deshalb zu beiden Ausgabearten gehören.

Die Befehle laufen aus dem Studienverzeichnis nach der [gemeinsamen Einrichtung](../../README.md#messungen-wiederholen).

```bash
# Oktober
OUT="$arbeit/640" bash qa-tests-ausfuehren.sh measure
# November
bash version_comparison/versuch.sh measure 640
```

[Testcode Oktober](../../qa-kurzfassung-tokenbudget.test.ts) · [Testcode November](../../version_comparison/qa-stichtag.test.ts)

[Alle Ergebnisse dieses Testfalls](ergebnisse.md) · [Übersicht und Einrichtung](../../README.md)
