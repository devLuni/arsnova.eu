# Position der Untertitelfrage

Im 100er-Datensatz wird ein Beitrag durch die Frage »Sind für die Vorlesungsaufzeichnungen Untertitel vorgesehen?« ersetzt. Der Test tauscht den Inhalt zwischen zwei ansonsten gleich gewichteten Einträgen. In einer Variante steht die Frage auf ID-Position 7, in der anderen auf 100. So lässt sich nachvollziehen, ob das Anliegen in der Auswahl, im Modelltext oder erst in der Hostausgabe fehlt.

Der [November-Test](../../version_comparison/qa-stichtag.test.ts) führt die Szenarien gemeinsam aus. Für jede Variante gibt es drei Messläufe in A und drei in B, jeweils mit 1.024 Ausgabetoken. Im Roharchiv ist dieser Test am Namen **focus7 und focus100** erkennbar. Die gemeinsamen Warm-ups gehören zu `order6`.

Die Befehle laufen aus dem Studienverzeichnis nach der [gemeinsamen Einrichtung](../../README.md#messungen-wiederholen). Diese beiden Befehle erzeugen die vier Erweiterungstests in **einer** Serie. Einmal ausführen genügt.

```bash
bash version_comparison/versuch.sh pack erweitert
bash version_comparison/versuch.sh measure erweitert
```

[Versuchsplan](../../version_comparison/methodik.md) · [Referenz bei 1.024 Token](../ausgabelimit-1024/ergebnisse.md)

[Alle Ergebnisse dieses Testfalls](ergebnisse.md) · [Übersicht und Einrichtung](../../README.md)
