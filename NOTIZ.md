C-Lehrer 3.1 — der Kurs auf Englisch, und jedes Codebeispiel erklärt

**Alle 411 Texte übersetzt.** Kapitel, Lektionen, Aufgaben, Begründungen,
Einstufung, Herleitungen und die neuen Codeerklärungen. Der
Sprachschalter erscheint, weil `sprachen` jetzt `["de", "en"]` ist.

Programmtext bleibt unverändert — ein C-Programm ist in beiden Sprachen
dasselbe, und ein englischer Bezeichner in einer deutschen Aufgabe wäre
nur verwirrend.

**Neu: jedes der 24 Codebeispiele Zeile für Zeile erklärt** — auch die
Zeilen, die man beim Lesen überspringt, weil sie selbstverständlich
aussehen:

* warum `xn` als Zwischenwert dasteht und was ohne ihn geschähe (es wäre
  ein anderes Verfahren),
* warum die Schleife bei 1 beginnt und bei n−2 endet,
* warum zwei Felder nötig sind und nicht eines genügt,
* warum `n / 2.0` den Punkt braucht,
* was `sizeof` in `malloc` soll und was passiert, wenn man es vergisst,
* warum `%e` statt `%f`, wenn die Werte Größenordnungen umspannen,
* was der Unterstrich in `for _schritt` bedeutet,
* warum bei der Instabilität nicht die Größe der Zahl zählt, sondern das
  Sägezahnmuster,
* warum `struct` in C einen Strichpunkt braucht und in Rust nicht.

Jede Erklärung sagt auch, worauf beim Laufenlassen zu achten ist.

**Neu: die Formeln stehen zweimal da** — einmal als die Zeile, die im
Beispielprogramm wirklich vorkommt, und darunter dieselbe Sache gesetzt:

    xn = x + v * dt;          x_{n+1} = x_n + v_n Δt

Gesetzt wird beim Bauen mit `tools/formeln.py` (matplotlib.mathtext, also
ein TeX-Setzer ohne TeX-Installation, Schrift Computer Modern). Das Gerät
bekommt nur ein PNG zu sehen; auf Sailfish wird es vom Thema eingefärbt,
damit es auch auf hellem Grund lesbar bleibt. Die Formeln selbst stehen in
`kursformeln.py`, nach Lektion geordnet — zehn in sechs Lektionen:
Euler, Velocity-Verlet, Diffusionsstern, Stabilitätsgrenze, Auf- und
Abwind, Auslöschung.

Warum als Bild und nicht als Text: QtQuick 1.1 und Silica können beide
Rich Text, aber keinen Bruchstrich, keine Wurzel und kein Summenzeichen
mit Grenzen. Ein Setzer auf dem Gerät (KaTeX in einer WebView) ginge — die
N950 hat QtWebKit —, kostet aber eine Browsermaschine je Formel und bringt
nichts ein, weil die Formeln beim Bauen schon feststehen.

**Pakete**

* `c-lehrer_3.2_armel.deb` — Nokia N9 / N950, `dpkg -i`
* `harbour-clehrer-1.4.0-1.aarch64.rpm` und `…armv7hl.rpm` — Sailfish
