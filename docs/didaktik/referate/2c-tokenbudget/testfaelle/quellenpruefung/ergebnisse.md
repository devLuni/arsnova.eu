# Ergebnisse · Quellenbelege mit bekannten Fehlern

## Oktober-Baseline · direkte Quellenbindung

| Fall                                            | Ausgabe                                                                                   |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Nur unbekannte ID (`unknown`)                   | Aussage entfernt, Status `uncertain`.                                                     |
| Bekannte und unbekannte ID (`mixed`)            | Aussage behalten, unbekannte ID entfernt.                                                 |
| Falsche Aussage, bekannte ID (`false-semantic`) | »Alle 200 Studierenden haben die Regression verstanden.« bleibt erhalten, Status `ready`. |

Beide Oktober-Archive enthalten diese drei Kontrollausgaben wortgleich unter `controls.json`. [Archiv 640](../../messdaten-640/messarchiv.jsonl) · [Archiv 1.024](../../ausgabelimit-1024/messarchiv.jsonl)

## November-Baseline · gesamter Validierungspfad

| Eingespeister Fall                                                     | Backend-Entscheidung       |
| ---------------------------------------------------------------------- | -------------------------- |
| Zwei korrekte Aussagen (`korrekt`)                                     | Modelltext angenommen.     |
| Unbekannte ID (`unbekannte-id`)                                        | Extraktiver Ersatz.        |
| Bekannte und unbekannte ID (`gemischte-ids`)                           | Extraktiver Ersatz.        |
| Keine ID (`fehlende-id`)                                               | Extraktiver Ersatz.        |
| Echte ID zur falschen Frage (`falscher-beleg`)                         | Falschen Beleg angenommen. |
| Erfundenes Ergebnis von 73 Personen (`erfundene-statistik`)            | Falschaussage angenommen.  |
| Unbelegte Aussage zum Lernstand (`lernstandsdiagnose`)                 | Falschaussage angenommen.  |
| Ungeprüften Beitrag als abgelehnt gedeutet (`pending-fehldeutung`)     | Falschaussage angenommen.  |
| Geteilte Stimmen als Gleichgültigkeit gedeutet (`stimmen-fehldeutung`) | Falschaussage angenommen.  |
| Nur eine Aussage (`nur-ein-anliegen`)                                  | Extraktiver Ersatz.        |

Alle zehn Endergebnisse erhielten den Status `ready`, darunter die vier Ersatzantworten. Der gemeinsame Fall mit gemischten IDs zeigt den Unterschied der Testgrenzen: Im Oktober wurde nur die letzte Quellenbindung aufgerufen. Im November konnte bereits der Adapter die ganze Antwort durch einen Ersatz ersetzen. Die fünf angenommenen fachlichen Fehler zeigen, was die Prüfung durchlässt. Ihre Anzahl ist keine Fehlerrate von Qwen. [Vollständige Eingaben und Entscheidungen](../../extended_experiments/kontrollantworten.json) · [Audit der 56 archivierten Modellaufrufe](../../extended_experiments/pruefstufen.json) · [Anleitung](anleitung.md)
