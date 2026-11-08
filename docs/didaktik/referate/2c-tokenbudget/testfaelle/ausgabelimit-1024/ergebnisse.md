# Ergebnisse · Ausgabelimit von 1.024 Token

Pro Softwarestand gab es zwei Warm-ups (P0) und 20 gewertete Läufe (R1–R5). A umfasst die ausgewählten Registerdaten, B nur die ausgewählten Fragen und ihre IDs. Die Zeit reicht vom Packen der Eingabe bis zur geprüften Backend-Ausgabe. [Anleitung](anleitung.md)

## Oktober-Baseline · v1.3.0 vom 8. Oktober, gemessen am 4. November

Alle 20 Modellantworten endeten mit vollständigem JSON. Der Host erhielt die generierte Fassung. Sie benötigte 666 bis 704 Token. Gegenüber den zugehörigen 640er-Läufen dauerte die Komponente im Median 0,482 s länger. Die Rubrik ergab 5/10 für S6-A, 7/10 für S100-A und 5/10 für beide B-Bedingungen. S100-A nannte z. B. zwei ausgelassene Fragen, tatsächlich waren es 97. [Laufpaare](../../ausgabelimit-1024/laufpaare-640-1024.csv) · [Sichtbare Texte](../../ausgabelimit-1024/sichtbare-ausgaben.json) In S6 und S100 sah Qwen jeweils drei Fragetexte.

| Datensatz | Eingabe | Eingabetoken | Ausgabetoken | Dauer (Median) |
| --------- | ------- | ------------ | ------------ | -------------- |
| S6        | A       | 2153         | 704          | 8,887 s        |
| S6        | B       | 295          | 666          | 7,368 s        |
| S100      | A       | 2162         | 684          | 8,689 s        |
| S100      | B       | 295          | 666          | 7,384 s        |

### Alle Läufe der Oktober-Baseline

[Rohantworten, Requests und Hostausgaben](../../ausgabelimit-1024/messarchiv.jsonl)

| Lauf-ID   | Eingabetoken | Ausgabetoken | Erstes Textfragment (ms) | Komponentenzeit (s) | Vollständiges JSON | Hostausgabe |
| --------- | ------------ | ------------ | ------------------------ | ------------------- | ------------------ | ----------- |
| P0-S100-A | 2162         | 684          | 663,5                    | 8,888               | ja                 | generiert   |
| P0-S100-B | 295          | 666          | 104,9                    | 7,516               | ja                 | generiert   |
| R1-S100-A | 2162         | 684          | 617,8                    | 8,648               | ja                 | generiert   |
| R1-S100-B | 295          | 666          | 99,2                     | 7,408               | ja                 | generiert   |
| R1-S6-A   | 2153         | 704          | 617,7                    | 8,908               | ja                 | generiert   |
| R1-S6-B   | 295          | 666          | 94,0                     | 7,403               | ja                 | generiert   |
| R2-S100-A | 2162         | 684          | 614,0                    | 8,709               | ja                 | generiert   |
| R2-S100-B | 295          | 666          | 115,7                    | 7,384               | ja                 | generiert   |
| R2-S6-A   | 2153         | 704          | 617,3                    | 8,864               | ja                 | generiert   |
| R2-S6-B   | 295          | 666          | 93,3                     | 7,354               | ja                 | generiert   |
| R3-S100-A | 2162         | 684          | 613,1                    | 8,696               | ja                 | generiert   |
| R3-S100-B | 295          | 666          | 93,3                     | 7,336               | ja                 | generiert   |
| R3-S6-A   | 2153         | 704          | 615,5                    | 8,887               | ja                 | generiert   |
| R3-S6-B   | 295          | 666          | 95,8                     | 7,387               | ja                 | generiert   |
| R4-S100-A | 2162         | 684          | 626,1                    | 8,651               | ja                 | generiert   |
| R4-S100-B | 295          | 666          | 94,1                     | 7,327               | ja                 | generiert   |
| R4-S6-A   | 2153         | 704          | 616,2                    | 8,999               | ja                 | generiert   |
| R4-S6-B   | 295          | 666          | 95,8                     | 7,368               | ja                 | generiert   |
| R5-S100-A | 2162         | 684          | 617,2                    | 8,689               | ja                 | generiert   |
| R5-S100-B | 295          | 666          | 93,3                     | 7,427               | ja                 | generiert   |
| R5-S6-A   | 2153         | 704          | 616,7                    | 8,860               | ja                 | generiert   |
| R5-S6-B   | 295          | 666          | 99,3                     | 7,335               | ja                 | generiert   |

## November-Baseline · Stand vom 6. November, gemessen am 8. November

Alle 20 Modellantworten hatten vollständiges JSON und zulässige IDs. Der neue Formfilter lehnte alle 20 ab. In S6-B fehlte der Aussage »Klausurrelevanz von Kapitel 4 ist unklar.« die geforderte Themenüberschrift. Alle Hosts erhielten einen extraktiven Ersatz (4/10 Rubrikpunkte). Bei S6 enthielt er die Prüfungs- und Anwesenheitsfrage, bei S100 Regressions- und Prüfungsfragen.

| Datensatz | Eingabe | Eingabetoken | Ausgabetoken | Dauer (Median) |
| --------- | ------- | ------------ | ------------ | -------------- |
| S6        | A       | 2158         | 372          | 5,160 s        |
| S6        | B       | 296          | 289          | 3,430 s        |
| S100      | A       | 2211         | 564          | 7,284 s        |
| S100      | B       | 748          | 586          | 6,707 s        |

### Alle Läufe der November-Baseline

[Rohantworten, Requests und Hostausgaben](../../version_comparison/rohdaten-1024.jsonl) · [Bewertung der Ersatztexte](../../extended_experiments/inhaltsbewertung.json)

| Lauf-ID        | Eingabetoken | Ausgabetoken | Erstes Textfragment (ms) | Komponentenzeit (s) | Vollständiges JSON | Hostausgabe |
| -------------- | ------------ | ------------ | ------------------------ | ------------------- | ------------------ | ----------- |
| 1024-P0-S100-A | 2211         | 564          | 660,4                    | 7,381               | ja                 | Ersatz      |
| 1024-P0-S100-B | 748          | 586          | 210,0                    | 6,723               | ja                 | Ersatz      |
| 1024-R1-S100-A | 2211         | 564          | 635,5                    | 7,276               | ja                 | Ersatz      |
| 1024-R1-S100-B | 748          | 586          | 208,7                    | 6,801               | ja                 | Ersatz      |
| 1024-R1-S6-A   | 2158         | 372          | 612,1                    | 5,173               | ja                 | Ersatz      |
| 1024-R1-S6-B   | 296          | 289          | 93,2                     | 3,420               | ja                 | Ersatz      |
| 1024-R2-S100-A | 2211         | 564          | 632,7                    | 7,282               | ja                 | Ersatz      |
| 1024-R2-S100-B | 748          | 586          | 212,7                    | 6,703               | ja                 | Ersatz      |
| 1024-R2-S6-A   | 2158         | 372          | 638,6                    | 5,100               | ja                 | Ersatz      |
| 1024-R2-S6-B   | 296          | 289          | 94,8                     | 3,430               | ja                 | Ersatz      |
| 1024-R3-S100-A | 2211         | 564          | 645,7                    | 7,284               | ja                 | Ersatz      |
| 1024-R3-S100-B | 748          | 586          | 206,9                    | 6,707               | ja                 | Ersatz      |
| 1024-R3-S6-A   | 2158         | 372          | 627,1                    | 5,160               | ja                 | Ersatz      |
| 1024-R3-S6-B   | 296          | 289          | 90,6                     | 3,350               | ja                 | Ersatz      |
| 1024-R4-S100-A | 2211         | 564          | 636,7                    | 7,316               | ja                 | Ersatz      |
| 1024-R4-S100-B | 748          | 586          | 211,0                    | 6,858               | ja                 | Ersatz      |
| 1024-R4-S6-A   | 2158         | 372          | 618,6                    | 5,178               | ja                 | Ersatz      |
| 1024-R4-S6-B   | 296          | 289          | 98,7                     | 3,437               | ja                 | Ersatz      |
| 1024-R5-S100-A | 2211         | 564          | 640,3                    | 7,355               | ja                 | Ersatz      |
| 1024-R5-S100-B | 748          | 586          | 217,6                    | 6,703               | ja                 | Ersatz      |
| 1024-R5-S6-A   | 2158         | 372          | 628,1                    | 5,135               | ja                 | Ersatz      |
| 1024-R5-S6-B   | 296          | 289          | 104,0                    | 3,455               | ja                 | Ersatz      |

## Was änderte sich zwischen den Softwareständen?

Im Oktober machte das höhere Budget alle 20 Ausgaben verwendbar. Im November waren die Antworten bei 640 und 1.024 Token für jede Eingabe bereits bytegleich. Die Differenz der gepaarten Zeiten für die beiden Budgets betrug im November im Median −0,006 s. Im Versionsvergleich bei festgehaltenen 1.024 Token sank die Komponentenzeit im Median der 20 Paare um 2,576 s. Die Eingangsdaten waren gleich. Die November-Version wählte bei S6 zwei statt drei und bei S100 zehn statt drei Texte. Auch Prompt, Ausgabeformat und Formfilter änderten sich gemeinsam. Ein Zeitgewinn lässt sich daher keinem dieser Schritte allein zuschreiben. [Versionspaare](../../version_comparison/tabellen/versionspaare.csv) · [Quellenauswahl](../../version_comparison/tabellen/fragenauswahl.csv)
