#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setzt die Formeln des Kurses und legt sie als Bilder daneben.

Warum Bilder und nicht Text: Die Oberflaeche ist QtQuick 1.1 auf Harmattan
und Silica auf Sailfish. Beide koennen Rich Text, aber keiner von beiden
kann einen Bruchstrich, eine Wurzel oder ein Summenzeichen mit Grenzen --
`\\frac{a+b}{2}` laesst sich in HTML nur als Tabelle nachbauen, und das
sieht in jeder Schriftgroesse anders falsch aus.

Ein TeX-Setzer auf dem Geraet waere die andere Moeglichkeit (KaTeX in einer
WebView; die N950 hat QtWebKit). Er kostet aber eine ganze Browsermaschine
je Formel, auf der SGX 530 spuerbar, und bringt nichts ein: Die Formeln des
Kurses stehen beim Bauen schon fest. Also werden sie hier gesetzt, einmal,
und das Geraet zeigt nur noch ein PNG.

Gesetzt wird mit matplotlib.mathtext -- das ist ein eigener TeX-Setzer fuer
Mathematik, der keine TeX-Installation braucht, und mit dem Zeichensatz
"cm" schreibt er in Computer Modern, also in der Schrift, die man von LaTeX
kennt. Was er kann: \\frac \\sqrt \\sum \\int \\vec, Indizes, Exponenten,
Griechisch, \\mathrm. Was er nicht kann: \\begin{array}, \\begin{cases},
\\underbrace, \\tfrac. Dafuer braeuchte es echtes LaTeX (texlive + dvisvgm).

    tools/formeln.py            # alle Formeln des Kurses neu setzen
    tools/formeln.py --probe    # Vergleichsbild der Zeichensaetze

Die Bilder und bilder/formeln.json gehoeren ins Repository: matplotlib ist
auf dem Baurechner da, nicht ueberall, und make-kurs.py soll ohne es laufen.
"""
from __future__ import unicode_literals

import hashlib
import io
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)
sys.path.insert(0, WURZEL)

BILDER = os.path.join(WURZEL, "bilder")
INDEX = os.path.join(BILDER, "formeln.json")

# Die Schrift wird hell gesetzt, nicht in der Akzentfarbe: Auf Harmattan
# liegt sie auf dem dunklen Codegrund, auf Sailfish wird sie ohnehin
# eingefaerbt (ColorOverlay), und dort zaehlt nur der Alphakanal.
FARBE = "#e4e4ec"
# Grundgroesse in Geraetepunkten, und wie oft feiner gerendert wird. Der N9
# zeigt 480 Punkte auf der Breite, ein Sailfish-Geraet bis 1080 -- dreifach
# gerendert bleibt die Formel auf beiden scharf.
GROESSE = 22
SCHAERFE = 3


def kennung(tex):
    """Dateiname aus dem Formeltext -- gleiche Formel, gleiche Datei."""
    roh = hashlib.sha1(tex.encode("utf-8")).hexdigest()[:8]
    return "formel-" + roh


def setzen(tex, pfad=None, groesse=GROESSE, schaerfe=SCHAERFE, farbe=FARBE,
           zeichensatz="cm"):
    """Eine Formel setzen. Gibt (Bild, Breite, Hoehe) in Geraetepunkten."""
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["mathtext.fontset"] = zeichensatz
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from PIL import Image

    dpi = 100
    fig = Figure(figsize=(0.01, 0.01), dpi=dpi)
    FigureCanvasAgg(fig)
    fig.patch.set_alpha(0.0)
    fig.text(0, 0, tex, fontsize=groesse * schaerfe, color=farbe)
    puffer = io.BytesIO()
    fig.savefig(puffer, format="png", dpi=dpi, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    puffer.seek(0)
    bild = Image.open(puffer).convert("RGBA")
    breite = int(round(bild.size[0] / float(schaerfe)))
    hoehe = int(round(bild.size[1] / float(schaerfe)))
    if pfad:
        bild.save(pfad)
    return bild, breite, hoehe


def gesetzte():
    """Was schon gesetzt ist: Kennung -> {tex, breite, hoehe}.

    Liest nur die Datei; matplotlib wird dafuer nicht gebraucht. So kann
    make-kurs.py auf jedem Rechner laufen, auch ohne Setzer.
    """
    if not os.path.exists(INDEX):
        return {}
    with io.open(INDEX, encoding="utf-8") as fh:
        return json.load(fh)


def formeln_im_kurs():
    """Jede Formel des Kurses, in der Reihenfolge, in der sie vorkommt."""
    import curriculum
    raus = []
    for kapitel in curriculum.CHAPTERS:
        for lektion in kapitel["lessons"]:
            for eintrag in lektion.get("formeln", []):
                raus.append((lektion["id"], eintrag["tex"]))
    return raus


def probe():
    """Vergleicht die Zeichensaetze -- welcher sieht nach LaTeX aus."""
    from PIL import Image, ImageDraw
    tex = r"$L = \frac{1}{2}\,\rho\,v^{2}\,S\,c_A$"
    saetze = ["cm", "dejavusans", "stix"]
    bilder = [setzen(tex, zeichensatz=s, schaerfe=2)[0] for s in saetze]
    breite = max(b.size[0] for b in bilder) + 20
    hoehe = sum(b.size[1] for b in bilder) + 20 * len(bilder)
    blatt = Image.new("RGBA", (breite, hoehe), (14, 14, 18, 255))
    mal = ImageDraw.Draw(blatt)
    y = 10
    for name, b in zip(saetze, bilder):
        blatt.alpha_composite(b, (10, y))
        mal.text((breite - 90, y + 4), name, fill=(120, 120, 130, 255))
        y += b.size[1] + 20
    pfad = os.path.join(WURZEL, "build", "formel-probe.png")
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    blatt.convert("RGB").save(pfad)
    print(pfad)
    return 0


def main(argv):
    if "--probe" in argv:
        return probe()

    eintraege = formeln_im_kurs()
    if not eintraege:
        print("Der Kurs enthaelt keine Formeln.", file=sys.stderr)
        return 0

    os.makedirs(BILDER, exist_ok=True)
    index = gesetzte()

    neu, bekannt = 0, 0
    gebraucht = set()
    for lektion, tex in eintraege:
        name = kennung(tex)
        gebraucht.add(name)
        pfad = os.path.join(BILDER, name + ".png")
        if name in index and os.path.exists(pfad):
            bekannt += 1
            continue
        _, breite, hoehe = setzen(tex, pfad)
        index[name] = {"tex": tex, "breite": breite, "hoehe": hoehe}
        print("%-14s %-24s %3dx%-3d  %s" % (name, lektion, breite, hoehe, tex))
        neu += 1

    # Formeln, die aus dem Kurs verschwunden sind, fallen auf -- geloescht
    # wird von Hand, damit ein Tippfehler im Kurs keine Bilder wegraeumt.
    verwaist = sorted(set(index) - gebraucht)
    for name in verwaist:
        print("verwaist: %s.png (nicht mehr im Kurs)" % name, file=sys.stderr)

    with io.open(INDEX, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, ensure_ascii=False, indent=1,
                            sort_keys=True))
    print("%d Formeln: %d neu gesetzt, %d schon da" % (len(gebraucht), neu,
                                                       bekannt))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
