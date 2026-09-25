C-Lehrer 4.0 — erst die Mathematik, dann die Physik, dann die Aufgabe

Eine Aufgabe ohne genannte Annahmen ist ein Rätsel. Wer nicht weiß, welche
Gleichung überhaupt gelöst wird, mit welchen Rand- und Anfangsbedingungen, mit
welcher Diskretisierung und unter welcher Stabilitätsbedingung, rät nicht
schlechter — er rät nur an einer anderen Stelle.

Über jeder der 73 Aufgaben stehen deshalb jetzt vier Blöcke, in genau dieser
Reihenfolge:

**Mathematisch** — das Modell mit seinen Formeln. Die Gleichung, das Gebiet,
Anfangs- und Randbedingungen, die Diskretisierung, die Bedingung, unter der
das Verfahren hält. Auch dort, wo es nicht nach Physik aussieht:
Ganzzahldivision ist `a/b = trunc(a/b)` mit Abschneiden zur Null,
Fließkomma ist `fl: R → F` mit `|fl(x) − x| ≤ eps·|x|`, `eps = 2⁻⁵³`.

**Physikalisch** — woher die Gleichung kommt und was weggelassen wurde: keine
Reibung, keine Luft, keine Quellen; welche Größe welche Einheit hat.

**Annahmen** — was in keines von beiden gehört: was die Maschine tut, was die
Aufgabe vorgibt, wie verglichen wird.

**Ziel** — was man am Ende gesehen haben soll.

Ein paar Beispiele für das, was jetzt dasteht statt nur einer Zahl:

* **Explizites Euler:** `x'' = −x` als System, Erhaltung `dE/dt = 0`, dann die
  Diskretisierung — und das Einsetzen, aus dem `E_(n+1) = (1 + dt²)·E_n` folgt.
  Über die ganze Rechnung `E(T) ≈ E₀·e^(T·dt)`; mit `dt = 0,05` ist das
  `0,5·1,0025⁴⁰⁰ = 1,3574`, mit `dt = 0,005` sind es `0,5·e^0,1 = 0,5526` —
  beides genau die Zahlen, die das Programm ausgibt.
* **Symplektisches Euler:** erhält nicht `E`, aber exakt
  `H = ½v² + ½x² − (dt/2)·x·v` — deshalb schwankt `E` in einem festen Band
  (0,4878 bis 0,5128) statt zu wachsen.
* **Stabilitätsgrenze:** von Neumann mit `u_i^n = gⁿ·e^(i·k·h)` liefert
  `g = 1 − 4r·sin²(k·h/2)`, und `|g| ≤ 1` verlangt `r ≤ ½`, also
  `dt ≤ h²/(2D)`.
* **Aufwind gegen zentral:** zentral hat `|g|² = 1 + C²·sin²(k·h) > 1` für
  jedes `C > 0` — unbedingt instabil, obwohl der Abbruchfehler `O(h²)` ist.
* **Druckschritt:** `div u = 0` als Zwangsbedingung, `p` als
  Lagrange-Multiplikator, `∇²p = (ρ/dt)·div u*`, und Helmholtz-Hodge als der
  Satz, der das Ganze trägt.
* **Wärmeerhaltung:** `d/dt ∫u dx = D·[∂u/∂x]` am Rand — daraus folgt, warum
  die isolierte Randzelle nur mit ihrem *einen* Nachbarn tauscht.

Alles zweisprachig, wie der übrige Kurs; leere Blöcke werden gar nicht erst
angezeigt. Die Kästen stehen **über** der Aufgabe und nicht in der
Rückmeldung: Sie verraten nichts, sie sagen nur, worüber gerechnet wird. Auch
auf den Karteikarten — eine Karte kommt Tage später wieder, und dann ist die
Lektion nicht mehr im Kopf.

**N9 / N950:** `dpkg -i c-lehrer_4.0_armel.deb`
**Sailfish:** `harbour-clehrer-1.14.0-1` (aarch64 und armv7hl)
