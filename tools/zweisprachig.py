# -*- coding: utf-8 -*-
"""Macht aus einem einsprachigen Kurs einen zweisprachigen.

Der Lehrtext steht auf Deutsch in kurs.py und fragen.py, und dort soll er
auch bleiben: Es sind ein paar tausend Zeilen gewachsener Text, und sie
jetzt mit t("...", "...") zu durchsetzen hiesse, jede einzelne Zeile
anzufassen, um an keiner etwas zu aendern.

Stattdessen liegt die Uebersetzung daneben, in uebersetzung.py, als
schlichte Zuordnung deutscher Satz -> englischer Satz. Der Schluessel ist
der deutsche Text selbst; damit braucht keine Frage eine Kennung, und
aendert sich der deutsche Satz, faellt beim naechsten Bauen sofort auf,
dass seine Uebersetzung veraltet ist.

Uebersetzt werden nur Felder, die ein Mensch liest. Kennungen, Bildnamen,
Zahlen und Einheiten bleiben, wie sie sind.
"""
from __future__ import unicode_literals

# Felder, deren Inhalt gelesen wird.
TEXTFELDER = ("titel", "text", "q", "warum", "frage", "untertitel",
              "codeerklaerung", "erklaerung", "zeichen",
              "mathematisch", "physikalisch", "annahmen", "ziel")
# Felder, die eine Liste von Texten tragen.
LISTENFELDER = ("optionen", "options")


def paaren(wert, tabelle, fehlt):
    """Aus einem deutschen Text ein Sprachpaar."""
    if not isinstance(wert, str) or not wert.strip():
        return wert
    en = tabelle.get(wert)
    if en is None:
        fehlt.append(wert)
        en = wert
    return {"de": wert, "en": en}


def durchgehen(knoten, tabelle, fehlt):
    """Geht den Kursbaum durch und ersetzt jeden Text durch sein Paar."""
    if isinstance(knoten, list):
        return [durchgehen(x, tabelle, fehlt) for x in knoten]
    if not isinstance(knoten, dict):
        return knoten
    aus = {}
    for schluessel, wert in knoten.items():
        if schluessel in TEXTFELDER:
            aus[schluessel] = paaren(wert, tabelle, fehlt)
        elif schluessel in LISTENFELDER and isinstance(wert, list):
            aus[schluessel] = [paaren(x, tabelle, fehlt) for x in wert]
        else:
            aus[schluessel] = durchgehen(wert, tabelle, fehlt)
    return aus


def einheit_paaren(knoten, tabelle, fehlt):
    """Einheiten sind kurz und oft gleich; nur uebersetzen, wenn noetig."""
    if isinstance(knoten, list):
        for x in knoten:
            einheit_paaren(x, tabelle, fehlt)
    elif isinstance(knoten, dict):
        for schluessel, wert in knoten.items():
            if schluessel == "einheit" and isinstance(wert, str) and wert.strip():
                en = tabelle.get(wert, wert)
                knoten[schluessel] = {"de": wert, "en": en}
            else:
                einheit_paaren(wert, tabelle, fehlt)
    return knoten
