# Ergebnisse · Kontext und Kurzfassung bei 640 Token

Pro Softwarestand gab es zwei Warm-ups (P0) und 20 gewertete Läufe (R1–R5). A umfasst die ausgewählten Registerdaten, B nur die ausgewählten Fragen und ihre IDs. Die Zeit reicht vom Packen der Eingabe bis zur geprüften Backend-Ausgabe. [Anleitung](anleitung.md)

## Oktober-Baseline · v1.3.0 vom 8. Oktober, gemessen am 4. November

Alle 20 Modellantworten erreichten die Grenze von 640 Token mitten im JSON. Der Host erhielt jedes Mal denselben extraktiven Ersatz (4/10 Rubrikpunkte). Vor der Serie scheiterte ein Serverstart an einer fehlenden Bibliothek. Dabei entstand keine Modellantwort. [Startprotokoll](../../messdaten-640/gpu-pruefungen.txt) In S6 und S100 sah Qwen jeweils drei Fragetexte.

| Datensatz | Eingabe | Eingabetoken | Ausgabetoken | Dauer (Median) |
| --------- | ------- | ------------ | ------------ | -------------- |
| S6        | A       | 2153         | 640          | 8,081 s        |
| S6        | B       | 295          | 640          | 6,924 s        |
| S100      | A       | 2162         | 640          | 8,124 s        |
| S100      | B       | 295          | 640          | 7,032 s        |

### Alle Läufe der Oktober-Baseline

[Rohantworten, Requests und Hostausgaben](../../messdaten-640/messarchiv.jsonl)

| Lauf-ID   | Eingabetoken | Ausgabetoken | Erstes Textfragment (ms) | Komponentenzeit (s) | Vollständiges JSON | Hostausgabe |
| --------- | ------------ | ------------ | ------------------------ | ------------------- | ------------------ | ----------- |
| P0-S100-A | 2162         | 640          | 657,0                    | 8,204               | nein               | Ersatz      |
| P0-S100-B | 295          | 640          | 102,6                    | 7,094               | nein               | Ersatz      |
| R1-S100-A | 2162         | 640          | 631,1                    | 8,175               | nein               | Ersatz      |
| R1-S100-B | 295          | 640          | 94,1                     | 7,108               | nein               | Ersatz      |
| R1-S6-A   | 2153         | 640          | 607,4                    | 8,098               | nein               | Ersatz      |
| R1-S6-B   | 295          | 640          | 97,6                     | 6,912               | nein               | Ersatz      |
| R2-S100-A | 2162         | 640          | 623,9                    | 8,177               | nein               | Ersatz      |
| R2-S100-B | 295          | 640          | 93,9                     | 7,022               | nein               | Ersatz      |
| R2-S6-A   | 2153         | 640          | 625,9                    | 8,086               | nein               | Ersatz      |
| R2-S6-B   | 295          | 640          | 96,7                     | 6,924               | nein               | Ersatz      |
| R3-S100-A | 2162         | 640          | 613,3                    | 8,124               | nein               | Ersatz      |
| R3-S100-B | 295          | 640          | 117,5                    | 7,165               | nein               | Ersatz      |
| R3-S6-A   | 2153         | 640          | 604,4                    | 8,050               | nein               | Ersatz      |
| R3-S6-B   | 295          | 640          | 93,8                     | 6,932               | nein               | Ersatz      |
| R4-S100-A | 2162         | 640          | 613,8                    | 8,101               | nein               | Ersatz      |
| R4-S100-B | 295          | 640          | 126,2                    | 7,032               | nein               | Ersatz      |
| R4-S6-A   | 2153         | 640          | 605,9                    | 8,081               | nein               | Ersatz      |
| R4-S6-B   | 295          | 640          | 94,5                     | 6,935               | nein               | Ersatz      |
| R5-S100-A | 2162         | 640          | 648,1                    | 8,101               | nein               | Ersatz      |
| R5-S100-B | 295          | 640          | 99,3                     | 7,025               | nein               | Ersatz      |
| R5-S6-A   | 2153         | 640          | 633,5                    | 8,062               | nein               | Ersatz      |
| R5-S6-B   | 295          | 640          | 94,1                     | 6,869               | nein               | Ersatz      |

## November-Baseline · Stand vom 6. November, gemessen am 8. November

Alle 20 Modellantworten hatten vollständiges JSON und zulässige IDs. Der neue Formfilter lehnte alle 20 ab. In S6-B fehlte der Aussage »Klausurrelevanz von Kapitel 4 ist unklar.« die geforderte Themenüberschrift. Alle Hosts erhielten einen extraktiven Ersatz (4/10 Rubrikpunkte). Bei S6 enthielt er die Prüfungs- und Anwesenheitsfrage, bei S100 Regressions- und Prüfungsfragen.

| Datensatz | Eingabe | Eingabetoken | Ausgabetoken | Dauer (Median) |
| --------- | ------- | ------------ | ------------ | -------------- |
| S6        | A       | 2158         | 372          | 5,141 s        |
| S6        | B       | 296          | 289          | 3,390 s        |
| S100      | A       | 2211         | 564          | 7,314 s        |
| S100      | B       | 748          | 586          | 6,738 s        |

### Alle Läufe der November-Baseline

[Rohantworten, Requests und Hostausgaben](../../version_comparison/rohdaten-640.jsonl) · [Bewertung der Ersatztexte](../../extended_experiments/inhaltsbewertung.json)

| Lauf-ID       | Eingabetoken | Ausgabetoken | Erstes Textfragment (ms) | Komponentenzeit (s) | Vollständiges JSON | Hostausgabe |
| ------------- | ------------ | ------------ | ------------------------ | ------------------- | ------------------ | ----------- |
| 640-P0-S100-A | 2211         | 564          | 652,4                    | 7,446               | ja                 | Ersatz      |
| 640-P0-S100-B | 748          | 586          | 205,1                    | 6,737               | ja                 | Ersatz      |
| 640-R1-S100-A | 2211         | 564          | 633,0                    | 7,293               | ja                 | Ersatz      |
| 640-R1-S100-B | 748          | 586          | 206,2                    | 6,738               | ja                 | Ersatz      |
| 640-R1-S6-A   | 2158         | 372          | 607,8                    | 5,229               | ja                 | Ersatz      |
| 640-R1-S6-B   | 296          | 289          | 93,4                     | 3,406               | ja                 | Ersatz      |
| 640-R2-S100-A | 2211         | 564          | 629,5                    | 7,314               | ja                 | Ersatz      |
| 640-R2-S100-B | 748          | 586          | 217,3                    | 6,660               | ja                 | Ersatz      |
| 640-R2-S6-A   | 2158         | 372          | 613,1                    | 5,106               | ja                 | Ersatz      |
| 640-R2-S6-B   | 296          | 289          | 96,1                     | 3,390               | ja                 | Ersatz      |
| 640-R3-S100-A | 2211         | 564          | 635,8                    | 7,376               | ja                 | Ersatz      |
| 640-R3-S100-B | 748          | 586          | 208,1                    | 6,726               | ja                 | Ersatz      |
| 640-R3-S6-A   | 2158         | 372          | 616,4                    | 5,180               | ja                 | Ersatz      |
| 640-R3-S6-B   | 296          | 289          | 107,7                    | 3,388               | ja                 | Ersatz      |
| 640-R4-S100-A | 2211         | 564          | 636,6                    | 7,298               | ja                 | Ersatz      |
| 640-R4-S100-B | 748          | 586          | 205,6                    | 6,768               | ja                 | Ersatz      |
| 640-R4-S6-A   | 2158         | 372          | 615,3                    | 5,133               | ja                 | Ersatz      |
| 640-R4-S6-B   | 296          | 289          | 108,9                    | 3,395               | ja                 | Ersatz      |
| 640-R5-S100-A | 2211         | 564          | 646,1                    | 7,385               | ja                 | Ersatz      |
| 640-R5-S100-B | 748          | 586          | 219,8                    | 6,760               | ja                 | Ersatz      |
| 640-R5-S6-A   | 2158         | 372          | 609,7                    | 5,141               | ja                 | Ersatz      |
| 640-R5-S6-B   | 296          | 289          | 101,6                    | 3,378               | ja                 | Ersatz      |

## Was änderte sich zwischen den Softwareständen?

Bei 640 stieg die Zahl vollständiger Antworten von 0 auf 20. Der Host erhielt in beiden Serien ausschließlich Ersatz. Die Komponentenzeit sank im Median der 20 einander zugeordneten Laufpaare um 1,875 s. Die Eingangsdaten waren gleich. Die November-Version wählte bei S6 zwei statt drei und bei S100 zehn statt drei Texte. Auch Prompt, Ausgabeformat und Formfilter änderten sich gemeinsam. Ein Zeitgewinn lässt sich daher keinem dieser Schritte allein zuschreiben. [Versionspaare](../../version_comparison/tabellen/versionspaare.csv) · [Quellenauswahl](../../version_comparison/tabellen/fragenauswahl.csv)

Die vorläufige Bewertung der sichtbaren Ersatztexte lag auf beiden Ständen bei 4/10. Im eigenen Datensatz erreichte der Regelkompass der 2A-Gruppe 5/10. Unterschiedliche Eingaben und Messgrenzen erlauben keinen direkten Leistungsvergleich. Für 2B liegen in dieser Untersuchung keine Gruppenergebnisse vor. [Bewertung Oktober](../../messdaten-640/rubrikpunkte-pro-lauf.csv) · [Ergebnisse 2A](https://github.com/XarotDev/arsnova.eu/blob/3fc9f5ceffc769804e2a085d95f4608d3f1cd788/docs/didaktik/referate/2a-regelbasierte-extraktive-referenz/evidence/E4/bewertung-a657798e.md)
