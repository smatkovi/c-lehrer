#!/usr/bin/env python3
"""Turns the authored course into data the C++ app reads.

The course is written in Python because that is where the test harness
lives -- tools/test-curriculum.py runs every example and every model
solution through the real interpreter before anything ships. The app
itself is C++ and reads only the JSON that comes out of here.

    tools/make-kurs.py        # -> data/kurs.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import curriculum
import placement
from zweisprachig import durchgehen, einheit_paaren

try:
    from uebersetzung import EN
except ImportError:      # noch keine Uebersetzung vorhanden
    EN = {}


def mischen(optionen, antwort, saat):
    """Die Antwortmöglichkeiten durchmischen und den Index nachführen.

    Beim Schreiben steht die richtige Antwort bequem an erster Stelle. Bliebe
    sie dort, wäre der ganze Kurs mit einem Fingertipp lösbar, ohne eine
    einzige Frage gelesen zu haben -- und genau so ist es aufgefallen: "es
    wird immer die erste Antwort ausgewählt".

    Gemischt wird deterministisch aus der Fragenkennung, nicht zufällig: Die
    Reihenfolge muss über Neubauten hinweg gleich bleiben, sonst sitzt eine
    gemerkte Position beim nächsten Update woanders.

    Die Streuung ist FNV-1a mit Nachmischung. Ein einfaches "mal 131 plus
    Zeichen" genügt hier nicht: Die Saatwerte unterscheiden sich oft nur in
    der letzten Ziffer, und dann liefern aufeinanderfolgende Fragen
    systematisch verwandte Reihenfolgen -- im ersten Versuch landete die
    richtige Antwort dadurch in der Hälfte aller Fälle wieder vorne.
    """
    zustand = 2166136261
    for zeichen in saat:
        zustand = ((zustand ^ ord(zeichen)) * 16777619) & 0xffffffff
    zustand ^= zustand >> 15
    zustand = (zustand * 2246822519) & 0xffffffff
    zustand ^= zustand >> 13
    zustand = (zustand * 3266489917) & 0xffffffff
    zustand ^= zustand >> 16

    def naechste():
        nonlocal zustand
        zustand ^= (zustand << 13) & 0xffffffff
        zustand ^= zustand >> 17
        zustand ^= (zustand << 5) & 0xffffffff
        return zustand

    reihen = list(range(len(optionen)))
    for i in range(len(reihen) - 1, 0, -1):
        j = naechste() % (i + 1)
        reihen[i], reihen[j] = reihen[j], reihen[i]
    return [optionen[k] for k in reihen], reihen.index(antwort)



def aufgabe(task, saat):
    """Auswahlfragen mischen; alles andere unverändert durchreichen."""
    if task.get("kind") != "mc":
        return task
    out = dict(task)
    optionen, antwort = mischen(task["options"], task["answer"], saat)
    out["options"] = optionen
    out["answer"] = antwort
    return out


def main():
    chapters = []
    for chapter in curriculum.CHAPTERS:
        lessons = []
        for lesson in chapter["lessons"]:
            lessons.append({
                "id": lesson["id"],
                "titel": lesson["title"],
                "begriffe": lesson["concepts"],
                "text": lesson["text"],
                "codeerklaerung": lesson.get("codeerklaerung", ""),
                "beispiel": lesson["example"],
                "ausgabe": lesson["output"],
                "aufgaben": [aufgabe(t, lesson["id"] + "#" + str(i))
                             for i, t in enumerate(lesson["exercises"])],
            })
        chapters.append({
            "id": chapter["id"],
            "titel": chapter["title"],
            "stufe": chapter["level"],
            "sprache": chapter["lang"],
            "text": chapter["blurb"],
            "lektionen": lessons,
        })

    plan = []
    for ident, titel, stufe, sprache, fertig in curriculum.PLAN:
        plan.append({"id": ident, "titel": titel, "stufe": stufe,
                     "sprache": sprache, "fertig": fertig})

    items = []
    for entry in placement.ITEMS:
        e_optionen, e_antwort = mischen(entry["options"], entry["answer"],
                                        entry["id"])
        items.append({
            "id": entry["id"], "stufe": entry["level"],
            "thema": entry["topic"], "frage": entry["q"],
            "code": entry["code"], "optionen": e_optionen,
            "antwort": e_antwort, "warum": entry["why"],
        })

    # Aus einsprachig zweisprachig machen. Fehlt eine Uebersetzung, sagt
    # der Bau welche -- und liefert nicht stillschweigend Deutsch aus.
    fehlt = []
    chapters = durchgehen(chapters, EN, fehlt)
    items = durchgehen(items, EN, fehlt)
    themen = durchgehen(placement.TOPICS, EN, fehlt)
    einheit_paaren(chapters, EN, fehlt)
    einheit_paaren(items, EN, fehlt)

    # Codeerklaerung an den Lektionstext haengen, in jeder Sprache
    # einzeln. Erst hier, damit beide ihren eigenen Schluessel behalten.
    for kap in chapters:
        for lek in kap["lektionen"]:
            erk = lek.pop("codeerklaerung", "")
            if not erk:
                continue
            for code in ("de", "en"):
                lek["text"][code] = (lek["text"][code] + "\n\n"
                                     + erk[code])

    vollstaendig = not fehlt
    if fehlt:
        einzig = sorted(set(fehlt), key=len)
        pfad = os.path.join(ROOT, "data", "fehlt.json")
        with open(pfad, "w", encoding="utf-8") as fh:
            json.dump(einzig, fh, ensure_ascii=False, indent=1)
        print("%d Uebersetzungen fehlen (%d verschiedene), Liste in "
              "data/fehlt.json" % (len(fehlt), len(einzig)), file=sys.stderr)
        if os.environ.get("UNVOLLSTAENDIG") != "1":
            return 1
        print("UNVOLLSTAENDIG=1: wird trotzdem geschrieben", file=sys.stderr)
    else:
        print("Zweisprachigkeit: vollstaendig (%d Texte)" % len(EN))
        pfad = os.path.join(ROOT, "data", "fehlt.json")
        if os.path.exists(pfad):
            os.remove(pfad)

    out = {
        "titel": {"de": "C-Lehrer", "en": "C Teacher"},
        "untertitel": {
            "de": ("C und C++ für Physik- und Strömungssimulation. "
                   "Der Code, den du schreibst, läuft auf diesem Gerät "
                   "wirklich."),
            "en": ("C and C++ for physics and fluid simulation. The code "
                   "you write really runs on this device."),
        },
        "ausfuehrbar": True,
        # Englisch erst anbieten, wenn es auch vollstaendig ist.
        "sprachen": ["de", "en"] if vollstaendig else ["de"],
        "kapitel": chapters,
        "plan": plan,
        "einstufung": {"themen": themen, "fragen": items},
    }
    path = os.path.join(ROOT, "data", "kurs.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    size = os.path.getsize(path)
    print("data/kurs.json: %d Kapitel, %d Lektionen, %d Einstufungsfragen, %d B"
          % (len(chapters),
             sum(len(c["lektionen"]) for c in chapters),
             len(items), size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
