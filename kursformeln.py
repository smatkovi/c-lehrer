# -*- coding: utf-8 -*-
"""Die Formeln des Kurses, zweimal aufgeschrieben.

Links steht die Zeile so, wie sie im Beispielprogramm wirklich vorkommt,
rechts dieselbe Sache gesetzt. Das ist der ganze Zweck: Ein Verfahren
erkennt man an der Formel schneller als an der Zuweisung, aber schreiben
muss man am Ende die Zuweisung. Wer beides nebeneinander sieht, kann das
eine ins andere uebersetzen -- und genau das ist die Arbeit, die numerische
Programmierung ausmacht.

Der Code muss Zeichen fuer Zeichen aus dem Beispiel der Lektion stammen.
Eine aufgeraeumte Fassung waere eine dritte Schreibweise und damit eine
Huerde mehr, keine weniger.

Gesetzt werden die Formeln beim Bauen, siehe tools/formeln.py. Das Geraet
bekommt nur PNG-Dateien zu sehen.
"""
from __future__ import unicode_literals

def formel(code, tex, untertitel="", erklaerung=""):
    """Dieselbe Sache zweimal: wie sie im Programm steht und wie sie gesetzt
    aussieht.

    Der Code ist die Zeile, die unten im Beispiel wirklich vorkommt -- nicht
    eine aufgeraeumte Fassung davon. Wer die Formel verstanden hat, soll sie
    im Programm wiedererkennen, und dafuer muessen beide Seiten Zeichen fuer
    Zeichen zusammenpassen.

    `tex` ist Mathematik in TeX-Schreibweise, in Dollarzeichen. Gesetzt wird
    beim Bauen (tools/formeln.py), das Geraet zeigt nur noch ein Bild.
    `untertitel` ist die halbe Zeile, die sagt, was dasteht. `erklaerung`
    ist die Antwort auf die Frage, die beim Hinsehen entsteht -- warum
    dieses Glied, warum dieser Faktor, woher die Haelfte. Beide werden
    uebersetzt, Code und TeX nicht: Eine Formel ist in jeder Sprache
    dieselbe.
    """
    return {"code": code, "tex": tex, "untertitel": untertitel,
            "erklaerung": erklaerung}

KURSFORMELN = {

    "l-euler": [
        formel("xn = x + v * dt;",
               r"$x_{n+1} = x_n + v_n\,\Delta t$",
               "Ort, aus dem alten Zustand",
               "Rechts steht das alte `v`, nicht das neue. Das ist gemeint mit **explizit**: Alles auf der rechten Seite ist der Zustand vom Anfang des Schritts. Wer hier schon das neue `v` einsetzt, hat ein anderes Verfahren programmiert -- ein besseres sogar, aber eben nicht Euler."),
        formel("v  = v + a * dt;",
               r"$v_{n+1} = v_n + a_n\,\Delta t$",
               "Geschwindigkeit, ebenfalls aus dem alten",
               "Der ganze Schritt wird mit der Beschleunigung vom **Anfang** gerechnet. Bei einer Feder zeigt sie zur Ruhelage und ist für den Bogen, den der Punkt tatsächlich durchläuft, zu klein. Jeder Schritt setzt ihn ein Stückchen zu weit außen ab, und das summiert sich, statt sich herauszumitteln."),
        formel("0.5*v*v + 0.5*x*x",
               r"$E = \frac{1}{2}v^{2} + \frac{1}{2}x^{2}$",
               "Die Energie, die gleich bleiben sollte",
               "`½v²` ist die Bewegungsenergie (mit m = 1). `½x²` ist die Spannenergie der Feder: Die Federkraft wächst linear mit der Auslenkung, `F = k·x`, ist am Anfang also null und erst am Ende `k·x` -- im Mittel `½k·x`. Arbeit ist mittlere Kraft mal Weg, also `½k·x²`, die Dreiecksfläche unter der Geraden `F(x)`. Mit k = 1 bleibt `½x²`. Die Probe, dass es die richtige Größe ist: `dE/dt = v·v̇ + x·ẋ = v·(−x) + x·v = 0`."),
    ],

    "l-verlet": [
        formel("x = x + v * dt + 0.5 * a * dt * dt;",
               r"$x_{n+1} = x_n + v_n\,\Delta t"
               r" + \frac{1}{2}a_n\,\Delta t^{2}$",
               "Der Ort bekommt das halbe Beschleunigungsglied",
               "Das ist ein Glied mehr aus der Taylorreihe als bei Euler, und es ist genau der Weg, den eine gleichmäßige Beschleunigung in der Zeit `dt` zurücklegt: `s = ½a·t²`. Deshalb ist der Ort hier von zweiter Ordnung genau, und deshalb braucht Verlet auch kein `xn` als Zwischenwert -- `x` wird fertig gerechnet, bevor `a` sich ändert."),
        formel("v = v + 0.5 * (a + an) * dt;",
               r"$v_{n+1} = v_n + \frac{a_n + a_{n+1}}{2}\,\Delta t$",
               "Die Geschwindigkeit mittelt alte und neue Beschleunigung",
               "Statt der Beschleunigung vom Anfang (Euler) wird der Mittelwert aus Anfang und Ende genommen -- die Trapezregel statt des Rechtecks. Das ist der ganze Unterschied, und er genügt: Der Energiefehler wächst nicht mehr, er schwankt nur noch um einen festen Wert."),
    ],

    "l-stencil": [
        formel("w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);",
               r"$u_i^{\,n+1} = u_i^{\,n}"
               r" + r\,\left(u_{i-1}^{\,n} - 2u_i^{\,n} + u_{i+1}^{\,n}\right)$",
               "Ein Zeitschritt der Diffusion",
               "Die Klammer ist die **zweite Ableitung** in Differenzenform: Addiert man die Taylorreihen des linken und des rechten Nachbarn, heben sich die ersten Ableitungen weg und übrig bleibt `u₋ − 2u₀ + u₊ ≈ h²·u''`. Sie misst also die Krümmung: Liegt ein Punkt unter dem Mittel seiner Nachbarn, steigt er. Genau das tut Wärme."),
    ],

    "l-cfl": [
        formel("double r = 0.6;          /* ueber der Grenze von 0.5 */",
               r"$r = \frac{D\,\Delta t}{\Delta x^{2}} \leq \frac{1}{2}$",
               "Was r bedeutet, und wo es aufhört zu gehen",
               "Setzt man eine einzelne Welle in den Stern ein, wird sie je Schritt mit `g = 1 − 4r·sin²(kh/2)` multipliziert. Am schlimmsten ist die kürzeste Welle, die von Zelle zu Zelle springt: dort ist `g = 1 − 4r`, und `|g| ≤ 1` verlangt `r ≤ ½`. Darüber verdoppelt sich der Zickzack mit jedem Schritt. Halbes `h` heißt deshalb ein Viertel `dt`."),
    ],

    "l-upwind": [
        formel("b[i] = a[i] - C * (a[i] - a[i-1]);",
               r"$a_i^{\,n+1} = a_i^{\,n}"
               r" - C\,\left(a_i^{\,n} - a_{i-1}^{\,n}\right)$",
               "Stromaufwärts: die Zelle, aus der es kommt",
               "Die Information kommt mit der Strömung, also von links, wenn `v > 0` ist -- und genau von dort holt der Schritt seinen Wert. Das Verfahren schaut dorthin, wo die Physik herkommt. Es ist nur erster Ordnung und verschmiert die Kante, aber es erfindet keine Werte, die nie da waren."),
        formel("y[i] = z[i] - 0.5 * C * (z[i+1] - z[i-1]);",
               r"$z_i^{\,n+1} = z_i^{\,n}"
               r" - \frac{C}{2}\left(z_{i+1}^{\,n} - z_{i-1}^{\,n}\right)$",
               "Zentral: beide Nachbarn, und deshalb instabil",
               "Der zentrale Differenzenquotient ist genauer (zweiter Ordnung), aber der eigene Wert `z_i` kommt in der Ableitung gar nicht vor -- es gibt nichts, was ihn festhält. Die Zickzack-Welle wird dadurch verstärkt statt gedämpft, und das Ergebnis schwingt, bevor es explodiert. Genauigkeit und Stabilität sind zwei verschiedene Dinge."),
    ],

    "l-fliesskomma": [
        formel("double summe = gross + klein;",
               r"$10^{16} + 1 = 10^{16}$",
               "Was double hier wirklich rechnet",
               "`double` hat 53 Bit Mantisse, also knapp 16 Dezimalstellen. Bei der Größenordnung 10¹⁶ ist der Abstand zweier benachbarter darstellbarer Zahlen schon 2 -- eine 1 dazuzuzählen trifft gar keine neue Zahl. Das Ergebnis ist nicht gerundet, es ist unverändert. Deshalb summiert man lange Reihen vom kleinsten Glied her."),
    ],
}
