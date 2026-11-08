# 2C · Q&A-Kurzfassungen mit lokalem Qwen

Die Tests prüfen, wie der Moderationskompass Fragen für die Lehrperson zusammenfasst. Wer mit dem Hauptversuch beginnen möchte, findet unter **Kontext und Kurzfassung bei 640 Token** den Aufbau und jede einzelne Messung. Der Folgeversuch mit 1.024 Token verwendet pro Softwarestand dieselben vier Eingaben.

| Testfall                              | Was wird geprüft?                                                              | Anleitung                                             | Ergebnisse aller Läufe                                             |
| ------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------- | ------------------------------------------------------------------ |
| GPU-Kompatibilität                    | Funktionieren GPU-Berechnung und lokale Qwen-Inferenz unter WSL?               | [Aufbau](testfaelle/gpu-kompatibilitaet/anleitung.md) | [Ergebnisse](testfaelle/gpu-kompatibilitaet/ergebnisse.md)         |
| Kontext und Kurzfassung bei 640 Token | Was bewirken Registerdaten bei sechs oder 100 verfügbaren Fragen?              | [Aufbau](testfaelle/kontext-640/anleitung.md)         | [Oktober und November](testfaelle/kontext-640/ergebnisse.md)       |
| Ausgabelimit bei 1.024 Token          | Wann reicht mehr Platz für eine verwendbare Antwort?                           | [Aufbau](testfaelle/ausgabelimit-1024/anleitung.md)   | [Oktober und November](testfaelle/ausgabelimit-1024/ergebnisse.md) |
| Eingabekapazität                      | Wie viele Fragetexte passen rechnerisch und wie viele erreichen das Modell?    | [Aufbau](testfaelle/kapazitaet/anleitung.md)          | [Ergebnisse](testfaelle/kapazitaet/ergebnisse.md)                  |
| Längere Fragetexte                    | Welche Quellen kürzt der Packer und wie ändert sich die Laufzeit?              | [Aufbau](testfaelle/lange-fragetexte/anleitung.md)    | [Ergebnisse](testfaelle/lange-fragetexte/ergebnisse.md)            |
| Stimmen und Status                    | Was gewinnt die Kurzfassung durch zwei Zusatzfelder?                           | [Aufbau](testfaelle/stimmen-und-status/anleitung.md)  | [Ergebnisse](testfaelle/stimmen-und-status/ergebnisse.md)          |
| Prüfung der Quellenbelege             | Welche Fehler passieren den Binder bzw. den vollständigen Validierungspfad?    | [Aufbau](testfaelle/quellenpruefung/anleitung.md)     | [Oktober und November](testfaelle/quellenpruefung/ergebnisse.md)   |
| Alle zwölf Fragen direkt an Qwen      | Fehlt ein Anliegen bei der Auswahl oder geht es bei der Formulierung verloren? | [Aufbau](direktvergleich/README.md)                   | [Ergebnisse](direktvergleich/ergebnisse.md)                        |

## Softwarestände und Messgrenzen

Die **Oktober-Baseline** ist der Tag `v1.3.0` vom 8. Oktober. Die zugehörigen Hauptmessungen liefen am 4. November. Die **November-Baseline** ist der vereinbarte Stand vom 6. November vor dem Release vom 7. November. Die dazugehörigen Messungen liefen am 8. November. Die beiden Hauptversuche vergleichen dieselben synthetischen Datensätze auf derselben lokalen RX 9070 XT. [Oktober-Commit](https://github.com/kqc-real/arsnova.eu/commit/87c39334619fbcb0c5782b061da1ba0df0ba3142) · [November-Commit](https://github.com/kqc-real/arsnova.eu/commit/1d71bd9583954d5304e3d56ee2cc716196190a65)

In den Ergebnissen kennzeichnet **Modellantwort** den Text, den Qwen erzeugt hat. **Hostausgabe** ist das geprüfte Backend-Ergebnis für die Lehrperson. Es kann ein extraktiver Ersatz sein. Die Zeit der Hauptversuche umfasst Auswahl, Modellanfrage und Prüfung. Der direkte Vergleich mit zwölf Fragen misst nur die Modellanfrage. Warm-ups sind aufgeführt und aus den Medianen ausgeschlossen. Alle 2C-Inferenzläufe verwendeten Qwen3-4B-Instruct-2507 Q4_K_M mit Temperatur 0 und Seed 456. Vor jeder Anfrage wurde der KV-Slot geleert. Die Abgabe enthält 100 gewertete Modellaufrufe: 80 aus den beiden Hauptversuchen, zwölf aus den November-Erweiterungen und acht aus dem Direktvergleich. Die Archive enthalten zusätzlich zehn Warm-ups. GPU-Kompatibilität, Kapazitätsrechnungen und eingespeiste Kontrollantworten werden separat gezählt.

**Evidenz für 2C.** Im Projekt implementiert sind die [Kontextaufbereitung](../../../../apps/backend/src/lib/moderationSummaryContext.ts) und der [Qualitätsfilter](../../../../apps/backend/src/lib/qaSummaryQuality.ts). Lokal geprüft wurden die Ausgaben anhand der synthetischen Fragen. Die inhaltlichen Bewertungen sind vorläufig und KI-gestützt. Weitere Veranstaltungsformen, parallele Anfragen und Wartezeiten im Livebetrieb wurden nicht getestet. Die [Rubrik der Gruppe 2A](https://github.com/XarotDev/arsnova.eu/blob/3fc9f5ceffc769804e2a085d95f4608d3f1cd788/docs/didaktik/referate/2a-regelbasierte-extraktive-referenz/evidence/E4/rubrik.md) bewertet Fragenbezug, Stimmen, Trennung der Anliegen, Informationslücken und Themenabdeckung. Im produktiven System sind 14.671 angenommene Q&A-Fragen und 10.568 Bewertungen im erfassten 30-Tage-Zeitraum beobachtet. Für Qualität, Laufzeit oder Akzeptanz von Modellantworten in Produktion liegen hier keine Messungen vor. Eine zusätzliche inhaltliche Prüfung generierter Aussagen bleibt ein hypothetischer Verbesserungsvorschlag. [Nutzungsbericht](version_comparison/nutzungsbericht-2026-11-04.json) · [Quellenkontrollen](testfaelle/quellenpruefung/ergebnisse.md)

## Messungen wiederholen

Für alle folgenden Befehle zuerst im Stamm des Worktrees starten. Die Auswertung archivierter Ergebnisse braucht keine GPU. Die Messungen benötigen die [GPU-Testumgebung](testfaelle/gpu-kompatibilitaet/anleitung.md), Docker und für die einmalige Einrichtung der Anwendungsexporte einen Paketdownload. Die Modellanfragen laufen danach im Container ohne externes Netz.

```bash
repo=$(git rev-parse --show-toplevel)
cd "$repo/docs/didaktik/referate/2c-tokenbudget"
mkdir -p "$repo/tmp"
arbeit=$(mktemp -d "$repo/tmp/studie-2c.XXXXXX")
export TOPIC2C_SCRATCH="$arbeit/oktober"
export STUDY_WORK="$arbeit/november"
export GPU_DIR="$repo/tmp/wsl-gpu-validation"
```

Auf dem bereits eingerichteten WSL-Rechner liegen Modell und Server im Hauptworktree. In einem neuen Worktree kann der gemeinsame GPU-Ordner einmalig verknüpft werden. Der historische Oktober-Runner erwartet ihn genau an diesem Pfad.

```bash
# Nur beim Wiederverwenden der bestehenden Installation und bei fehlendem Ziel:
if [ -d /home/lena/Projects/arsnova.eu/tmp/wsl-gpu-validation ] && [ ! -e "$GPU_DIR" ]; then
  ln -s /home/lena/Projects/arsnova.eu/tmp/wsl-gpu-validation "$GPU_DIR"
fi
```

Nur die für den jeweiligen Test nötige Baseline einrichten. Die folgenden Kommandos verwenden dieselbe Shell und getrennte, frische Arbeitsverzeichnisse. Die eigentlichen Messbefehle stehen in der Anleitung des Testfalls.

```bash
# Oktober
OUT="$arbeit/oktober-vorbereitung" bash qa-tests-ausfuehren.sh setup
OUT="$arbeit/oktober-vorbereitung" bash qa-tests-ausfuehren.sh pack
# November
bash version_comparison/versuch.sh setup
```

## Archivierte Ergebnisse ohne Modellaufruf prüfen

Ab dem Studienverzeichnis ausführen. Der Vergleich liest die Rohdaten und schreibt die neu berechneten Tabellen in ein temporäres Verzeichnis.

```bash
sha256sum --quiet -c messdaten-640/SHA256SUMS
(cd ausgabelimit-1024 && sha256sum --quiet -c SHA256SUMS)
sha256sum --quiet -c version_comparison/SHA256SUMS
(cd direktvergleich && sha256sum --quiet -c SHA256SUMS)
ziel=$(mktemp -d)
python3 messlaeufe-auswerten.py --out "$ziel/640"
diff -u messdaten-640/einzelmessungen.csv "$ziel/640/einzelmessungen.csv"
python3 ausgabelimit-1024/ausgabelimits-vergleichen.py --pairs "$ziel/paare.csv"
diff -u ausgabelimit-1024/laufpaare-640-1024.csv "$ziel/paare.csv"
python3 version_comparison/auswerten.py --ausgabe "$ziel/november"
diff -ru version_comparison/tabellen "$ziel/november"
python3 direktvergleich/auswerten.py direktvergleich/rohdaten "$ziel/direkt" \
  --bewertung direktvergleich/inhaltsbewertung.json
diff -ru direktvergleich/tabellen "$ziel/direkt"
```
