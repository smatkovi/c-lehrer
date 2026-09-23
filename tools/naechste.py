#!/usr/bin/env python3
"""Zeigt die naechsten noch nicht uebersetzten Texte.

    tools/naechste.py [anzahl] [--lang]
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
try:
    from uebersetzung import EN
except ImportError:
    EN = {}
offen = [t for t in json.load(open(os.path.join(ROOT, "data", "fehlt.json")))
         if t not in EN]
n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20
lang = "--lang" in sys.argv
offen.sort(key=len, reverse=lang)
print("### noch offen: %d von %d" % (len(offen), len(json.load(open(
    os.path.join(ROOT, "data", "fehlt.json"))))))
for t in offen[:n]:
    print("---")
    print(t)
