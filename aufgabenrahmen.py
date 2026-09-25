# -*- coding: utf-8 -*-
"""Annahmen und Ziel jeder Aufgabe.

Der Schluessel ist Lektion und Nummer der Aufgabe. Nach dem Fragetext zu
ordnen ginge nicht: "Was schreibt dieses Programm?" steht siebenmal im
Kurs, jedesmal vor einem anderen Programm.

Jeder Eintrag hat vier Felder, und sie stehen in der Reihenfolge, in der
sie auch angezeigt werden:

``mathematisch``
    Das **Modell**, mit den Formeln dazu: die Gleichung, die geloest wird,
    das Gebiet, Anfangs- und Randbedingungen, die Diskretisierung, die
    Bedingung, unter der das Verfahren haelt.  Auch dort, wo es nicht nach
    Physik aussieht: Ganzzahldivision ist eine Abbildung `Z x Z -> Z` mit
    Abschneiden zur Null, Fliesskomma eine Abbildung `R -> F` mit
    `|fl(x) - x| <= eps*|x|`.  Ohne das steht in der Aufgabe eine Zahl,
    aber kein Grund.

``physikalisch``
    Woraus die Gleichung kommt und was weggelassen wurde: welche Kraefte
    wirken, welche nicht, welche Groessen welche Einheit haben.  Leer, wo
    keine Physik im Spiel ist.

``annahmen``
    Was in keines von beiden gehoert: was die Maschine tut, was die
    Aufgabe vorgibt, wie verglichen wird.

``ziel``
    Was man am Ende gesehen haben soll.  Leer lassen, was nichts
    beitraegt: Ein "Ziel: Sag voraus, was das Programm schreibt" unter der
    Frage "Was schreibt dieses Programm?" ist Laerm.

Die Formeln stehen in derselben Schreibweise wie im uebrigen Kurs --
`x_i^n`, `dt`, `h`, `^2` --, damit sie im Kasten ohne Formelsatz lesbar
bleiben; gesetzt wird nur, was in kursformeln.py steht.
"""
from __future__ import unicode_literals


def rahmen(mathematisch="", physikalisch="", annahmen="", ziel=""):
    """Ein Eintrag. Benannte Felder, weil vier Zeichenketten in einer Reihe
    nach dem dritten Komma niemand mehr auseinanderhaelt."""
    return {"mathematisch": mathematisch, "physikalisch": physikalisch,
            "annahmen": annahmen, "ziel": ziel}


RAHMEN = {
# --- C: Werte und Typen ---------------------------------------------------
("l-erstes", 0): rahmen(
    annahmen=
        "`printf` schreibt genau die Zeichen, die dastehen, und bricht die "
        "Zeile nur um, wo `\\n` im Text steht.",
),
("l-erstes", 1): rahmen(
    annahmen=
        "Die Zahl soll als Text erscheinen, gefolgt von einem Zeilenumbruch. "
        "Verglichen wird Zeichen fuer Zeichen, der Umbruch gehoert dazu.",
    ziel=
        "Die eine fehlende Zeile so ergaenzen, dass `42` und ein Umbruch "
        "herauskommen.",
),
("l-erstes", 2): rahmen(
    annahmen=
        "Ein Programm ohne Eingabe. Verglichen wird Zeichen fuer Zeichen, "
        "der Zeilenumbruch gehoert dazu.",
    ziel=
        "Den kleinsten vollstaendigen C-Rumpf schreiben, der eine Zeile "
        "ausgibt.",
),
("l-variablen", 0): rahmen(
    mathematisch=
        "Eine Zahl im Speicher ist ein Bitmuster; erst die Deutung macht "
        "einen Wert daraus. `double` deutet 64 Bit als `(-1)^s · m · 2^e` "
        "mit 53 Bit Mantisse, `int` deutet 32 Bit als Zweierkomplement-"
        "Ganzzahl. Es sind zwei verschiedene Abbildungen von Bitmuster auf "
        "Zahl -- keine ist eine Naeherung der anderen.",
    annahmen=
        "`printf` erfaehrt die Deutung **nur** aus dem Platzhalter. Ein "
        "falscher liest dieselben Bits nach der falschen Vorschrift; das "
        "ist kein Rundungsfehler, sondern eine andere Zahl.",
    ziel=
        "Den Platzhalter nennen, der zu einer Kommazahl doppelter "
        "Genauigkeit gehoert.",
),
("l-variablen", 1): rahmen(
    mathematisch=
        "Zwei Zahlmengen und zwei verschiedene Divisionen. `int` ist der "
        "Ausschnitt `-2^31 ... 2^31-1` der ganzen Zahlen, und `a/b` heisst "
        "dort `trunc(a/b)`, also Abschneiden zur Null hin. `double` ist die "
        "endliche Menge `F` der darstellbaren Kommazahlen, und `a/b` ist "
        "dort die gerundete reelle Division. **Welche der beiden gilt, "
        "entscheidet der Typ der Operanden** -- nicht der Typ, in den das "
        "Ergebnis gelegt wird.",
    ziel=
        "Vorhersagen, was herauskommt, wenn Ganzzahlen und Kommazahlen "
        "aufeinandertreffen.",
),
("l-variablen", 2): rahmen(
    mathematisch=
        "Die kinetische Energie ist die Abbildung `E(m, v) = ½·m·v²`. Zwei "
        "Eingaben, eine Ausgabe, keine Naeherung -- die ganze Aufgabe ist, "
        "sie in zwei Zeilen C zu uebersetzen.",
    physikalisch=
        "Punktmasse `m = 2,5 kg` mit `v = 4,0 m/s`, geradlinig; keine "
        "Rotation, kein Wechsel des Bezugssystems. `E` in Joule, "
        "`1 J = 1 kg·m²/s²`, also `½·2,5·4,0² = 20,00 J`.",
    ziel=
        "Zwei Groessen anlegen, die Formel hinschreiben und das Ergebnis "
        "mit zwei Nachkommastellen ausgeben.",
),
("l-intdiv", 0): rahmen(
    mathematisch=
        "Ganzzahldivision bildet zwei ganze Zahlen wieder auf eine ganze "
        "ab: `a/b = trunc(a/b)`, Abschneiden **zur Null hin** und nicht "
        "Abrunden -- `-7/2` ist `-3` und nicht `-4`. Der Nachkommaanteil "
        "existiert im Ergebnis gar nicht, er geht nicht verloren.",
    ziel=
        "Erkennen, dass abgeschnitten wird, bevor der Wert irgendwo "
        "ankommt.",
),
("l-intdiv", 1): rahmen(
    mathematisch=
        "Das Gebiet `[0, 1]` wird in `n = 10` gleich breite Zellen geteilt, "
        "die Zellweite ist `h = 1/n`. In den reellen Zahlen ist "
        "`1/10 = 0,1`, in den ganzen ist `1/10 = 0`. `1.0/n` rechnet in `F` "
        "-- dort ist `h ≈ 0,1` --, `1/n` rechnet in den ganzen Zahlen.",
    physikalisch=
        "`h` ist die Zellweite eines eindimensionalen Gitters, in Metern, "
        "wenn das Gebiet ein Meter lang ist. Ein `h = 0` macht jede spaetere "
        "Ableitung `(u[i+1]-u[i])/h` unbrauchbar -- deshalb ist diese Zeile "
        "die erste, die in jedem Loeser stimmen muss.",
    ziel="Die Zeile finden, die wirklich 0,1 ergibt -- und nicht 0.",
),
("l-intdiv", 2): rahmen(
    mathematisch=
        "Der Mittelwert `m = s/n` zweier ganzer Zahlen liegt im Allgemeinen "
        "**nicht** in den ganzen Zahlen. Damit die Division in `F` "
        "stattfindet, muss mindestens ein Operand dort liegen; die "
        "Umwandlung danach kommt zu spaet, weil abgeschnitten schon ist.",
    annahmen="Drei Nachkommastellen heisst `%.3f`.",
    ziel="Den Mittelwert so rechnen, dass der Nachkommaanteil ueberlebt.",
),

# --- C: Ablauf ------------------------------------------------------------
("l-if", 0): rahmen(
    mathematisch=
        "In C ist die Zuweisung ein **Ausdruck mit Wert**: `(x = 2)` hat "
        "den Wert 2. Die Bedingung prueft danach nur `Wert ≠ 0`. Also ist "
        "`if (x = 2)` immer wahr und `if (x = 0)` immer falsch, unabhaengig "
        "von `x`. `==` dagegen ist die Gleichheitsrelation und liefert 0 "
        "oder 1.",
    ziel="Vorhersagen, welcher Zweig genommen wird.",
),
("l-if", 1): rahmen(
    mathematisch=
        "Verglichen wird auf Gleichheit zweier ganzer Zahlen -- eine "
        "Relation ohne Toleranz, und hier ist das richtig. Bei gerechneten "
        "Kommazahlen waere dieselbe Zeile die falsche Frage (siehe das "
        "Kapitel ueber Fliesskomma).",
    ziel="Die Zeile nennen, die vergleicht statt zuzuweisen.",
),
("l-for", 0): rahmen(
    mathematisch=
        "`for (i = a; i < b; i++)` durchlaeuft die Menge `{a, a+1, ..., "
        "b-1}`, also das halboffene Intervall `[a, b)`: `b - a` Werte, der "
        "letzte ist `b-1`. Dieselbe Konvention gilt bei Feldindizes -- "
        "deshalb passt `for (i = 0; i < n; i++)` genau auf ein Feld mit `n` "
        "Elementen.",
    ziel=
        "Zaehlen, wie viele Zeilen herauskommen, und den letzten Wert "
        "nennen.",
),
("l-for", 1): rahmen(
    mathematisch=
        "Die Summe `S = 1 + 2 + 3 + 4 + 5 = 15` als Rekursion: `S_0 = 0`, "
        "`S_k = S_(k-1) + k`. Der Startwert 0 gehoert zur Rekursion; eine "
        "Variable ohne Zuweisung enthaelt in C **keinen** definierten Wert, "
        "also summiert man sonst zu etwas Beliebigem dazu.",
    ziel="Die Zeilen so ordnen, dass die Summe 1+2+3+4+5 herauskommt.",
),
("l-for", 2): rahmen(
    mathematisch=
        "Die harmonische Teilsumme `H_10 = Σ_(i=1..10) 1/i = 2,9289682...`, "
        "auf vier Stellen `2,9290`. Jeder Summand `1/i` muss in `F` "
        "gerechnet werden -- in den ganzen Zahlen waere `1/i = 0` fuer "
        "jedes `i ≥ 2` und die Summe 1. `H_n` waechst wie `ln n + γ` und "
        "ist unbeschraenkt: Die Reihe hat keinen Grenzwert, nur diese "
        "Teilsumme hat einen Wert.",
    ziel="Die Summe mit vier Nachkommastellen ausgeben (2,9290).",
),

# --- C: Bewegung ----------------------------------------------------------
("l-euler", 0): rahmen(
    mathematisch=
        "Anfangswertproblem `x'' = -(k/m)·x` mit `x(0) = 1`, `x'(0) = 0`, "
        "geschrieben als System erster Ordnung: `x' = v`, `v' = -(k/m)·x`. "
        "Die Loesung ist `x(t) = cos(ω·t)` mit `ω = √(k/m)`.\n\n"
        "Erhalten ist `E = ½mv² + ½kx²`, denn `dE/dt = m·v·v' + k·x·x' = "
        "-k·x·v + k·x·v = 0`.\n\n"
        "Diskretisiert wird explizit (beide Seiten aus dem **alten** "
        "Schritt): `x_(n+1) = x_n + v_n·dt`, `v_(n+1) = v_n - x_n·dt`. "
        "Einsetzen ergibt `E_(n+1) = (1 + dt²)·E_n` -- das Verfahren "
        "erhaelt die Energie nicht, es multipliziert sie in jedem Schritt "
        "mit einem Faktor groesser als 1.",
    physikalisch=
        "Punktmasse `m = 1 kg` an einer Feder mit `k = 1 N/m`, deshalb "
        "`a = -x`. Keine Reibung, keine Luft, keine Schwerkraft -- ein "
        "abgeschlossenes System, in dem die Energie sich nicht aendern "
        "**darf**. Start bei `x = 1 m`, `v = 0`, also `E = 0,5 J`.",
    annahmen="Zeitschritt `dt = 0,05 s`, 400 Schritte, also 20 s.",
    ziel=
        "Erkennen, dass eine wachsende Energie kein Rundungsfehler ist, "
        "sondern das Verfahren selbst.",
),
("l-euler", 1): rahmen(
    mathematisch=
        "Derselbe Wachstumsfaktor, jetzt ueber die ganze Rechnung: "
        "`E_N = (1 + dt²)^N · E_0` mit `N = T/dt`, also "
        "`E(T) ≈ E_0 · e^(T·dt)`. Der Fehler faellt **linear** mit `dt` und "
        "verschwindet nicht.\n\n"
        "`dt = 0,05`: `0,5 · 1,0025^400 = 1,3574`. `dt = 0,005`: "
        "`0,5 · e^0,1 = 0,5526`. Beides sind genau die Zahlen, die das "
        "Programm ausgibt -- die App laesst sich hier von Hand nachrechnen.",
    physikalisch="Dieselbe Feder, dieselbe Zeitspanne von 20 s.",
    annahmen="`dt = 0,005 s` und dafuer 4000 Schritte.",
    ziel=
        "Nachmessen, um welchen Faktor der Energiefehler faellt, wenn der "
        "Zeitschritt auf ein Zehntel geht -- und sehen, dass er faellt und "
        "nicht verschwindet.",
),
("l-euler", 2): rahmen(
    mathematisch=
        "Symplektisches (halbimplizites) Euler-Verfahren: erst "
        "`v_(n+1) = v_n - x_n·dt`, dann `x_(n+1) = x_n + v_(n+1)·dt` mit "
        "dem **neuen** `v`. Nur die Reihenfolge aendert sich.\n\n"
        "Es erhaelt `E` nicht exakt, aber es erhaelt exakt eine benachbarte "
        "Groesse: `H = ½v² + ½x² - (dt/2)·x·v` bleibt bei dieser Feder bis "
        "auf Rundung konstant. Weil `H` und `E` sich nur um `O(dt)` "
        "unterscheiden, schwankt `E` in einem **festen Band** (hier "
        "0,4878 bis 0,5128) und waechst nicht.",
    physikalisch="Dieselbe Feder, derselbe Zeitschritt wie im Beispiel.",
    ziel=
        "Zeigen, dass eine vertauschte Zeile aus einem Verfahren, das "
        "Energie erzeugt, eines macht, das sie haelt.",
),
("l-verlet", 0): rahmen(
    mathematisch=
        "Velocity-Verlet: `x_(n+1) = x_n + v_n·dt + ½·a_n·dt²`, dann "
        "`a_(n+1) = -x_(n+1)`, dann `v_(n+1) = v_n + ½·(a_n + a_(n+1))·dt`. "
        "Das Verfahren ist von zweiter Ordnung, symplektisch und "
        "zeitumkehrbar.\n\n"
        "Daraus folgt: `E` schwankt mit `O(dt²)` um den wahren Wert, ohne "
        "Drift. Bei `dt = 0,05` ist das Band `dt²/8 = 3,1·10^-4` breit -- "
        "die Energie bleibt zwischen 0,4997 und 0,5000.",
    physikalisch=
        "Dieselbe Feder `m = 1 kg`, `k = 1 N/m`, derselbe Start "
        "`x = 1 m`, `v = 0`, also `E = 0,5 J`.",
    annahmen="`dt = 0,05 s`, 400 Schritte.",
    ziel=
        "Vorhersagen, dass die Energie weder waechst noch faellt, sondern "
        "in einem schmalen Band bleibt.",
),
("l-verlet", 1): rahmen(
    mathematisch=
        "Ein Schritt in vier Teilen, und die Reihenfolge ist das Verfahren: "
        "`a_n` aus dem alten Ort, dann der Ort mit `v_n·dt + ½a_n·dt²`, "
        "dann `a_(n+1)` aus dem **neuen** Ort, dann die Geschwindigkeit mit "
        "dem Mittel `½(a_n + a_(n+1))`. Wer die Beschleunigung nur einmal "
        "auswertet, hat wieder ein Verfahren erster Ordnung.",
    ziel=
        "Den Schritt so zusammensetzen, dass jede halbe "
        "Geschwindigkeitsstufe die Beschleunigung ihres eigenen Zeitpunkts "
        "benutzt.",
),
("l-verlet", 2): rahmen(
    mathematisch=
        "Beide Verfahren auf derselben Gleichung `x'' = -x`, mit demselben "
        "`dt = 0,05` und denselben 400 Schritten -- der einzige Unterschied "
        "ist das Verfahren. Erwartet werden `1,3574` (Euler, "
        "`0,5·(1+dt²)^400`) und `0,4997` (Verlet, im Band `dt²/8`).",
    physikalisch="Dieselbe Feder, derselbe Start `x = 1 m`, `v = 0`.",
    ziel=
        "Die beiden Energiekurven nebeneinander sehen: die eine laeuft "
        "davon, die andere bleibt.",
),

# --- C: Funktionen und Fliesskomma ---------------------------------------
("l-funktionen", 0): rahmen(
    mathematisch=
        "Uebergabe als Wert: die Funktion bekommt eine **Kopie** und ist "
        "damit eine Abbildung `Wert -> Wert` ohne Nebenwirkung auf den "
        "Aufrufer. Was sie an ihrem Parameter aendert, endet mit ihr.",
    ziel="Vorhersagen, welchen Wert der Aufrufer nach dem Aufruf sieht.",
),
("l-funktionen", 1): rahmen(
    mathematisch=
        "Gesucht ist `I = ∫_0^π sin(x) dx = 2`.\n\n"
        "Trapezregel auf `n` gleich breiten Streifen der Breite "
        "`h = π/n`: `T_n = h·(f(x_0)/2 + Σ_(i=1..n-1) f(x_i) + f(x_n)/2)` "
        "mit `x_i = i·h`.\n\n"
        "Der Fehler ist `I - T_n = -(b-a)·h²/12 · f''(ξ)` fuer ein `ξ` im "
        "Intervall, also `O(h²) = O(1/n²)`: **verdoppeltes `n` viertelt "
        "den Fehler**. Bei `n = 1000` sind das rund `10^-6`.",
    ziel=
        "Die Funktion schreiben und sehen, wie nah sie bei 2 landet -- und "
        "um welchen Faktor der Fehler faellt, wenn `n` verdoppelt wird.",
),
("l-fliesskomma", 0): rahmen(
    mathematisch=
        "`double` ist die **endliche** Menge `F` der Zahlen `±m·2^e` mit "
        "53 Bit Mantisse. Die Rundung `fl` bildet jede reelle Zahl auf die "
        "naechste davon ab und erfuellt `|fl(x) - x| ≤ eps·|x|` mit "
        "`eps = 2^-53 ≈ 1,11·10^-16`.\n\n"
        "`0,1` und `0,2` sind im Zweiersystem periodisch, liegen also nicht "
        "in `F`. Gerechnet wird `fl(fl(0,1) + fl(0,2))`, und das ist nicht "
        "`fl(0,3)`.",
    annahmen=
        "Die Lektion wird gelesen und vorhergesagt, nicht ausgefuehrt: Der "
        "kleine C-Deuter dieser App kennt `float` und `double` nicht "
        "getrennt.",
    ziel=
        "Vorhersagen, was ein echter Uebersetzer schreibt -- und warum die "
        "zweite Zeile nicht die erwartete ist.",
),
("l-fliesskomma", 1): rahmen(
    mathematisch=
        "Jede Grundrechenart liefert `fl(a ∘ b)` und nicht `a ∘ b`. Zwei "
        "Rechenwege zum selben reellen Wert enden deshalb bei zwei "
        "verschiedenen Elementen von `F`. Die Gleichheit ist auf `F` "
        "sauber definiert -- sie beantwortet nur nicht die Frage, die "
        "gemeint war.",
    ziel=
        "Begruenden, warum auf Gleichheit zu pruefen hier die falsche Frage "
        "ist -- und welche die richtige waere.",
),
("l-fliesskomma", 2): rahmen(
    mathematisch=
        "Der Abstand zweier benachbarter Elemente von `F` bei `x` ist "
        "`ulp(x) = 2^(e-52)`, wenn `2^e ≤ |x| < 2^(e+1)`. Fuer "
        "`x = 10^16` ist `e = 53`, also `ulp = 2`. Damit ist "
        "`fl(10^16 + 1) = 10^16`: Die Addition ist dort nicht mehr "
        "injektiv -- der Summand verschwindet vollstaendig.",
    ziel=
        "Vorhersagen, was `1e16 + 1` ergibt, und erklaeren, warum das nicht "
        "Rundung heisst, sondern Unveraendertheit.",
),
("l-fliesskomma", 3): rahmen(
    mathematisch=
        "Gefragt ist nicht `a = b`, sondern `|a - b| ≤ tol`.\n\n"
        "Absolut mit festem `tol` taugt nur in einem Groessenbereich: `10^-9` "
        "ist fuer Millionen zu streng und fuer Millionstel zu grosszuegig. "
        "Relativ `|a - b| ≤ rtol·max(|a|, |b|)` waechst mit den Zahlen mit, "
        "versagt aber bei `a = b = 0`. Ueblich ist deshalb die Mischung "
        "`|a - b| ≤ atol + rtol·max(|a|, |b|)`.",
    ziel="Eine Pruefung schreiben, die mit der Groesse der Zahlen mitwaechst.",
),

# --- C: Felder und Zeiger -------------------------------------------------
("l-felder", 0): rahmen(
    mathematisch=
        "`double u[10];` legt die Plaetze `u[0] ... u[9]` an -- die Indizes "
        "durchlaufen `[0, n)`, nicht `[1, n]`. Zwei Zaehlweisen sind im "
        "Umlauf, „n Elemente“ und „Index bis n-1“; "
        "`for (i = 0; i < n; i++)` hat beide in einer Zeile richtig.",
    annahmen=
        "C prueft beim Zugriff **nichts**: `u[10]` wird uebersetzt und "
        "laeuft, es liest nur, was zufaellig dahinter liegt.",
    ziel="Den letzten Index nennen, der noch zum Feld gehoert.",
),
("l-felder", 1): rahmen(
    mathematisch=
        "Ein einzelner `double` wird beim Aufruf kopiert, ein Feld nicht: "
        "Der Feldname **zerfaellt zur Adresse** seines ersten Elements. "
        "Uebergeben wird also ein Zeiger; der ist zwar selbst eine Kopie, "
        "aber die Kopie einer Adresse zeigt auf dasselbe. Die Funktion "
        "arbeitet am Original.",
    ziel="Vorhersagen, ob die Aenderung in `aendern` beim Aufrufer ankommt.",
),
("l-felder", 2): rahmen(
    mathematisch=
        "Gesucht ist `max{v_0, ..., v_(n-1)}`. Als Rekursion: `M_0 = v_0`, "
        "`M_k = max(M_(k-1), v_k)`. Der Startwert **muss** `v_0` sein und "
        "nicht 0 -- mit 0 rechnet man das Maximum von "
        "`{0, v_0, ..., v_(n-1)}`, und fuer lauter negative Werte ist das "
        "eine Zahl, die im Feld gar nicht vorkommt. Fuer `n = 0` ist das "
        "Maximum nicht definiert; dieser Fall kommt hier nicht vor.",
    annahmen="Acht Werte, das Maximum ist 9,0.",
    ziel=
        "Das Maximum mit dem ersten Element als Startwert suchen und sehen, "
        "warum die naheliegende 0 falsch ist.",
),
("l-zeiger", 0): rahmen(
    mathematisch=
        "Ein Zeiger ist eine Adresse. `&a` liefert die Adresse von `a`, "
        "`*p` den Wert an der Adresse `p` -- die beiden Abbildungen sind "
        "zueinander invers: `*(&a)` ist `a`. Der Stern hat dabei zwei "
        "Rollen: in der Deklaration „Zeiger auf“, im Ausdruck "
        "„der Wert dort“.",
    ziel=
        "Vorhersagen, was ein Schreiben ueber den Zeiger an der Variablen "
        "aendert.",
),
("l-zeiger", 1): rahmen(
    mathematisch=
        "`u[i]` ist in C **definiert** als `*(u + i)`. Die Zeigerrechnung "
        "zaehlt in Elementen und nicht in Bytes: `u + i` ist die Adresse "
        "`u + i·sizeof(*u)`. Aus der Definition folgt nebenbei, dass auch "
        "`3[u]` gueltiges C ist -- gebraeuchlich ist das nicht, es zeigt "
        "nur, wie woertlich die Regel gemeint ist.",
    ziel="Die Schreibweise nennen, die dasselbe bedeutet wie `u[3]`.",
),
("l-zeiger", 2): rahmen(
    mathematisch=
        "Gesucht ist `v_i := f·v_i` fuer alle `i`, eine Skalierung an Ort "
        "und Stelle. Die Summe danach ist "
        "`f·Σ v_i = 2,5·(1+2+3+4) = 25`. `*(v + i)` und `v[i]` erzeugen "
        "denselben Maschinencode -- die Wahl ist eine des Lesens.",
    ziel=
        "Ein Feld an Ort und Stelle veraendern und sehen, dass die "
        "Aenderung beim Aufrufer ankommt, weil `w` die Adresse **ist**.",
),

# --- C: Waermeleitung -----------------------------------------------------
("l-stencil", 0): rahmen(
    mathematisch=
        "Waermeleitungsgleichung `∂u/∂t = D·∂²u/∂x²`.\n\n"
        "Zweite Ableitung als Drei-Punkt-Stern: "
        "`∂²u/∂x² ≈ (u_(i-1) - 2u_i + u_(i+1))/h²`, Fehler `O(h²)`. Zeit "
        "explizit: `u_i^(n+1) = u_i^n + r·(u_(i-1)^n - 2u_i^n + "
        "u_(i+1)^n)` mit `r = D·dt/h²`.\n\n"
        "Die hochgestellte `n` steht in **jedem** Term rechts: Alle drei "
        "Nachbarn sind vom alten Zeitschritt. Schreibt man direkt in `u`, "
        "ist `u_(i-1)` beim Erreichen von `i` bereits der neue Wert -- das "
        "ist dann das Gauss-Seidel-Verfahren, ein anderes Verfahren mit "
        "anderer Loesung, keine Ersparnis.",
    physikalisch=
        "Waerme in einem duennen Stab: `u` ist die Temperatur, `D` die "
        "Temperaturleitfaehigkeit in m²/s. Keine Quellen, keine Strahlung, "
        "kein Waermestrom laengs der Zeit -- nur Diffusion.",
    ziel=
        "Sehen, warum das zweite Feld kein Umweg ist, sondern zur "
        "Definition des Verfahrens gehoert.",
),
("l-stencil", 1): rahmen(
    mathematisch=
        "Die Erhaltung folgt aus der Gleichung: `d/dt ∫u dx = "
        "D·[∂u/∂x]` an den Raendern. Ohne Waermestrom ueber den Rand "
        "(`∂u/∂x = 0`, Neumann-Bedingung) bleibt `∫u dx` konstant.\n\n"
        "Diskret heisst das: Die Randzelle tauscht nur mit ihrem **einen** "
        "Nachbarn, `u_0^(n+1) = u_0^n + r·(u_1^n - u_0^n)`, ebenso am "
        "anderen Ende. Dann ist die Summe ueber alle Zellen ein Teleskop "
        "und bleibt exakt bei 1. Mit `u_0 = 0` (Dirichlet) statt dessen "
        "fliesst Waerme ab, und die Summe faellt.",
    physikalisch=
        "Stab mit **isolierten** Enden statt festgehaltener Temperatur. "
        "Anfangszustand: alles kalt, eine Einheit Waerme in der Mittelzelle. "
        "`n = 41` Zellen, `r = 0,4`, 200 Schritte; erwartet `0,031829` in "
        "der Mitte und `1,000000` als Summe.",
    ziel=
        "Die Randbedingung so aendern, dass die Erhaltung, die in der "
        "Gleichung steht, auch im Programm gilt.",
),
("l-cfl", 0): rahmen(
    mathematisch=
        "Stabilitaet des expliziten Sterns, nach von Neumann: Der Ansatz "
        "`u_i^n = g^n·e^(i·k·h)` liefert den Verstaerkungsfaktor "
        "`g = 1 - 4r·sin²(k·h/2)`. `|g| ≤ 1` fuer alle `k` verlangt "
        "`r ≤ ½`.\n\n"
        "Mit `r = D·dt/h²` heisst das `dt ≤ h²/(2D)`: **Halbiert man `h`, "
        "muss `dt` geviertelt werden.** Die Arbeit waechst dann um das "
        "Achtfache -- doppelt so viele Zellen, viermal so viele Schritte.",
    physikalisch=
        "`D` ist durch das Material gegeben und aendert sich nicht, wenn "
        "man das Gitter verfeinert. Frei ist nur `dt`.",
    ziel="Den Preis eines feineren Gitters ablesen.",
),
("l-cfl", 1): rahmen(
    mathematisch=
        "Bei `r = ½` ist `g = 1 - 2·sin²(k·h/2)`, also genau "
        "`|g| ≤ 1` -- gerade noch stabil, und die kuerzeste Welle "
        "(`k·h = π`) wird mit `g = -1` von Schritt zu Schritt gespiegelt "
        "statt gedaempft. Ueber der Grenze ist `|g| > 1`: Das Verfahren "
        "wird nicht ungenau, es schwingt sich mit wachsender Amplitude auf.",
    physikalisch=
        "`n = 41` Zellen, festgehaltene Raender (Temperatur 0), eine "
        "Einheit Waerme in der Mitte, 60 Schritte. Groesster Wert im Feld "
        "danach: `0,102578`.",
    ziel=
        "Die Grenze von beiden Seiten sehen: bei 0,5 haelt es, ein wenig "
        "darueber nicht mehr.",
),

# --- C: Strukturen und Speicher ------------------------------------------
("l-struct", 0): rahmen(
    mathematisch=
        "`p->x` ist die Kurzform fuer `(*p).x`. Die Klammern sind noetig, "
        "weil der Punkt staerker bindet als der Stern: `*p.x` hiesse "
        "„dereferenziere `p.x`“ und ist etwas anderes.",
    annahmen=
        "Der Pfeil ist nicht nur kuerzer, er macht verkettete Zugriffe "
        "ueberhaupt lesbar: `zelle->nachbar->druck` gegen "
        "`(*(*zelle).nachbar).druck`.",
    ziel=
        "Die Kurzform nennen, mit der man ueber einen Zeiger an ein Feld "
        "der Struktur kommt.",
),
("l-struct", 1): rahmen(
    mathematisch=
        "Der Schwerpunkt ist `x_s = (Σ m_i·x_i)/(Σ m_i)`. Sind alle Massen "
        "gleich, kuerzt sich `m` heraus und es bleibt der gewoehnliche "
        "Mittelwert `x_s = (Σ x_i)/n`.\n\n"
        "Hier sind die Orte `x_i = i²` fuer `i = 0..4`, also 0, 1, 4, 9, "
        "16; Summe 30, geteilt durch 5 ergibt 6,0000.",
    physikalisch=
        "Fuenf Teilchen auf einer Geraden, alle mit **derselben** Masse; "
        "deshalb faellt die Wichtung weg. Mit verschiedenen Massen waere "
        "der Mittelwert der Orte nicht der Schwerpunkt.",
    annahmen=
        "Der Parameter ist ein Zeiger auf die erste Struktur -- das Feld "
        "wird nicht kopiert, und `t[i].x` funktioniert trotzdem wie "
        "gewohnt.",
    ziel=
        "Den Schwerpunkt als Summe durch Anzahl rechnen und die uebliche "
        "C-Signatur lesen lernen: Zeiger auf das erste Element plus Anzahl.",
),
("l-speicher", 0): rahmen(
    mathematisch=
        "Ein zweidimensionales Gitter wird flach abgelegt, Zeile hinter "
        "Zeile: Die Zelle `(i, j)` liegt bei `j·nx + i`. Das ist eine "
        "Bijektion `[0, nx) × [0, ny) -> [0, nx·ny)` -- zeilenweise "
        "Anordnung, in C die uebliche.\n\n"
        "Merkhilfe: Der Index, der in der **inneren** Schleife laeuft, "
        "steht in der Formel ohne Faktor. `for (j...) for (i...)` mit "
        "`u[j*nx + i]` laeuft im Speicher hintereinander weg.",
    ziel=
        "Die Indexformel nennen, bei der die innere Schleife im Speicher "
        "hintereinander weglaeuft.",
),
("l-speicher", 1): rahmen(
    mathematisch=
        "Gitter `nx = 12` mal `ny = 10`, jede Zelle traegt `i·j`. Rand "
        "heisst `i = 0`, `i = nx-1`, `j = 0` oder `j = ny-1`.\n\n"
        "Die Zellen mit `i = 0` und die mit `j = 0` tragen null. Es "
        "bleiben die Kante `i = 11` mit `11·Σ_(j=0..9) j = 11·45 = 495` "
        "und die Kante `j = 9` mit `9·Σ_(i=0..11) i = 9·66 = 594`. Die Ecke "
        "`(11, 9) = 99` liegt in beiden Summen, also "
        "`495 + 594 - 99 = 990` -- wer die vier Kanten getrennt abgeht, "
        "zaehlt die Ecken doppelt.",
    physikalisch=
        "In einem Loeser steht am Rand die Randbedingung, deshalb wird er "
        "getrennt behandelt. Ueblich ist eine **Geisterzellenschicht**: "
        "eine zusaetzliche Zelle ringsherum, vor jedem Schritt gefuellt -- "
        "danach ist das Innere ohne Sonderfall zu rechnen.",
    ziel=
        "Ein flaches Gitter anlegen, es fuellen und den Rand genau einmal "
        "aufsummieren.",
),

# --- C++: Referenzen, RAII, Templates ------------------------------------
("cpp-ref", 0): rahmen(
    mathematisch=
        "Eine Referenz ist ein zweiter Name fuer dasselbe Objekt: keine "
        "Kopie und keine eigene Adresse, die man sehen koennte. Die "
        "Funktion arbeitet damit am Original des Aufrufers -- an der "
        "Aufrufstelle steht trotzdem nur `schritt(f)`.",
    ziel="Sagen, was mit dem Original des Aufrufers geschieht.",
),
("cpp-ref", 1): rahmen(
    mathematisch=
        "Ein Gitterfeld mit `N = 10^6` Zellen zu je 8 Byte sind 8 MB. Ohne "
        "`&` entsteht je Aufruf eine vollstaendige Kopie, also Aufwand "
        "`O(N)` **zusaetzlich** zu dem, was die Funktion rechnet. In einer "
        "Zeitschleife mit `M` Schritten macht das `O(M·N)` sinnlos "
        "kopierte Zahlen.",
    annahmen=
        "Die Faustregel in numerischem C++: alles, was groesser ist als ein "
        "paar Zahlen, per `const&`; kleine Werte wie `double` oder `int` "
        "als Kopie, die ist billiger als der Umweg ueber eine Adresse.",
    ziel=
        "Erkennen, dass das fehlende `&` kein Stilfehler ist, sondern der "
        "Unterschied zwischen Sekunden und Stunden.",
),
("cpp-ref", 2): rahmen(
    mathematisch=
        "Zwei Funktionen mit demselben Rumpf `x = x*2`, einmal auf einer "
        "Referenz (`int&`) und einmal auf einer Kopie (`int`). Der "
        "Unterschied ist genau der zwischen `f: Wert -> Wert` und einer "
        "Abbildung, die den Zustand des Aufrufers aendert.",
    annahmen="Beide Variablen starten bei 5.",
    ziel=
        "An zwei Zahlen ablesen, was die Referenz gegenueber der Kopie "
        "aendert.",
),
("cpp-raii", 0): rahmen(
    mathematisch=
        "Die Frage ist nach dem **Zeitpunkt**, nicht nach einem Aufruf: Der "
        "Destruktor laeuft, wenn der Block endet -- auch bei vorzeitigem "
        "`return` und wenn eine Ausnahme den Block verlaesst. In C steht am "
        "Ende jeder Funktion ein `free`, und jeder vorzeitige Ausgang "
        "braucht sein eigenes; fehlt eines, waechst der Verbrauch mit der "
        "Laufzeit.",
    ziel=
        "Den Zeitpunkt der Freigabe nennen und ihn mit dem `free` von Hand "
        "in C vergleichen.",
),
("cpp-raii", 1): rahmen(
    mathematisch=
        "Derselbe explizite Schritt wie in C: `w_i = u_i + r·(u_(i-1) - "
        "2u_i + u_(i+1))` fuer die inneren Zellen, die Raender bleiben "
        "stehen. `w` entsteht als **Kopie** von `u`, damit die Randwerte "
        "darin stehen und nicht Nullen.\n\n"
        "`u.swap(w)` tauscht nur die drei Zahlen, aus denen ein `vector` "
        "besteht (Zeiger, Laenge, Platz) -- Aufwand `O(1)`, unabhaengig von "
        "der Gittergroesse. In C ist das `double *t = u; u = w; w = t;`.",
    ziel=
        "Die Zeilen in die Reihenfolge bringen, die jeder Loeser hat: "
        "zweites Feld anlegen, innen rechnen, tauschen.",
),
("cpp-tmpl", 0): rahmen(
    mathematisch=
        "Eine Vorlage mit **einem** Typparameter `T` beschreibt eine Schar "
        "von Funktionen; der Uebersetzer erzeugt je benutztem Typ eine "
        "eigene. `groesser(3, 7)` bestimmt `T = int`, `groesser(2.5, 1.5)` "
        "bestimmt `T = double`. `groesser(3, 2.5)` haette zwei "
        "verschiedene Kandidaten fuer dasselbe `T` und ist ein Fehler; zu "
        "retten waere es mit zwei Typparametern oder mit "
        "`groesser<double>(3, 2.5)`.",
    ziel=
        "Vorhersagen, was zwei getrennte Aufrufe schreiben, und erkennen, "
        "warum ein gemischter nicht uebersetzt.",
),
("cpp-tmpl", 1): rahmen(
    mathematisch=
        "Verglichen wird mit einer von Hand je Typ geschriebenen Fassung, "
        "nicht mit Vererbung. Gefragt sind die Kosten zur **Laufzeit**, "
        "nicht beim Uebersetzen: Der Uebersetzer erzeugt denselben Code, "
        "also null.\n\n"
        "Bei Vererbung kostet jeder Aufruf einen Sprung ueber eine Tabelle "
        "-- und schlimmer als der Sprung ist, dass er das Einsetzen an Ort "
        "und Stelle verhindert und damit das Vektorisieren der inneren "
        "Schleife.",
    ziel=
        "Sehen, warum numerischer C++-Code Templates nimmt und nicht "
        "virtuelle Aufrufe.",
),
("cpp-tmpl", 2): rahmen(
    mathematisch=
        "Dasselbe Maximum wie in C, nur fuer jeden vergleichbaren Typ: "
        "`M_0 = v_0`, `M_k = max(M_(k-1), v_k)`, Start bei `v[0]`.\n\n"
        "`v.size()` liefert `std::size_t`, eine **vorzeichenlose** Zahl; "
        "der Zaehler braucht denselben Typ. Das hat eine eigene Falle: "
        "`for (std::size_t i = v.size()-1; i >= 0; --i)` endet nie, weil "
        "`i` nach null auf die groesste Zahl springt.",
    annahmen=
        "`const std::vector<T>&` uebergibt ohne Kopie und mit der Zusage, "
        "nichts zu aendern.",
    ziel=
        "Eine Vorlage zusammensetzen, die fuer jeden vergleichbaren Typ "
        "gilt -- und dabei den richtigen Indextyp nehmen.",
),

# --- Python: NumPy -------------------------------------------------------
("py-felder", 0): rahmen(
    mathematisch=
        "`np.arange(5.0)` ist `[0, 1, 2, 3, 4]`. Ein Schnitt "
        "`a[anfang:ende]` nimmt die Indizes `[anfang, ende)` -- halboffen "
        "wie die C-Schleife --, negative Zahlen zaehlen vom Ende her. "
        "`a[1:-1]` ist also `[1, n-1)`: genau die inneren Zellen, die der "
        "Stern rechnet.",
    annahmen=
        "Die Ausgabe zeigt `[1. 2. 3.]` mit Punkten, weil `arange(5.0)` "
        "Kommazahlen erzeugt; `arange(5)` ergaebe `[1 2 3]`.",
    ziel=
        "Den Schnitt lesen, der genau die inneren Zellen trifft -- die "
        "Raender fallen weg.",
),
("py-felder", 1): rahmen(
    mathematisch=
        "Derselbe explizite Stern wie in C, nur als **ein** Feldausdruck: "
        "`u[1:-1] += r·(u[:-2] - 2·u[1:-1] + u[2:])`. Die drei Schnitte "
        "sind `u_(i-1)`, `u_i`, `u_(i+1)` fuer alle inneren `i` "
        "gleichzeitig.\n\n"
        "`r = D·dt/h² = 0,4` liegt unter der Stabilitaetsgrenze `½`. Die "
        "Raender bleiben auf null (Dirichlet), deshalb faellt die Summe "
        "von 1 auf `0,989678` in 400 Schritten -- Waerme fliesst ab. Mit "
        "`u[0] = u[1]` und `u[-1] = u[-2]` nach jedem Schritt (Neumann) "
        "bliebe sie stehen.",
    physikalisch=
        "Stab mit `n = 101` Zellen, anfangs kalt, eine Einheit Waerme in "
        "der Mittelzelle; die Enden auf fester Temperatur 0.",
    ziel=
        "Die Schleife ueber die Zellen durch einen Feldausdruck ersetzen, "
        "der dieselben inneren Zellen trifft wie der C-Code.",
),
("py-felder", 2): rahmen(
    mathematisch=
        "Verglichen werden **dieselben** Rechnungen ueber dieselben Zellen "
        "-- die Zahl der Gleitkommaoperationen ist gleich. Verschieden ist, "
        "was drumherum passiert: In Python kostet jeder Durchlauf "
        "Objektverwaltung, beim Feldausdruck laeuft die Schleife einmal in "
        "uebersetztem C.\n\n"
        "Dazu der Speicherzugriff: Ein NumPy-Feld liegt zusammenhaengend, "
        "der Prozessor holt ganze Zeilen in den Zwischenspeicher; eine "
        "Python-Liste enthaelt Verweise auf Objekte, die irgendwo liegen. "
        "Deshalb bringt NumPy bei kleinen Feldern wenig und bei grossen "
        "sehr viel.",
    ziel=
        "Den Grund benennen -- und zwar den richtigen, nicht „NumPy ist "
        "eben schneller“.",
),

# --- Stroemung: Advektion -------------------------------------------------
("l-upwind", 0): rahmen(
    mathematisch=
        "Advektionsgleichung `∂a/∂t + v·∂a/∂x = 0` mit `v > 0`. Die "
        "Loesung ist `a(x, t) = a_0(x - v·t)`: Das Profil wird nur "
        "verschoben, nie gedaempft.\n\n"
        "Zentrale Ableitung, `(a_(i+1) - a_(i-1))/(2h)`: von Neumann "
        "liefert `g = 1 - i·C·sin(k·h)`, also `|g|² = 1 + C²·sin²(k·h) > 1` "
        "fuer jedes `C > 0` -- **unbedingt instabil**, obwohl der "
        "Abbruchfehler `O(h²)` ist.\n\n"
        "Aufwind, `(a_i - a_(i-1))/h`: `|g| ≤ 1` fuer `0 ≤ C ≤ 1`. Nur "
        "erste Ordnung, aber stabil -- und es nimmt die Information von "
        "dort, wo sie physikalisch herkommt.",
    physikalisch=
        "Reiner Transport mit fester Geschwindigkeit `v`: keine Diffusion, "
        "die etwas daempfen koennte, keine Quelle. Was stromabwaerts "
        "liegt, kann den Wert hier nicht beeinflussen -- genau das nimmt "
        "die zentrale Ableitung trotzdem an.",
    ziel=
        "Sehen, dass Fehlerordnung und Stabilitaet zwei verschiedene Fragen "
        "sind: Das genauere Verfahren ist hier das unbrauchbare.",
),
("l-upwind", 1): rahmen(
    mathematisch=
        "Courant-Zahl `C = v·dt/h`. Das Aufwindverfahren ist stabil fuer "
        "`C ≤ 1`; anschaulich heisst das, die Stroemung darf in einem "
        "Schritt hoechstens eine Zelle weit tragen -- sonst holt sich der "
        "Stern seine Information aus einer Zelle, aus der sie noch nicht "
        "gekommen ist.\n\n"
        "Bei `C = 1,5` ist `|g| > 1`, und der Fehler waechst geometrisch: "
        "nach 40 Schritten steht `7,789·10^10` im Feld. Das ist keine "
        "Ungenauigkeit mehr, sondern eine gesprengte Rechnung.",
    physikalisch=
        "41 Zellen, ein rechteckiger Block der Hoehe 1 auf dem Viertel bis "
        "zur Haelfte des Gebiets, Raender auf null. Physikalisch duerfte "
        "sich der Block nur verschieben.",
    ziel=
        "Sehen, was eine verletzte CFL-Bedingung anrichtet -- und dass es "
        "keine Frage der Genauigkeit ist.",
),

# --- Stroemung: Druckschritt ---------------------------------------------
("l-projektion", 0): rahmen(
    mathematisch=
        "Inkompressible Stroemung: Die Dichte ist konstant, damit schrumpft "
        "die Kontinuitaetsgleichung `∂ρ/∂t + div(ρu) = 0` auf die "
        "**Zwangsbedingung** `div u = 0`.\n\n"
        "Der Druck ist der Lagrange-Multiplikator dazu. Im Zeitschritt "
        "(Chorin): erst ein Zwischenfeld `u*` ohne Druck, dann "
        "`∇²p = (ρ/dt)·div u*`, dann `u^(n+1) = u* - (dt/ρ)·∇p`. Nach dem "
        "Satz von Helmholtz und Hodge zerfaellt jedes Feld eindeutig in "
        "einen divergenzfreien Teil und einen Gradienten -- der Druckschritt "
        "zieht genau den Gradienten ab.",
    physikalisch=
        "`p` ist hier **keine** thermodynamische Groesse: Es gibt keine "
        "Zustandsgleichung, die ihn mit Dichte und Temperatur verbindet. Er "
        "ist die Kraft, die noetig ist, damit nichts komprimiert wird. Bei "
        "kompressibler Stroemung ist es umgekehrt -- dort wird `p` "
        "mitgefuehrt, und der Zeitschritt muss die Schallgeschwindigkeit "
        "aufloesen.",
    ziel=
        "Sehen, wozu die Poisson-Gleichung im Zeitschritt ueberhaupt da "
        "ist.",
),
("l-projektion", 1): rahmen(
    mathematisch=
        "Der Druckschritt loest `∇²p = div u*` auf dem ganzen Gitter, "
        "einmal je Zeitschritt. Der diskrete Laplace-Operator hat die "
        "Kondition `O(1/h²)`, und Jacobi braucht entsprechend viele "
        "Durchlaeufe: Bei `N` Zellen je Richtung sind es `O(N²)`, also "
        "`O(N^4)` Arbeit je Zeitschritt. Bei einer Million Zellen ist das "
        "aussichtslos -- daher Mehrgitter (`O(N²)` Arbeit, also linear in "
        "der Zellzahl), konjugierte Gradienten oder FFT.",
    annahmen=
        "Jacobi **konvergiert** -- die Frage ist nicht Stabilitaet, sondern "
        "Geschwindigkeit. Zum Lernen ist er trotzdem die richtige Wahl: "
        "fuenf Zeilen, keine Matrix, Zelle fuer Zelle nachrechenbar.",
    ziel=
        "Erkennen, dass hier die Kosten entscheiden, und wissen, was "
        "stattdessen genommen wird.",
),

# --- Rust: Werte und Zahlen ----------------------------------------------
("rs-erstes", 0): rahmen(
    annahmen=
        "`print!` schreibt ohne Zeilenumbruch, `println!` mit -- der "
        "Unterschied steht im Namen und nicht in der Zeichenkette. Die "
        "Ausgabe wird zeilenweise wirklich hinausgeschrieben; wer den "
        "Fortschritt einer langen Rechnung ohne Umbruch ausgibt, sieht "
        "minutenlang nichts.",
),
("rs-erstes", 1): rahmen(
    mathematisch=
        "Gefragt ist die **Genauigkeit**, nicht die Breite: `{:.3}` sind "
        "drei Nachkommastellen, `{:3}` waeren drei Zeichen Feldbreite. "
        "Die C-Form `%.3f` geht nicht, weil `println!` seine Vorlage beim "
        "Uebersetzen liest und dabei jeden Platzhalter mit seinem Wert "
        "zusammenbringt.",
    ziel="Den Platzhalter fuer drei Nachkommastellen nennen.",
),
("rs-erstes", 2): rahmen(
    annahmen=
        "Verglichen wird Zeichen fuer Zeichen, der Zeilenumbruch gehoert "
        "dazu. Kein `#include` noetig und kein `return 0;`.",
    ziel="Den kleinsten Rust-Rumpf schreiben, der eine Zeile ausgibt.",
),
("rs-zahlen", 0): rahmen(
    mathematisch=
        "Dieselben zwei Divisionen wie in C: `7/2 = 3` in den ganzen "
        "Zahlen, `3,5` in `F`. Der Unterschied ist, dass Rust **nicht "
        "befoerdert**: Es gibt keine stillschweigende Umwandlung des "
        "kleineren Typs, jede Umwandlung muss dastehen (`as f64`). "
        "`a as f64 / b` waere schon ein Fehler -- links `F`, rechts ganze "
        "Zahl.",
    ziel=
        "Beide Zeilen vorhersagen und den Unterschied benennen: dieselbe "
        "Falle wie in C, nur in einer Sprache, die das Schweigen nicht "
        "zulaesst.",
),
("rs-zahlen", 1): rahmen(
    mathematisch=
        "Gebiet der Laenge 1 in `n = 10` Zellen, `h = 1/n = 0,1`. Zwei der "
        "falschen Zeilen sind Uebersetzungsfehler, weil `f64` und ganze Zahl "
        "sich nicht mischen. Eine uebersetzt und liefert trotzdem null: "
        "`(1 / n) as f64` rechnet erst in den ganzen Zahlen und wandelt "
        "dann die 0 um.\n\n"
        "Merksatz wie in C: **Der Typ des Ergebnisses entsteht im Ausdruck, "
        "nicht bei der Zuweisung.**",
    ziel=
        "Die Zeile finden, die wirklich 0,1 ergibt, und die Falle in "
        "Rust-Kleidung erkennen.",
),
("rs-zahlen", 2): rahmen(
    mathematisch=
        "`summe/anzahl = 7/2`; das Ergebnis liegt nicht in den ganzen "
        "Zahlen, also muessen **beide** Seiten nach `f64`. Wer es ohne `as` "
        "haben will, schreibt die Werte gleich als Kommazahlen -- in einem "
        "Loeser ist das die uebliche Antwort: Zellzahlen bleiben `usize`, "
        "alles Gerechnete ist von Anfang an `f64`.",
    annahmen=
        "Die Vorlage gibt die Zahlen einzeln aus, damit sie ueberhaupt "
        "uebersetzt; gefragt ist eine einzige Zeile mit der Rechnung.",
    ziel="Beide Seiten umwandeln und mit drei Nachkommastellen ausgeben.",
),

# --- Rust: Besitz und Ausleihen ------------------------------------------
("rs-besitz-lektion", 0): rahmen(
    mathematisch=
        "Ein `Vec` ist nicht `Copy`: Die Zuweisung **verschiebt** ihn, "
        "danach gilt der alte Name nicht mehr. Dahinter steht die Freigabe "
        "-- gaebe es zwei gueltige Namen fuer denselben Speicherblock, "
        "muesste zur Laufzeit jemand mitzaehlen, wer als Letzter geht. "
        "Genau diese Zaehlung spart Rust, und dafuer braucht es eine Regel, "
        "die beim Uebersetzen greift.",
    ziel=
        "Den Grund fuer den Uebersetzungsfehler nennen und ihn von den "
        "naheliegenden falschen Erklaerungen trennen.",
),
("rs-besitz-lektion", 1): rahmen(
    mathematisch=
        "Die Grenze verlaeuft dort, wo eine Kopie teuer oder gefaehrlich "
        "wuerde: Zahlen sind `Copy`, sie liegen vollstaendig im Register. "
        "Ein `Vec` haette danach zwei Besitzer desselben Speicherblocks -- "
        "also wird er verschoben. Eigene Strukturen sind deshalb "
        "standardmaessig nicht `Copy`; man kann es anfordern, wenn alle "
        "Felder es sind.",
    annahmen="`a` ist hier eine ganze Zahl, kein `Vec`.",
    ziel="Sehen, wo die Grenze zwischen Kopieren und Verschieben verlaeuft.",
),
("rs-besitz-lektion", 2): rahmen(
    mathematisch=
        "Gebraucht werden wirklich **zwei** Gitter zu je sieben Zellen, "
        "also `clone()`: ein zweiter Wert, Aufwand `O(n)`. `&u` waere "
        "`O(1)` und gaebe nur einen zweiten Blick auf dasselbe. Die Frage "
        "an jeder solchen Stelle lautet: zweiter Wert oder zweiter Blick?",
    ziel=
        "Die Entscheidung bewusst treffen statt sie vom Uebersetzer "
        "erzwingen zu lassen.",
),
("rs-ausleihen", 0): rahmen(
    mathematisch=
        "Die Regel: beliebig viele `&` gleichzeitig, oder **ein** `&mut` "
        "und sonst nichts. Formal ist das die Bedingung, unter der kein "
        "Schreibzugriff mit einem anderen Zugriff ueberlappt.\n\n"
        "Dieselbe Bedingung macht ein Programm auf mehreren Kernen richtig "
        "-- deshalb deckt die Pruefung, die hier einen Fehler im "
        "Einprozessorprogramm verhindert, auch Datenrennen mit ab.",
    ziel="Die erlaubte Kombination nennen und wissen, warum sie es ist.",
),
("rs-ausleihen", 1): rahmen(
    mathematisch=
        "`&mut f64` ist ein Verweis, den man beschreiben darf; `*x = *x * "
        "2.0` schreibt in die Variable des Aufrufers -- derselbe Stern wie "
        "in C. Beim Lesen in Rechnungen darf er meist entfallen, beim "
        "Schreiben nie.",
    annahmen=
        "`a` startet bei 2,5. Der Anzeigedruck `{}` schreibt die kuerzeste "
        "Form, die die Zahl zurueckliest -- also `5` und nicht `5.0`; "
        "`{:.1}` gaebe `5.0`.",
    ziel="Vorhersagen, was ankommt: der Wert **und** seine Schreibweise.",
),
("rs-ausleihen", 2): rahmen(
    mathematisch=
        "Dasselbe Maximum wie in C: `M_0 = v_0`, `M_k = max(M_(k-1), v_k)`. "
        "Der Startwert muss `v[0]` sein und nicht `0.0` -- sonst waere das "
        "Maximum eines Feldes aus lauter negativen Werten null. Vier Werte, "
        "das Maximum ist 9,0.",
    annahmen=
        "`v` wird nur gelesen, deshalb `&Vec<f64>`. Zwei Rust-Eigenheiten "
        "stecken in der Loesung: `m` braucht `mut`, und die letzte Zeile "
        "ohne Semikolon **ist** der Rueckgabewert -- ein Block ist in Rust "
        "ein Ausdruck.",
    ziel="Das Maximum ueber einen geliehenen Vektor finden.",
),

# --- Rust: der Loeser ----------------------------------------------------
("rs-vec", 0): rahmen(
    mathematisch=
        "Der Schritt liest aus dem alten Feld und schreibt in das neue: "
        "`&Vec<f64>` und `&mut Vec<f64>`. Die Signatur ist damit die "
        "Dokumentation -- in C stuende dort zweimal `double *`.\n\n"
        "Nebenbei faellt ein ganzer Fehler weg: `schritt(&u, &mut u, r)` "
        "wird abgelehnt, weil `&` und `&mut` auf dieselbe Variable nicht "
        "zusammengehen. Genau dieser Aufruf ist in C erlaubt und ergibt "
        "still das Gauss-Seidel-Verfahren statt des expliziten.",
    ziel=
        "Lesen, was die Signatur ueber das Verfahren sagt -- und was sie "
        "ausschliesst.",
),
("rs-vec", 1): rahmen(
    mathematisch=
        "Ein `Vec` besteht aus drei Zahlen: Zeiger, Laenge, Platz. "
        "`std::mem::swap` tauscht genau diese drei, Aufwand `O(1)` "
        "unabhaengig von der Zellzahl -- die Zellen selbst werden nicht "
        "angefasst. `u = w.clone()` waere dagegen `O(n)` je Zeitschritt.",
    ziel=
        "Vorhersagen, was nach dem Tausch in beiden Feldern steht, und "
        "sehen, warum der Tausch in einer Zeitschleife nichts kostet.",
),
("rs-vec", 2): rahmen(
    mathematisch=
        "Derselbe explizite Drei-Punkt-Stern wie im C-Kapitel: "
        "`w_i = u_i + r·(u_(i-1) - 2u_i + u_(i+1))` fuer die inneren "
        "Zellen. `r = 0,4` liegt unter der Stabilitaetsgrenze `½`; die "
        "Raender bleiben auf null, deshalb faellt die Summe von 1 auf "
        "`0,771801`, und in der Mitte stehen `0,031086`.\n\n"
        "Es sind **dieselben Zahlen wie in C** -- dieselbe Arithmetik, "
        "dieselbe Rundung. Die Sprache aendert am Ergebnis nichts. Sie "
        "aendert die Fehlersuche davor: `2.0` muss `2.0` heissen und nicht "
        "`2`, und ein Index daneben bricht mit Meldung ab.",
    physikalisch=
        "Stab mit 41 Zellen, anfangs kalt, eine Einheit Waerme in der "
        "Mitte, Enden auf fester Temperatur 0. 200 Schritte.",
    ziel=
        "Den Stern in `schritt` einbauen und nachrechnen, dass C und Rust "
        "bis auf die letzte Stelle dasselbe liefern.",
),
("rs-struct", 0): rahmen(
    mathematisch=
        "Eine eigene Struktur ist nicht `Copy`. `energie(p)` wuerde sie "
        "verschieben, und die naechste Zeile in `main` waere ein Fehler; "
        "`&Teilchen` leiht nur. Der Nebeneffekt ist derselbe wie bei "
        "`const&` in C++: Es wird nichts kopiert -- und die Regel gilt "
        "unabhaengig davon, wie gross die Struktur ist.",
    ziel="Den Grund fuer das `&` nennen: Besitz, nicht Geschwindigkeit.",
),
("rs-struct", 1): rahmen(
    mathematisch=
        "Symplektischer Schritt, und die Reihenfolge **ist** das "
        "Verfahren: `a = -x/m`, dann `v := v + a·dt`, dann `x := x + v·dt` "
        "mit dem **neuen** `v`. Wer `x` zuerst fortschreibt, hat das "
        "explizite Euler-Verfahren und eine Energie, die mit `(1 + dt²)` je "
        "Schritt waechst.",
    physikalisch=
        "Dieselbe Feder wie in Kapitel 3: `k = 1 N/m`, `m = 1 kg`, also "
        "`a = -x`. Keine Reibung.",
    annahmen=
        "Rust hilft hier nicht -- es ist ein Fehler des Verfahrens, nicht "
        "der Sprache. Was es hilft: `p` ist als `&mut` gekennzeichnet, der "
        "Leser sieht also sofort, dass die Funktion den Zustand aendert.",
    ziel=
        "Den symplektischen Schritt in der richtigen Reihenfolge "
        "zusammensetzen.",
),
("rs-struct", 2): rahmen(
    mathematisch=
        "Jetzt mit Masse in der Gleichung: `x'' = -(k/m)·x`, also "
        "`a = -x/m`. Die Kreisfrequenz ist `ω = √(k/m)`, die Schwingdauer "
        "`T = 2π/ω`.\n\n"
        "Die Energie ist `E = ½mv² + ½kx²`. Start bei `x = 1 m`, `v = 0`, "
        "also `E = ½·k·1² = 0,5 J` -- die Masse steht nicht darin, weil `v` "
        "null ist. Der symplektische Schritt haelt `E` in einem festen "
        "Band; `0,5004` ist kein Fehler, sondern dessen Breite.",
    physikalisch=
        "Feder mit `k = 1 N/m`, aber `m = 2 kg`: `ω = √(1/2) = 0,707 "
        "rad/s`, Schwingdauer `T = 8,9 s` -- die doppelte Masse schwingt "
        "langsamer. 400 Schritte zu `dt = 0,05 s` sind 20 s, also gut zwei "
        "Schwingungen.",
    annahmen=
        "`m` steht in der Struktur und wird nicht als zweiter Parameter "
        "durchgereicht -- genau dafuer sind Strukturen da.",
    ziel=
        "Die Masse in die Struktur aufnehmen und sehen, dass die "
        "Energieerhaltung auch mit `m ≠ 1` haelt.",
),
}
