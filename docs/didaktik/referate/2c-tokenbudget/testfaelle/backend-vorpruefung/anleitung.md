# Vorprüfung der arsnova-Komponenten

Die vorhandenen Backend-Suiten prüfen Kontextaufbereitung, Packen, Warteschlange und Modellclient. Am Novemberstand kommt die Suite für die Qualität der Kurzfassung hinzu. Die Vorprüfung zeigt, ob der für den Versuch verwendete Anwendungsexport seine eigenen Tests besteht. Sie bewertet keine Modellantwort.

Die Befehle laufen aus dem Studienverzeichnis nach der [gemeinsamen Einrichtung](../../README.md#messungen-wiederholen). Im Oktober führt `qa-tests-ausfuehren.sh setup` diese Suiten bereits aus. Für November:

```bash
bash version_comparison/versuch.sh verify
```

[Oktober-Runner](../../qa-tests-ausfuehren.sh) · [November-Runner](../../version_comparison/versuch.sh)

[Alle Ergebnisse dieses Testfalls](ergebnisse.md) · [Übersicht und Einrichtung](../../README.md)
