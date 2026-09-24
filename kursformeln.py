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

def formel(code, tex, untertitel=""):
    """Dieselbe Sache zweimal: wie sie im Programm steht und wie sie gesetzt
    aussieht.

    Der Code ist die Zeile, die unten im Beispiel wirklich vorkommt -- nicht
    eine aufgeraeumte Fassung davon. Wer die Formel verstanden hat, soll sie
    im Programm wiedererkennen, und dafuer muessen beide Seiten Zeichen fuer
    Zeichen zusammenpassen.

    `tex` ist Mathematik in TeX-Schreibweise, in Dollarzeichen. Gesetzt wird
    beim Bauen (tools/formeln.py), das Geraet zeigt nur noch ein Bild.
    Uebersetzt wird davon nur der Untertitel; eine Formel ist in jeder
    Sprache dieselbe.
    """
    return {"code": code, "tex": tex, "untertitel": untertitel}

KURSFORMELN = {

    "l-euler": [
        formel("xn = x + v * dt;",
               r"$x_{n+1} = x_n + v_n\,\Delta t$",
               "Ort, aus dem alten Zustand"),
        formel("v  = v + a * dt;",
               r"$v_{n+1} = v_n + a_n\,\Delta t$",
               "Geschwindigkeit, ebenfalls aus dem alten"),
        formel("0.5*v*v + 0.5*x*x",
               r"$E = \frac{1}{2}v^{2} + \frac{1}{2}x^{2}$",
               "Die Energie, die gleich bleiben sollte"),
    ],

    "l-verlet": [
        formel("x = x + v * dt + 0.5 * a * dt * dt;",
               r"$x_{n+1} = x_n + v_n\,\Delta t"
               r" + \frac{1}{2}a_n\,\Delta t^{2}$",
               "Der Ort bekommt das halbe Beschleunigungsglied"),
        formel("v = v + 0.5 * (a + an) * dt;",
               r"$v_{n+1} = v_n + \frac{a_n + a_{n+1}}{2}\,\Delta t$",
               "Die Geschwindigkeit mittelt alte und neue Beschleunigung"),
    ],

    "l-stencil": [
        formel("w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);",
               r"$u_i^{\,n+1} = u_i^{\,n}"
               r" + r\,\left(u_{i-1}^{\,n} - 2u_i^{\,n} + u_{i+1}^{\,n}\right)$",
               "Ein Zeitschritt der Diffusion"),
    ],

    "l-cfl": [
        formel("double r = 0.6;          /* ueber der Grenze von 0.5 */",
               r"$r = \frac{D\,\Delta t}{\Delta x^{2}} \leq \frac{1}{2}$",
               "Was r bedeutet, und wo es aufhört zu gehen"),
    ],

    "l-upwind": [
        formel("b[i] = a[i] - C * (a[i] - a[i-1]);",
               r"$a_i^{\,n+1} = a_i^{\,n}"
               r" - C\,\left(a_i^{\,n} - a_{i-1}^{\,n}\right)$",
               "Stromaufwärts: die Zelle, aus der es kommt"),
        formel("y[i] = z[i] - 0.5 * C * (z[i+1] - z[i-1]);",
               r"$z_i^{\,n+1} = z_i^{\,n}"
               r" - \frac{C}{2}\left(z_{i+1}^{\,n} - z_{i-1}^{\,n}\right)$",
               "Zentral: beide Nachbarn, und deshalb instabil"),
    ],

    "l-fliesskomma": [
        formel("double summe = gross + klein;",
               r"$10^{16} + 1 = 10^{16}$",
               "Was double hier wirklich rechnet"),
    ],
}
