#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Traegt eine Uebersetzung ein, mit korrekter Maskierung.

    tools/eintragen.py <nummer> <datei-mit-englisch>

Der deutsche Schluessel kommt aus data/fehlt.json (kuerzeste zuerst), das
Englische aus der Datei. Geschrieben wird mit repr(), damit Backslashes,
Anfuehrungszeichen und Zeilenumbrueche nicht verlorengehen -- ein von Hand
eingesetztes \\n wurde beim Einlesen zum Zeilenumbruch, und der Schluessel
passte dann auf nichts.
"""
import io, json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0, ROOT)
try: from uebersetzung import EN
except ImportError: EN={}
offen = sorted([t for t in json.load(open(os.path.join(ROOT,"data","fehlt.json")))
                if t not in EN], key=len)
de = offen[int(sys.argv[1])]
en = io.open(sys.argv[2], encoding="utf-8").read().rstrip("\n")
p = os.path.join(ROOT, "uebersetzung.py")
s = io.open(p, encoding="utf-8").read()
eintrag = "\n%s:\n%s,\n" % (repr(de), repr(en))
assert "\n})\n" in s, "Ankerpunkt fehlt"
s = s.replace("\n})\n", eintrag + "\n})\n")
io.open(p, "w", encoding="utf-8").write(s)
print("eingetragen (%d Zeichen): %s" % (len(de), de[:60].replace("\n", " ")))
