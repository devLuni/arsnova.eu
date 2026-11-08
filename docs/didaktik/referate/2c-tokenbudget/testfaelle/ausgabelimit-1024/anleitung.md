# Folgeversuch · 1.024 statt 640 Ausgabetoken

Für jeden Softwarestand nimmt dieser Versuch die gleichen vier Eingaben wie der [640er-Versuch](../kontext-640/anleitung.md). Nur die Ausgabegrenze steigt von 640 auf 1.024. So lässt sich prüfen, ob mehr Platz ein abgebrochenes JSON vervollständigt und wie sich die Laufzeit ändert.

Im Oktober erzeugt ein Skript die Testdatei aus den archivierten 640er-Requests. Im November verwendet der Test dieselbe Kontextaufbereitung und ändert das Limit im Request. Die Auswahl behält ihre ursprüngliche Reserve. Pro Stand folgen auf zwei Warm-ups 20 Messläufe. Der Paarvergleich ordnet sie nach Datensatz, A/B und Wiederholung zu.

Die Befehle laufen aus dem Studienverzeichnis nach der [gemeinsamen Einrichtung](../../README.md#messungen-wiederholen). Der erzeugte Oktober-Runner muss im Git-Worktree liegen. Dafür wird hier das vorbereitete Verzeichnis `$arbeit` verwendet.

```bash
# Oktober
python3 ausgabelimit-1024/1024-token-test-vorbereiten.py "$arbeit/harness"
OUT="$arbeit/1024" bash "$arbeit/harness/qa-tests-ausfuehren.sh" measure
# November
bash version_comparison/versuch.sh measure 1024
```

[Oktober-Runner erzeugen](../../ausgabelimit-1024/1024-token-test-vorbereiten.py) · [Läufe paarweise vergleichen](../../ausgabelimit-1024/ausgabelimits-vergleichen.py) · [November-Test](../../version_comparison/qa-stichtag.test.ts)

[Alle Ergebnisse dieses Testfalls](ergebnisse.md) · [Übersicht und Einrichtung](../../README.md)
