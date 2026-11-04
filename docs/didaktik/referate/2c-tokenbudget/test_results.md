# 2C – Testergebnisse der lokalen Q&A-Kurzfassung

Gemessen am 04.11.2026 mit arsnova v1.3.0 und Qwen3-4B-Instruct-2507 Q4_K_M auf einer Radeon RX 9070 XT unter WSL. Pro Ausgabegrenze wurden 20 Anfragen gewertet. **Bei 640 Token lieferte das Backend in allen 20 Fällen einen extraktiven Ersatz. Bei 1.024 Token akzeptierte es alle 20 generierten Kurzfassungen.** [Testaufbau und Startbefehle](README.md)

## Auswahl und Laufzeiten

Von sechs bzw. 100 vorhandenen Fragen gelangten in beiden Varianten dieselben drei Fragetexte ins Modell. **A** enthielt zusätzlich ausgewählte Registerdaten, **B** nur die Texte und Quellen-IDs. Jeder Tabellenwert zur Zeit ist der Median von fünf Wiederholungen. Die Gesamtzeit beginnt mit der Fragenauswahl und endet mit der vom Backend geprüften Ausgabe.

| Fragen im Datensatz | Eingabe               | Eingabetoken | Erstes Textfragment bei 640 | Gesamtzeit bei 640 | Gesamtzeit bei 1.024 | Erzeugte Token bei 1.024 |
| ------------------: | --------------------- | -----------: | --------------------------: | -----------------: | -------------------: | -----------------------: |
|                   6 | A · mit Registerdaten |        2.153 |                      607 ms |            8,081 s |              8,887 s |                      704 |
|                   6 | B · nur Texte und IDs |          295 |                       95 ms |            6,924 s |              7,368 s |                      666 |
|                 100 | A · mit Registerdaten |        2.162 |                      624 ms |            8,124 s |              8,689 s |                      684 |
|                 100 | B · nur Texte und IDs |          295 |                       99 ms |            7,032 s |              7,384 s |                      666 |

Im 100er-Datensatz benötigte das Modell bei 640 Token im Median **612 ms** für das Einlesen der Eingabe A und **90 ms** für B. Über alle 20 Laufpaare dauerte die Verarbeitung bei 1.024 Token **0,482 s länger (+6,7 %)** im Median. Hier wurde zuerst die Differenz jedes Paars berechnet. Die Mehrzeit lag zwischen 0,171 und 0,918 s. Beide Serien liefen nacheinander auf demselben Rechner. [Einzelmessungen bei 640](messdaten-640/einzelmessungen.csv) · [Gepaarter Vergleich mit 1.024](ausgabelimit-1024/laufpaare-640-1024.csv)

Die getrennte Kapazitätsrechnung ergab: Ohne Registerdaten hätten unter derselben Auswahlgrenze bis zu sechs bzw. 40 Fragetexte in die Eingabe gepasst. Für die Messung wurden in beiden Varianten nur die drei ausgewählten Texte verwendet. Im 640er-Versuch lagen die gemessenen Container-Speicherstände nach den Anfragen bei rund 3.535–3.673 MiB. [Rohdaten mit Kapazitätsrechnung](messdaten-640/messarchiv.jsonl) · [Messwertübersicht](messdaten-640/messwertuebersicht.json)

## Technische und inhaltliche Prüfung

| Backend-Prüfung                                                            | 640 Token | 1.024 Token |
| -------------------------------------------------------------------------- | --------: | ----------: |
| Vollständiges JSON vom Modell                                              |      0/20 |       20/20 |
| Generierte Antwort mit gültigem Format und gültigen Quellen-IDs angenommen |      0/20 |       20/20 |
| Ersatz aus bereits vorhandenen Belegen zurückgegeben                       |     20/20 |        0/20 |

Alle 640er-Antworten endeten mit `length` mitten im JSON. Jede 1.024er-Antwort begann mit genau demselben Text wie ihr 640er-Gegenstück und endete regulär mit `stop`. Für den Abschluss brauchte das Modell 26 bis 64 zusätzliche Token. [Modellantworten bei 640](messdaten-640/messarchiv.jsonl) · [Modellantworten bei 1.024](ausgabelimit-1024/messarchiv.jsonl)

Bei 640 war der sichtbare Ersatz in allen Läufen identisch. Bei 1.024 gab es drei unterschiedliche sichtbare Ausgaben. Sie wurden mit den tatsächlich übermittelten Quellen verglichen. Die Punkte sind eine vorläufige KI-gestützte Bewertung anhand der fünf Kriterien aus 2A: Fragenbezug, Bedeutung der Stimmen, Trennung der Anliegen, sichtbare Informationslücken und Themenabdeckung. Eine unabhängige Zweitbewertung liegt nicht vor. [Bewertungsrubrik 2A](https://github.com/XarotDev/arsnova.eu/blob/3fc9f5ceffc769804e2a085d95f4608d3f1cd788/docs/didaktik/referate/2a-regelbasierte-extraktive-referenz/evidence/E4/rubrik.md)

| Sichtbares Ergebnis                 | Beobachtung am Testfall                                                                                                                                                                                            | Punkte |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -----: |
| 640 · extraktiver Ersatz (20 Läufe) | Drei Fragen und ein Themenbeleg. Alle drei Anliegen sind erkennbar, die geteilten Stimmen zur Anwesenheit werden nicht erklärt.                                                                                    |   4/10 |
| 1.024 · S6, A (5 Läufe)             | Die Antwort stellt ein Lernziel als erreichte Fähigkeit dar. Sie meldet fehlende Bewertungen zur Anwesenheit, obwohl 40 positive und 40 negative Stimmen vorliegen. Sie nennt zwei ausgelassene Fragen statt drei. |   5/10 |
| 1.024 · S100, A (5 Läufe)           | Derselbe Fehler beim Lernziel. Die gleich verteilten Stimmen werden richtig beschrieben. Die Antwort nennt zwei ausgelassene Fragen statt 97.                                                                      |   7/10 |
| 1.024 · S6 und S100, B (10 Läufe)   | Die Antwort gibt alle drei Anliegen mit passenden IDs wieder. Für die Behauptung, zuständige Institutionen müssten die Prüfungsrelevanz oder Anwesenheitspflicht bestätigen, fehlt ein Beleg.                      |   5/10 |

Die gespeicherten Ausgaben zeigen, worauf die Bewertung beruht. Fünf Wiederholungen derselben Eingabe liefern Zeitmessungen für diesen Fall. Die 97 ausgelassenen Fragetexte können damit nicht inhaltlich bewertet werden. [Sichtbarer Ersatz bei 640](messdaten-640/sichtbare-ausgaben.json) · [Drei sichtbare Ausgaben bei 1.024](ausgabelimit-1024/sichtbare-ausgaben.json)

## Kontrolltests

Alle **90 Tests** der vier verwendeten Backend-Testsuiten bestanden. Die drei zusätzlichen Prüfungen der Quellenbindung ergaben:

- Eine Aussage mit ausschließlich unbekannter Quellen-ID wurde entfernt. Das Ergebnis erhielt den Status `uncertain`.
- Bei einer Aussage mit einer bekannten und einer unbekannten ID blieb nur die bekannte ID erhalten.
- Eine absichtlich falsche Lernstandsaussage mit existierender ID erhielt `ready`. Die ID-Prüfung allein erkennt diesen inhaltlichen Fehler nicht.

Die drei Kontrollausgaben sind unter `controls.json` im Archiv gespeichert. [Testergebnis der vier Suites](messdaten-640/backend-und-gpu-pruefungen.txt) · [Archiv der Kontrollen](messdaten-640/messarchiv.jsonl)
