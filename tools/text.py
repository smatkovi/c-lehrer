#!/usr/bin/env python3
"""Gibt den n-ten noch offenen Text vollstaendig aus (kuerzeste zuerst)."""
import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0, ROOT)
try: from uebersetzung import EN
except ImportError: EN={}
offen=[t for t in json.load(open(os.path.join(ROOT,"data","fehlt.json"))) if t not in EN]
offen.sort(key=len)
i=int(sys.argv[1]) if len(sys.argv)>1 else 0
print("### %d offen, Nummer %d, %d Zeichen" % (len(offen), i, len(offen[i])))
sys.stdout.write(offen[i])
