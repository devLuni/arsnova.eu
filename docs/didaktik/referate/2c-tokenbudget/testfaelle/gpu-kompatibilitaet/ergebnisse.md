# Ergebnisse · GPU-Kompatibilität unter WSL

Am 21. Oktober 2026 wurden der HIP-Rechentest und zwei Modellanfragen im WSL-Container ausgeführt. Projektstand: `9e3acea8f1c8260e9212c2ba26a44d5fc1ce92e0`.

| Test           | Ergebnis                                                                                                                           | Serverstart | Modellanfrage | Token ein / aus |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------: | ------------: | --------------: |
| HIP-Rechentest | Alle 262.144 Werte stimmten mit der CPU-Referenz überein.                                                                          |           – |             – |               – |
| Modelllauf 01  | Gültiges JSON. Der geforderte Nachweis zur GPU-Ausführung fehlte im Log. Der Test meldete `failed`.                                |     7,038 s |       1,444 s |        173 / 85 |
| Modelllauf 02  | Mit ausführlicherer Protokollierung bestätigte der Server 37 von 37 Modellschichten auf der RX 9070 XT. Der Test meldete `passed`. |     4,771 s |       1,318 s |        173 / 85 |

In beiden Antworten waren die zwei Fragen zur Steigung zusammengefasst und die Matrixfrage getrennt. Die Zeiten betreffen diese kurze Testanfrage. Die späteren 2C-Versuche verwendeten andere Fragen und Prompts. [HIP-Ergebnis](belege/hip-ergebnis.txt) · [Modelllauf 01](belege/lauf-01.json) · [Modelllauf 02](belege/lauf-02.json) · [Anleitung](anleitung.md)
