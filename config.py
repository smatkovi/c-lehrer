# -*- coding: utf-8 -*-
"""Where the learner's progress lives.

Python 2.6 on this device, so: no dict comprehensions, no set literals, no
"{}".format -- all of that is 2.7 and up.
"""
import json
import os


def _home():
    """The phone owner's home, even when started without an environment."""
    home = os.environ.get("HOME", "")
    if home and os.path.isdir(os.path.join(home, ".config")):
        return home
    try:
        import pwd
        return pwd.getpwnam("user").pw_dir
    except (ImportError, KeyError):
        return "/home/user"


HOME = _home()
DIR = os.path.join(HOME, ".config", "c-lehrer")
CACHE = os.path.join(HOME, ".cache", "c-lehrer")
PATH = os.path.join(DIR, "fortschritt.json")

ROOT = os.path.dirname(os.path.abspath(__file__))
CRUN = os.path.join(ROOT, "bin", "crun")

DEFAULTS = {
    "level": 0,             # 0 = placement test not taken yet
    "profil": {},           # topic -> 0..1, how the placement test went
    "lektionen": {},        # lesson id -> {"stand": ..., "versuche": n}
    "begriffe": {},         # concept id -> spaced repetition card
    "einstufung": None,     # the last placement test, for looking back at it
    "letzte": "",           # lesson the learner was last in
    "loesungen": {},        # lesson id -> the learner's own code, kept
}


def load():
    data = {}
    data.update(DEFAULTS)
    try:
        fh = open(PATH)
        try:
            data.update(json.load(fh))
        finally:
            fh.close()
    except (IOError, OSError, ValueError):
        pass
    return data


def save(data):
    if not os.path.isdir(DIR):
        os.makedirs(DIR, 0755)
    tmp = PATH + ".neu"
    fh = open(tmp, "w")
    try:
        json.dump(data, fh, indent=1, sort_keys=True)
    finally:
        fh.close()
    os.rename(tmp, PATH)
