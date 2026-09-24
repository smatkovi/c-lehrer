#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zeichnet die Skizzen zu den Herleitungen.

Eine Herleitung ist eine Kette von Saetzen, und an genau einer Stelle
haengt sie an einem Bild: dem Kraeftedreieck, der schiefen Ebene, der
Luftsaeule. Wer das Bild vor sich hat, liest die Rechnung als Beschreibung
dessen, was er sieht; wer es nicht hat, muss es sich nebenher bauen -- und
verliert dabei den Faden.

Gezeichnet wird schematisch, nicht abbildend: Gezeichnet wird das, woran
die Rechnung haengt: die Flaeche unter einer Geraden, der Unterschied
zwischen Bahn und Schritt, die Lage dreier Gitterpunkte. Alles bei 3x und am Ende verkleinert, sonst treppen die Schraegen.

Die Beschriftung steckt im Bild, also gibt es jede Skizze zweimal:
<name>.png und <name>.en.png. Welche gezeigt wird, entscheidet die App.

    tools/skizzen.py            # -> bilder/skizze-*.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "bilder")

W, H = 440, 300
S = 3

GRUND = (14, 14, 18)
LINIE = (120, 130, 150)
DUENN = (70, 78, 94)
TEXT = (226, 230, 240)
BETONT = (90, 169, 255)
WARN = (255, 177, 78)
GUT = (126, 231, 135)
ROT = (226, 74, 74)
KOERPER = (232, 236, 244)

SPRACHE = "de"

EN = {
    "Kraft": "force",
    "Auslenkung": "displacement",
    "Spannenergie": "strain energy",
    "Fläche = ½·k·x²": "area = ½·k·x²",
    "wahre Bahn": "true path",
    "Euler-Schritt": "Euler step",
    "Fehler": "error",
    "Steigung": "slope",
    "Zeit": "time",
    "Ort": "position",
    "Gitterpunkt": "grid point",
    "Mittel der Nachbarn": "mean of the neighbours",
    "liegt darunter, also steigt er": "lies below, so it rises",
    "Krümmung": "curvature",
}


def schrift(groesse):
    for pfad in ("/usr/share/fonts/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/TTF/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(pfad):
            return ImageFont.truetype(pfad, groesse)
    return ImageFont.load_default()


def leinwand():
    bild = Image.new("RGB", (W * S, H * S), GRUND)
    return bild, ImageDraw.Draw(bild)


def sichern(bild, name):
    os.makedirs(OUT, exist_ok=True)
    if SPRACHE != "de":
        name = name + "." + SPRACHE
    bild.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name + ".png"))
    print("  %s" % name)


def text(draw, x, y, inhalt, groesse=13, farbe=TEXT, mitte=False, rechts=False):
    if SPRACHE != "de":
        inhalt = EN.get(inhalt, inhalt)
    f = schrift(groesse * S)
    # Die Breite kommt in Geraetepunkten (die Schrift ist S-fach gross),
    # x und y sind in Zeicheneinheiten -- also erst umrechnen, sonst rueckt
    # der Text dreimal zu weit nach links und faellt aus dem Bild.
    kasten = draw.textbbox((0, 0), inhalt, font=f)
    breite = (kasten[2] - kasten[0]) / float(S)
    if mitte:
        x -= breite / 2.0
    elif rechts:
        x -= breite
    draw.text((x * S, y * S), inhalt, font=f, fill=farbe)


def strich(draw, x1, y1, x2, y2, farbe=LINIE, dicke=2):
    draw.line([(x1 * S, y1 * S), (x2 * S, y2 * S)], fill=farbe, width=dicke * S)


def gestrichelt(draw, x1, y1, x2, y2, farbe=DUENN, dicke=1, laenge=6):
    weite = math.hypot(x2 - x1, y2 - y1)
    if weite <= 0:
        return
    schritte = max(1, int(weite / laenge))
    for i in range(schritte):
        if i % 2:
            continue
        a, b = i / float(schritte), min(1.0, (i + 1) / float(schritte))
        strich(draw, x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
               x1 + (x2 - x1) * b, y1 + (y2 - y1) * b, farbe, dicke)


def pfeil(draw, x1, y1, x2, y2, farbe=BETONT, dicke=2, spitze=7):
    strich(draw, x1, y1, x2, y2, farbe, dicke)
    winkel = math.atan2(y2 - y1, x2 - x1)
    for seite in (+1, -1):
        a = winkel + seite * 2.6
        strich(draw, x2, y2, x2 + spitze * math.cos(a), y2 + spitze * math.sin(a),
               farbe, dicke)


def bogen(draw, cx, cy, r, von, bis, farbe=DUENN, dicke=1):
    """Winkelbogen; die Winkel in Grad, 0 ist rechts, positiv im Uhrzeigersinn."""
    draw.arc([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
             von, bis, fill=farbe, width=dicke * S)




# ---------------------------------------------------------------------------
# l-euler: woher die Haelfte in der Spannenergie kommt
# ---------------------------------------------------------------------------
def feder():
    bild, draw = leinwand()
    x0, y0 = 90, 220           # Ursprung
    x1, y1 = 360, 70           # Ende der Geraden F = k·x
    strich(draw, x0, y0, 396, y0, DUENN, 1)
    strich(draw, x0, y0, x0, 50, DUENN, 1)
    text(draw, 396, y0 + 24, "Auslenkung x", 11, DUENN, rechts=True)
    text(draw, x0 + 6, 52, "Kraft F", 11, DUENN)

    # Die Gerade F = k·x und die Dreiecksflaeche darunter
    draw.polygon([(x0 * S, y0 * S), (x1 * S, y0 * S), (x1 * S, y1 * S)],
                 fill=(26, 44, 66))
    strich(draw, x0, y0, x1, y1, BETONT, 2)
    text(draw, x1 - 40, y1 - 24, "F = k · x", 13, BETONT)

    gestrichelt(draw, x1, y0, x1, y1)
    gestrichelt(draw, x0, y1, x1, y1)
    text(draw, x1 + 6, y1 - 8, "k · x", 11, TEXT)
    text(draw, x1, y0 + 8, "x", 12, TEXT, mitte=True)

    text(draw, (x0 + x1) / 2 + 20, (y0 + y1) / 2 + 20, "Fläche = ½·k·x²", 12,
         GUT, mitte=True)
    text(draw, (x0 + x1) / 2 + 20, (y0 + y1) / 2 + 36, "Spannenergie", 11, GUT,
         mitte=True)

    text(draw, 22, 248, "Arbeit = Kraft × Weg, aber die Kraft wächst erst mit x",
         11, TEXT)
    text(draw, 22, 270, "im Mittel ½·k·x, mal Weg x   →   E = ½·k·x²", 13, GUT)
    sichern(bild, "skizze-feder")


# ---------------------------------------------------------------------------
# l-euler / l-verlet: der Schritt neben der Bahn
# ---------------------------------------------------------------------------
def eulerschritt():
    bild, draw = leinwand()
    x0, y0 = 70, 230
    strich(draw, x0, y0, 400, y0, DUENN, 1)
    strich(draw, x0, y0, x0, 50, DUENN, 1)
    text(draw, 398, y0 + 8, "Zeit", 11, DUENN, rechts=True)
    text(draw, x0 + 6, 52, "Ort", 11, DUENN)

    # Die wahre Bahn: eine Kurve, die sich nach oben biegt
    punkte = []
    for i in range(41):
        t = i / 40.0
        punkte.append((x0 + 20 + t * 260, y0 - 30 - 150 * t * t))
    for a, b in zip(punkte, punkte[1:]):
        strich(draw, a[0], a[1], b[0], b[1], KOERPER, 2)
    text(draw, punkte[-1][0] - 10, punkte[-1][1] - 24, "wahre Bahn", 11, KOERPER,
         rechts=True)

    # Der Schritt geht geradeaus, mit der Steigung am Anfang
    ax, ay = punkte[0]
    steigung = (punkte[1][1] - punkte[0][1]) / (punkte[1][0] - punkte[0][0])
    bx = punkte[-1][0]
    by = ay + steigung * (bx - ax)
    pfeil(draw, ax, ay, bx, by, BETONT, 2)
    text(draw, bx - 20, by + 14, "Euler-Schritt", 11, BETONT, rechts=True)
    text(draw, ax + 30, ay - 26, "Steigung = v", 10, BETONT)

    draw.ellipse([(ax - 5) * S, (ay - 5) * S, (ax + 5) * S, (ay + 5) * S],
                 fill=KOERPER)
    # Der Fehler ist der senkrechte Abstand am Ende
    pfeil(draw, bx, by, bx, punkte[-1][1], ROT, 2)
    pfeil(draw, bx, punkte[-1][1], bx, by, ROT, 2)
    text(draw, bx + 8, (by + punkte[-1][1]) / 2 - 8, "Fehler", 11, ROT)
    text(draw, bx + 8, (by + punkte[-1][1]) / 2 + 8, "≈ ½·a·dt²", 11, ROT)

    gestrichelt(draw, ax, y0, ax, ay)
    gestrichelt(draw, bx, y0, bx, min(by, punkte[-1][1]))
    text(draw, (ax + bx) / 2, y0 + 8, "dt", 12, TEXT, mitte=True)

    text(draw, 22, 258, "x(t+dt) = x + dt·v + dt²/2·a + ...", 12, TEXT)
    text(draw, 22, 280, "Euler nimmt die ersten zwei Glieder — der Rest ist der Fehler",
         11, GUT)
    sichern(bild, "skizze-eulerschritt")


# ---------------------------------------------------------------------------
# l-stencil: was die Klammer misst
# ---------------------------------------------------------------------------
def stern():
    bild, draw = leinwand()
    y0 = 200
    xs = (110, 220, 330)
    hoehen = (132, 62, 116)    # der mittlere Punkt liegt unter beiden
    strich(draw, 60, y0, 390, y0, DUENN, 1)
    for x in xs:
        gestrichelt(draw, x, y0, x, y0 - 150)
    beschriftung = ("u(i−1)", "u(i)", "u(i+1)")
    for x, h, name in zip(xs, hoehen, beschriftung):
        y = y0 - h
        draw.ellipse([(x - 6) * S, (y - 6) * S, (x + 6) * S, (y + 6) * S],
                     fill=BETONT)
        text(draw, x, y0 + 8, name, 11, TEXT, mitte=True)

    # Sehne zwischen den Nachbarn, und der Abstand zur Mitte
    ax, ay = xs[0], y0 - hoehen[0]
    cx, cy = xs[2], y0 - hoehen[2]
    strich(draw, ax, ay, cx, cy, DUENN, 1)
    mx = xs[1]
    my_sehne = ay + (cy - ay) * (mx - ax) / float(cx - ax)
    my = y0 - hoehen[1]
    pfeil(draw, mx, my, mx, my_sehne, GUT, 2)
    pfeil(draw, mx, my_sehne, mx, my, GUT, 2)
    text(draw, mx + 12, (my + my_sehne) / 2 - 16, "Mittel der Nachbarn", 10, GUT)
    text(draw, mx + 12, (my + my_sehne) / 2, "liegt darüber,", 10, GUT)
    text(draw, mx + 12, (my + my_sehne) / 2 + 14, "also steigt u(i)", 10, GUT)

    text(draw, 22, 240, "u(i−1) − 2·u(i) + u(i+1)  =  2 × dieser Abstand", 12, TEXT)
    text(draw, 22, 262, "das ist die Krümmung, mal h²  —  also u'' · h²", 11, TEXT)
    text(draw, 22, 282, "Wärme fließt dorthin, wo ein Punkt unter seinen Nachbarn liegt",
         11, GUT)
    sichern(bild, "skizze-stern")


def main():
    global SPRACHE
    for SPRACHE in ("de", "en"):
        print("Skizzen (%s):" % SPRACHE)
        feder()
        eulerschritt()
        stern()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
