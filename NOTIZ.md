C-Lehrer 2.9 — jede Formel wird hergeleitet

**Neu:** Sieben Herleitungen für die Numerik, jeweils am Ende der
Lektion. Bei einem Simulationskurs ist das keine Kür: Wer die
Stabilitätsgrenze nur auswendig kennt, sucht bei einem anderen Verfahren
im Dunkeln.

* **Euler** — Schrittfehler O(dt²) aus der Taylorreihe, Gesamtfehler
  O(dt), weil N = T/dt Schritte ein dt wegkürzen. Dazu die Rechnung, die
  zeigt, dass die Energie beim Oszillator mit genau (1 + dt²) je Schritt
  wächst — kein Rundungsfehler, sondern das Verfahren selbst.
* **Verlet** — warum der Ort eine Ordnung besser ist, und warum die
  symmetrische Mittelung der Beschleunigung das dt-Glied aufhebt.
* **Der Drei-Punkt-Stern** — zwei Taylorentwicklungen addiert, ungerade
  Glieder heben sich, Fehler O(h²) aus drei Werten. Und `r = D·dt/h²` als
  die eine dimensionslose Zahl, an der alles hängt.
* **Die Stabilitätsgrenze** — von-Neumann-Analyse mit
  g = 1 − 4r·sin²(kh/2), daraus r ≤ ½, und daraus, warum die
  Instabilität immer als Sägezahn beginnt. Dazu die CFL-Bedingung
  0 ≤ c ≤ 1 auf beiden Wegen.
* **Trapezregel O(h²), Simpson O(h⁴)** — samt der Erklärung, warum die
  halben Randwerte von selbst anfallen.
* **Aufwind** — die modifizierte Gleichung mit D_num = (v·h/2)(1−c), und
  warum das Verfahren bei c = 1 exakt wird.
* **Druckprojektion** — Helmholtz-Hodge, die Poisson-Gleichung, und warum
  der Druck kein Zustand ist, sondern der Lagrange-Multiplikator der
  Divergenzfreiheit.

Alle Ordnungen sind nachgerechnet, nicht nur behauptet: Wärmeleitung
kippt zwischen r = 0,50 und 0,51, Euler halbiert den Fehler bei halbem
dt, Verlet viertelt ihn, Trapez /4, Simpson /16.

**Außerdem:** Die Oberfläche spricht Englisch (`qml/worte.js`, 119
Einträge), und der Sprachschalter erscheint, sobald ein Kurs mehr als
eine Sprache trägt.

**Pakete**

* `c-lehrer_2.9_armel.deb` — Nokia N9 / N950, `dpkg -i`
* `harbour-clehrer-1.1.0-1.aarch64.rpm` und `…armv7hl.rpm` —
  Sailfish OS, `pkcon install-local <datei>.rpm`
