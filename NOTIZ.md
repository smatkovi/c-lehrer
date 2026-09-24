C-Lehrer 3.8 — die Spielwiese sagt, was gedeutet und was übersetzt wird

Wer in der Spielwiese dieselbe Kleinigkeit in allen vier Sprachen laufen lässt,
merkt sofort: C und Rust sind augenblicklich da, Python braucht einen Moment,
C++ ein paar Sekunden. Das sah aus wie eine Aussage über die Sprachen — und
das wäre falsch.

Unter der Sprachwahl steht jetzt je ein Satz dazu:

* **C** läuft hier *gedeutet* (picoc) — kein Übersetzen, also sofort.
* **Rust** ebenso, mit `rrun`.
* **Python** wird gedeutet, aber CPython selbst muss erst hochkommen.
* **C++** wird wirklich *übersetzt*: g++ macht Maschinencode und bindet ihn.

Aufgeklappt steht darunter, was der Unterschied ist: Ein Deuter liest den Text
und tut Zeile für Zeile, was dort steht — nichts zu übersetzen, dafür ist er
beim Laufen die ganze Zeit dabei. Ein Übersetzer macht einmal Maschinencode,
den der Prozessor unmittelbar ausführt — die Arbeit fällt vorher an, das
Ergebnis läuft danach schnell. Bei kurzen Programmen sieht man deshalb fast
nur das Übersetzen.

Und bei C++ kommt dazu, dass eine einzige Zeile wie `#include <iostream>` rund
37 000 Zeilen Schablonen hereinholt, die der Übersetzer jedes Mal neu liest.
Das ist der größte Teil der Wartezeit, nicht das eigene Programm.

Der Schlusssatz steht ausdrücklich da: Das sagt nichts darüber, welche Sprache
schnell ist. C ist hier nur deshalb sofort da, weil die App einen kleinen
C-Deuter mitbringt — richtig übersetztes C läuft schneller als alles andere
hier, man wartet nur vorher.

Zweisprachig wie der Rest der Oberfläche.

## Paket

**N9 / N950:** `dpkg -i c-lehrer_3.8_armel.deb`
