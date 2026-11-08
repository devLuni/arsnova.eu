# Ergebnisse · Kontext und Kurzfassung bei 640 Token

Es gab zwei Warm-ups (P0) und 20 gewertete Läufe (R1–R5). A umfasst die ausgewählten Registerdaten, B nur die ausgewählten Fragen und ihre IDs. Die Zeit reicht vom Packen der Eingabe bis zur geprüften Backend-Ausgabe. [Anleitung](anleitung.md)

## Messung vom 8. November 2026

Alle 20 Modellantworten hatten vollständiges JSON und zulässige IDs. Der Formfilter lehnte alle 20 ab. In S6-B fehlte der Aussage »Klausurrelevanz von Kapitel 4 ist unklar.« die geforderte Themenüberschrift. Alle Hosts erhielten einen extraktiven Ersatz (4/10 Rubrikpunkte). Bei S6 enthielt er die Prüfungs- und Anwesenheitsfrage, bei S100 Regressions- und Prüfungsfragen.

| Datensatz | Eingabe | Eingabetoken | Ausgabetoken | Dauer (Median) |
| --------- | ------- | ------------ | ------------ | -------------- |
| S6        | A       | 2158         | 372          | 5,141 s        |
| S6        | B       | 296          | 289          | 3,390 s        |
| S100      | A       | 2211         | 564          | 7,314 s        |
| S100      | B       | 748          | 586          | 6,738 s        |

### Alle Läufe einschließlich Warm-ups

[Rohantworten, Requests und Hostausgaben](../../messreihe/rohdaten-640.jsonl) · [Bewertung der Ersatztexte](../../extended_experiments/inhaltsbewertung.json)

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

Im Datensatz S100 fragte eine Quelle »Ist Kapitel 4 klausurrelevant?«. Qwen formulierte in B: »Kapitel 4: Die Relevanz für die Klausur wird durch mehrere Fragen bestätigt und ist ein zentrales Lernziel.« Mehrere Nachfragen belegen den Klärungsbedarf. Sie bestätigen keinen Prüfungsstoff. Die Passage stand nur im Rohtext. [Lauf 640-R1-S100-B](../../messreihe/rohdaten-640.jsonl#L4)
