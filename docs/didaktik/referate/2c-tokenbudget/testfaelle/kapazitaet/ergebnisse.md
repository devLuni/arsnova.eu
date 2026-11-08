# Ergebnisse · Platz für Fragetexte

## Oktober-Baseline · Rechenkontrolle für S6 und S100

| Datensatz | Enthalten bei 4.096 | Enthalten bei 8.192 | Rechnerisch passend als Text + ID | Nach zusätzlicher Obergrenze von 40 |
| --------- | ------------------: | ------------------: | --------------------------------: | ----------------------------------: |
| S6        |                   1 |                   3 |                                 6 |                                   6 |
| S100      |                   1 |                   3 |                                52 |                                  40 |

Die Rechnung ist in beiden Oktober-Serien unter `capacity.json` identisch gespeichert. Die 640er- und 1.024er-Modellläufe nutzten jeweils nur die drei ausgewählten Texte. Für eine mit 40 oder 52 Texten gefüllte Eingabe gibt es hier keine Messung zur Qualität oder Dauer. [Archiv 640](../../messdaten-640/messarchiv.jsonl) · [Archiv 1.024](../../ausgabelimit-1024/messarchiv.jsonl)

## November-Baseline · Beobachtung beim Packen

Bei 8.192 Token gingen auf dem neuen Stand in beiden Budgetserien **2 von 6** beziehungsweise **10 von 100** Texten an Qwen. Das sind die tatsächlichen Eingaben der Hauptversuche. Die separate Oktober-Rechnung mit 4.096 Token und aufgefülltem Textbudget wurde im November nicht wiederholt. [Auswahl aller Fälle](../../version_comparison/tabellen/fragenauswahl.csv) · [Anleitung](anleitung.md)
