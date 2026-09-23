# C-Lehrer

Programmieren lernen auf dem Nokia N9 und N950 (MeeGo 1.2 Harmattan) — mit
Blick auf das, wofür man es dort braucht: Simulation.

Kurze Lektionen, ein Beispiel, das wirklich läuft, dann Aufgaben, die vom
Lesen über das Ergänzen zum Selberschreiben führen. Was einmal saß, kommt in
wachsenden Abständen zur Wiederholung wieder. Am Anfang steht eine Einstufung
von etwa zwanzig Fragen, damit niemand bei `printf` anfangen muss, der schon
Zeiger kann.

Vier Sprachen, 15 Kapitel, 27 Lektionen:

* **C** — Werte und Typen, Schleifen, Funktionen, Felder und Zeiger,
  Strukturen und Speicher, und darauf aufbauend die Numerik: Euler gegen
  Verlet, Wärmeleitung, die CFL-Bedingung, Advektion, Druckprojektion.
* **C++** — Referenzen, `vector` und RAII, Templates.
* **Rust** — Werte und Typen ohne stillschweigende Umwandlung, Besitz und
  Ausleihen, und derselbe Löser wie in C.
* **Python** — NumPy: ganze Felder statt Schleifen.

## Was wirklich läuft

Die C- und Rust-Lektionen führen den eigenen Code auf dem Gerät aus:

* **crun** ist [picoc](https://gitlab.com/zsaleeba/picoc) (New BSD). Ein
  Deuter und kein Übersetzer: Eine Endlosschleife im ersten eigenen Programm
  kostet einen Kindprozess, nicht die App.
* **rrun** ist ein eigener Deuter für genau den Rust-Ausschnitt, den der Kurs
  lehrt — `let`/`let mut`, Funktionen, `if`, Schleifen, `Vec`, Strukturen,
  Besitz und Ausleihen. Er meldet die drei Fehler, um die es in Rust geht, mit
  den echten Nummern: E0382, E0499, E0502. Er prüft während des Laufs und
  nicht vorher; wer hier ein Programm zum Laufen bringt, hat es noch nicht an
  rustc vorbei, und genau das steht in der ersten Rust-Lektion.

C++ braucht das Zusatzpaket `c-lehrer-cpp` (g++ 4.4 aus dem Harmattan-SDK);
ohne es bleiben die C++-Kapitel lesbar. Python braucht das Python 3.11 unter
`/opt/wunderw` samt NumPy.

Gezeichnet wird durch Ausgeben: Jede Zeile, die mit `plot` beginnt, wird zu
einem Punkt einer Kurve. Deshalb sieht man dem expliziten Euler-Verfahren an,
wie die Energie davonläuft, und dem zu großen Zeitschritt, wie er explodiert.

## Derselbe Kurs woanders

Die Sailfish-Fassung liegt in
[harbour-lehrer](https://github.com/smatkovi/harbour-lehrer) — dieselbe
Maschine, Silica statt com.nokia.meego. Und weil das Programm nichts über sein
Fach weiß, tragen dieselben Binärdateien auch die Kurse *Segelschein* und
*Segelflug*: ein weiterer Kurs ist ein weiteres Paket, kein zweites Programm.

## Bauen

    tools/build-crun.sh      # den C-Deuter
    tools/build-rrun.sh      # den Rust-Deuter
    tools/build.sh           # die App
    tools/build-deb.sh 2.8   # das Paket

## Wie geprüft wird

    tools/test-curriculum.py

führt jedes Beispiel, jede Musterlösung und jede Aufgabenvorlage durch den
echten Deuter und vergleicht mit der hinterlegten Ausgabe — C und Rust unter
`qemu-arm` auf dem Baurechner, C++ und Python auf dem Gerät. Nichts geht
hinaus, was dort nicht durchgelaufen ist; zuletzt 89 von 89.
