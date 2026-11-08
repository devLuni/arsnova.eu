# Wie viele Fragetexte passen in die Eingabe?

Der Oktober-Test packt S6 und S100 einmal mit dem Release-Profil (4.096 Token) und einmal mit dem Studienprofil (8.192 Token). Anschließend berechnet er für dieselbe Reihenfolge, wie viele kompakte Texte mit ID in 7.424 Eingabeeinheiten passen würden. Das Backend schätzt konservativ anhand der UTF-8-Bytes. Für die zusätzlich passenden Texte wird kein Modell aufgerufen.

Die Befehle laufen aus dem Studienverzeichnis nach der [gemeinsamen Einrichtung](../../README.md#messungen-wiederholen). Die Kapazitätsrechnung läuft im Packschritt der Oktober-Einrichtung. Für eine eigene Ausgabe:

```bash
OUT="$arbeit/kapazitaet" bash qa-tests-ausfuehren.sh pack
```

[Testcode](../../qa-kurzfassung-tokenbudget.test.ts) · [Roharchiv mit capacity.json](../../messdaten-640/messarchiv.jsonl)

[Alle Ergebnisse dieses Testfalls](ergebnisse.md) · [Übersicht und Einrichtung](../../README.md)
