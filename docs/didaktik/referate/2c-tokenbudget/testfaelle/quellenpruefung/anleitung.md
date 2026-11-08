# Quellenbelege mit bekannten Fehlern prüfen

Im Oktober setzt der Test drei vorbereitete Antworten direkt in die Quellenbindung ein. Im November gehen zehn vorbereitete Antworten durch den Backend-Adapter, die Formatprüfung und die abschließende Quellenbindung. Die Antworten stehen vorab fest. Qwen wird dafür nicht aufgerufen.

Im November überprüft der Test außerdem die Validierungsstufen der bereits gespeicherten 76 Modellaufrufe (inklusive Warm-ups). Dazu braucht er die drei vollständigen November-Serien im selben Arbeitsverzeichnis.

Die Befehle laufen aus dem Studienverzeichnis nach der [gemeinsamen Einrichtung](../../README.md#messungen-wiederholen). Für Oktober genügt `pack`. Nach den drei November-Serien (`640`, `1024`, `erweitert`) ausführen:

```bash
bash version_comparison/versuch.sh kontrollen
```

[Oktober-Test](../../qa-kurzfassung-tokenbudget.test.ts) · [November-Kontrollen](../../extended_experiments/quellenpruefung.test.ts)

[Alle Ergebnisse dieses Testfalls](ergebnisse.md) · [Übersicht und Einrichtung](../../README.md)
