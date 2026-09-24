# -*- coding: utf-8 -*-
"""Haengt an eine Herleitung etwas an und zieht die Uebersetzung nach.

Der Schluessel der Uebersetzung ist der ganze deutsche Lektionstext. Wird
die Herleitung laenger, passt der alte Schluessel nicht mehr -- also wird
der Eintrag ersetzt: neuer deutscher Schluessel, alte englische Fassung
plus die Uebersetzung des Zusatzes.

    import nachziehen
    nachziehen.vorher()          # vor der Aenderung an herleitungen.py
    ... herleitungen.py aendern ...
    nachziehen.nachher({"l-upwind": "<english addition>"})
"""
import importlib, io, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SPEICHER = "/tmp/alte-texte.json"


def _texte():
    for name in ("curriculum", "herleitungen", "kursformeln", "uebersetzung"):
        if name in sys.modules:
            del sys.modules[name]
    import curriculum
    return {l["id"]: l["text"]
            for kap in curriculum.CHAPTERS for l in kap["lessons"]}


def vorher():
    io.open(SPEICHER, "w", encoding="utf-8").write(
        json.dumps(_texte(), ensure_ascii=False))


def nachher(zusaetze):
    alt_texte = json.load(io.open(SPEICHER, encoding="utf-8"))
    neu_texte = _texte()
    from uebersetzung import EN
    p = os.path.join(ROOT, "uebersetzung.py")
    s = io.open(p, encoding="utf-8").read()
    for lid, extra_en in zusaetze.items():
        alt, neu = alt_texte[lid], neu_texte[lid]
        assert alt != neu, lid + ": nichts geaendert"
        assert neu.startswith(alt), lid + ": der Zusatz steht nicht am Ende"
        assert alt in EN, lid + ": alte Uebersetzung fehlt"
        schluessel = repr(alt)
        assert schluessel in s, lid + ": alter Schluessel nicht in der Datei"
        s = s.replace(schluessel, repr(neu), 1)
        i = s.index(repr(neu)) + len(repr(neu))
        j = s.index(":\n", i) + 2
        k = s.index(",\n", j)
        s = s[:j] + repr(EN[alt] + extra_en) + s[k:]
        print("nachgezogen:", lid)
    io.open(p, "w", encoding="utf-8").write(s)
