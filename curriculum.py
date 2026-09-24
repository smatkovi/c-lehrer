# -*- coding: utf-8 -*-
"""The course: chapters, lessons, exercises.

Shape of the thing, and why it is this shape:

* A lesson is short -- one idea, a worked example that runs, then exercises.
  A phone screen holds about that much, and one idea per card is what the
  learning research keeps finding anyway.
* The exercises go from least to most effort: first read and predict, then
  fill a gap, then assemble from given lines, then write it yourself. The
  worked example is faded out step by step rather than dropped.
* Everything in "c"-language chapters must run under crun (picoc). That
  interpreter has real limits, found by trying:
      - one struct member per line; "double x, y;" is a syntax error
      - no "const" on a declaration
      - no function pointers
      - a pointer may not be used as a truth value: no "if (p)", no "p ? a : b"
      - float and double are the same type, so a lesson about their
        difference has to be read and predicted, never run
  Those limits are why some things are taught as predictions instead.

C++ chapters are read-and-predict throughout: there is no C++ interpreter on
this device, and pretending otherwise with a fake "run" button would teach
people to trust an output nobody produced.
"""
from __future__ import unicode_literals

from herleitungen import HERLEITUNGEN
from codeerklaerungen import CODEERKLAERUNGEN
from kursformeln import KURSFORMELN


def mc(q, options, answer, why, code=""):
    """Read something, pick the right statement about it."""
    return {"kind": "mc", "q": q, "code": code, "options": options,
            "answer": answer, "why": why}


def predict(q, code, answer, why, run=True):
    """Say what it will print -- then watch it actually print.

    The most valuable exercise in the whole app. Being wrong here, and
    seeing it immediately, is what changes someone's model of the machine.
    """
    return {"kind": "predict", "q": q, "code": code, "answer": answer,
            "why": why, "run": run}


def blank(q, code, answers, why, alts=None):
    """The example again, with the load-bearing part removed."""
    return {"kind": "blank", "q": q, "code": code, "answers": answers,
            "alts": alts or [], "why": why}


def parsons(q, lines, why, distractors=None):
    """Put the given lines in order. Tap to build -- no typing.

    Assembling correct lines teaches the structure without the syntax
    fight, and on a touch keyboard it is the difference between an exercise
    someone does and one they skip.
    """
    return {"kind": "parsons", "q": q, "lines": lines, "why": why,
            "distractors": distractors or []}


def code(q, starter, expect, solution, why, plot=False, seconds=10):
    """Write it, run it, compare with what it should say."""
    return {"kind": "code", "q": q, "starter": starter, "expect": expect,
            "solution": solution, "why": why, "plot": plot,
            "seconds": seconds}


def lesson(ident, title, concepts, text, example, exercises, output="",
           formeln=None):
    # Die Herleitung haengt hinten an. Sie steht in herleitungen.py, damit
    # alle Formeln des Kurses an einer Stelle zu ueberblicken sind: Was
    # dort fehlt, hat im Kurs keine Begruendung.
    h = HERLEITUNGEN.get(ident)
    if h:
        text = text + "\n\n" + h
    # Die Erklaerung des Codebeispiels kommt als eigenes Feld. Sie an
    # den Text zu haengen wuerde dessen Schluessel aendern und damit
    # seine Uebersetzung entwerten; zusammengesetzt wird erst im
    # Erzeuger, nachdem beide ihr Sprachpaar haben.
    return {"id": ident, "title": title, "concepts": concepts, "text": text,
            "codeerklaerung": CODEERKLAERUNGEN.get(ident, ""),
            "example": example, "output": output, "exercises": exercises,
            "formeln": formeln or KURSFORMELN.get(ident, [])}


def chapter(ident, title, level, lang, blurb, lessons):
    return {"id": ident, "title": title, "level": level, "lang": lang,
            "blurb": blurb, "lessons": lessons}


# ---------------------------------------------------------------------------
# 1 -- C: Werte, Typen, Ausgabe
# ---------------------------------------------------------------------------

K1 = chapter("c-werte", "Werte und Typen", 1, "c",
             "Zahlen, Variablen, printf -- und die eine Falle, die in jeder "
             "Simulation steckt: Ganzzahlen teilen anders, als man denkt.", [

    lesson("l-erstes", "Das erste Programm", ["programmaufbau", "printf"],
        "Jedes C-Programm beginnt in `main`. Was `printf` bekommt, schreibt "
        "es auf den Bildschirm; `\\n` ist der Zeilenumbruch. Am Ende gibt "
        "`return 0;` zurück: alles in Ordnung.\n\n"
        "`#include <stdio.h>` holt die Deklaration von `printf` dazu. Ohne "
        "die Zeile kennt der Übersetzer den Namen nicht.\n\n"
        "**Warum `main`?** Das Betriebssystem muss wissen, wo es anfangen "
        "soll. Es sucht nach genau diesem Namen; heißt die Funktion anders, "
        "übersetzt das Programm zwar, aber es startet nicht. Der Rückgabewert "
        "geht zurück an die Umgebung, die das Programm aufgerufen hat: `0` "
        "heißt gut gegangen, alles andere ist eine Fehlernummer. In einer "
        "Rechenkette -- Netz erzeugen, lösen, auswerten -- entscheidet genau "
        "diese Zahl, ob der nächste Schritt überhaupt anläuft.\n\n"
        "**Was `#include` wirklich tut:** es kopiert den Inhalt der Datei an "
        "diese Stelle, bevor der Übersetzer überhaupt hinsieht. In `stdio.h` "
        "steht nicht der Programmtext von `printf`, sondern nur seine "
        "Beschreibung: wie es heißt, was es nimmt, was es zurückgibt. Der "
        "fertige Programmtext kommt erst beim Binden aus der C-Bibliothek "
        "dazu. Deshalb sind es zwei verschiedene Fehlermeldungen -- "
        "„unbekannter Name“ beim Übersetzen, „undefined reference“ beim "
        "Binden.\n\n"
        "**Die Falle:** die geschweiften Klammern begrenzen den Rumpf, der "
        "Strichpunkt beendet jede Anweisung. Ein vergessener Strichpunkt "
        "wird meist erst in der **nächsten** Zeile gemeldet -- wer die "
        "gemeldete Zeile anstarrt, sucht am falschen Ort.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    printf(\"Stroemung\\n\");\n"
        "    return 0;\n}\n",
        [
            predict("Was schreibt dieses Programm?",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    printf(\"a\");\n    printf(\"b\\n\");\n"
                    "    return 0;\n}\n",
                    "ab",
                    "`printf` bricht die Zeile nur um, wenn `\\n` darin "
                    "steht. Zwei Aufrufe ohne `\\n` schreiben also "
                    "hintereinander in dieselbe Zeile.\n\n"
                    "Das ist kein Schönheitsfehler: die Ausgabe wird "
                    "gesammelt und erst zeilenweise wirklich "
                    "hinausgeschrieben. Wer in einer langen Rechnung "
                    "den Fortschritt ohne `\\n` ausgibt, sieht "
                    "minutenlang gar nichts und hält das Programm für "
                    "hängengeblieben."),
            blank("Ergänze, damit das Programm `42` und einen Zeilenumbruch schreibt.",
                  "#include <stdio.h>\n\nint main()\n{\n"
                  "    printf(\"___\");\n    return 0;\n}\n",
                  ["42\\n"],
                  "Der Text in den Anführungszeichen geht unverändert hinaus, "
                  "`\\n` ist der Umbruch.\n\n"
                  "Der Rückstrich leitet eine Ersatzdarstellung ein: "
                  "`\\n` Umbruch, `\\t` Tabulator, `\\\\` der Rückstrich "
                  "selbst, `\\\"` das Anführungszeichen mitten im Text. "
                  "Man braucht sie, weil Umbruch und Anführungszeichen "
                  "sonst gar nicht in eine Zeichenkette hineinpassen."),
            code("Schreibe ein Programm, das `Hallo Simulation` in einer "
                 "eigenen Zeile ausgibt.",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    \n    return 0;\n}\n",
                 "Hallo Simulation",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    printf(\"Hallo Simulation\\n\");\n    return 0;\n}\n",
                 "Genau ein `printf` mit dem Text und `\\n` am Ende.\n\n"
                 "Der Text steht hier unmittelbar im Aufruf. Sobald "
                 "Zahlen dazukommen, wird daraus eine Vorlage mit "
                 "Platzhaltern -- das ist die nächste Lektion."),
        ],
        output="Stroemung\n"),

    lesson("l-variablen", "Variablen und Typen", ["typen", "deklaration"],
        "Eine Variable hat einen Typ. `int` ist eine ganze Zahl, `double` "
        "eine Fließkommazahl mit etwa 15 gültigen Stellen. In der Numerik ist "
        "`double` der Normalfall -- alles andere muss man begründen.\n\n"
        "Bei `printf` gehört zu jedem Typ ein Platzhalter: `%d` für `int`, "
        "`%f` für `double`. `%.3f` schreibt drei Nachkommastellen.\n\n"
        "**Was hinter den Typen steckt.** Ein `int` belegt auf diesem Gerät "
        "4 Byte und zählt von etwa -2,1 Milliarden bis +2,1 Milliarden. Ein "
        "`double` belegt 8 Byte und speichert die Zahl in zwei Teilen: eine "
        "Mantisse mit den Ziffern und einen Exponenten mit der "
        "Größenordnung. Daher die etwa 15 gültigen Stellen -- und daher "
        "auch, dass 0.1 nicht genau darstellbar ist, so wie 1/3 im "
        "Zehnersystem nicht aufgeht.\n\n"
        "**Warum in der Numerik `double` und nicht `float`.** Ein `float` "
        "hat nur etwa 7 Stellen. Nach zehntausend Zeitschritten, die jeder "
        "einen winzigen Rundungsfehler beisteuern, ist davon nichts mehr "
        "übrig, was man ein Ergebnis nennen möchte. Speicher spart man "
        "damit nur dort, wo Millionen Zellen gleichzeitig im Speicher "
        "liegen -- eine bewusste Entscheidung, keine Voreinstellung.\n\n"
        "**Der Name ist kein Typ.** `int schritte` sagt dem Übersetzer, wie "
        "viele Bytes er nehmen und wie er sie deuten soll. Dieselben Bytes "
        "als `double` gelesen ergeben eine völlig andere Zahl. Genau das "
        "passiert, wenn der Platzhalter nicht zum Typ passt: `printf` kennt "
        "die Typen nicht, es glaubt der Vorlage.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    int schritte = 100;\n"
        "    double dt = 0.01;\n\n"
        "    printf(\"%d Schritte zu je %.3f s\\n\", schritte, dt);\n"
        "    printf(\"Gesamtzeit: %.2f s\\n\", schritte * dt);\n"
        "    return 0;\n}\n",
        [
            mc("Welcher Platzhalter gehört zu einer `double`-Variablen?",
               ["%d", "%f", "%i", "%s"], 1,
               "`%d` ist für ganze Zahlen, `%s` für Text. Ein `double` mit "
               "`%d` auszugeben ist ein klassischer Fehler -- es kommt "
               "Unsinn heraus, und der Übersetzer sagt oft nichts.\n\n"
               "Der Grund: `printf` bekommt beliebig viele Werte und erfährt erst "
               "aus der Vorlage, wie es sie lesen soll. Steht dort `%d`, liest es "
               "vier Bytes als Ganzzahl -- auch wenn acht Bytes Fließkomma "
               "übergeben wurden. Danach ist es beim nächsten Platzhalter "
               "verrutscht, und der Rest der Zeile wird vollends unsinnig."),
            predict("Was kommt heraus?",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    double x = 2.0;\n"
                    "    double y = 3.0;\n"
                    "    printf(\"%.1f\\n\", x * y);\n"
                    "    return 0;\n}\n",
                    "6.0",
                    "`%.1f` schneidet auf eine Nachkommastelle.\n\n"
                    "Genauer: es rundet, es schneidet nicht ab -- aus 2.47 wird `2.5`. "
                    "Und es rundet nur die **Anzeige**. Im Speicher steht die Zahl "
                    "unverändert weiter; wer mit der angezeigten Zahl weiterrechnet "
                    "statt mit der gespeicherten, bekommt andere Ergebnisse als das "
                    "Programm."),
            code("Lege `double masse = 2.5;` und `double v = 4.0;` an und gib "
                 "die kinetische Energie `0.5*m*v*v` mit zwei Nachkommastellen aus.",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double masse = 2.5;\n"
                 "    double v = 4.0;\n\n"
                 "    \n    return 0;\n}\n",
                 "20.00",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double masse = 2.5;\n"
                 "    double v = 4.0;\n\n"
                 "    printf(\"%.2f\\n\", 0.5 * masse * v * v);\n"
                 "    return 0;\n}\n",
                 "0.5 * 2.5 * 16 = 20. Mit `%.2f` also `20.00`.\n\n"
                 "`v * v` statt einer Potenzfunktion ist Absicht: eine "
                 "Multiplikation kostet so gut wie nichts, `pow(v, 2)` ruft dagegen "
                 "eine Bibliotheksfunktion auf, die den allgemeinen Fall mit "
                 "Logarithmus und Exponent rechnet. In einer Zeitschleife über "
                 "Millionen Schritte ist das der Unterschied zwischen Sekunden und "
                 "Minuten."),
        ],
        output="100 Schritte zu je 0.010 s\nGesamtzeit: 1.00 s\n"),

    lesson("l-intdiv", "Die Ganzzahlfalle", ["intdiv", "typumwandlung"],
        "Das ist der Fehler, der in echten Simulationen am längsten "
        "unentdeckt bleibt: **teilt man zwei `int`, ist das Ergebnis wieder "
        "ein `int`** -- der Rest fällt weg, ohne Warnung.\n\n"
        "`7 / 2` ist also `3`, nicht `3.5`. Ein Gitterabstand `h = 1 / n` ist "
        "damit glatt `0`, und die ganze Rechnung ist tot, bevor sie anfängt.\n\n"
        "Heilmittel: einen der beiden zu `double` machen -- `(double)a / b` "
        "oder gleich `1.0 / n` schreiben.\n\n"
        "**Warum C das so macht.** Jeder Operator sieht sich seine beiden "
        "Operanden an und wählt danach die Rechenart. Zwei `int` heißt "
        "Ganzzahlrechnung, und die kennt keinen Bruch: 7/2 ist 3 Rest 1, "
        "und der Rest fällt weg (zu haben ist er mit `%`). Erst wenn **ein** "
        "Operand Fließkomma ist, wird der andere vorher umgewandelt. Das "
        "ist keine Nachlässigkeit der Sprache, sondern Absicht: "
        "Ganzzahlrechnung ist exakt und schnell.\n\n"
        "**Warum der Fehler so lange überlebt.** Er wirft keine Meldung. "
        "Das Programm läuft, die Kurve sieht plausibel aus, nur zu flach. "
        "Und er versteckt sich gern in Zwischenschritten: `dt = 1/100` ist "
        "null, `flaeche = breite/2 * hoehe` halbiert bei ungerader Breite "
        "falsch. Die Regel, die davor schützt: **in einer Formel, deren "
        "Ergebnis Fließkomma sein soll, steht keine nackte ganze Zahl in "
        "einer Division** -- also `1.0`, `2.0`, `0.5` schreiben.\n\n"
        "**Die Umwandlung genau genommen.** `(double)a / b` wandelt nur `a` "
        "um; die Division ist danach Fließkomma und zieht `b` mit. "
        "`(double)(a / b)` dagegen dividiert erst ganzzahlig und wandelt "
        "das falsche Ergebnis um -- dieselbe Falle, nur mit Klammern "
        "getarnt.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    int n = 4;\n\n"
        "    printf(\"falsch: %f\\n\", 1 / n);\n"
        "    printf(\"richtig: %f\\n\", 1.0 / n);\n"
        "    return 0;\n}\n",
        [
            predict("Was schreibt das Programm? Überlege genau.",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    int a = 7;\n"
                    "    int b = 2;\n"
                    "    printf(\"%d\\n\", a / b);\n"
                    "    printf(\"%.3f\\n\", (double)a / b);\n"
                    "    return 0;\n}\n",
                    "3\n3.500",
                    "`a / b` sind zwei `int`, also Ganzzahldivision: 3. Erst "
                    "`(double)a` zwingt die Rechnung ins Fließkomma.\n\n"
                    "Beide Zeilen benutzen dieselben Variablen: es liegt nicht an den "
                    "Werten, sondern allein an den Typen im Ausdruck. Wer `7 / 2` im "
                    "Kopf rechnet, kommt auf 3.5 -- C rechnet hier nicht in Mathematik, "
                    "sondern in Maschinenwerten."),
            mc("Ein Gitter der Länge 1 hat `int n = 10;` Zellen. Welche Zeile "
               "berechnet den Zellabstand `h` richtig?",
               ["double h = 1 / n;", "double h = 1.0 / n;",
                "int h = 1 / n;", "double h = (1 / n) * 1.0;"], 1,
               "Nur `1.0 / n` rechnet von Anfang an im Fließkomma. Die "
               "vierte Zeile ist besonders tückisch: `1 / n` ist schon `0`, "
               "bevor irgendetwas mit `1.0` multipliziert wird.\n\n"
               "Die Zuweisung an ein `double` kommt immer zu spät: sie wandelt um, "
               "was der Ausdruck ergeben hat, und der ist da schon fertig "
               "gerechnet. Merksatz: **der Typ des Ergebnisses entsteht im "
               "Ausdruck, nicht bei der Zuweisung.**"),
            code("Das Programm soll den Mittelwert von `summe` und `anzahl` "
                 "als Fließkommazahl mit drei Stellen ausgeben. Repariere es.",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    int summe = 7;\n"
                 "    int anzahl = 2;\n\n"
                 "    printf(\"%.3f\\n\", summe / anzahl);\n"
                 "    return 0;\n}\n",
                 "3.500",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    int summe = 7;\n"
                 "    int anzahl = 2;\n\n"
                 "    printf(\"%.3f\\n\", (double)summe / anzahl);\n"
                 "    return 0;\n}\n",
                 "Eine Umwandlung genügt: sobald ein Operand `double` ist, "
                 "rechnet C die ganze Division im Fließkomma.\n\n"
                 "Genauso gut geht `summe * 1.0 / anzahl` oder gleich "
                 "`double`-Variablen. Was **nicht** genügt: den Platzhalter auf "
                 "`%.3f` zu setzen. Er beschreibt nur die Ausgabe -- gerechnet wurde "
                 "da längst falsch, und `%.3f` auf einer Ganzzahl gibt obendrein "
                 "Unsinn aus."),
        ],
        output="falsch: 0.000000\nrichtig: 0.250000\n"),
])


# ---------------------------------------------------------------------------
# 2 -- C: Schleifen und Verzweigungen
# ---------------------------------------------------------------------------

K2 = chapter("c-fluss", "Schleifen und Verzweigungen", 2, "c",
             "Die Zeitschleife ist das Herz jeder Simulation. Hier wird sie "
             "gebaut -- und zum ersten Mal etwas ausgerechnet, das man "
             "nachprüfen kann.", [

    lesson("l-if", "Verzweigen", ["if", "vergleich"],
        "`if` führt etwas nur aus, wenn die Bedingung zutrifft, `else` sonst. "
        "Verglichen wird mit `==`, `!=`, `<`, `<=`, `>`, `>=`.\n\n"
        "Die häufigste Verwechslung: `=` weist zu, `==` vergleicht. "
        "`if (x = 3)` ist gültiges C und tut etwas ganz anderes als gemeint.\n\n"
        "**Was eine Bedingung in C ist.** Es gibt keinen eigenen "
        "Wahrheitstyp: ein Vergleich liefert `1` oder `0`, und `if` führt "
        "aus, sobald der Wert **nicht null** ist. Deshalb ist `if (x = 3)` "
        "erlaubt -- die Zuweisung liefert 3, und 3 ist nicht null, also "
        "trifft die Bedingung immer zu, und `x` ist nebenbei überschrieben. "
        "Ein Schutz dagegen: die Konstante nach links schreiben, `if (3 == "
        "x)`. Ein Tippfehler wird dann zum Fehler beim Übersetzen.\n\n"
        "**Fließkomma vergleicht man nicht mit `==`.** `0.1 + 0.2 == 0.3` "
        "ist falsch, weil keine der drei Zahlen exakt gespeichert ist. In "
        "der Numerik prüft man deshalb auf einen Abstand: `if (fabs(a - b) "
        "< 1e-9)`. Dieselbe Regel gilt für Abbruchbedingungen -- eine "
        "Zeitschleife läuft bis `t < ende - 1e-12`, nicht bis `t != ende`.\n\n"
        "**Klammern auch bei einer Zeile.** `if (x > 0) a = 1; b = 2;` "
        "sieht aus, als gehörten beide Zuweisungen zur Bedingung. `b = 2;` "
        "läuft aber immer. Geschweifte Klammern kosten nichts und sparen "
        "genau diesen Fehler.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    double cfl = 0.7;\n\n"
        "    if (cfl <= 0.5) {\n"
        "        printf(\"stabil\\n\");\n"
        "    } else {\n"
        "        printf(\"zu grosser Zeitschritt\\n\");\n"
        "    }\n"
        "    return 0;\n}\n",
        [
            predict("Was kommt heraus?",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    int n = 5;\n"
                    "    if (n > 3) printf(\"gross\\n\");\n"
                    "    if (n > 10) printf(\"riesig\\n\");\n"
                    "    return 0;\n}\n",
                    "gross",
                    "Die zweite Bedingung trifft nicht zu, also passiert dort "
                    "nichts. Ohne `else` sind das zwei unabhängige Prüfungen.\n\n"
                    "Mit `else if` wäre es eine Kette, in der nach dem ersten Treffer "
                    "nichts mehr geprüft wird. Beides ist richtig -- nur eben "
                    "verschieden. Bei sich überschneidenden Bereichen (`n > 3`, `n > "
                    "10`) trifft ohne `else` mehr als ein Zweig zu."),
            mc("Welche Zeile prüft, ob `x` gleich 2 ist?",
               ["if (x = 2)", "if (x == 2)", "if (x := 2)", "if (x eq 2)"], 1,
               "`=` weist zu und liefert den zugewiesenen Wert -- `if (x = 2)` "
               "ist deshalb immer wahr und verändert obendrein `x`.\n\n"
               "`:=` gibt es in C nicht, `eq` auch nicht -- das sind Schreibweisen "
               "aus Pascal beziehungsweise aus Shell-Skripten. Übersetzer melden "
               "die Verwechslung von `=` und `==` heute oft als Warnung; sie "
               "einzuschalten (`-Wall`) und ernst zu nehmen, ist die eigentliche "
               "Lehre aus dieser Aufgabe."),
        ],
        output="zu grosser Zeitschritt\n"),

    lesson("l-for", "Die Zeitschleife", ["for", "akkumulator"],
        "`for (int i = 0; i < n; i++)` heißt: fang bei 0 an, laufe solange "
        "`i < n`, zähle danach eins hoch. Der Rumpf läuft damit genau `n` mal, "
        "mit `i` von `0` bis `n-1`.\n\n"
        "Fast jede Simulation ist eine solche Schleife über die Zeit, in der "
        "eine Größe schrittweise fortgeschrieben wird. Man nennt die Variable, "
        "die dabei anwächst, einen Akkumulator.\n\n"
        "**Die drei Teile im Kopf der Schleife** laufen zu verschiedenen "
        "Zeiten: `i = 0` einmal am Anfang; `i < n` vor **jedem** Durchlauf, "
        "auch vor dem ersten; `i++` nach jedem Durchlauf. Daraus folgt, "
        "dass der Rumpf null mal laufen kann -- bei `n = 0` prüft die "
        "Schleife einmal und ist fertig. Programme, die stillschweigend "
        "mindestens einen Durchlauf annehmen, fallen genau hier um.\n\n"
        "**Warum von 0 gezählt wird.** Weil Feldindizes bei 0 anfangen: "
        "`for (i = 0; i < n; i++)` besucht `a[0]` bis `a[n-1]`, also genau "
        "die n vorhandenen Zellen. Die Schreibweise `i <= n` ist der "
        "häufigste Weg, einen Schritt zu weit zu gehen -- in einem Feld ist "
        "das der Zugriff hinter das Ende.\n\n"
        "**Der Akkumulator muss vor der Schleife stehen und gesetzt sein.** "
        "Eine Variable, die nur angelegt und nicht besetzt wird, enthält in "
        "C das, was zufällig im Speicher lag. Die Summe wäre dann bei jedem "
        "Start eine andere -- ein Fehler, der sich als „läuft meistens“ "
        "tarnt.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    double t = 0.0;\n"
        "    double dt = 0.25;\n"
        "    int i;\n\n"
        "    for (i = 0; i < 4; i++) {\n"
        "        t = t + dt;\n"
        "        printf(\"Schritt %d, t = %.2f\\n\", i, t);\n"
        "    }\n"
        "    return 0;\n}\n",
        [
            predict("Wie viele Zeilen schreibt diese Schleife, und was steht "
                    "in der letzten?",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    int i;\n"
                    "    for (i = 0; i < 3; i++) printf(\"%d\\n\", i * i);\n"
                    "    return 0;\n}\n",
                    "0\n1\n4",
                    "Drei Durchläufe mit `i` = 0, 1, 2 -- nicht 3. Der "
                    "Abbruch `i < 3` wird geprüft, **bevor** der Rumpf läuft.\n\n"
                    "Die Quadratzahlen sind 0, 1, 4 -- nicht 1, 4, 9. Wer die Grenze "
                    "als „bis 3“ liest, verschiebt die ganze Reihe. Das ist derselbe "
                    "Denkfehler, der bei Feldern zum Zugriff hinter das Ende führt."),
            parsons("Setze eine Schleife zusammen, die die Zahlen 1 bis 5 "
                    "aufsummiert und die Summe ausgibt.",
                    ["int summe = 0;",
                     "int i;",
                     "for (i = 1; i <= 5; i++) {",
                     "    summe = summe + i;",
                     "}",
                     "printf(\"%d\\n\", summe);"],
                    "Erst den Akkumulator auf 0 setzen, dann in jedem "
                    "Durchlauf dazuzählen, und **nach** der Schleife ausgeben. "
                    "Steht die Ausgabe im Rumpf, kommen fünf Zeilen statt einer.\n\n"
                    "Der Ablauf, den die Zeilen abbilden, ist immer derselbe: "
                    "vorbereiten, in der Schleife fortschreiben, danach auswerten. In "
                    "einer Simulation stehen an denselben drei Stellen das Anfangsfeld, "
                    "der Zeitschritt und die Auswertung -- diese Aufgabe ist das "
                    "Gerüst, in das später Physik kommt.",
                    distractors=["summe = summe + 1;",
                                 "for (i = 1; i < 5; i++) {"]),
            code("Berechne mit einer Schleife die Summe 1/1 + 1/2 + ... + 1/10 "
                 "und gib sie mit vier Nachkommastellen aus.",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double summe = 0.0;\n"
                 "    int i;\n\n"
                 "    \n"
                 "    printf(\"%.4f\\n\", summe);\n"
                 "    return 0;\n}\n",
                 "2.9290",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double summe = 0.0;\n"
                 "    int i;\n\n"
                 "    for (i = 1; i <= 10; i++) summe = summe + 1.0 / i;\n"
                 "    printf(\"%.4f\\n\", summe);\n"
                 "    return 0;\n}\n",
                 "Wichtig ist `1.0 / i` statt `1 / i` -- sonst schlägt die "
                 "Ganzzahlfalle zu und die Summe bleibt 1.\n\n"
                 "Genauer: `1 / i` ist für jedes `i > 1` null, nur der erste Term "
                 "trägt bei. Nebenbei ist das die harmonische Reihe -- sie wächst "
                 "immer weiter, aber unerträglich langsam (für 100 braucht man etwa "
                 "10^43 Glieder). Wer Summen in Fließkomma bildet, addiert übrigens "
                 "am besten von klein nach groß: sonst verschluckt der große "
                 "Zwischenwert die kleinen Beiträge."),
        ],
        output="Schritt 0, t = 0.25\nSchritt 1, t = 0.50\n"
               "Schritt 2, t = 0.75\nSchritt 3, t = 1.00\n"),
])


# ---------------------------------------------------------------------------
# 3 -- C: Bewegung integrieren
# ---------------------------------------------------------------------------

K3 = chapter("c-bewegung", "Bewegung integrieren", 3, "c",
             "Der erste echte Simulationsschritt. Hier zeigt sich, dass die "
             "Wahl des Verfahrens keine Geschmacksfrage ist: dieselbe Feder, "
             "dieselbe Schrittweite, zwei vertauschte Zeilen -- und einmal "
             "läuft die Energie davon.", [

    lesson("l-euler", "Explizites Euler-Verfahren", ["euler", "zeitschritt"],
        "Eine Bewegung ist durch die Beschleunigung gegeben: `a = F/m`. "
        "Gesucht sind Ort und Geschwindigkeit über die Zeit.\n\n"
        "Das naheliegendste Verfahren nimmt an, dass sich während eines "
        "kleinen Schritts `dt` nichts ändert, und schreibt **beide** Größen "
        "aus den alten Werten fort:\n\n"
        "    x_neu = x + v*dt\n"
        "    v_neu = v + a*dt\n\n"
        "Das heißt explizites Euler-Verfahren. Es ist leicht zu schreiben "
        "und für eine Schwingung still falsch: die Energie wächst mit jedem "
        "Schritt. Die Feder startet mit E = 0.5 -- sieh nach, wo sie endet.\n\n"
        "Gezeichnet wird durch Ausgeben: jede Zeile, die mit `plot` beginnt, "
        "wird zu einem Punkt einer Kurve statt zu Text.\n\n"
        "**Woher das Verfahren kommt.** Die Ableitung ist der Grenzwert des "
        "Differenzenquotienten. Lässt man den Grenzübergang weg und nimmt "
        "ein endliches `dt`, steht da `x(t+dt) ≈ x(t) + v(t)·dt`. Das ist "
        "alles. Der Fehler je Schritt ist von der Ordnung `dt²`; über die "
        "`1/dt` Schritte einer festen Zeitspanne bleibt `dt` übrig -- "
        "deshalb heißt das Verfahren von erster Ordnung: halbe "
        "Schrittweite, halber Fehler.\n\n"
        "**Warum gerade eine Schwingung das aufdeckt.** Bei einer Feder "
        "zeigt die Beschleunigung immer zur Ruhelage. Euler rechnet den "
        "ganzen Schritt mit der Beschleunigung vom **Anfang** des Schritts, "
        "die für den durchlaufenen Bogen zu klein ist. Jeder Schritt setzt "
        "den Punkt ein Stückchen zu weit außen ab, und weil das in jeder "
        "Schwingung zweimal geschieht, wächst die Bahn spiralförmig an. Der "
        "Fehler mittelt sich nicht heraus, er summiert sich.\n\n"
        "**Die Reihenfolge der Zuweisungen ist das Verfahren.** Deshalb "
        "steht im Beispiel `xn` als Zwischenwert: `x` darf erst überschrieben "
        "werden, wenn `v` mit dem alten `x` gerechnet ist. Wer den "
        "Zwischenwert weglässt, hat unbemerkt ein anderes Verfahren "
        "programmiert -- was in der übernächsten Aufgabe ausgerechnet der "
        "bessere Fall ist, aber eben nicht als Zufall.\n\n"
        "**Gezeichnet statt gedruckt:** `plot t x` schreibt einen Punkt, "
        "`plot name t x` mehrere Kurven in ein Bild. Die Zeilen sind "
        "gewöhnliche Ausgaben -- dasselbe Programm liefert auf einem "
        "Rechner ohne Zeichenfläche einfach Zahlen.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    double x = 1.0;\n"
        "    double v = 0.0;\n"
        "    double dt = 0.05;\n"
        "    double t = 0.0;\n"
        "    double a, xn;\n"
        "    int i;\n\n"
        "    for (i = 0; i < 400; i++) {\n"
        "        a = -x;              /* Feder: F = -k*x, k = 1, m = 1 */\n"
        "        xn = x + v * dt;     /* beide aus den ALTEN Werten */\n"
        "        v  = v + a * dt;\n"
        "        x  = xn;\n"
        "        t  = t + dt;\n"
        "        printf(\"plot %.3f %.5f\\n\", t, x);\n"
        "    }\n"
        "    printf(\"Energie am Ende: %.4f\\n\", 0.5*v*v + 0.5*x*x);\n"
        "    return 0;\n}\n",
        [
            mc("Die Energie startet bei 0.5 und steht am Ende bei 1.3574. "
               "Was bedeutet das?",
               ["Die Feder wird von selbst immer schneller -- physikalisch "
                "unmöglich.",
                "Das ist die richtige Lösung, Federn verhalten sich so.",
                "Die Energie schwankt nur zufällig hin und her.",
                "Im Programm steht ein Tippfehler."], 0,
               "Eine reibungsfreie Feder erhält ihre Energie exakt. Was hier "
               "wächst, ist kein Effekt der Physik, sondern der Fehler des "
               "Verfahrens: explizites Euler pumpt bei jeder Schwingung "
               "Energie hinein. Über lange Zeiten fliegt so eine Simulation "
               "auseinander.\n\n"
               "Ein Prüfstein, der in jede Simulation gehört: eine Größe "
               "mitrechnen, die sich physikalisch nicht ändern darf -- Energie, "
               "Masse, Impuls, Teilchenzahl. Läuft sie weg, ist das Verfahren "
               "schuld, nicht die Natur. Diese eine Zeile hätte schon manchem "
               "Ergebnis widersprochen, bevor es in einem Bericht stand."),
            code("Der übliche erste Reflex: Zeitschritt verkleinern. Nimm "
                 "`dt = 0.005` und dafür 4000 Schritte, damit dieselbe Zeit "
                 "simuliert wird. Gib die Energie mit vier Stellen aus.",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double x = 1.0;\n"
                 "    double v = 0.0;\n"
                 "    double dt = 0.05;\n"
                 "    double a, xn;\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 400; i++) {\n"
                 "        a = -x;\n"
                 "        xn = x + v * dt;\n"
                 "        v  = v + a * dt;\n"
                 "        x  = xn;\n"
                 "    }\n"
                 "    printf(\"%.4f\\n\", 0.5*v*v + 0.5*x*x);\n"
                 "    return 0;\n}\n",
                 "0.5526",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double x = 1.0;\n"
                 "    double v = 0.0;\n"
                 "    double dt = 0.005;\n"
                 "    double a, xn;\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 4000; i++) {\n"
                 "        a = -x;\n"
                 "        xn = x + v * dt;\n"
                 "        v  = v + a * dt;\n"
                 "        x  = xn;\n"
                 "    }\n"
                 "    printf(\"%.4f\\n\", 0.5*v*v + 0.5*x*x);\n"
                 "    return 0;\n}\n",
                 "Von 1.3574 auf 0.5526 -- besser, aber immer noch falsch, "
                 "und für zehnmal so viel Rechenzeit. Der Fehler wird nur "
                 "langsamer, er verschwindet nicht. Die nächste Aufgabe "
                 "kostet dagegen gar nichts.\n\n"
                 "Zehnmal kleiner ist auch zehnmal mehr Rundung: irgendwann macht "
                 "ein noch kleinerer Schritt das Ergebnis wieder schlechter, weil "
                 "die vielen winzigen Additionen ihre eigene Ungenauigkeit "
                 "mitbringen. Ein schlechtes Verfahren lässt sich nicht mit "
                 "Rechenzeit reparieren -- man wechselt das Verfahren.",
                 seconds=25),
            code("Jetzt der Trick: rechne `v` **zuerst** aus und benutze für "
                 "`x` schon das neue `v`. Also `v = v + a*dt;` und in der "
                 "Zeile darunter `x = x + v*dt;`. Sonst alles wie im "
                 "Beispiel, `dt = 0.05`, 400 Schritte.",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double x = 1.0;\n"
                 "    double v = 0.0;\n"
                 "    double dt = 0.05;\n"
                 "    double a;\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 400; i++) {\n"
                 "        a = -x;\n"
                 "        \n"
                 "        \n"
                 "    }\n"
                 "    printf(\"%.4f\\n\", 0.5*v*v + 0.5*x*x);\n"
                 "    return 0;\n}\n",
                 "0.4912",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double x = 1.0;\n"
                 "    double v = 0.0;\n"
                 "    double dt = 0.05;\n"
                 "    double a;\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 400; i++) {\n"
                 "        a = -x;\n"
                 "        v = v + a * dt;\n"
                 "        x = x + v * dt;\n"
                 "    }\n"
                 "    printf(\"%.4f\\n\", 0.5*v*v + 0.5*x*x);\n"
                 "    return 0;\n}\n",
                 "0.4912 statt 1.3574 -- bei gleicher Schrittweite und "
                 "gleicher Rechenzeit. Zwei vertauschte Zeilen. Das ist das "
                 "**symplektische Euler-Verfahren**, und der Unterschied ist "
                 "kein Zufall: es erhält eine Größe, die nahe an der Energie "
                 "liegt, deshalb kann die Energie nicht davonlaufen. Wer "
                 "diese Verwechslung kennt, hat den häufigsten Anfängerfehler "
                 "der Simulationsprogrammierung schon hinter sich.\n\n"
                 "Symplektisch heißt: das Verfahren erhält das Phasenraumvolumen. "
                 "Für die Praxis genügt die Folge davon -- die Energie schwankt um "
                 "einen festen Wert, statt fortzulaufen. Molekulardynamik und "
                 "Himmelsmechanik rechnen deshalb grundsätzlich mit solchen "
                 "Verfahren; ein genaueres, aber nicht symplektisches Runge-Kutta "
                 "wäre über Millionen Umläufe schlechter.",
                 seconds=25),
        ],
        output="Energie am Ende: 1.3574\n"),

    lesson("l-verlet", "Velocity-Verlet", ["verlet", "energieerhaltung"],
        "Velocity-Verlet benutzt die Beschleunigung an **beiden** Enden des "
        "Schritts:\n\n"
        "    x = x + v*dt + 0.5*a*dt*dt\n"
        "    a_neu = kraft(x)\n"
        "    v = v + 0.5*(a + a_neu)*dt\n"
        "    a = a_neu\n\n"
        "Das kostet kaum mehr als symplektisches Euler, ist aber eine "
        "Ordnung genauer: der Ort stimmt nach `dt^2` statt nach `dt`. Wie "
        "das symplektische Euler driftet auch hier die Energie nicht weg -- "
        "auch nach Millionen Schritten nicht. Deshalb rechnet die "
        "Molekulardynamik seit Jahrzehnten damit.\n\n"
        "Zwei Kurven im selben Bild: `plot euler t x` und `plot verlet t x` "
        "zeichnen getrennt.\n\n"
        "**Warum die Mittelung hilft.** Der Ortsschritt benutzt zusätzlich "
        "den Term `0.5·a·dt²` -- also die Krümmung der Bahn, nicht nur ihre "
        "Steigung. Und die Geschwindigkeit nimmt den Mittelwert der "
        "Beschleunigung an beiden Enden des Schritts. Beides zusammen hebt "
        "die Fehler erster Ordnung gegeneinander auf; übrig bleibt `dt²`.\n\n"
        "**Eine Kraftauswertung je Schritt.** Das ist der Grund, warum "
        "Verlet in der Molekulardynamik alles andere verdrängt hat: `an` "
        "des einen Schritts ist `a` des nächsten. Die Kraftberechnung ist "
        "bei tausend Teilchen der ganze Rechenaufwand -- ein Verfahren, das "
        "sie viermal braucht (Runge-Kutta 4), muss viermal besser sein, um "
        "sich zu lohnen.\n\n"
        "**Was Verlet nicht kann.** Reibung, also Kräfte, die von der "
        "Geschwindigkeit abhängen, passen nicht sauber in das Schema -- die "
        "Geschwindigkeit am Ende des Schritts wird ja erst daraus "
        "berechnet. Dafür gibt es eigene Varianten. Und genauer als `dt²` "
        "wird es nicht: wer sechs Stellen braucht, nimmt ein Verfahren "
        "höherer Ordnung und bezahlt es mit Kraftauswertungen.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    double x = 1.0;\n"
        "    double v = 0.0;\n"
        "    double dt = 0.05;\n"
        "    double t = 0.0;\n"
        "    double a = -1.0;\n"
        "    double an;\n"
        "    int i;\n\n"
        "    for (i = 0; i < 400; i++) {\n"
        "        x = x + v * dt + 0.5 * a * dt * dt;\n"
        "        an = -x;\n"
        "        v = v + 0.5 * (a + an) * dt;\n"
        "        a = an;\n"
        "        t = t + dt;\n"
        "        printf(\"plot verlet %.3f %.5f\\n\", t, x);\n"
        "    }\n"
        "    printf(\"Energie am Ende: %.4f\\n\", 0.5*v*v + 0.5*x*x);\n"
        "    return 0;\n}\n",
        [
            predict("Die Energie startet bei 0.5000. Was steht nach 400 "
                    "Verlet-Schritten da? Vier Nachkommastellen.",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    double x = 1.0;\n"
                    "    double v = 0.0;\n"
                    "    double dt = 0.05;\n"
                    "    double a = -1.0;\n"
                    "    double an;\n"
                    "    int i;\n\n"
                    "    for (i = 0; i < 400; i++) {\n"
                    "        x = x + v * dt + 0.5 * a * dt * dt;\n"
                    "        an = -x;\n"
                    "        v = v + 0.5 * (a + an) * dt;\n"
                    "        a = an;\n"
                    "    }\n"
                    "    printf(\"%.4f\\n\", 0.5*v*v + 0.5*x*x);\n"
                    "    return 0;\n}\n",
                    "0.4997",
                    "Praktisch unverändert -- und näher an 0.5 als die "
                    "0.4912 des symplektischen Euler. Gleiche Schrittweite, "
                    "gleiche Rechenzeit wie der explizite Lauf, der die "
                    "Energie fast verdreifacht hat.\n\n"
                    "Dass es nicht exakt 0.5000 ist, gehört dazu: die Energie schwankt "
                    "bei Verlet um den richtigen Wert, mit einer Schwankung von der "
                    "Größe `dt²`. Entscheidend ist, dass sie nicht **wandert**. Über "
                    "eine Million Schritte sieht man denselben schmalen Streifen wie "
                    "nach zehn."),
            parsons("Setze den Rumpf eines Velocity-Verlet-Schritts in die "
                    "richtige Reihenfolge.",
                    ["x = x + v * dt + 0.5 * a * dt * dt;",
                     "an = -x;",
                     "v = v + 0.5 * (a + an) * dt;",
                     "a = an;"],
                    "Erst der Ort mit der **alten** Beschleunigung, dann die "
                    "neue Beschleunigung am neuen Ort, dann die "
                    "Geschwindigkeit aus dem Mittel beider. Wer `a = an;` zu "
                    "früh setzt, mittelt zweimal dieselbe Zahl und rechnet "
                    "wieder Euler.\n\n"
                    "Wer das Programm später umbaut, stolpert genau hier: die vier "
                    "Zeilen sehen austauschbar aus. Eine Zeile Kommentar über dem "
                    "Block -- „alte Beschleunigung für den Ort, neue für die halbe "
                    "Geschwindigkeit“ -- ist an dieser Stelle mehr wert als anderswo "
                    "zehn.",
                    distractors=["v = v + a * dt;"]),
            code("Lass beide Verfahren im selben Programm laufen -- "
                 "explizites Euler und Verlet -- und zeichne beide mit "
                 "`plot euler t xe` und `plot verlet t xv`. Gib am Ende beide "
                 "Energien in einer Zeile aus, Euler zuerst, vier Stellen.",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double xe = 1.0;\n"
                 "    double ve = 0.0;\n"
                 "    double xv = 1.0;\n"
                 "    double vv = 0.0;\n"
                 "    double dt = 0.05;\n"
                 "    double t = 0.0;\n"
                 "    double av = -1.0;\n"
                 "    double ae, an, xn;\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 400; i++) {\n"
                 "        /* explizites Euler auf xe, ve */\n"
                 "        \n"
                 "        /* Verlet auf xv, vv, av */\n"
                 "        \n"
                 "        t = t + dt;\n"
                 "    }\n"
                 "    printf(\"%.4f %.4f\\n\", 0.5*ve*ve + 0.5*xe*xe,\n"
                 "                             0.5*vv*vv + 0.5*xv*xv);\n"
                 "    return 0;\n}\n",
                 "1.3574 0.4997",
                 "#include <stdio.h>\n\nint main()\n{\n"
                 "    double xe = 1.0;\n"
                 "    double ve = 0.0;\n"
                 "    double xv = 1.0;\n"
                 "    double vv = 0.0;\n"
                 "    double dt = 0.05;\n"
                 "    double t = 0.0;\n"
                 "    double av = -1.0;\n"
                 "    double ae, an, xn;\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 400; i++) {\n"
                 "        ae = -xe;\n"
                 "        xn = xe + ve * dt;\n"
                 "        ve = ve + ae * dt;\n"
                 "        xe = xn;\n"
                 "        xv = xv + vv * dt + 0.5 * av * dt * dt;\n"
                 "        an = -xv;\n"
                 "        vv = vv + 0.5 * (av + an) * dt;\n"
                 "        av = an;\n"
                 "        t = t + dt;\n"
                 "        printf(\"plot euler %.3f %.5f\\n\", t, xe);\n"
                 "        printf(\"plot verlet %.3f %.5f\\n\", t, xv);\n"
                 "    }\n"
                 "    printf(\"%.4f %.4f\\n\", 0.5*ve*ve + 0.5*xe*xe,\n"
                 "                             0.5*vv*vv + 0.5*xv*xv);\n"
                 "    return 0;\n}\n",
                 "Im Bild wächst die Euler-Kurve sichtbar über ihre "
                 "Anfangsamplitude hinaus, während Verlet auf seiner Bahn "
                 "bleibt. Das ist der Unterschied zwischen einer Simulation, "
                 "der man über lange Zeiten glauben darf, und einer, der man "
                 "nicht glauben darf.\n\n"
                 "Zwei Verfahren nebeneinander laufen zu lassen ist ein Werkzeug, "
                 "kein Schulbeispiel: Wenn zwei unabhängige Verfahren dasselbe "
                 "sagen, ist das Ergebnis vermutlich in Ordnung; laufen sie "
                 "auseinander, weiß man wenigstens, dass etwas nicht stimmt. In der "
                 "Praxis vergleicht man außerdem dieselbe Rechnung mit halber "
                 "Schrittweite -- ändert sich das Ergebnis, war die Schrittweite zu "
                 "groß.",
                 plot=True, seconds=30),
        ],
        output="Energie am Ende: 0.4997\n"),
])


# ---------------------------------------------------------------------------
# 4 -- C++: was es gegenueber C bringt
# ---------------------------------------------------------------------------
#
# C++ hat auf diesem Geraet keinen Interpreter, also wird hier gelesen und
# vorhergesagt statt ausgefuehrt. Das ist kein Notbehelf: den groessten Teil
# seiner Zeit verbringt man mit fremdem C++ ohnehin lesend, und ein
# "Ausfuehren"-Knopf, hinter dem nichts laeuft, waere eine Luege.

K4 = chapter("cpp-grund", "C++: was es bringt", 8, "cpp",
             "Warum Strömungslöser wie OpenFOAM und SU2 in C++ geschrieben "
             "sind und nicht in C. Drei Dinge machen den Unterschied: "
             "Referenzen, Container, die sich selbst aufräumen, und "
             "Templates.", [

    lesson("cpp-ref", "Referenzen statt Zeiger", ["referenz", "constref"],
        "Eine **Referenz** ist ein zweiter Name für dasselbe Objekt. Kein "
        "Zeiger, keine Kopie, keine Sternchen:\n\n"
        "    void schritt(Feld& f);      // f ist das Original\n"
        "    void lesen(const Feld& f);  // ... und wird nicht verändert\n\n"
        "Das `const&` ist in der Numerik der wichtigste Handgriff überhaupt. "
        "Ein Gitterfeld als Wert zu übergeben kopiert bei jedem Aufruf "
        "Megabyte:\n\n"
        "    double summe(std::vector<double> v);        // kopiert alles\n"
        "    double summe(const std::vector<double>& v); // kopiert nichts\n\n"
        "Die zweite Fassung übergibt nichts und verspricht zugleich, nichts "
        "zu ändern — der Übersetzer hält das nach.\n\n"
        "In C ginge dasselbe mit `const double *v` plus Länge. C++ nimmt "
        "einem das Mitführen der Länge ab und die Möglichkeit, aus Versehen "
        "`NULL` zu übergeben: eine Referenz kann nicht leer sein.\n\n"
        "**Was der Übersetzer daraus macht.** Eine Referenz ist zur "
        "Laufzeit meist eine Adresse, genau wie ein Zeiger -- der "
        "Unterschied liegt in dem, was die Sprache zusichert: sie zeigt "
        "immer auf ein gültiges Objekt und lässt sich nicht umhängen. Man "
        "bezahlt nichts für die Sicherheit; es ist derselbe Maschinenbefehl "
        "mit besseren Regeln.\n\n"
        "**`const` ist zweierlei.** Für den Leser eine Zusage („diese "
        "Funktion verändert mein Gitter nicht“), für den Übersetzer eine "
        "Prüfung: jeder Schreibversuch ist ein Fehler. In großen Lösern ist "
        "`const` das Mittel, mit dem man aus einer Signatur ablesen kann, "
        "was ein Rechenschritt anfasst -- ohne den Rumpf zu lesen.\n\n"
        "**Die Falle:** eine Referenz auf etwas zurückgeben, das beim "
        "Verlassen der Funktion verschwindet. `const Feld& machen() { Feld "
        "f; return f; }` übersetzt anstandslos und zeigt danach auf "
        "Speicher, der nicht mehr da ist. Zurückgegeben wird ein Wert -- "
        "Referenzen zeigen nach **innen**, nicht nach außen.",
        "",
        [
            mc("Was bewirkt das `&` in `void schritt(Feld& f)`?",
               ["Es übergibt eine Kopie des Feldes.",
                "Es übergibt das Original; Änderungen bleiben erhalten.",
                "Es übergibt die Adresse als Zahl.",
                "Es ist nur Dokumentation."], 1,
               "Eine Referenz ist ein anderer Name für dasselbe Objekt — ohne "
               "Kopie und ohne Zeigersyntax. Ändert die Funktion `f`, ändert "
               "sie das Original des Aufrufers.\n\n"
               "In der Aufrufstelle sieht man das übrigens **nicht**: `schritt(f)` "
               "sieht aus wie eine Übergabe per Wert. Deshalb die Gewohnheit, "
               "verändernde Parameter entweder als Referenz **ohne** `const` ganz "
               "vorn zu führen oder gleich einen Zeiger zu nehmen, wo die Aufrufstelle das `&` zeigen soll."),
            mc("Warum nimmt man in einem Strömungslöser "
               "`const std::vector<double>&` statt `std::vector<double>`?",
               ["Damit der Vektor schneller wächst.",
                "Um die Kopie des ganzen Gitterfeldes zu vermeiden.",
                "Weil vector sonst nicht übergeben werden kann.",
                "Damit er automatisch freigegeben wird."], 1,
               "Bei einer Million Zellen sind das 8 MB je Aufruf. In einer "
               "Zeitschleife, die millionenfach aufruft, ist das der "
               "Unterschied zwischen Sekunden und Stunden.\n\n"
               "Die Kopie entsteht still: kein Stern, kein `copy`, nur ein "
               "fehlendes `&`. Genau deshalb steht in Regelwerken für numerischen "
               "Code, dass alles, was größer ist als ein paar Zahlen, per "
               "`const&` übergeben wird -- kleine Werte wie `double` oder `int` "
               "dagegen als Kopie, die ist billiger als der Umweg über eine "
               "Adresse."),
            predict("Was schreibt dieses C++-Programm?",
                    "#include <iostream>\n\n"
                    "void verdoppeln(int& x) { x = x * 2; }\n"
                    "void nichts(int x)      { x = x * 2; }\n\n"
                    "int main()\n{\n"
                    "    int a = 5;\n"
                    "    int b = 5;\n"
                    "    verdoppeln(a);\n"
                    "    nichts(b);\n"
                    "    std::cout << a << \" \" << b << std::endl;\n"
                    "}\n",
                    "10 5",
                    "`verdoppeln` bekommt eine Referenz und verändert das "
                    "Original. `nichts` bekommt eine Kopie; die Änderung daran "
                    "ist mit dem Funktionsende weg. Genau dieser Unterschied "
                    "ist in C die Frage, ob man `int x` oder `int *x` "
                    "schreibt.\n\n"
                    "In C schreibt der Aufrufer dann `verdoppeln(&x)` und die Funktion "
                    "`*x = *x * 2;`. Dasselbe Ergebnis, zwei Stellen mehr, an denen ein "
                    "Stern fehlen kann. Die Referenz nimmt einem beide ab -- und die "
                    "Frage, was bei `NULL` passiert.",
                    run=True),
        ]),

    lesson("cpp-raii", "vector und RAII", ["vector", "raii"],
        "In C legt man ein Gitter mit `malloc` an und muss es mit `free` "
        "wieder loswerden — an **jedem** Ausgang der Funktion. Vergisst man "
        "einen, läuft der Speicher voll; gibt man zweimal frei, stürzt es "
        "ab.\n\n"
        "C++ dreht das um: `std::vector<double> u(n);` besorgt den Speicher, "
        "und der **Destruktor** gibt ihn frei, sobald `u` den Block verlässt "
        "— auch bei einem vorzeitigen `return`, auch wenn eine Ausnahme "
        "fliegt. Das Prinzip heißt RAII.\n\n"
        "    std::vector<double> u(n, 0.0);   // n Nullen\n"
        "    u[n/2] = 1.0;\n"
        "    // kein free, kein delete, kein Leck\n\n"
        "Deshalb kommt moderner C++-Simulationscode fast ohne `new` und "
        "`delete` aus. Und `u.size()` weiß immer, wie lang das Feld ist — was "
        "man in C von Hand mitschleppen muss.\n\n"
        "**Woher der Name kommt.** RAII heißt „resource acquisition is "
        "initialization“: das Beschaffen des Speichers geschieht beim "
        "Anlegen, das Freigeben beim Zerstören. Es gilt nicht nur für "
        "Speicher -- offene Dateien, Netzverbindungen und Sperren werden "
        "genauso gehalten. Wer das verstanden hat, braucht in C++ fast nie "
        "einen Aufräumzweig am Funktionsende.\n\n"
        "**Was `vector` sonst noch mitbringt:** `u.size()` ist immer die "
        "wahre Länge, `u.at(i)` prüft die Grenze (und kostet dafür etwas), "
        "`u[i]` prüft nicht -- genau wie in C. Beim Wachsen verdoppelt "
        "`vector` seinen Platz und kopiert um; in einer Zeitschleife legt "
        "man die Größe deshalb **einmal** vorher fest (`u.reserve(n)` oder "
        "gleich `vector<double> u(n)`).\n\n"
        "**Kopieren kostet hier wirklich.** `vector<double> w = u;` legt "
        "ein zweites Feld an und kopiert alles hinüber. Genau dafür gibt es "
        "`u.swap(w)`: es vertauscht nur die inneren Zeiger, egal wie groß "
        "die Felder sind. In einer Wärmeleitungsschleife ist das der "
        "Unterschied zwischen einer Kopie je Zeitschritt und keiner.",
        "",
        [
            mc("Wann gibt ein `std::vector` seinen Speicher frei?",
               ["Wenn man delete aufruft.",
                "Wenn er den Gültigkeitsbereich verlässt.",
                "Erst am Programmende.",
                "Wenn ein Aufräumer läuft."], 1,
               "Der Destruktor räumt auf, sobald der Block endet — auch bei "
               "vorzeitigem `return` und auch, wenn eine Ausnahme den Block "
               "verlässt. Das ist der ganze Punkt von RAII.\n\n"
               "Der Vergleich mit C ist lehrreich: dort steht am Ende jeder "
               "Funktion ein `free`, und jeder vorzeitige Ausgang braucht sein "
               "eigenes. Fehlt eines, wächst der Verbrauch mit der Laufzeit -- in "
               "einer Rechnung, die Tage läuft, ist das kein Schönheitsfehler."),
            parsons("Setze die Zeilen zu einem C++-Wärmeleitungsschritt "
                    "zusammen.",
                    ["std::vector<double> u(n, 0.0);",
                     "std::vector<double> w(u);",
                     "for (int i = 1; i < n - 1; ++i) {",
                     "    w[i] = u[i] + r * (u[i-1] - 2*u[i] + u[i+1]);",
                     "}",
                     "u.swap(w);"],
                    "`u.swap(w)` statt Kopieren: das tauscht nur die inneren "
                    "Zeiger, kostet also nichts, egal wie groß das Gitter ist. "
                    "In C schreibt man dafür `double *t = u; u = w; w = t;` — "
                    "dasselbe, nur von Hand.\n\n"
                    "Der Zeilenaufbau ist derselbe wie in C: zweites Feld anlegen, "
                    "innere Zellen aus dem alten berechnen, dann tauschen. Wichtig "
                    "bleibt, dass `w` aus `u` entsteht -- sonst stehen in `w` an den "
                    "Rändern Nullen statt der Randwerte.",
                    distractors=["free(u);", "u = w;"]),
        ]),
])


# ---------------------------------------------------------------------------
# 5 -- Python und NumPy
# ---------------------------------------------------------------------------
#
# Laeuft wirklich: auf diesem Geraet liegt Python 3.11, und seit dem
# Cross-Build auch NumPy.

K5 = chapter("py-numpy", "Python und NumPy", 9, "python",
             "In der Praxis schreibt man den Löser in C oder C++ und alles "
             "drumherum in Python: Aufbau, Auswertung, Bilder. Hier steht "
             "dasselbe Problem wie in Kapitel 3 — einmal ohne Schleife.", [

    lesson("py-felder", "Ganze Felder statt Schleifen", ["numpy", "slicing"],
        "NumPy rechnet mit **ganzen Feldern auf einmal**. Was in C eine "
        "Schleife ist, ist hier eine Zeile:\n\n"
        "    u[1:-1] += r * (u[:-2] - 2*u[1:-1] + u[2:])\n\n"
        "Das ist derselbe Drei-Punkt-Stern wie in C, nur für alle inneren "
        "Zellen gleichzeitig. `u[:-2]` heißt „alle außer den letzten zwei\", "
        "`u[2:]` heißt „ab dem dritten\" — gegeneinander verschoben ergeben "
        "sie die Nachbarn.\n\n"
        "Der Gewinn ist nicht die Kürze, sondern das Tempo: die Schleife "
        "läuft in C, nicht in Python. Eine Python-Schleife über eine Million "
        "Zellen ist quälend langsam; derselbe Feldausdruck ist in der Nähe "
        "von C.\n\n"
        "Gezeichnet wird wie in C: `print('plot %f %f' % (x, y))`.\n\n"
        "**Was ein NumPy-Feld ist.** Kein Python-Listenobjekt, sondern ein "
        "zusammenhängender Block gleichartiger Zahlen, wie ein C-Feld -- "
        "dazu die Angaben über Form und Typ. Deshalb kann die Schleife in "
        "C laufen: sie muss nicht bei jedem Element nachsehen, was für ein "
        "Objekt da liegt.\n\n"
        "**Ein Schnitt ist eine Sicht, keine Kopie.** `u[1:-1]` zeigt in "
        "dieselben Zahlen; `u[1:-1] += ...` verändert `u` selbst. Wer eine "
        "echte Kopie braucht, schreibt `u[1:-1].copy()`. Das ist der "
        "Unterschied zu Listen, wo `liste[1:-1]` kopiert -- und die "
        "häufigste Überraschung beim Umstieg.\n\n"
        "**Die Reihenfolge innerhalb einer Zeile.** `u[1:-1] += r * (u[:-2] "
        "- 2*u[1:-1] + u[2:])` liest zuerst die ganze rechte Seite und "
        "schreibt dann. Deshalb braucht man hier kein zweites Feld wie in "
        "C. Wer dagegen in einer Schleife Zelle für Zelle `u[i] += ...` "
        "rechnet, benutzt bereits neu berechnete Nachbarn -- das ist ein "
        "anderes Verfahren (Gauß-Seidel statt Jacobi).\n\n"
        "**Was Speicher kostet:** jeder Feldausdruck legt Zwischenfelder "
        "an. Bei einer Million Zellen sind `u[:-2] - 2*u[1:-1] + u[2:]` "
        "drei Zwischenergebnisse zu je 8 MB. Auf großen Gittern schreibt "
        "man deshalb `np.add(a, b, out=ziel)` oder rechnet blockweise.",
        "import numpy as np\n\n"
        "n = 101\n"
        "u = np.zeros(n)\n"
        "u[n // 2] = 1.0\n"
        "r = 0.4\n\n"
        "for schritt in range(400):\n"
        "    u[1:-1] += r * (u[:-2] - 2*u[1:-1] + u[2:])\n\n"
        "for i in range(0, n, 4):\n"
        "    print('plot %d %.6f' % (i, u[i]))\n"
        "print('Summe %.6f' % u.sum())\n",
        [
            predict("Was schreibt das Programm?",
                    "import numpy as np\n"
                    "a = np.arange(5.0)\n"
                    "print(a[1:-1])\n",
                    "[1. 2. 3.]",
                    "`[1:-1]` lässt das erste und das letzte Element weg — "
                    "genau die Randzellen, die beim Stencil nicht "
                    "mitgerechnet werden dürfen.\n\n"
                    "Zu lesen ist das so: `a[anfang:ende]` nimmt ab `anfang` bis "
                    "**vor** `ende`; negative Zahlen zählen vom Ende her. `a[1:-1]` ist "
                    "also „ohne das erste und ohne das letzte“. Die Ausgabe zeigt "
                    "`[1. 2. 3.]` mit Punkten, weil `arange(5.0)` Fließkommazahlen "
                    "erzeugt -- `arange(5)` ergäbe `[1 2 3]`."),
            code("Baue den Wärmeleitungsschritt als Feldausdruck. `u` und `r` "
                 "sind vorgegeben; gib am Ende die Summe mit sechs Stellen "
                 "aus.",
                 "import numpy as np\n\n"
                 "n = 101\n"
                 "u = np.zeros(n)\n"
                 "u[n // 2] = 1.0\n"
                 "r = 0.4\n\n"
                 "for schritt in range(400):\n"
                 "    pass    # hier der Feldausdruck\n\n"
                 "print('%.6f' % u.sum())\n",
                 "0.989678",
                 "import numpy as np\n\n"
                 "n = 101\n"
                 "u = np.zeros(n)\n"
                 "u[n // 2] = 1.0\n"
                 "r = 0.4\n\n"
                 "for schritt in range(400):\n"
                 "    u[1:-1] += r * (u[:-2] - 2*u[1:-1] + u[2:])\n\n"
                 "print('%.6f' % u.sum())\n",
                 "Die Summe bleibt nicht ganz bei 1, weil an den Rändern "
                 "Wärme abfließt — die Randzellen bleiben auf null. Genau so "
                 "verhält sich das explizite Verfahren auch in C.\n\n"
                 "Wer stattdessen die Summe erhalten will, braucht andere "
                 "Randbedingungen: `u[0] = u[1]` und `u[-1] = u[-2]` nach jedem "
                 "Schritt bedeutet „kein Wärmestrom über den Rand“, und dann "
                 "bleibt die Summe bis auf Rundung stehen. Was am Rand steht, ist "
                 "Teil des Modells, kein Detail.",
                 seconds=40),
            mc("Warum ist der Feldausdruck schneller als eine "
               "Python-Schleife über dieselben Zellen?",
               ["Weil NumPy die Schleife in kompiliertem C ausführt.",
                "Weil Python Schleifen automatisch optimiert.",
                "Weil weniger Speicher gebraucht wird.",
                "Er ist nicht schneller, nur kürzer."], 0,
               "Jeder Schleifendurchlauf in Python kostet Objektverwaltung. "
               "Beim Feldausdruck läuft die Schleife einmal in C durch den "
               "Speicher — auf diesem Telefon der Unterschied zwischen "
               "Sekunden und Minuten.\n\n"
               "Der zweite Gewinn ist der Speicherzugriff: die Zahlen liegen "
               "hintereinander, der Prozessor holt sie in ganzen Zeilen aus dem "
               "Zwischenspeicher. Eine Python-Liste enthält dagegen Verweise auf "
               "Objekte, die irgendwo liegen -- jeder Zugriff ein Sprung. Genau "
               "deshalb bringt NumPy bei kleinen Feldern wenig und bei großen "
               "sehr viel."),
        ],
        output="Summe 0.989678\n"),
])


# ---------------------------------------------------------------------------
# 4 -- C: Funktionen und Fliesskomma
# ---------------------------------------------------------------------------

K6 = chapter("c-funktionen", "Funktionen und Fließkomma", 4, "c",
             "Eigene Funktionen — und die Zahlen, mit denen sie rechnen. "
             "Fließkomma verhält sich anders, als die Schule es lehrt, und "
             "genau daran scheitern numerische Programme am unauffälligsten.", [

    lesson("l-funktionen", "Eigene Funktionen", ["funktion", "rueckgabe"],
        "Eine Funktion hat einen Rückgabetyp, einen Namen, Parameter und "
        "einen Rumpf:\n\n"
        "    double kraft(double x, double k)\n"
        "    {\n"
        "        return -k * x;\n"
        "    }\n\n"
        "Die Parameter sind **Kopien**. Ändert die Funktion `x`, bleibt das "
        "`x` des Aufrufers unberührt — ein Punkt, an dem sich C von Python "
        "unterscheidet und der später beim Thema Zeiger wichtig wird.\n\n"
        "Funktionen müssen **vor** ihrem ersten Aufruf stehen oder vorher "
        "angekündigt werden. In der Numerik lohnt sich das Herauslösen der "
        "Kraft besonders: Wer `kraft(x)` schreibt statt `-x`, kann das "
        "Pendel gegen eine Feder, gegen Gravitation oder gegen ein "
        "beliebiges Potential austauschen, ohne die Zeitschleife "
        "anzufassen.\n\n"
        "**Was beim Aufruf geschieht.** Die Werte der Argumente werden auf "
        "den Stapel gelegt, die Funktion legt ihre eigenen Variablen "
        "darüber und räumt beim `return` alles wieder ab. Deshalb sind "
        "Parameter Kopien, deshalb ist eine lokale Variable nach dem "
        "Rücksprung weg -- und deshalb ist ein Zeiger auf eine lokale "
        "Variable nach dem `return` wertlos.\n\n"
        "**Ankündigen statt umsortieren.** `double kraft(double x);` vor "
        "`main` ist eine Deklaration: Name, Typ, Parameter. Der Rumpf darf "
        "weiter unten stehen. In größeren Programmen stehen diese Zeilen in "
        "einer `.h`-Datei -- genau das, was `#include <stdio.h>` für "
        "`printf` tut.\n\n"
        "**Wann sich eine Funktion lohnt.** Nicht, um Zeilen zu sparen, "
        "sondern um eine Entscheidung an **eine** Stelle zu legen. Steht "
        "die Kraft dreimal im Programm, sind es drei Stellen, die bei einer "
        "Änderung auseinanderlaufen können. Der Preis ist ein Sprung je "
        "Aufruf; in einer inneren Zeitschleife über Millionen Schritte ist "
        "das messbar, aber selten entscheidend -- und ein Übersetzer setzt "
        "kleine Funktionen ohnehin an Ort und Stelle ein.",
        "#include <stdio.h>\n\n"
        "double kraft(double x, double k)\n{\n"
        "    return -k * x;\n}\n\n"
        "double energie(double x, double v, double k)\n{\n"
        "    return 0.5 * v * v + 0.5 * k * x * x;\n}\n\n"
        "int main()\n{\n"
        "    double x = 1.0;\n"
        "    double v = 0.0;\n"
        "    double k = 4.0;\n\n"
        "    printf(\"F = %.2f\\n\", kraft(x, k));\n"
        "    printf(\"E = %.2f\\n\", energie(x, v, k));\n"
        "    return 0;\n}\n",
        [
            predict("Was schreibt dieses Programm?",
                    "#include <stdio.h>\n\n"
                    "void verdoppeln(double x)\n{\n"
                    "    x = 2 * x;\n}\n\n"
                    "int main()\n{\n"
                    "    double a = 5.0;\n"
                    "    verdoppeln(a);\n"
                    "    printf(\"%.1f\\n\", a);\n"
                    "    return 0;\n}\n",
                    "5.0",
                    "Die Funktion bekommt eine **Kopie**. Sie verdoppelt ihre "
                    "eigene Kopie, und die ist beim `return` weg. Wer das "
                    "Original ändern will, braucht einen Zeiger — das kommt "
                    "im nächsten Kapitel.\n\n"
                    "Dass die Funktion etwas zurückgibt, ist der saubere Weg: `x = "
                    "verdoppeln(x);`. Eine Funktion, die nur über ihre Parameter wirkt, "
                    "verbirgt ihre Wirkung vor dem Leser der Aufrufstelle -- in C "
                    "erkennt man das wenigstens am `&` beim Aufruf."),
            code("Schreibe eine Funktion `double trapez(int n)`, die das "
                 "Integral von sin(x) zwischen 0 und pi nach der "
                 "Trapezregel berechnet, und gib das Ergebnis für n = 10 "
                 "mit sechs Stellen aus. Die Trapezregel: halbe Randwerte, "
                 "volle Zwischenwerte, mal Schrittweite.",
                 "#include <stdio.h>\n#include <math.h>\n\n"
                 "double trapez(int n)\n{\n"
                 "    double h = M_PI / n;\n"
                 "    double summe;\n"
                 "    int i;\n\n"
                 "    \n"
                 "    return 0.0;\n}\n\n"
                 "int main()\n{\n"
                 "    printf(\"%.6f\\n\", trapez(10));\n"
                 "    return 0;\n}\n",
                 "1.983524",
                 "#include <stdio.h>\n#include <math.h>\n\n"
                 "double trapez(int n)\n{\n"
                 "    double h = M_PI / n;\n"
                 "    double summe;\n"
                 "    int i;\n\n"
                 "    summe = 0.5 * (sin(0.0) + sin(M_PI));\n"
                 "    for (i = 1; i < n; i++) summe += sin(i * h);\n"
                 "    return summe * h;\n}\n\n"
                 "int main()\n{\n"
                 "    printf(\"%.6f\\n\", trapez(10));\n"
                 "    return 0;\n}\n",
                 "Der wahre Wert ist 2. Mit zehn Trapezen fehlt rund ein "
                 "Prozent; der Fehler der Trapezregel fällt mit h², also "
                 "bringt die Verzehnfachung der Stützstellen hundertmal "
                 "weniger Fehler.\n\n"
                 "Die halben Randwerte sind kein Schönheitsfehler, sondern die "
                 "Regel selbst: jedes Trapez trägt seine beiden Ecken zur Hälfte "
                 "bei, und alle inneren Punkte sind Ecke von zwei Trapezen. Wer alle "
                 "Werte voll nimmt, rechnet die Rechteckregel und hat einen Fehler "
                 "erster Ordnung. Die nächste Stufe wäre Simpson: Gewichte 1, 4, 2, "
                 "4, ..., 1 und ein Fehler von der Ordnung h⁴."),
        ],
        output="F = -4.00\nE = 2.00\n"),

    lesson("l-fliesskomma", "Fließkomma lügt", ["epsilon", "ausloeschung"],
        "`double` speichert Zahlen zur Basis **zwei**. Und 0,1 ist im "
        "Zweiersystem so wenig endlich darstellbar wie ein Drittel im "
        "Zehnersystem. Was gespeichert wird, ist ein naher Nachbar.\n\n"
        "Daraus folgt die erste Regel: **Fließkommazahlen nie mit `==` "
        "vergleichen.** Verglichen wird ein Abstand:\n\n"
        "    if (fabs(a - b) < 1e-9) ...\n\n"
        "Die zweite Falle heißt **Auslöschung**. Zieht man zwei fast gleich "
        "große Zahlen voneinander ab, bleiben von fünfzehn gültigen Stellen "
        "vielleicht drei übrig — der Rest war in beiden Zahlen gleich und "
        "hebt sich weg. Deshalb rechnet man Differenzen möglichst nicht aus "
        "großen Summanden, sondern formt die Formel um.\n\n"
        "Die dritte: Addiert man zu einer großen Zahl eine sehr kleine, "
        "kann sie **ganz verschwinden**. `1e16 + 1.0` ist wieder `1e16`. "
        "Genau das passiert in einer Zeitschleife, die eine Million kleine "
        "Schritte auf einen großen Wert addiert.\n\n"
        "**Wie eine Zahl im Speicher aussieht.** 64 Bit: ein Vorzeichen, "
        "elf Bit Exponent, 52 Bit Mantisse. Die Zahl ist also "
        "Vorzeichen·1,m·2^e -- ein Gitter von Werten, das um null herum "
        "dicht liegt und bei großen Zahlen grob wird. Der Abstand zweier "
        "benachbarter Zahlen bei 1,0 ist etwa 2,2·10⁻¹⁶; bei 10¹⁶ ist er "
        "größer als 1. Genau daher kommt die dritte Falle.\n\n"
        "**Die Reihenfolge ändert das Ergebnis.** Fließkommaaddition ist "
        "nicht assoziativ: `(a+b)+c` und `a+(b+c)` können sich "
        "unterscheiden. Deshalb liefert dieselbe Summe, auf vier Kerne "
        "verteilt, ein anderes letztes Bit als der serielle Lauf -- kein "
        "Fehler, aber ein Grund, Ergebnisse nie zeichenweise zu "
        "vergleichen. Wer es genauer braucht: die Kahan-Summation führt den "
        "verlorenen Rest mit und holt die verschluckten Beiträge zurück.\n\n"
        "**Was noch darin steckt:** `inf` entsteht bei Überlauf und bei "
        "Division durch null, `nan` bei `0.0/0.0` oder `inf-inf`. `nan` ist "
        "mit sich selbst **nicht** gleich -- `x != x` ist der übliche Test "
        "darauf. In einer Simulation, die instabil wird, wandert ein "
        "einziges `nan` innerhalb weniger Schritte durch das ganze Gitter; "
        "wer früh darauf prüft, weiß wenigstens, in welchem Schritt es "
        "begann.",
        "#include <stdio.h>\n#include <math.h>\n\n"
        "int main()\n{\n"
        "    double gross = 1e16;\n"
        "    double klein = 1.0;\n"
        "    double summe = gross + klein;\n\n"
        "    printf(\"verschwunden: %.1f\\n\", summe - gross);\n"
        "    printf(\"ausgeloescht: %.1f\\n\", (1e8 + 1.0) - 1e8);\n"
        "    printf(\"nah genug?    %d\\n\", fabs(0.5 - 0.5) < 1e-9);\n"
        "    return 0;\n}\n",
        [
            predict("Ein echter C-Übersetzer schreibt für dieses Programm "
                    "zwei Zeilen. Welche? (Die erste ist eine Zahl mit 20 "
                    "Nachkommastellen, die zweite 0 oder 1.)",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    double a = 0.1 + 0.2;\n\n"
                    "    printf(\"%.20f\\n\", a);\n"
                    "    printf(\"%d\\n\", a == 0.3);\n"
                    "    return 0;\n}\n",
                    "0.30000000000000004441\n0",
                    "0,1 und 0,2 sind im Zweiersystem beide ungenau, und "
                    "ihre Summe landet knapp **neben** dem, was `0.3` "
                    "ergibt. Der Vergleich ist deshalb falsch.\n\n"
                    "Diese Aufgabe läuft hier bewusst nicht: Der "
                    "C-Interpreter dieser App liest Dezimalzahlen zu grob "
                    "ein und liefert für `a == 0.3` eine 1. Das ist "
                    "nebenbei die beste Lehre des Kapitels — auch das "
                    "Werkzeug rechnet nicht immer so, wie man annimmt, und "
                    "man sollte wissen, wem man was glaubt.\n\n"
                    "Auf einem gewöhnlichen Rechner lässt sich das mit einer Zeile "
                    "nachprüfen: ein `printf` mit zwanzig Nachkommastellen für `0.1 + "
                    "0.2`. Die zwanzig Stellen sind der Trick -- mit `%f` zeigt C nur "
                    "sechs und rundet die Abweichung weg, weshalb die meisten "
                    "Programmierer jahrelang nichts davon merken.",
                    run=False),
            mc("Warum ist `if (x == 0.3)` bei einer gerechneten Größe `x` "
               "eine schlechte Idee?",
               ["Weil 0.3 im Binärformat nicht exakt darstellbar ist und "
                "die Rechnung einen Nachbarwert liefert.",
                "Weil `==` bei double gar nicht erlaubt ist.",
                "Weil es langsamer ist als ein Vergleich mit <.",
                "Weil 0.3 zu klein ist."], 0,
               "Der Vergleich ist syntaktisch erlaubt und schnell — er ist "
               "nur fast immer falsch. Verglichen wird ein Abstand, und "
               "zwar mit einer Toleranz, die zur Größenordnung der Zahlen "
               "passt.\n\n"
               "Es gibt Ausnahmen: Werte, die nur zugewiesen und nie gerechnet "
               "wurden, sind exakt vergleichbar -- etwa ein Kennwert wie -1.0, der "
               "„nicht gesetzt“ bedeutet. Sobald eine Rechnung dazwischen liegt, "
               "gilt wieder die Toleranz."),
            predict("Was schreibt das Programm?",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    double gross = 1e16;\n"
                    "    double summe = gross + 1.0;\n\n"
                    "    printf(\"%.1f\\n\", summe - gross);\n"
                    "    return 0;\n}\n",
                    "0.0",
                    "Die 1 verschwindet: `double` hat rund sechzehn "
                    "Dezimalstellen, und bei 1e16 liegt die letzte davon "
                    "schon über der Einerstelle. In einer Zeitschleife, die "
                    "t immer wieder um dt erhöht, ist das der Grund, warum "
                    "man t lieber als `i * dt` berechnet.\n\n"
                    "`t = i * dt` hat einen einzigen Rundungsfehler statt einer Million "
                    "aufsummierter. Bei 10⁶ Schritten mit dt = 10⁻⁶ liegt das "
                    "aufsummierte t am Ende sichtbar neben 1,0 -- und wer die Schleife "
                    "mit `while (t < 1.0)` abbricht, bekommt je nach Rundung einen "
                    "Schritt mehr oder weniger."),
            code("Schreibe eine Funktion `int nahe(double a, double b)`, "
                 "die 1 zurückgibt, wenn sich a und b um weniger als 1e-9 "
                 "unterscheiden, sonst 0. Gib damit die beiden Vergleiche "
                 "aus: erst `0.1+0.2` gegen `0.3`, dann `1.0` gegen `1.1`, "
                 "durch Leerzeichen getrennt.",
                 "#include <stdio.h>\n#include <math.h>\n\n"
                 "int nahe(double a, double b)\n{\n"
                 "    \n"
                 "    return 0;\n}\n\n"
                 "int main()\n{\n"
                 "    printf(\"%d %d\\n\", nahe(0.1 + 0.2, 0.3), nahe(1.0, 1.1));\n"
                 "    return 0;\n}\n",
                 "1 0",
                 "#include <stdio.h>\n#include <math.h>\n\n"
                 "int nahe(double a, double b)\n{\n"
                 "    if (fabs(a - b) < 1e-9) return 1;\n"
                 "    return 0;\n}\n\n"
                 "int main()\n{\n"
                 "    printf(\"%d %d\\n\", nahe(0.1 + 0.2, 0.3), nahe(1.0, 1.1));\n"
                 "    return 0;\n}\n",
                 "Eine feste Toleranz wie 1e-9 taugt für Zahlen in der "
                 "Größenordnung eins. Bei sehr großen oder sehr kleinen "
                 "Werten nimmt man eine **relative** Toleranz: "
                 "`fabs(a-b) <= 1e-9 * fabs(b)`.\n\n"
                 "In der Praxis nimmt man beides zusammen: `fabs(a-b) <= atol + rtol "
                 "* fabs(b)`. Der absolute Anteil fängt den Fall ab, dass `b` null "
                 "ist -- sonst wäre die Toleranz dort ebenfalls null. Genau diese "
                 "Form steht in jeder ernsthaften Prüfbibliothek."),
        ],
        output="verschwunden: 0.0\nausgeloescht: 1.0\nnah genug?    1\n"),
])


# ---------------------------------------------------------------------------
# 5 -- C: Felder und Zeiger
# ---------------------------------------------------------------------------

K7 = chapter("c-felder", "Felder und Zeiger", 5, "c",
             "Ein Gitter ist ein Feld, und ein Feld ist in C fast dasselbe "
             "wie ein Zeiger. Wer diesen Zusammenhang einmal verstanden "
             "hat, liest jeden Strömungscode.", [

    lesson("l-felder", "Felder", ["feld", "index"],
        "`double u[41];` legt 41 Werte nebeneinander. Gültig sind die "
        "Indizes **0 bis 40** — `u[41]` schreibt daneben, und C sagt nichts "
        "dazu. Das ist der Fehler, der nicht dort abstürzt, wo er passiert, "
        "sondern irgendwo später.\n\n"
        "Übergibt man ein Feld an eine Funktion, wird **nicht kopiert**: Die "
        "Funktion bekommt die Adresse und arbeitet am Original. Deshalb "
        "braucht sie die Länge als zweiten Parameter — die steckt nicht im "
        "Feld drin.\n\n"
        "    double summe(double *v, int n)\n\n"
        "In echtem C sind `double v[]` und `double *v` als Parameter "
        "**dasselbe**. Der Interpreter dieser App ist an dieser Stelle "
        "strenger als ein Übersetzer: Er kopiert bei `double v[]` "
        "tatsächlich. Schreib hier also immer die Zeigerform — sie ist "
        "ohnehin die ehrlichere, weil sie zeigt, was wirklich übergeben "
        "wird.\n\n"
        "In der Numerik ist das genau richtig: Ein Gitter mit einer Million "
        "Zellen soll bei jedem Aufruf nicht kopiert werden.\n\n"
        "**Was ein Feld im Speicher ist:** n Werte lückenlos "
        "hintereinander. `u[i]` heißt „ab der Anfangsadresse i Elemente "
        "weiter“ -- eine Multiplikation mit der Elementgröße und eine "
        "Addition, sonst nichts. Deshalb ist der Zugriff überall gleich "
        "teuer, und deshalb kostet ein Index außerhalb der Grenzen keine "
        "Prüfung: es gibt niemanden, der prüfen könnte.\n\n"
        "**Warum der Fehler woanders auffällt.** `u[41]` beschreibt "
        "Speicher, der einer anderen Variablen gehört. Das Programm läuft "
        "weiter; erst wenn jene Variable gelesen wird, steht dort Unsinn. "
        "Zwischen Ursache und Wirkung können Minuten liegen -- der Grund, "
        "warum solche Fehler mit Werkzeugen wie `valgrind` gesucht werden "
        "und nicht mit Nachdenken.\n\n"
        "**Die Länge gehört zum Feld, aber nicht ins Feld.** `sizeof(u)` "
        "liefert in der Funktion, die einen Zeiger bekommen hat, die Größe "
        "des **Zeigers**, nicht des Feldes. Deshalb wandert die Länge "
        "grundsätzlich als eigener Parameter mit -- in C++ nimmt einem das "
        "`std::vector` ab, in C bleibt es Disziplin.",
        "#include <stdio.h>\n\n"
        "double summe(double *v, int n)\n{\n"
        "    double s = 0.0;\n"
        "    int i;\n\n"
        "    for (i = 0; i < n; i++) s += v[i];\n"
        "    return s;\n}\n\n"
        "void verdoppeln(double *v, int n)\n{\n"
        "    int i;\n\n"
        "    for (i = 0; i < n; i++) v[i] = 2 * v[i];\n}\n\n"
        "int main()\n{\n"
        "    double w[4];\n"
        "    w[0] = 1.0; w[1] = 2.0; w[2] = 3.0; w[3] = 4.0;\n\n"
        "    printf(\"%.1f\\n\", summe(w, 4));\n"
        "    verdoppeln(w, 4);\n"
        "    printf(\"%.1f\\n\", summe(w, 4));\n"
        "    return 0;\n}\n",
        [
            mc("`double u[10];` — welcher ist der letzte gültige Index?",
               ["u[10]", "u[9]", "u[0]", "u[11]"], 1,
               "Zehn Plätze, von 0 bis 9. `u[10]` liegt schon daneben und "
               "wird trotzdem übersetzt — in der Numerik meist genau an der "
               "Randzelle, die man beim Stencil vergessen hat.\n\n"
               "Die Grenzen sind deshalb so leicht zu verfehlen, weil zwei "
               "Zählweisen im Umlauf sind: „n Elemente“ und „Index bis n-1“. "
               "Wer die Schleife als `for (i = 0; i < n; i++)` schreibt, hat beide "
               "in einer Zeile richtig -- deshalb ist das die Standardform, und "
               "jede Abweichung davon verdient einen zweiten Blick."),
            predict("Was schreibt das Programm? Beachte, dass "
                    "`aendern` ein Feld bekommt.",
                    "#include <stdio.h>\n\n"
                    "void aendern(double *v, int n)\n{\n"
                    "    v[0] = 99.0;\n}\n\n"
                    "int main()\n{\n"
                    "    double a[3];\n"
                    "    a[0] = 1.0; a[1] = 2.0; a[2] = 3.0;\n"
                    "    aendern(a, 3);\n"
                    "    printf(\"%.1f\\n\", a[0]);\n"
                    "    return 0;\n}\n",
                    "99.0",
                    "Anders als bei einem einzelnen `double` wird ein Feld "
                    "nicht kopiert: Die Funktion arbeitet am Original. Genau "
                    "deshalb kann ein Stencil-Schritt das Gitter direkt "
                    "fortschreiben.\n\n"
                    "Das ist kein Sonderfall für Felder, sondern die Folge davon, dass "
                    "der Feldname zur Adresse zerfällt: übergeben wird ein Zeiger, und "
                    "der ist zwar eine Kopie -- die Kopie einer Adresse zeigt aber auf "
                    "dasselbe. Wer wirklich kopieren will, legt ein zweites Feld an und "
                    "kopiert Zelle für Zelle (oder mit `memcpy`)."),
            code("Schreibe `double groesster(double *v, int n)`, die den "
                 "größten Wert zurückgibt, und gib ihn für das gegebene "
                 "Feld mit einer Nachkommastelle aus.",
                 "#include <stdio.h>\n\n"
                 "double groesster(double *v, int n)\n{\n"
                 "    \n"
                 "    return 0.0;\n}\n\n"
                 "int main()\n{\n"
                 "    double w[8];\n"
                 "    w[0] = 3.0; w[1] = 1.0; w[2] = 4.0; w[3] = 1.0;\n"
                 "    w[4] = 5.0; w[5] = 9.0; w[6] = 2.0; w[7] = 6.0;\n\n"
                 "    printf(\"%.1f\\n\", groesster(w, 8));\n"
                 "    return 0;\n}\n",
                 "9.0",
                 "#include <stdio.h>\n\n"
                 "double groesster(double *v, int n)\n{\n"
                 "    double m = v[0];\n"
                 "    int i;\n\n"
                 "    for (i = 1; i < n; i++)\n"
                 "        if (v[i] > m) m = v[i];\n"
                 "    return m;\n}\n\n"
                 "int main()\n{\n"
                 "    double w[8];\n"
                 "    w[0] = 3.0; w[1] = 1.0; w[2] = 4.0; w[3] = 1.0;\n"
                 "    w[4] = 5.0; w[5] = 9.0; w[6] = 2.0; w[7] = 6.0;\n\n"
                 "    printf(\"%.1f\\n\", groesster(w, 8));\n"
                 "    return 0;\n}\n",
                 "Wichtig ist der Start bei `v[0]` und nicht bei 0: Ein Feld "
                 "aus lauter negativen Werten hätte sonst das Maximum 0, das "
                 "gar nicht darin vorkommt. Derselbe Fehler steckt in vielen "
                 "selbstgebauten Normberechnungen.\n\n"
                 "Für n = 0 hat die Funktion keine sinnvolle Antwort -- `v[0]` wäre "
                 "dann schon der Zugriff hinter das Ende. In einer Bibliothek würde "
                 "man das abfangen; in einem Löser schreibt man die Bedingung an die "
                 "Stelle, an der das Feld entsteht, und verlässt sich darauf."),
        ],
        output="10.0\n20.0\n"),

    lesson("l-zeiger", "Zeiger", ["zeiger", "adresse"],
        "Ein **Zeiger** enthält eine Adresse. `&a` liefert die Adresse von "
        "`a`, `*p` den Wert an der Adresse `p`.\n\n"
        "    double a = 1.0;\n"
        "    double *p = &a;\n"
        "    *p = 5.0;          /* a ist jetzt 5.0 */\n\n"
        "Damit lässt sich die Beschränkung aus dem letzten Kapitel umgehen: "
        "Eine Funktion, die den Wert des Aufrufers ändern soll, bekommt "
        "seine Adresse statt seines Wertes.\n\n"
        "    void tauschen(double *a, double *b)\n\n"
        "**Feld und Zeiger** sind fast dasselbe: Der Name eines Feldes ist "
        "die Adresse seines ersten Elements. `u[i]` und `*(u + i)` sind "
        "exakt gleichbedeutend, und eine Funktion, die `double v[]` "
        "erwartet, kann ebenso gut `double *v` schreiben — es ist derselbe "
        "Typ.\n\n"
        "Der Interpreter dieser App nimmt die Arithmetik allerdings nur auf "
        "einer **Zeigervariablen** an, nicht direkt auf dem Feldnamen. "
        "Deshalb steht im Beispiel erst `p = feld;` — was in echtem C "
        "überflüssig wäre.\n\n"
        "Der Trick, den jeder Strömungscode benutzt: Statt das neue Gitter "
        "über das alte zu **kopieren**, tauscht man die beiden **Zeiger**. "
        "Das kostet nichts, egal wie groß das Gitter ist.\n\n"
        "**Warum ein Zeiger einen Typ hat.** `p + 1` springt nicht ein "
        "Byte, sondern ein Element weiter -- bei `double *` also acht "
        "Bytes. Der Typ sagt der Arithmetik, wie weit ein Schritt ist. "
        "Deshalb ist `void *` zwar für jede Adresse zu haben, aber man kann "
        "damit nicht rechnen, bevor man ihn umgedeutet hat.\n\n"
        "**Der Stern an zwei Stellen.** In `double *p;` gehört er zur "
        "Deklaration (p ist ein Zeiger auf double), in `*p = 5.0;` ist er "
        "der Zugriff. Wer `double* p, q;` schreibt, bekommt einen Zeiger "
        "und ein gewöhnliches double -- der Stern gehört zum Namen, nicht "
        "zum Typ. Deshalb schreibt man ihn besser an den Namen.\n\n"
        "**Der Tausch im Löser.** `double *t = u; u = w; w = t;` vertauscht "
        "drei Adressen; das Gitter selbst bleibt liegen. Danach ist `u` das "
        "neue Feld und `w` der Platz für den nächsten Schritt. Diese drei "
        "Zeilen stehen in jedem expliziten Löser und sind der Grund, warum "
        "genau zwei Felder genügen -- egal wie viele Zeitschritte kommen.",
        "#include <stdio.h>\n\n"
        "void tauschen(double *a, double *b)\n{\n"
        "    double t = *a;\n\n"
        "    *a = *b;\n"
        "    *b = t;\n}\n\n"
        "int main()\n{\n"
        "    double x = 1.0;\n"
        "    double y = 2.0;\n"
        "    double feld[3];\n"
        "    double *p;\n\n"
        "    feld[0] = 10.0; feld[1] = 20.0; feld[2] = 30.0;\n"
        "    p = feld;              /* der Feldname ist die Adresse */\n\n"
        "    tauschen(&x, &y);\n"
        "    printf(\"%.1f %.1f\\n\", x, y);\n"
        "    printf(\"%.1f %.1f\\n\", p[1], *(p + 1));\n"
        "    return 0;\n}\n",
        [
            predict("Was schreibt das Programm?",
                    "#include <stdio.h>\n\nint main()\n{\n"
                    "    double a = 1.0;\n"
                    "    double *p = &a;\n\n"
                    "    *p = 5.0;\n"
                    "    printf(\"%.1f\\n\", a);\n"
                    "    return 0;\n}\n",
                    "5.0",
                    "`p` zeigt auf `a`; `*p = 5.0` schreibt also in `a`. "
                    "Der Stern hat zwei ganz verschiedene Bedeutungen: in "
                    "der Deklaration „ist ein Zeiger auf\", im Ausdruck "
                    "„der Wert an dieser Adresse\".\n\n"
                    "`&` hat dieselbe Doppelrolle: vor einer Variablen liefert es deren "
                    "Adresse, in einer C++-Deklaration macht es eine Referenz daraus. "
                    "Wer die beiden Rollen beim Lesen sauber trennt, verliert die "
                    "Hälfte der Verwirrung um Zeiger."),
            mc("Was ist gleichbedeutend mit `u[3]`?",
               ["*(u + 3)", "&u + 3", "*u + 3", "u + 3"], 0,
               "Der Feldname ist die Adresse des ersten Elements; drei "
               "weiter und dann dereferenziert ist genau das vierte "
               "Element. `*u + 3` wäre dagegen der erste Wert plus drei.\n\n"
               "Dass beide Schreibweisen gleichbedeutend sind, ist keine "
               "Spitzfindigkeit: `u[i]` ist in C **definiert** als `*(u + i)`. "
               "Daraus folgt die Kuriosität, dass auch `3[u]` gültiges C ist -- "
               "gebräuchlich ist das nicht, aber es zeigt, wie wörtlich die Regel "
               "gemeint ist."),
            code("Schreibe `void skalieren(double *v, int n, double f)`, "
                 "die jedes Element mit f multipliziert — mit Zeigersyntax, "
                 "also `*(v + i)` statt `v[i]`. Gib danach die Summe mit "
                 "einer Nachkommastelle aus.",
                 "#include <stdio.h>\n\n"
                 "void skalieren(double *v, int n, double f)\n{\n"
                 "    \n}\n\n"
                 "int main()\n{\n"
                 "    double w[4];\n"
                 "    double s = 0.0;\n"
                 "    int i;\n\n"
                 "    w[0] = 1.0; w[1] = 2.0; w[2] = 3.0; w[3] = 4.0;\n"
                 "    skalieren(w, 4, 2.5);\n"
                 "    for (i = 0; i < 4; i++) s += w[i];\n"
                 "    printf(\"%.1f\\n\", s);\n"
                 "    return 0;\n}\n",
                 "25.0",
                 "#include <stdio.h>\n\n"
                 "void skalieren(double *v, int n, double f)\n{\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < n; i++) *(v + i) = *(v + i) * f;\n}\n\n"
                 "int main()\n{\n"
                 "    double w[4];\n"
                 "    double s = 0.0;\n"
                 "    int i;\n\n"
                 "    w[0] = 1.0; w[1] = 2.0; w[2] = 3.0; w[3] = 4.0;\n"
                 "    skalieren(w, 4, 2.5);\n"
                 "    for (i = 0; i < 4; i++) s += w[i];\n"
                 "    printf(\"%.1f\\n\", s);\n"
                 "    return 0;\n}\n",
                 "1+2+3+4 = 10, mal 2,5 ergibt 25. Dass die Änderung beim "
                 "Aufrufer ankommt, ist kein Zufall: `w` **ist** die "
                 "Adresse.\n\n"
                 "`*(v + i)` und `v[i]` erzeugen denselben Maschinencode; die Wahl "
                 "ist eine des Lesens. In Schleifen über Gitter liest sich die "
                 "Indexform besser, in Bibliotheksfunktionen, die über Puffer "
                 "laufen, oft die Zeigerform."),
        ],
        output="2.0 1.0\n20.0 20.0\n"),
])


# ---------------------------------------------------------------------------
# 6 -- C: Waermeleitung, das erste Feld
# ---------------------------------------------------------------------------

K8 = chapter("c-waerme", "Wärmeleitung: das erste Feld", 6, "c",
             "Die erste partielle Differentialgleichung. Hier wird aus "
             "einzelnen Zahlen ein Feld, und aus der Zeitschleife ein "
             "Löser — mit einer Stabilitätsgrenze, die man sehen kann.", [

    lesson("l-stencil", "Der Drei-Punkt-Stern", ["stencil", "diffusion"],
        "Die Wärmeleitungsgleichung lautet\n\n"
        "    du/dt = D · d²u/dx²\n\n"
        "Die zweite Ableitung auf einem Gitter mit Abstand h ist der "
        "**Drei-Punkt-Stern**:\n\n"
        "    (u[i-1] - 2·u[i] + u[i+1]) / h²\n\n"
        "Anschaulich: der Nachbarschaftsmittelwert minus dem eigenen Wert. "
        "Ist eine Zelle kälter als ihre Nachbarn, wird sie wärmer — "
        "Diffusion glättet.\n\n"
        "Mit `r = D·dt/h²` wird daraus ein Zeitschritt:\n\n"
        "    w[i] = u[i] + r · (u[i-1] - 2·u[i] + u[i+1])\n\n"
        "Zwei Dinge sind Pflicht:\n\n"
        "**Zwei Felder.** Wer direkt in `u` schreibt, benutzt für den "
        "rechten Nachbarn noch den alten Wert, für den linken aber schon "
        "den neuen. Das ist ein anderes Verfahren, und es rechnet still "
        "etwas Falsches.\n\n"
        "**Die Ränder.** Die Zellen 0 und n-1 haben keinen vollständigen "
        "Stern. Hier werden sie festgehalten — das ist eine "
        "Dirichlet-Randbedingung und bedeutet physikalisch: an beiden Enden "
        "sitzt ein Kühlkörper auf null Grad.\n\n"
        "**Woher der Stern kommt.** Die zweite Ableitung ist die Änderung "
        "der Steigung. Nimmt man links und rechts je einen "
        "Differenzenquotienten und zieht sie voneinander ab, steht da "
        "`(u[i+1] - 2u[i] + u[i-1]) / h²`. Eine Taylorentwicklung zeigt, "
        "dass die ungeraden Glieder sich aufheben -- deshalb ist der Stern "
        "von **zweiter** Ordnung genau, obwohl er nur drei Werte benutzt.\n\n"
        "**Was `r` bedeutet.** `r = D·dt/h²` ist die dimensionslose Zahl "
        "des Problems: wie weit sich Wärme in einem Zeitschritt im "
        "Verhältnis zur Zellgröße ausbreitet. Alles, was über die "
        "Stabilität entscheidet, hängt nur an ihr -- nicht an D, dt oder h "
        "einzeln. Das ist der Grund, warum man in der Numerik zuerst die "
        "dimensionslosen Kennzahlen bildet.\n\n"
        "**Warum gerade dieses Problem am Anfang steht:** Die "
        "Wärmeleitungsgleichung glättet. Fehler werden kleiner, nicht "
        "größer, solange die Stabilitätsgrenze eingehalten wird -- ein "
        "gutmütiges Testfeld, an dem man Randbedingungen, Felderwechsel und "
        "Erhaltungsgrößen üben kann, bevor es mit Advektion unangenehm "
        "wird.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    int n = 41;\n"
        "    int schritte = 200;\n"
        "    double r = 0.4;\n"
        "    double u[41];\n"
        "    double w[41];\n"
        "    double summe = 0.0;\n"
        "    int i, s;\n\n"
        "    for (i = 0; i < n; i++) u[i] = 0.0;\n"
        "    u[n / 2] = 1.0;\n\n"
        "    for (s = 0; s < schritte; s++) {\n"
        "        for (i = 1; i < n - 1; i++)\n"
        "            w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);\n"
        "        w[0] = 0.0;\n"
        "        w[n-1] = 0.0;\n"
        "        for (i = 0; i < n; i++) u[i] = w[i];\n"
        "    }\n\n"
        "    for (i = 0; i < n; i++) {\n"
        "        printf(\"plot %d %.6f\\n\", i, u[i]);\n"
        "        summe += u[i];\n"
        "    }\n"
        "    printf(\"Mitte %.6f  Summe %.6f\\n\", u[n/2], summe);\n"
        "    return 0;\n}\n",
        [
            mc("Warum wird in ein zweites Feld `w` geschrieben statt direkt "
               "in `u`?",
               ["Damit jeder Punkt mit den Werten desselben Zeitschritts "
                "gerechnet wird.",
                "Weil C das Überschreiben verbietet.",
                "Aus Geschwindigkeitsgründen.",
                "Damit die Ränder erhalten bleiben."], 0,
               "Schreibt man direkt in `u`, ist `u[i-1]` beim Erreichen von "
               "`i` schon der neue Wert, `u[i+1]` aber noch der alte. Das "
               "ist das Gauß-Seidel-Verfahren statt des expliziten — es "
               "läuft, konvergiert sogar, löst aber eine andere Aufgabe.\n\n"
               "Der Unterschied fällt bei einem groben Gitter kaum auf und wird "
               "bei feinem systematisch: Das Ergebnis ist um einen halben "
               "Zeitschritt versetzt und nicht mehr zweiter Ordnung. Für **das "
               "Lösen eines Gleichungssystems** ist Gauß-Seidel dagegen genau "
               "richtig und schneller als Jacobi -- dieselbe Zeile, anderer Zweck. "
               "Der Fehler liegt nicht im Code, sondern darin, nicht zu wissen, "
               "welches Verfahren man gerade schreibt."),
            code("Die Summe über alle Zellen nimmt ab, weil an den Rändern "
                 "Wärme abfließt. Ändere die Randbedingung so, dass **nichts "
                 "abfließt**: Die Randzelle tauscht nur mit ihrem einen "
                 "Nachbarn, also `w[0] = u[0] + r*(u[1] - u[0])` und "
                 "entsprechend am anderen Ende. Gib danach Mitte und Summe "
                 "mit sechs Stellen aus, durch Leerzeichen getrennt.",
                 "#include <stdio.h>\n\n"
                 "int main()\n{\n"
                 "    int n = 41;\n"
                 "    int schritte = 200;\n"
                 "    double r = 0.4;\n"
                 "    double u[41];\n"
                 "    double w[41];\n"
                 "    double summe = 0.0;\n"
                 "    int i, s;\n\n"
                 "    for (i = 0; i < n; i++) u[i] = 0.0;\n"
                 "    u[n / 2] = 1.0;\n\n"
                 "    for (s = 0; s < schritte; s++) {\n"
                 "        for (i = 1; i < n - 1; i++)\n"
                 "            w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);\n"
                 "        w[0] = 0.0;\n"
                 "        w[n-1] = 0.0;\n"
                 "        for (i = 0; i < n; i++) u[i] = w[i];\n"
                 "    }\n\n"
                 "    for (i = 0; i < n; i++) summe += u[i];\n"
                 "    printf(\"%.6f %.6f\\n\", u[n/2], summe);\n"
                 "    return 0;\n}\n",
                 "0.031829 1.000000",
                 "#include <stdio.h>\n\n"
                 "int main()\n{\n"
                 "    int n = 41;\n"
                 "    int schritte = 200;\n"
                 "    double r = 0.4;\n"
                 "    double u[41];\n"
                 "    double w[41];\n"
                 "    double summe = 0.0;\n"
                 "    int i, s;\n\n"
                 "    for (i = 0; i < n; i++) u[i] = 0.0;\n"
                 "    u[n / 2] = 1.0;\n\n"
                 "    for (s = 0; s < schritte; s++) {\n"
                 "        for (i = 1; i < n - 1; i++)\n"
                 "            w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);\n"
                 "        w[0] = u[0] + r * (u[1] - u[0]);\n"
                 "        w[n-1] = u[n-1] + r * (u[n-2] - u[n-1]);\n"
                 "        for (i = 0; i < n; i++) u[i] = w[i];\n"
                 "    }\n\n"
                 "    for (i = 0; i < n; i++) summe += u[i];\n"
                 "    printf(\"%.6f %.6f\\n\", u[n/2], summe);\n"
                 "    return 0;\n}\n",
                 "Die Summe bleibt jetzt exakt bei 1: Was hineingesteckt "
                 "wurde, bleibt drin. Wichtig ist die **Flussform**: Wer "
                 "stattdessen einfach `w[0] = w[1]` setzt, kopiert einen "
                 "Wert, statt eine Bilanz zu ziehen — dann wächst die Summe "
                 "auf 1,0386, und das Verfahren erfindet Wärme. Dass eine "
                 "Erhaltungsgröße erhalten bleibt, ist die beste "
                 "Selbstprüfung, die ein Löser haben kann, und der erste "
                 "Test, den man einbaut.\n\n"
                 "Die Flussform macht das deutlich: Was eine Zelle verliert, "
                 "gewinnt die Nachbarzelle -- der Austausch steht einmal da und "
                 "wirkt auf beide. Löser, die so gebaut sind, heißen "
                 "**konservativ**; bei Stoßwellen ist das nicht Kosmetik, sondern "
                 "entscheidet über die richtige Ausbreitungsgeschwindigkeit.",
                 plot=False, seconds=30),
        ],
        output="Mitte 0.031086  Summe 0.771801\n"),

    lesson("l-cfl", "Die Stabilitätsgrenze", ["stabilitaet", "cfl"],
        "Das explizite Verfahren ist nur stabil, solange\n\n"
        "    r = D·dt/h² ≤ 1/2\n\n"
        "Darüber wächst die kürzeste darstellbare Welle — die, die von "
        "Zelle zu Zelle das Vorzeichen wechselt — mit jedem Schritt an. Das "
        "ist kein Rundungsfehler, sondern das Verfahren selbst: Der "
        "Verstärkungsfaktor für diese Welle ist `1 - 4r`, und für r > 1/2 "
        "ist sein Betrag größer als eins.\n\n"
        "Was das praktisch bedeutet, ist unangenehm: **Halbiert man h, muss "
        "dt geviertelt werden.** Doppelte Auflösung kostet also nicht "
        "doppelt, sondern achtmal so viel Rechenzeit — zweimal so viele "
        "Zellen, viermal so viele Schritte.\n\n"
        "Genau deshalb gibt es implizite Verfahren. Sie sind pro Schritt "
        "teurer, weil ein Gleichungssystem zu lösen ist, aber sie haben "
        "diese Schranke nicht.\n\n"
        "Im Bild ist die Instabilität unverkennbar: keine glatte Kurve, "
        "sondern ein Zickzack von Zelle zu Zelle, dessen Ausschlag "
        "explodiert.\n\n"
        "**Wie man auf 1/2 kommt.** Man setzt eine Welle `u[i] = g^n · "
        "e^(i k x)` in das Verfahren ein und sieht nach, was der Faktor `g` "
        "je Schritt ist -- das ist die Von-Neumann-Analyse. Für den "
        "Drei-Punkt-Stern kommt `g = 1 - 4r·sin²(kh/2)` heraus. Am "
        "schlimmsten ist die kürzeste Welle (sin² = 1), also `g = 1 - 4r`, "
        "und `|g| <= 1` verlangt `r <= 1/2`.\n\n"
        "**Woran man sie erkennt.** Instabilität sieht nie aus wie ein zu "
        "großer Fehler, sondern immer wie ein Zickzack von Zelle zu Zelle, "
        "der sich verdoppelt und verdoppelt. Wer im Bild diese Sägezähne "
        "sieht, braucht nicht nach einem Tippfehler zu suchen -- der "
        "Zeitschritt ist zu groß.\n\n"
        "**Was implizit heißt.** Man schreibt den Stern mit den **neuen** "
        "Werten und löst das entstehende Gleichungssystem. In 1D ist die "
        "Matrix tridiagonal und mit dem Thomas-Algorithmus in O(n) zu "
        "lösen; der Schritt ist dann für jedes dt stabil. Bezahlt wird mit "
        "Genauigkeit, nicht mit Stabilität: zu große Schritte ergeben ein "
        "stabiles, aber falsches Ergebnis -- die unangenehmere Sorte "
        "Fehler.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    int n = 41;\n"
        "    int schritte = 60;\n"
        "    double r = 0.6;          /* ueber der Grenze von 0.5 */\n"
        "    double u[41];\n"
        "    double w[41];\n"
        "    double gross = 0.0;\n"
        "    int i, s;\n\n"
        "    for (i = 0; i < n; i++) u[i] = 0.0;\n"
        "    u[n / 2] = 1.0;\n\n"
        "    for (s = 0; s < schritte; s++) {\n"
        "        for (i = 1; i < n - 1; i++)\n"
        "            w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);\n"
        "        w[0] = 0.0;\n"
        "        w[n-1] = 0.0;\n"
        "        for (i = 0; i < n; i++) u[i] = w[i];\n"
        "    }\n\n"
        "    for (i = 0; i < n; i++) {\n"
        "        printf(\"plot %d %.3e\\n\", i, u[i]);\n"
        "        if (u[i] > gross) gross = u[i];\n"
        "    }\n"
        "    printf(\"groesster Wert %.3e\\n\", gross);\n"
        "    return 0;\n}\n",
        [
            mc("Du verdoppelst die Auflösung, halbierst also h. Was muss mit "
               "dt geschehen, damit das explizite Verfahren stabil bleibt?",
               ["dt muss geviertelt werden.",
                "dt muss halbiert werden.",
                "dt kann bleiben.",
                "dt kann verdoppelt werden."], 0,
               "r = D·dt/h² hängt von h **im Quadrat** ab. Halbes h heißt "
               "viertel dt — und damit achtmal so viel Rechenaufwand für die "
               "doppelte Auflösung. Das ist der Grund, warum in der Praxis "
               "implizit gerechnet wird.\n\n"
               "In zwei Dimensionen wird es schlimmer: doppelte Auflösung heißt "
               "viermal so viele Zellen und viermal so viele Schritte, also "
               "sechzehnmal. In drei Dimensionen zweiunddreißigmal. Diese Rechnung "
               "erklärt die Größe von Rechenzentren besser als jede andere."),
            code("Setze r auf den größten Wert, bei dem das Verfahren noch "
                 "stabil ist, lass 60 Schritte laufen und gib den größten "
                 "Wert im Feld mit sechs Stellen aus. (Bei genau dieser "
                 "Grenze ist das Verfahren gerade noch stabil.)",
                 "#include <stdio.h>\n\n"
                 "int main()\n{\n"
                 "    int n = 41;\n"
                 "    int schritte = 60;\n"
                 "    double r = 0.6;\n"
                 "    double u[41];\n"
                 "    double w[41];\n"
                 "    double gross = 0.0;\n"
                 "    int i, s;\n\n"
                 "    for (i = 0; i < n; i++) u[i] = 0.0;\n"
                 "    u[n / 2] = 1.0;\n\n"
                 "    for (s = 0; s < schritte; s++) {\n"
                 "        for (i = 1; i < n - 1; i++)\n"
                 "            w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);\n"
                 "        w[0] = 0.0;\n"
                 "        w[n-1] = 0.0;\n"
                 "        for (i = 0; i < n; i++) u[i] = w[i];\n"
                 "    }\n\n"
                 "    for (i = 0; i < n; i++)\n"
                 "        if (u[i] > gross) gross = u[i];\n"
                 "    printf(\"%.6f\\n\", gross);\n"
                 "    return 0;\n}\n",
                 "0.102578",
                 "#include <stdio.h>\n\n"
                 "int main()\n{\n"
                 "    int n = 41;\n"
                 "    int schritte = 60;\n"
                 "    double r = 0.5;\n"
                 "    double u[41];\n"
                 "    double w[41];\n"
                 "    double gross = 0.0;\n"
                 "    int i, s;\n\n"
                 "    for (i = 0; i < n; i++) u[i] = 0.0;\n"
                 "    u[n / 2] = 1.0;\n\n"
                 "    for (s = 0; s < schritte; s++) {\n"
                 "        for (i = 1; i < n - 1; i++)\n"
                 "            w[i] = u[i] + r * (u[i-1] - 2 * u[i] + u[i+1]);\n"
                 "        w[0] = 0.0;\n"
                 "        w[n-1] = 0.0;\n"
                 "        for (i = 0; i < n; i++) u[i] = w[i];\n"
                 "    }\n\n"
                 "    for (i = 0; i < n; i++)\n"
                 "        if (u[i] > gross) gross = u[i];\n"
                 "    printf(\"%.6f\\n\", gross);\n"
                 "    return 0;\n}\n",
                 "Mit r = 0,5 bleibt der Ausschlag bei 0,10 und die "
                 "Verteilung glatt; mit 0,6 stand dort eine Zahl in der "
                 "Größenordnung 10⁷. Zwischen „rechnet\" und „explodiert\" "
                 "liegt in diesem Verfahren ein Zehntel.\n\n"
                 "Genau an der Grenze (r = 1/2) ist `g = -1`: die kürzeste Welle "
                 "wechselt jeden Schritt das Vorzeichen, ohne zu wachsen. Stabil ist "
                 "das, schön nicht. In der Praxis nimmt man deshalb Sicherheit "
                 "mit -- 0,8 bis 0,9 der zulässigen Schrittweite ist üblich, weil "
                 "variable Koeffizienten die Grenze örtlich verschieben.",
                 seconds=30),
        ],
        output="groesster Wert 3.246e+07\n"),
])


# ---------------------------------------------------------------------------
# 7 -- C: Strukturen und Speicher
# ---------------------------------------------------------------------------

K9 = chapter("c-struct", "Strukturen und Speicher", 7, "c",
             "Zusammengesetzte Daten und Gitter, deren Größe erst zur "
             "Laufzeit feststeht. Ab hier sieht der Code aus wie ein "
             "richtiger Löser.", [

    lesson("l-struct", "Strukturen", ["struct", "teilchen"],
        "Eine **Struktur** fasst zusammen, was zusammengehört:\n\n"
        "    struct Teilchen {\n"
        "        double x;\n"
        "        double v;\n"
        "    };\n\n"
        "Zugegriffen wird mit dem Punkt (`t.x`), über einen Zeiger mit dem "
        "Pfeil (`p->x`, die Kurzform für `(*p).x`).\n\n"
        "In der Simulation ist das der Unterschied zwischen einem Programm, "
        "das man noch lesen kann, und einem, das aus sieben parallelen "
        "Feldern besteht. Ein Feld von Strukturen — `struct Teilchen "
        "t[100];` — hält alle Teilchen beisammen.\n\n"
        "Nebenbei: Der Interpreter dieser App will **ein Feld je Zeile**; "
        "`double x, v;` in einer Struktur mag er nicht. Ein echter "
        "Übersetzer nimmt beides.\n\n"
        "**Was im Speicher liegt.** Die Felder stehen in der Reihenfolge "
        "der Deklaration hintereinander, mit Lücken zur Ausrichtung: ein "
        "`double` möchte auf einer durch acht teilbaren Adresse beginnen. "
        "Deshalb kann eine Struktur größer sein als die Summe ihrer Teile, "
        "und deshalb lohnt es sich, große Felder zuerst zu deklarieren.\n\n"
        "**Struktur von Feldern oder Feld von Strukturen?** `struct "
        "Teilchen t[1000]` (AoS) hält alles eines Teilchens beisammen -- "
        "angenehm zu lesen. `double x[1000]; double v[1000];` (SoA) legt "
        "gleichartige Werte zusammen -- angenehm für den Prozessor, der "
        "acht Werte auf einmal verrechnen kann. Molekulardynamikprogramme "
        "rechnen deshalb intern oft in SoA, auch wenn sie nach außen wie "
        "AoS aussehen.\n\n"
        "**`typedef` spart das Wort `struct`.** `typedef struct { double x; "
        "double v; } Teilchen;` erlaubt danach `Teilchen t;`. In C++ ist "
        "das überflüssig -- dort ist der Strukturname sofort ein Typname.",
        "#include <stdio.h>\n\n"
        "struct Teilchen {\n"
        "    double x;\n"
        "    double v;\n"
        "};\n\n"
        "double energie(struct Teilchen t)\n{\n"
        "    return 0.5 * t.v * t.v + 0.5 * t.x * t.x;\n}\n\n"
        "int main()\n{\n"
        "    struct Teilchen feld[4];\n"
        "    double gesamt = 0.0;\n"
        "    int i;\n\n"
        "    for (i = 0; i < 4; i++) {\n"
        "        feld[i].x = i * 0.5;\n"
        "        feld[i].v = 1.0;\n"
        "    }\n"
        "    for (i = 0; i < 4; i++) gesamt += energie(feld[i]);\n\n"
        "    printf(\"Gesamtenergie %.4f\\n\", gesamt);\n"
        "    return 0;\n}\n",
        [
            mc("Wie greift man über den Zeiger `p` auf das Feld `x` einer "
               "Struktur zu?",
               ["p.x", "p->x", "*p.x", "&p.x"], 1,
               "`p->x` ist die Kurzform für `(*p).x`. Die Klammern sind "
               "nötig, weil der Punkt stärker bindet als der Stern — "
               "`*p.x` hieße „dereferenziere p.x\" und ist etwas ganz "
               "anderes.\n\n"
               "Der Pfeil ist nicht nur Abkürzung, sondern die Form, in der man "
               "verkettete Zugriffe überhaupt lesen kann: `zelle->nachbar->druck` "
               "gegenüber `(*(*zelle).nachbar).druck`. In Datenstrukturen mit "
               "Verweisen -- Listen, Bäumen, unstrukturierten Gittern -- steht "
               "deshalb fast nur der Pfeil."),
            code("Schreibe `double schwerpunkt(struct Teilchen *t, int n)`, "
                 "die den mit der Masse ungewichteten Mittelwert der "
                 "Positionen liefert, und gib ihn mit vier Stellen aus.",
                 "#include <stdio.h>\n\n"
                 "struct Teilchen {\n"
                 "    double x;\n"
                 "    double v;\n"
                 "};\n\n"
                 "double schwerpunkt(struct Teilchen *t, int n)\n{\n"
                 "    \n"
                 "    return 0.0;\n}\n\n"
                 "int main()\n{\n"
                 "    struct Teilchen feld[5];\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 5; i++) {\n"
                 "        feld[i].x = i * i * 1.0;\n"
                 "        feld[i].v = 0.0;\n"
                 "    }\n"
                 "    printf(\"%.4f\\n\", schwerpunkt(feld, 5));\n"
                 "    return 0;\n}\n",
                 "6.0000",
                 "#include <stdio.h>\n\n"
                 "struct Teilchen {\n"
                 "    double x;\n"
                 "    double v;\n"
                 "};\n\n"
                 "double schwerpunkt(struct Teilchen *t, int n)\n{\n"
                 "    double s = 0.0;\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < n; i++) s += t[i].x;\n"
                 "    return s / n;\n}\n\n"
                 "int main()\n{\n"
                 "    struct Teilchen feld[5];\n"
                 "    int i;\n\n"
                 "    for (i = 0; i < 5; i++) {\n"
                 "        feld[i].x = i * i * 1.0;\n"
                 "        feld[i].v = 0.0;\n"
                 "    }\n"
                 "    printf(\"%.4f\\n\", schwerpunkt(feld, 5));\n"
                 "    return 0;\n}\n",
                 "0+1+4+9+16 = 30, geteilt durch 5 ergibt 6. Beachte, dass "
                 "der Parameter ein **Zeiger auf Struktur** ist — damit "
                 "wird das Feld nicht kopiert, und `t[i].x` funktioniert "
                 "trotzdem wie gewohnt.\n\n"
                 "Genau diese Signatur -- Zeiger auf das erste Element plus Anzahl "
                 "-- ist die übliche Form in C, von `qsort` bis zu jeder "
                 "Gitterfunktion. Wer sie einmal liest wie „ein Feld von n "
                 "Teilchen“, hat die halbe C-Standardbibliothek entschlüsselt."),
        ],
        output="Gesamtenergie 3.7500\n"),

    lesson("l-speicher", "Speicher zur Laufzeit", ["malloc", "flach"],
        "Bis hierher stand die Gittergröße im Quelltext. Ein Löser bekommt "
        "sie aber erst beim Start:\n\n"
        "    double *u = malloc(n * sizeof(double));\n"
        "    ...\n"
        "    free(u);\n\n"
        "`malloc` will **Bytes**, nicht Elemente — daher `sizeof`. Und "
        "jedem `malloc` gehört genau ein `free`.\n\n"
        "**Zweidimensional** legt man nicht als Feld von Zeigern an, "
        "sondern **flach**:\n\n"
        "    double *u = malloc(ny * nx * sizeof(double));\n"
        "    u[j * nx + i]        /* Zeile j, Spalte i */\n\n"
        "Der Grund ist der Zwischenspeicher der CPU: Eine Zeile liegt am "
        "Stück, und wer sie der Reihe nach durchläuft, bekommt die nächsten "
        "Werte geschenkt. Deshalb läuft in jedem Strömungscode die "
        "**innere** Schleife über `i` und die äußere über `j` — andersherum "
        "kostet es leicht das Dreifache an Zeit, ohne dass sich am Ergebnis "
        "etwas ändert.\n\n"
        "**Was `malloc` zurückgibt.** Eine Adresse -- oder `NULL`, wenn "
        "kein Speicher da ist. Auf einem Gerät mit 1 GB ist das keine "
        "graue Theorie: Ein Gitter von 4000×4000 `double` sind 128 MB je "
        "Feld, und ein Löser braucht zwei bis fünf davon. Der Rückgabewert "
        "gehört geprüft, bevor die erste Zelle beschrieben wird.\n\n"
        "**Was `free` nicht tut.** Es gibt den Speicher zurück, ändert aber "
        "den Zeiger nicht -- der zeigt weiterhin auf fremdes Land. Deshalb "
        "die Gewohnheit, nach `free(u)` gleich `u = NULL;` zu schreiben: "
        "ein Zugriff auf `NULL` stürzt sofort ab, ein Zugriff auf "
        "freigegebenen Speicher erst irgendwann.\n\n"
        "**Warum flach und nicht `double **u`.** Das Feld von Zeigern "
        "kostet einen zusätzlichen Sprung je Zugriff, verteilt die Zeilen "
        "über den Speicher und macht `memcpy` über das ganze Gitter "
        "unmöglich. Der einzige Vorteil wäre die Schreibweise `u[j][i]` -- "
        "dafür schreibt man sich lieber ein `#define IDX(i,j) ((j)*nx+(i))` "
        "und behält die Klammern im Auge.",
        "#include <stdio.h>\n#include <stdlib.h>\n\n"
        "int main()\n{\n"
        "    int nx = 8;\n"
        "    int ny = 6;\n"
        "    int gesamt = nx * ny;\n"
        "    double *u = malloc(gesamt * sizeof(double));\n"
        "    double summe = 0.0;\n"
        "    int i, j;\n\n"
        "    for (j = 0; j < ny; j++)\n"
        "        for (i = 0; i < nx; i++)\n"
        "            u[j * nx + i] = i + j;\n\n"
        "    for (j = 0; j < ny; j++)\n"
        "        for (i = 0; i < nx; i++)\n"
        "            summe += u[j * nx + i];\n\n"
        "    printf(\"%d Zellen, Summe %.1f\\n\", gesamt, summe);\n"
        "    printf(\"Zelle (3,2) = %.1f\\n\", u[2 * nx + 3]);\n"
        "    free(u);\n"
        "    return 0;\n}\n",
        [
            mc("Ein Gitter hat `nx` Spalten. Wie erreicht man die Zelle in "
               "Zeile j, Spalte i?",
               ["u[i * nx + j]", "u[j * nx + i]", "u[i + j]",
                "u[j][i] — flach geht das nicht"], 1,
               "Zeile j beginnt bei `j * nx`; darin ist i der Versatz. Die "
               "Verwechslung der beiden Indizes ist der häufigste Fehler "
               "beim Umstieg auf flache Felder — und sie fällt bei einem "
               "quadratischen Gitter erst auf, wenn das Ergebnis gespiegelt "
               "aussieht.\n\n"
               "Eine Merkhilfe: Der Index, der **zuletzt** in der Schleife läuft, "
               "gehört in die Formel ohne Faktor. Wer `for (j...) for (i...)` "
               "schreibt und `u[j*nx + i]` benutzt, läuft im Speicher "
               "hintereinander weg -- das ist die schnelle Reihenfolge, und die "
               "Formel passt dazu."),
            code("Lege ein Gitter mit nx = 12, ny = 10 flach an, setze jede "
                 "Zelle auf `i * j`, und gib die Summe aller Randzellen mit "
                 "einer Nachkommastelle aus. Rand heißt: i = 0, i = nx-1, "
                 "j = 0 oder j = ny-1.",
                 "#include <stdio.h>\n#include <stdlib.h>\n\n"
                 "int main()\n{\n"
                 "    int nx = 12;\n"
                 "    int ny = 10;\n"
                 "    double *u = malloc(nx * ny * sizeof(double));\n"
                 "    double rand = 0.0;\n"
                 "    int i, j;\n\n"
                 "    \n"
                 "    printf(\"%.1f\\n\", rand);\n"
                 "    free(u);\n"
                 "    return 0;\n}\n",
                 "990.0",
                 "#include <stdio.h>\n#include <stdlib.h>\n\n"
                 "int main()\n{\n"
                 "    int nx = 12;\n"
                 "    int ny = 10;\n"
                 "    double *u = malloc(nx * ny * sizeof(double));\n"
                 "    double rand = 0.0;\n"
                 "    int i, j;\n\n"
                 "    for (j = 0; j < ny; j++)\n"
                 "        for (i = 0; i < nx; i++)\n"
                 "            u[j * nx + i] = i * j;\n"
                 "    for (j = 0; j < ny; j++)\n"
                 "        for (i = 0; i < nx; i++)\n"
                 "            if (i == 0 || i == nx - 1 || j == 0 || j == ny - 1)\n"
                 "                rand += u[j * nx + i];\n"
                 "    printf(\"%.1f\\n\", rand);\n"
                 "    free(u);\n"
                 "    return 0;\n}\n",
                 "Die Ränder eines Gitters einzeln zu behandeln ist in jedem "
                 "Löser Alltag — dort stehen die Randbedingungen. Wer die "
                 "vier Kanten mit vier getrennten Schleifen abarbeitet, "
                 "zählt leicht die Ecken doppelt; die Abfrage im Durchlauf "
                 "vermeidet das.\n\n"
                 "Für große Gitter dreht sich das um: die Abfrage in der inneren "
                 "Schleife kostet bei jeder Zelle etwas, obwohl sie nur am Rand "
                 "zutrifft. Dann trennt man die Ränder heraus und zählt die Ecken "
                 "bewusst einmal. Der übliche Weg in Lösern ist eine "
                 "**Geisterzellenschicht**: eine zusätzliche Zelle rings herum, die "
                 "vor jedem Schritt gefüllt wird -- danach ist der innere Teil ohne "
                 "jede Sonderbehandlung zu rechnen."),
        ],
        output="48 Zellen, Summe 288.0\nZelle (3,2) = 5.0\n"),
])


# ---------------------------------------------------------------------------
# 8 -- C: Advektion und die CFL-Bedingung
# ---------------------------------------------------------------------------

K10 = chapter("c-advektion", "Advektion und die CFL-Bedingung", 10, "c",
              "Transport statt Diffusion. Hier entscheidet die Wahl der "
              "räumlichen Ableitung darüber, ob überhaupt etwas "
              "herauskommt — und die naheliegendste Wahl ist die falsche.", [

    lesson("l-upwind", "Zentral oder stromaufwärts", ["advektion", "upwind"],
        "Die Advektionsgleichung transportiert ein Profil mit der "
        "Geschwindigkeit c, ohne es zu verändern:\n\n"
        "    du/dt + c · du/dx = 0\n\n"
        "Für die räumliche Ableitung gibt es zwei naheliegende Wahlen. Die "
        "**zentrale** ist die genauere:\n\n"
        "    (u[i+1] - u[i-1]) / (2h)\n\n"
        "und sie ist für dieses Problem **unbrauchbar**: Sie schwingt, und "
        "die Schwingung wächst. Nach vierzig Schritten steht im Feld ±15, "
        "obwohl der Anfangswert zwischen 0 und 1 lag.\n\n"
        "Die **stromaufwärtige** Wahl (upwind) ist ungenauer, aber richtig:\n\n"
        "    (u[i] - u[i-1]) / h      für c > 0\n\n"
        "Sie nimmt die Information von dort, wo sie physikalisch herkommt. "
        "Der Preis ist **numerische Diffusion**: Die Kante verschmiert, das "
        "Profil wird flacher. Aber es bleibt zwischen 0 und 1.\n\n"
        "Dazu die **CFL-Bedingung**:\n\n"
        "    C = c·dt/h ≤ 1\n\n"
        "In einem Zeitschritt darf die Strömung höchstens eine Zelle weit "
        "laufen. Darüber holt das Verfahren die Information nicht mehr ein, "
        "und kein explizites Schema rettet das.\n\n"
        "**Warum die zentrale Ableitung hier versagt.** Die "
        "Von-Neumann-Analyse liefert für zentrale Differenzen mit Euler "
        "vorwärts einen Verstärkungsfaktor mit Betrag größer als eins -- "
        "für **jede** Schrittweite. Das Verfahren ist nicht „bei zu großem "
        "dt“ instabil, sondern immer. Genauigkeit sagt eben nichts über "
        "Stabilität.\n\n"
        "**Was numerische Diffusion ist.** Entwickelt man das "
        "Aufwindverfahren in einer Taylorreihe, steht dort die "
        "Advektionsgleichung **plus** ein Diffusionsterm mit dem "
        "Koeffizienten `u·h/2·(1-C)`. Das Verfahren löst also, genau "
        "genommen, eine andere Gleichung als die beabsichtigte. Deshalb "
        "verschmiert die Kante -- und deshalb verschwindet der Effekt bei "
        "C = 1 ganz.\n\n"
        "**Woher der Name CFL kommt:** Courant, Friedrichs und Lewy, 1928. "
        "Die Bedingung ist älter als jeder Computer und keine Eigenheit des "
        "Verfahrens, sondern eine Aussage über Information: Der "
        "Abhängigkeitsbereich des Verfahrens muss den der Gleichung "
        "enthalten. Rechnet man mit C > 1, holt sich die Zelle ihren Wert "
        "aus einer Nachbarschaft, in der die Antwort gar nicht steht.\n\n"
        "**Was man in der Praxis nimmt:** weder das eine noch das andere "
        "rein, sondern begrenzte Verfahren höherer Ordnung (TVD, MUSCL, "
        "WENO). Sie rechnen dort, wo das Feld glatt ist, mit zweiter oder "
        "dritter Ordnung und schalten an Kanten auf Aufwind zurück -- "
        "genauer als das eine, stabil wie das andere.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    int n = 41;\n"
        "    int schritte = 40;\n"
        "    double C = 0.5;\n"
        "    double a[41];\n"
        "    double b[41];\n"
        "    double z[41];\n"
        "    double y[41];\n"
        "    int i, s;\n\n"
        "    for (i = 0; i < n; i++) {\n"
        "        a[i] = 0.0;\n"
        "        if (i >= n / 4 && i < n / 2) a[i] = 1.0;\n"
        "        z[i] = a[i];\n"
        "    }\n\n"
        "    for (s = 0; s < schritte; s++) {\n"
        "        for (i = 1; i < n - 1; i++) {\n"
        "            b[i] = a[i] - C * (a[i] - a[i-1]);\n"
        "            y[i] = z[i] - 0.5 * C * (z[i+1] - z[i-1]);\n"
        "        }\n"
        "        b[0] = 0.0; b[n-1] = 0.0;\n"
        "        y[0] = 0.0; y[n-1] = 0.0;\n"
        "        for (i = 0; i < n; i++) { a[i] = b[i]; z[i] = y[i]; }\n"
        "    }\n\n"
        "    for (i = 0; i < n; i++) {\n"
        "        printf(\"plot aufwind %d %.5f\\n\", i, a[i]);\n"
        "        printf(\"plot zentral %d %.5f\\n\", i, z[i]);\n"
        "    }\n"
        "    return 0;\n}\n",
        [
            mc("Warum ist die zentrale Ableitung für reine Advektion "
               "unbrauchbar, obwohl sie genauer ist?",
               ["Sie nimmt Information von stromabwärts, wo physikalisch "
                "keine herkommt, und schwingt sich auf.",
                "Sie ist zu langsam zu rechnen.",
                "Sie braucht zwei Felder.",
                "Sie funktioniert nur bei C > 1."], 0,
               "Genauigkeit und Stabilität sind zwei verschiedene Dinge. Das "
               "zentrale Schema ist zweiter Ordnung genau und für dieses "
               "Problem trotzdem unbedingt instabil — ein Lehrstück dafür, "
               "dass man beides getrennt prüfen muss.\n\n"
               "Rettbar ist die zentrale Ableitung übrigens schon -- nur nicht "
               "mit Euler vorwärts: mit Leapfrog, Runge-Kutta oder einem "
               "Diffusionsanteil im Modell wird sie brauchbar. Die Aussage lautet "
               "also genau: **diese** Raumdiskretisierung mit **diesem** "
               "Zeitschritt ist instabil. Stabilität ist eine Eigenschaft der "
               "Kombination."),
            code("Lass nur das Aufwindverfahren laufen, aber mit C = 1,5 — "
                 "also über der CFL-Grenze. Gib den größten Betrag im Feld "
                 "nach 40 Schritten im Format %.3e aus.",
                 "#include <stdio.h>\n#include <math.h>\n\n"
                 "int main()\n{\n"
                 "    int n = 41;\n"
                 "    int schritte = 40;\n"
                 "    double C = 0.5;\n"
                 "    double a[41];\n"
                 "    double b[41];\n"
                 "    double gross = 0.0;\n"
                 "    int i, s;\n\n"
                 "    for (i = 0; i < n; i++) {\n"
                 "        a[i] = 0.0;\n"
                 "        if (i >= n / 4 && i < n / 2) a[i] = 1.0;\n"
                 "    }\n"
                 "    for (s = 0; s < schritte; s++) {\n"
                 "        for (i = 1; i < n - 1; i++)\n"
                 "            b[i] = a[i] - C * (a[i] - a[i-1]);\n"
                 "        b[0] = 0.0; b[n-1] = 0.0;\n"
                 "        for (i = 0; i < n; i++) a[i] = b[i];\n"
                 "    }\n"
                 "    for (i = 0; i < n; i++)\n"
                 "        if (fabs(a[i]) > gross) gross = fabs(a[i]);\n"
                 "    printf(\"%.3e\\n\", gross);\n"
                 "    return 0;\n}\n",
                 "7.789e+10",
                 "#include <stdio.h>\n#include <math.h>\n\n"
                 "int main()\n{\n"
                 "    int n = 41;\n"
                 "    int schritte = 40;\n"
                 "    double C = 1.5;\n"
                 "    double a[41];\n"
                 "    double b[41];\n"
                 "    double gross = 0.0;\n"
                 "    int i, s;\n\n"
                 "    for (i = 0; i < n; i++) {\n"
                 "        a[i] = 0.0;\n"
                 "        if (i >= n / 4 && i < n / 2) a[i] = 1.0;\n"
                 "    }\n"
                 "    for (s = 0; s < schritte; s++) {\n"
                 "        for (i = 1; i < n - 1; i++)\n"
                 "            b[i] = a[i] - C * (a[i] - a[i-1]);\n"
                 "        b[0] = 0.0; b[n-1] = 0.0;\n"
                 "        for (i = 0; i < n; i++) a[i] = b[i];\n"
                 "    }\n"
                 "    for (i = 0; i < n; i++)\n"
                 "        if (fabs(a[i]) > gross) gross = fabs(a[i]);\n"
                 "    printf(\"%.3e\\n\", gross);\n"
                 "    return 0;\n}\n",
                 "Aus Werten zwischen 0 und 1 werden 7,8·10¹⁰. Auch das "
                 "richtige Verfahren hilft nichts, wenn der Zeitschritt zu "
                 "groß ist — Stabilität ist immer eine Aussage über das "
                 "Verfahren **und** seine Schrittweite.\n\n"
                 "In einem Löser schreibt man deshalb den Zeitschritt nicht fest, "
                 "sondern rechnet ihn in jedem Schritt aus der aktuellen "
                 "Geschwindigkeit: `dt = cfl_zahl * h / max|u|` mit einer Zahl "
                 "unter eins. Wird die Strömung schneller, wird der Schritt von "
                 "selbst kleiner.",
                 seconds=25),
        ],
        output="plot ... (2 Kurven zu je 41 Punkten)\n"),
])


# ---------------------------------------------------------------------------
# 9 -- C: Druckprojektion
# ---------------------------------------------------------------------------

K11 = chapter("c-druck", "Druckprojektion", 11, "c",
              "Der Schritt, der aus einem Geschwindigkeitsfeld eine "
              "inkompressible Strömung macht. Hier steckt der Kern jedes "
              "Navier-Stokes-Lösers — und er ist überraschend kurz.", [

    lesson("l-projektion", "Divergenzfrei machen", ["divergenz", "poisson"],
        "Inkompressibel heißt: In jede Zelle fließt genauso viel hinein wie "
        "heraus, also **div u = 0**. Ein beliebig fortgeschriebenes "
        "Geschwindigkeitsfeld erfüllt das nicht.\n\n"
        "Der Druck ist bei inkompressibler Strömung keine eigene "
        "Zustandsgröße, sondern genau die Kraft, die diese Bedingung "
        "erzwingt. Daraus wird ein Rezept in drei Schritten:\n\n"
        "**1. Divergenz ausrechnen.**\n\n"
        "    d = (ux[i+1] - ux[i-1])/2 + (uy[j+1] - uy[j-1])/2\n\n"
        "**2. Poisson-Gleichung lösen:** Δp = d. Am einfachsten mit dem "
        "Jacobi-Verfahren — jede Zelle wird immer wieder auf den Mittelwert "
        "ihrer Nachbarn minus der Divergenz gesetzt:\n\n"
        "    p[i][j] = (p[i+1][j] + p[i-1][j] + p[i][j+1] + p[i][j-1] - d) / 4\n\n"
        "**3. Druckgradient abziehen:**\n\n"
        "    ux -= (p[i+1][j] - p[i-1][j]) / 2\n"
        "    uy -= (p[i][j+1] - p[i][j-1]) / 2\n\n"
        "Danach ist das Feld (fast) divergenzfrei. „Fast\", weil Jacobi "
        "langsam konvergiert — hundert Durchläufe drücken die Divergenz um "
        "etwa den Faktor dreißig. Genau deshalb steckt in echten Lösern an "
        "dieser Stelle ein Mehrgitterverfahren und nicht Jacobi: Der "
        "Druckschritt ist der teuerste des ganzen Zeitschritts.\n\n"
        "**Warum überhaupt eine Poisson-Gleichung entsteht.** Man nimmt die "
        "Divergenz der Impulsgleichung und verlangt, dass die Divergenz des "
        "Ergebnisses null ist. Übrig bleibt Δp = div u*/dt -- die "
        "Zeitableitung fällt heraus, und der Druck erscheint ohne eigene "
        "Zeitentwicklung. Das ist der mathematische Grund, warum inkompressible Strömung keinen Schallwellen-Zeitschritt braucht: "
        "Information wandert im Druckfeld augenblicklich durch das ganze "
        "Gebiet.\n\n"
        "**Was der Druck hier ist.** Kein Zustand, sondern ein "
        "Lagrange-Multiplikator zur Zwangsbedingung. Er ist nur bis auf "
        "eine Konstante bestimmt -- mit reinen Neumann-Rändern hat das "
        "Gleichungssystem einen Nullraum, und man setzt eine Zelle fest "
        "oder zieht am Ende den Mittelwert ab. Wer das vergisst, sieht ein "
        "langsam davonlaufendes Druckniveau bei völlig richtiger "
        "Geschwindigkeit.\n\n"
        "**Warum Jacobi so langsam ist.** Jeder Durchlauf trägt Information "
        "genau eine Zelle weit. Bei n Zellen je Richtung braucht sie n "
        "Durchläufe, um einmal durch das Gebiet zu laufen, und der Fehler "
        "fällt erst danach. Mehrgitter umgeht das, indem es dieselbe "
        "Gleichung auf gröberen Gittern löst, wo dieselbe Information in "
        "wenigen Schritten ankommt -- Aufwand proportional zur Zellenzahl "
        "statt zu ihrem Quadrat.\n\n"
        "**Das Muster dahinter** heißt Projektionsmethode (Chorin, 1968): "
        "erst ohne Rücksicht auf die Nebenbedingung fortschreiben, dann auf "
        "den zulässigen Raum zurückprojizieren. Dieselben drei Schritte stehen in jedem inkompressiblen Löser, von der Spielzeugfassung "
        "bis OpenFOAM.",
        "#include <stdio.h>\n\n"
        "int main()\n{\n"
        "    int n = 16;\n"
        "    double ux[16][16];\n"
        "    double uy[16][16];\n"
        "    double d[16][16];\n"
        "    double p[16][16];\n"
        "    double q[16][16];\n"
        "    double vorher = 0.0;\n"
        "    double nachher = 0.0;\n"
        "    double w;\n"
        "    int i, j, it;\n\n"
        "    for (j = 0; j < n; j++)\n"
        "        for (i = 0; i < n; i++) {\n"
        "            ux[j][i] = (i - n / 2.0) / n;\n"
        "            uy[j][i] = (j - n / 2.0) / n;\n"
        "            p[j][i] = 0.0;\n"
        "            d[j][i] = 0.0;\n"
        "        }\n\n"
        "    for (j = 1; j < n - 1; j++)\n"
        "        for (i = 1; i < n - 1; i++) {\n"
        "            d[j][i] = 0.5 * (ux[j][i+1] - ux[j][i-1])\n"
        "                    + 0.5 * (uy[j+1][i] - uy[j-1][i]);\n"
        "            w = d[j][i];\n"
        "            if (w < 0) w = -w;\n"
        "            if (w > vorher) vorher = w;\n"
        "        }\n\n"
        "    for (it = 0; it < 200; it++) {\n"
        "        for (j = 1; j < n - 1; j++)\n"
        "            for (i = 1; i < n - 1; i++)\n"
        "                q[j][i] = 0.25 * (p[j][i+1] + p[j][i-1]\n"
        "                                + p[j+1][i] + p[j-1][i] - d[j][i]);\n"
        "        for (j = 1; j < n - 1; j++)\n"
        "            for (i = 1; i < n - 1; i++)\n"
        "                p[j][i] = q[j][i];\n"
        "    }\n\n"
        "    for (j = 1; j < n - 1; j++)\n"
        "        for (i = 1; i < n - 1; i++) {\n"
        "            ux[j][i] -= 0.5 * (p[j][i+1] - p[j][i-1]);\n"
        "            uy[j][i] -= 0.5 * (p[j+1][i] - p[j-1][i]);\n"
        "        }\n\n"
        "    for (j = 2; j < n - 2; j++)\n"
        "        for (i = 2; i < n - 2; i++) {\n"
        "            w = 0.5 * (ux[j][i+1] - ux[j][i-1])\n"
        "              + 0.5 * (uy[j+1][i] - uy[j-1][i]);\n"
        "            if (w < 0) w = -w;\n"
        "            if (w > nachher) nachher = w;\n"
        "        }\n\n"
        "    printf(\"Divergenz vorher %.6f nachher %.6f\\n\", vorher, nachher);\n"
        "    return 0;\n}\n",
        [
            mc("Wozu dient der Druckschritt bei inkompressibler Strömung?",
               ["Er erzwingt div u = 0.",
                "Er erhöht die Genauigkeit der Zeitintegration.",
                "Er bestimmt die Temperatur.",
                "Er dämpft die Turbulenz."], 0,
               "Der Druck ist hier keine thermodynamische Größe, sondern ein "
               "Lagrange-Multiplikator: genau die Kraft, die die "
               "Zwangsbedingung div u = 0 durchsetzt. Deshalb braucht jeder "
               "inkompressible Löser eine Poisson-Gleichung.\n\n"
               "Bei **kompressibler** Strömung ist das anders: dort ist der Druck "
               "über eine Zustandsgleichung mit Dichte und Temperatur verbunden "
               "und wird mitgeführt wie jede andere Größe. Der Preis ist ein "
               "Zeitschritt, der die Schallgeschwindigkeit auflösen muss -- bei "
               "langsamen Strömungen ein schlechtes Geschäft, und genau deshalb "
               "gibt es beide Sorten Löser."),
            mc("Warum nimmt man in echten Lösern nicht Jacobi für den "
               "Druckschritt?",
               ["Weil Jacobi viel zu langsam konvergiert; der Druckschritt "
                "wäre der teuerste Teil.",
                "Weil Jacobi instabil ist.",
                "Weil Jacobi zu viel Speicher braucht.",
                "Weil Jacobi nur in 1D funktioniert."], 0,
               "Jacobi konvergiert, aber die Zahl der nötigen Durchläufe "
               "wächst mit dem Quadrat der Gitterweite. Bei einer Million "
               "Zellen ist das aussichtslos — deshalb Mehrgitter, "
               "konjugierte Gradienten oder FFT.\n\n"
               "Für den Anfang ist Jacobi trotzdem die richtige Wahl: er ist in "
               "fünf Zeilen geschrieben, braucht keine Matrix und lässt sich "
               "Zelle für Zelle nachrechnen. Wer das Verfahren verstanden hat, "
               "kann den Löser später austauschen -- die Aufgabe bleibt dieselbe."),
        ],
        output="Divergenz vorher 0.125000 nachher 0.004342\n"),
])


# ---------------------------------------------------------------------------
# 10 -- C++: Templates
# ---------------------------------------------------------------------------

K12 = chapter("cpp-template", "C++: Templates", 12, "cpp",
              "Derselbe Löser für float und double, ohne ihn zweimal zu "
              "schreiben und ohne Laufzeitkosten. Auch dieses Kapitel wird "
              "gelesen, nicht ausgeführt.", [

    lesson("cpp-tmpl", "Ein Löser, mehrere Typen", ["template", "generisch"],
        "Ein **Template** ist eine Vorlage, aus der der Übersetzer für "
        "jeden benutzten Typ eine eigene Fassung erzeugt:\n\n"
        "    template <typename T>\n"
        "    T quadrat(T x) { return x * x; }\n\n"
        "    quadrat(3);      // erzeugt die int-Fassung\n"
        "    quadrat(3.0);    // erzeugt die double-Fassung\n\n"
        "Der entscheidende Punkt: Das geschieht beim **Übersetzen**. Es gibt "
        "keine Typprüfung zur Laufzeit, keinen virtuellen Aufruf, keinen "
        "Umweg — der erzeugte Code ist genau so schnell, wie wenn man ihn "
        "von Hand für `double` geschrieben hätte.\n\n"
        "Deshalb sind Strömungslöser in C++ oft von oben bis unten "
        "templatisiert: Derselbe Code rechnet in `float` auf der GPU und in "
        "`double` auf der CPU, und man kann für eine Fehleruntersuchung "
        "einen Typ mit mehr Stellen einsetzen, ohne eine Zeile zu ändern.\n\n"
        "Die Kehrseite: Fehlermeldungen werden lang, und der Übersetzer "
        "braucht länger. In C löst man dasselbe mit Präprozessormakros — "
        "schneller getippt, aber ohne jede Typprüfung.\n\n"
        "**Wann der Code entsteht.** Erst bei der Benutzung. Ein Template, "
        "das nie aufgerufen wird, erzeugt keinen Maschinencode -- und seine "
        "Fehler zeigen sich auch erst dann. Deshalb die Gewohnheit, "
        "Templates in Kopfdateien zu schreiben: der Übersetzer muss den "
        "Rumpf an der Stelle sehen, an der er die Fassung erzeugt.\n\n"
        "**Was ein Template vom Typ verlangt,** steht nirgends "
        "geschrieben -- es ergibt sich daraus, was im Rumpf benutzt wird. "
        "Steht dort `a > b`, muss der Typ vergleichbar sein; steht dort "
        "`v.size()`, braucht er diese Funktion. Genau daher die langen "
        "Fehlermeldungen. Seit C++20 lassen sich die Anforderungen mit "
        "Concepts hinschreiben, und die Meldung nennt dann die verletzte "
        "Bedingung statt einer Zeile tief im Rumpf.\n\n"
        "**Der Preis heißt Codegröße.** Jede benutzte Typkombination "
        "erzeugt eigenen Maschinencode. Bei einem Löser, der in `float`, "
        "`double` und `long double` vorliegt, ist das Programm dreimal so "
        "groß -- auf einem Telefon ein Argument, in einem Rechenzentrum "
        "keines.",
        "",
        [
            predict("Was schreibt dieses Programm?",
                    "#include <iostream>\n\n"
                    "template <typename T>\n"
                    "T groesser(T a, T b) { return a > b ? a : b; }\n\n"
                    "int main()\n{\n"
                    "    std::cout << groesser(3, 7) << \" \"\n"
                    "              << groesser(2.5, 1.5) << std::endl;\n"
                    "}\n",
                    "7 2.5",
                    "Der Übersetzer erzeugt zwei Fassungen: eine für `int` "
                    "und eine für `double`. Hätte man `groesser(3, 2.5)` "
                    "geschrieben, gäbe es einen Fehler — die Vorlage hat "
                    "**einen** Typ T, und der kann nicht gleichzeitig int "
                    "und double sein.\n\n"
                    "Zu retten wäre der Aufruf mit zwei Typparametern (`template "
                    "<typename A, typename B>`) oder durch eine ausdrückliche Angabe: "
                    "`groesser<double>(3, 2.5)`. Der Übersetzer wandelt dann die 3 in "
                    "3.0 um. Beides ist üblich; die erste Form braucht allerdings eine "
                    "Antwort auf die Frage, welchen Typ das Ergebnis hat.",
                    run=True),
            mc("Was kostet ein Template zur Laufzeit gegenüber einer von "
               "Hand geschriebenen Fassung?",
               ["Nichts — der Code wird beim Übersetzen erzeugt.",
                "Einen virtuellen Aufruf je Benutzung.",
                "Eine Typprüfung je Aufruf.",
                "Etwa zehn Prozent."], 0,
               "Das ist der Grund, warum numerischer C++-Code Templates "
               "benutzt und nicht Vererbung: Vererbung kostet bei jedem "
               "Aufruf einen Sprung über eine Tabelle, ein Template kostet "
               "nur Übersetzungszeit.\n\n"
               "Der Sprung selbst ist nicht das Schlimmste: Er verhindert, dass "
               "der Übersetzer die Funktion an Ort und Stelle einsetzt, und damit "
               "auch das Vektorisieren der inneren Schleife. In einem Stencil, der "
               "milliardenfach ausgeführt wird, ist das der Unterschied zwischen "
               "einem und acht Werten je Takt."),
            parsons("Setze eine Template-Funktion zusammen, die das Maximum "
                    "eines Feldes liefert.",
                    ["template <typename T>",
                     "T groesster(const std::vector<T>& v)",
                     "{",
                     "    T m = v[0];",
                     "    for (std::size_t i = 1; i < v.size(); ++i)",
                     "        if (v[i] > m) m = v[i];",
                     "    return m;",
                     "}"],
                    "`const std::vector<T>&` statt `std::vector<T>`: kein "
                    "Kopieren und die Zusage, nichts zu ändern. Und "
                    "`v.size()` liefert `std::size_t`, weshalb der Zähler "
                    "denselben Typ hat — ein `int` gäbe hier je nach "
                    "Übersetzer eine Warnung.\n\n"
                    "`std::size_t` ist vorzeichenlos -- was eine eigene Falle "
                    "mitbringt: eine Rückwärtsschleife `for (std::size_t i = v.size() "
                    "- 1; i >= 0; --i)` endet nie, weil `i` nach null auf die größte "
                    "Zahl springt. Entweder rückwärts mit `i-- > 0` zählen oder den "
                    "Index als vorzeichenbehaftete Zahl führen.",
                    distractors=["std::vector<T> v;",
                                 "for (int i = 0; i < v.size(); i++)"]),
        ]),
])




# ---------------------------------------------------------------------------
# 11 -- Rust: Werte, Typen, Ausgabe
# ---------------------------------------------------------------------------
#
# Laeuft wirklich, aber nicht mit rustc: neben der App liegt "rrun", ein
# eigener Deuter fuer genau den Ausschnitt, den dieser Kurs lehrt. Warum
# kein echter Uebersetzer -- rustc mit LLVM sind Hunderte Megabyte, und
# schon ein Einzeiler braeuchte auf diesem Geraet laenger als eine ganze
# Lektion. Was der Deuter kann und was nicht, steht in der ersten Lektion;
# so zu tun, als sei er rustc, waere die eine Luege, die eine Lernapp sich
# nicht leisten darf.

K13 = chapter("rs-werte", "Rust: Werte und Typen", 13, "rust",
              "Dieselben Rechnungen wie in Kapitel 1, in einer Sprache, die "
              "nichts stillschweigend umwandelt -- und die dafür die Fehler "
              "meldet, die in C erst im Ergebnis auffallen.", [

    lesson("rs-erstes", "Das erste Rust-Programm", ["fn main", "println"],
        "Jedes Rust-Programm beginnt in `fn main()`. Ausgegeben wird mit dem "
        "Makro `println!` -- das Ausrufezeichen gehört zum Namen und sagt, "
        "dass hier kein gewöhnlicher Aufruf steht, sondern etwas, das der "
        "Übersetzer vor dem Übersetzen einsetzt.\n\n"
        "Die Platzhalter heißen `{}` und tragen keinen Typ: `{}` passt auf "
        "eine Zahl so gut wie auf Text. Nachkommastellen schreibt man "
        "`{:.3}`.\n\n"
        "**Warum `{}` ohne Typ auskommt.** In C sagt `%d` dem `printf`, wie "
        "es die Bytes lesen soll -- passt der Platzhalter nicht zum Wert, "
        "kommt Unsinn heraus, und meist merkt es niemand. In Rust erzeugt "
        "das Makro für jeden Wert den passenden Ausgabecode, und zwar beim "
        "Übersetzen. Ein falscher Platzhalter ist damit kein stiller "
        "Fehler, sondern gar kein Programm.\n\n"
        "**Was `!` sonst noch bedeutet.** Makros können Dinge, die eine "
        "Funktion nicht kann: beliebig viele Argumente nehmen, ihre "
        "Zeichenkette beim Übersetzen prüfen und Code erzeugen. Dafür sieht "
        "man ihnen am Ausrufezeichen an, dass sie keine gewöhnlichen "
        "Funktionen sind. `vec![]` weiter hinten ist das zweite Makro, das "
        "der Kurs braucht.\n\n"
        "**Was dieser Deuter ist und was nicht.** Neben der App liegt "
        "`rrun`, ein Deuter für genau den Ausschnitt, den dieser Kurs "
        "lehrt -- ein echter Rust-Übersetzer passt auf dieses Gerät nicht. "
        "Er kennt `let`, Funktionen, `if`, Schleifen, `Vec`, Strukturen, "
        "Besitz und Ausleihen, und er meldet die drei wichtigen Fehler mit "
        "den echten Nummern (E0382, E0499, E0502). Er prüft aber **während "
        "des Laufs**, nicht vorher, und er kennt keine Lebensdauern über "
        "Funktionsgrenzen. Wer hier ein Programm zum Laufen bringt, hat es "
        "noch nicht an rustc vorbei -- aber die Denkfehler, um die es geht, "
        "sieht er alle.\n\n"
        "Gezeichnet wird wie in C: jede Zeile, die mit `plot` beginnt, wird "
        "zu einem Punkt einer Kurve.",
        "fn main() {\n"
        "    let schritte = 100;\n"
        "    let dt = 0.01;\n\n"
        "    println!(\"{} Schritte zu je {:.3} s\", schritte, dt);\n"
        "    println!(\"Gesamtzeit: {:.2} s\", schritte as f64 * dt);\n"
        "}\n",
        [
            predict("Was schreibt dieses Programm?",
                    "fn main() {\n"
                    "    print!(\"a\");\n"
                    "    println!(\"b\");\n"
                    "}\n",
                    "ab",
                    "`print!` schreibt ohne Zeilenumbruch, `println!` mit. "
                    "Das ist dieselbe Unterscheidung wie in C zwischen "
                    "`printf(\"a\")` und `printf(\"a\\n\")` -- nur steht sie "
                    "hier im Namen statt in der Zeichenkette.\n\n"
                    "Der Umbruch am Ende ist kein Schönheitsfehler: Die "
                    "Ausgabe wird zeilenweise wirklich hinausgeschrieben. "
                    "Wer den Fortschritt einer langen Rechnung ohne Umbruch "
                    "ausgibt, sieht minutenlang nichts."),
            mc("Wie gibt man eine Kommazahl mit drei Nachkommastellen aus?",
               ["println!(\"{:.3}\", x)", "println!(\"%.3f\", x)",
                "println!(\"{:3}\", x)", "println!(\"{}\", x.round(3))"], 0,
               "Die Form steht nach einem Doppelpunkt **im** Platzhalter. "
               "`{:3}` wäre etwas anderes: drei Zeichen breit, rechts "
               "ausgerichtet -- eine Breitenangabe, keine Genauigkeit.\n\n"
               "`%.3f` ist die C-Form; sie geht hier nicht, weil `println!` "
               "die Vorlage beim Übersetzen liest und dabei jeden "
               "Platzhalter mit seinem Wert zusammenbringt. Genau daher "
               "kommt auch die Fehlermeldung, wenn mehr `{}` dastehen als "
               "Werte dahinter."),
            code("Schreibe ein Programm, das `Hallo Simulation` in einer "
                 "eigenen Zeile ausgibt.",
                 "fn main() {\n"
                 "    \n"
                 "}\n",
                 "Hallo Simulation",
                 "fn main() {\n"
                 "    println!(\"Hallo Simulation\");\n"
                 "}\n",
                 "Ein `println!` mit dem Text -- der Umbruch steckt im "
                 "Namen.\n\n"
                 "Auffällig für Umsteiger: kein `#include`, kein "
                 "`return 0;`. Was `println!` braucht, ist über das "
                 "Vorspiel (`std::prelude`) schon da, und `main` ohne "
                 "Rückgabetyp meldet dem Betriebssystem von selbst den "
                 "Erfolg. Fehler meldet man in Rust nicht mit einer Zahl, "
                 "sondern mit einem Rückgabewert, der den Fehler trägt."),
        ],
        output="100 Schritte zu je 0.010 s\nGesamtzeit: 1.00 s\n"),

    lesson("rs-zahlen", "Ganzzahl und Kommazahl, streng getrennt",
        ["typen", "as"],
        "Rust kennt dieselbe Ganzzahlfalle wie C -- `7 / 2` ist `3` --, aber "
        "es kennt die zweite, viel unangenehmere Hälfte nicht: **es wandelt "
        "nie stillschweigend um**.\n\n"
        "    let n = 10;\n"
        "    let h = 1.0 / n;        // Fehler, kein Ergebnis\n"
        "    let h = 1.0 / n as f64; // so ist es gemeint\n\n"
        "In C wäre `1.0 / n` gültig und richtig, `1 / n` gültig und falsch. "
        "Rust lehnt die Mischung ab und zwingt dazu, die Umwandlung "
        "hinzuschreiben. Der Fehler aus Kapitel 1, der in echten "
        "Simulationen am längsten unentdeckt bleibt, ist hier kein Fehler "
        "mehr, den man machen kann.\n\n"
        "**Was die Typen heißen.** `i64` ist die vorzeichenbehaftete "
        "Ganzzahl mit 64 Bit, `f64` die Kommazahl mit doppelter "
        "Genauigkeit -- dieselben acht Byte wie ein `double` in C, "
        "dieselben etwa fünfzehn Stellen, dieselben Fallen aus dem Kapitel "
        "„Fließkomma lügt“. Für Indizes gibt es `usize`: vorzeichenlos und "
        "so breit wie eine Adresse.\n\n"
        "**Typen stehen selten da.** `let dt = 0.01;` ist ein `f64`, ohne "
        "dass es jemand hinschreibt -- der Übersetzer schließt es aus dem "
        "Wert und aus dem, was später damit geschieht. Hinschreiben kann "
        "man ihn trotzdem: `let dt: f64 = 0.01;`. In einer Signatur ist es "
        "Pflicht, und das ist Absicht: Eine Funktion soll man lesen können, "
        "ohne ihren Rumpf zu lesen.\n\n"
        "**Überlauf ist kein Schweigen.** `i64` läuft in C still über und "
        "rechnet mit Unsinn weiter. Rust bricht im Prüflauf ab und rechnet "
        "erst im geschliffenen Lauf mit Umlauf -- und wer den Umlauf "
        "wirklich will, schreibt `wrapping_add`. Auch hier dieselbe Linie: "
        "Was gemeint ist, steht da.",
        "fn main() {\n"
        "    let n = 4;\n"
        "    let h = 1.0 / n as f64;\n"
        "    let ganz = 7 / 2;\n"
        "    println!(\"h = {:.3}\", h);\n"
        "    println!(\"7 / 2 = {}\", ganz);\n"
        "    println!(\"7.0 / 2.0 = {}\", 7.0 / 2.0);\n"
        "}\n",
        [
            predict("Was schreibt das Programm?",
                    "fn main() {\n"
                    "    let a = 7;\n"
                    "    let b = 2;\n"
                    "    println!(\"{}\", a / b);\n"
                    "    println!(\"{:.3}\", a as f64 / b as f64);\n"
                    "}\n",
                    "3\n3.500",
                    "Zwei Ganzzahlen ergeben eine Ganzzahldivision, genau "
                    "wie in C. Der Unterschied ist die zweite Zeile: Sie "
                    "**muss** die Umwandlung hinschreiben.\n\n"
                    "`a as f64 / b as f64` wandelt beide um; `a as f64 / b` "
                    "wäre schon ein Fehler, weil links eine Kommazahl und "
                    "rechts eine Ganzzahl stünde. Rust hat keine "
                    "Beförderung des kleineren Typs -- die halbe "
                    "Fehlerklasse aus C fällt damit weg."),
            mc("Ein Gitter der Länge 1 hat `let n = 10;` Zellen. Welche "
               "Zeile berechnet den Zellabstand?",
               ["let h = 1.0 / n as f64;", "let h = 1.0 / n;",
                "let h: f64 = 1 / n;", "let h = (1 / n) as f64;"], 0,
               "Die zweite Zeile ist ein Übersetzungsfehler (`f64` und "
               "`i64` vertragen sich nicht), die dritte auch. Die vierte "
               "übersetzt sogar -- und ist die C-Falle in Rust-Kleidung: "
               "`1 / n` ist bereits `0`, die Umwandlung kommt zu spät.\n\n"
               "Merksatz wie in C: **der Typ des Ergebnisses entsteht im "
               "Ausdruck, nicht bei der Zuweisung.** Rust nimmt einem nur "
               "die Fälle ab, in denen man die Umwandlung ganz vergessen "
               "hat."),
            code("Das Programm soll den Mittelwert von `summe` und "
                 "`anzahl` mit drei Nachkommastellen ausgeben. Repariere "
                 "die Rechnung.",
                 "fn main() {\n"
                 "    let summe = 7;\n"
                 "    let anzahl = 2;\n"
                 "    println!(\"{}\", summe);\n"
                 "    println!(\"{}\", anzahl);\n"
                 "}\n",
                 "3.500",
                 "fn main() {\n"
                 "    let summe = 7;\n"
                 "    let anzahl = 2;\n"
                 "    println!(\"{:.3}\", summe as f64 / anzahl as f64);\n"
                 "}\n",
                 "Beide Seiten umwandeln, dann teilen. Die Vorlage gibt "
                 "die Zahlen einzeln aus, damit sie überhaupt läuft -- "
                 "gefragt ist eine einzige Zeile mit der Rechnung.\n\n"
                 "Wer es lieber ohne `as` hat, schreibt die Werte gleich "
                 "als Kommazahlen: `let summe = 7.0;`. In einem Löser ist "
                 "das die übliche Antwort -- Zellzahlen bleiben `usize`, "
                 "alles Gerechnete ist von Anfang an `f64`, und "
                 "Umwandlungen stehen genau an der Grenze dazwischen."),
        ],
        output="h = 0.250\n7 / 2 = 3\n7.0 / 2.0 = 3.5\n"),
])


# ---------------------------------------------------------------------------
# 12 -- Rust: Besitz und Ausleihen
# ---------------------------------------------------------------------------

K14 = chapter("rs-besitz", "Rust: Besitz und Ausleihen", 14, "rust",
              "Der Teil, den es in C nicht gibt und der die Sprache erklärt: "
              "Jeder Wert hat genau einen Besitzer, und wer ihn nur lesen "
              "will, leiht ihn aus. Dafür entfallen die drei Fehlerarten, "
              "die numerischen Code sonst nachts aufwecken.", [

    lesson("rs-besitz-lektion", "Ein Wert, ein Besitzer", ["besitz", "clone"],
        "In C ist eine Zuweisung eine Kopie der Bytes -- bei einem Zeiger "
        "also eine zweite Adresse auf dieselben Daten. Wer sie freigibt, "
        "entscheidet niemand; daher die doppelten `free`, die hängenden "
        "Zeiger und die Speicherlecks.\n\n"
        "Rust legt fest: **jeder Wert hat genau einen Besitzer.** Eine "
        "Zuweisung gibt den Besitz weiter, und die alte Variable ist danach "
        "nicht mehr benutzbar:\n\n"
        "    let a = vec![0.0; 5];\n"
        "    let b = a;          // der Besitz wandert zu b\n"
        "    println!(\"{}\", a.len());   // Fehler E0382\n\n"
        "Das ist keine Schikane, sondern der Grund, warum am Ende des "
        "Blocks genau **einmal** freigegeben wird -- ohne Aufräumer und "
        "ohne Zählung zur Laufzeit. Es ist dasselbe RAII wie in C++, nur "
        "vom Übersetzer geprüft statt von der Aufmerksamkeit des Autors.\n\n"
        "**Wer nicht verschoben wird.** Kleine Werte, deren Kopie nichts "
        "kostet -- `i64`, `f64`, `bool` -- sind `Copy`: bei ihnen kopiert "
        "die Zuweisung, und das Original bleibt. Deshalb fällt in den "
        "ersten Lektionen gar nicht auf, dass es Besitz gibt. Sobald "
        "`String`, `Vec` oder eine eigene Struktur im Spiel ist, fällt es "
        "sofort auf.\n\n"
        "**Die drei Wege, trotzdem weiterzuarbeiten:**\n\n"
        "    let b = a.clone();  // eine echte Kopie, kostet auch echt\n"
        "    let b = &a;         // nur ausleihen, lesen (nächste Lektion)\n"
        "    fn f(v: Vec<f64>) -> Vec<f64>  // nehmen und zurückgeben\n\n"
        "`clone` ist mit Absicht sichtbar. In Sprachen, die still kopieren, "
        "steht die teuerste Zeile eines Lösers oft unscheinbar mitten im "
        "Code; hier steht sie mit Namen da.\n\n"
        "**Was beim Funktionsaufruf geschieht.** Ein Parameter ohne `&` "
        "nimmt den Besitz. `nimm(u)` macht `u` beim Aufrufer unbrauchbar -- "
        "gewollt, wenn die Funktion den Wert wirklich übernimmt (etwa, um "
        "ihn in eine Liste zu hängen), und fast immer falsch, wenn sie nur "
        "hineinsehen will. Deshalb steht in numerischem Rust vor fast jedem "
        "Gitterparameter ein `&`.",
        "fn main() {\n"
        "    let gitter = vec![0.0; 5];\n"
        "    let kopie = gitter.clone();\n"
        "    let weitergegeben = gitter;\n\n"
        "    println!(\"weitergegeben: {} Zellen\", weitergegeben.len());\n"
        "    println!(\"Kopie:         {} Zellen\", kopie.len());\n"
        "}\n",
        [
            mc("Warum meldet `let b = a; println!(\"{}\", a.len());` einen "
               "Fehler, wenn `a` ein `Vec` ist?",
               ["Weil der Besitz an `b` übergegangen ist und `a` danach "
                "nicht mehr gilt.",
                "Weil `Vec` keine Länge hat.",
                "Weil `a` nicht `mut` ist.",
                "Weil `b` nicht benutzt wird."], 0,
               "Ein `Vec` ist nicht `Copy`: Die Zuweisung verschiebt ihn. "
               "Danach ist `a` leer im Sinne der Sprache -- der Übersetzer "
               "verbietet jeden weiteren Zugriff.\n\n"
               "Der Sinn dahinter ist die Freigabe: Gäbe es zwei gültige "
               "Namen für dasselbe Gitter, müsste zur Laufzeit jemand "
               "mitzählen, wer als Letzter geht. Genau diese Zählung spart "
               "Rust -- und genau deshalb braucht es hier eine Regel, die "
               "beim Übersetzen greift."),
            predict("Was schreibt dieses Programm?",
                    "fn main() {\n"
                    "    let a = 5;\n"
                    "    let b = a;\n"
                    "    println!(\"{} {}\", a, b);\n"
                    "}\n",
                    "5 5",
                    "`i64` ist `Copy` -- hier wird kopiert, nicht "
                    "verschoben, und `a` gilt weiter. Mit `Vec` an "
                    "derselben Stelle wäre es ein Fehler.\n\n"
                    "Die Grenze verläuft dort, wo eine Kopie teuer oder "
                    "gefährlich würde: Zahlen liegen vollständig im "
                    "Register, ein `Vec` hätte danach zwei Besitzer für "
                    "denselben Speicherblock. Eigene Strukturen sind "
                    "deshalb standardmäßig nicht `Copy`; man kann es "
                    "anfordern, wenn alle Felder es sind."),
            code("Das Programm soll die Länge **beider** Gitter ausgeben, "
                 "des ursprünglichen und des zweiten. Ändere die mittlere "
                 "Zeile so, dass `u` weiter benutzbar bleibt.",
                 "fn main() {\n"
                 "    let u = vec![0.0; 7];\n"
                 "    let v = u.clone();\n"
                 "    println!(\"{} {}\", u.len(), v.len());\n"
                 "}\n",
                 "7 7",
                 "fn main() {\n"
                 "    let u = vec![0.0; 7];\n"
                 "    let v = u.clone();\n"
                 "    println!(\"{} {}\", u.len(), v.len());\n"
                 "}\n",
                 "`clone()` ist hier richtig, weil wirklich zwei Gitter "
                 "gebraucht werden -- so wie der Löser aus Kapitel 6 zwei "
                 "Felder braucht.\n\n"
                 "Wäre nur zu lesen, wäre `&u` das Mittel der Wahl und "
                 "würde nichts kosten. Die Frage, die man sich an jeder "
                 "solchen Stelle stellt, lautet deshalb: Brauche ich einen "
                 "zweiten Wert -- oder nur einen zweiten Blick?"),
        ],
        output="weitergegeben: 5 Zellen\nKopie:         5 Zellen\n"),

    lesson("rs-ausleihen", "Ausleihen: & und &mut", ["ausleihe", "aliasing"],
        "Ausleihen heißt: hineinsehen dürfen, ohne zu besitzen. Es gibt "
        "genau zwei Sorten:\n\n"
        "    fn summe(v: &Vec<f64>) -> f64        // lesen\n"
        "    fn skalieren(v: &mut Vec<f64>, f: f64) // ändern\n\n"
        "Und die eine Regel, aus der fast alles folgt: **entweder beliebig "
        "viele `&`, oder genau ein `&mut` -- nie beides zugleich.**\n\n"
        "**Warum diese Regel?** Weil zwei Wege zu denselben Daten, von "
        "denen einer schreibt, genau die Lage sind, in der Datenrennen und "
        "ungültig gewordene Zeiger entstehen. In C ist das die Normallage; "
        "man merkt es an den Kommentaren („Achtung: darf nicht dasselbe "
        "Feld sein“) und an Schlüsselwörtern wie `restrict`, mit denen man "
        "dem Übersetzer verspricht, was er nicht prüfen kann. In Rust ist "
        "es das, was der Übersetzer prüft.\n\n"
        "**Was das einbringt, ist nicht nur Sicherheit.** Wenn `&mut` "
        "bedeutet, dass niemand sonst hinsieht, darf der Übersetzer Werte "
        "in Registern halten, Schleifen umstellen und vektorisieren, ohne "
        "sich abzusichern -- dieselbe Freiheit, die `restrict` in C von "
        "Hand verspricht.\n\n"
        "**Am Aufruf sichtbar.** `skalieren(&mut u, 2.5)` zeigt an der "
        "Aufrufstelle, dass `u` verändert wird. In C++ steht dort nur "
        "`skalieren(u, 2.5)`, und ob es eine Referenz ist, verrät erst die "
        "Deklaration. Das ist einer der Gründe, warum Rust-Code auch ohne "
        "Werkzeuge lesbar bleibt.\n\n"
        "**Wie lange eine Ausleihe lebt:** so lange sie gebraucht wird, "
        "nicht bis zum Ende des Blocks. Wer nach der letzten Benutzung "
        "eines `&` wieder ein `&mut` nimmt, bekommt keinen Fehler. Diese "
        "Regel heißt nicht-lexikalische Lebensdauer und hat Rust deutlich "
        "angenehmer gemacht, als es früher war.\n\n"
        "**`for x in &v`** leiht das Gitter für die Schleife aus, statt es "
        "zu verschieben -- `for x in v` würde es aufbrauchen, und danach "
        "wäre `v` weg. Derselbe Unterschied, dieselbe Regel.",
        "fn summe(v: &Vec<f64>) -> f64 {\n"
        "    let mut s = 0.0;\n"
        "    for x in v {\n"
        "        s = s + x;\n"
        "    }\n"
        "    s\n"
        "}\n\n"
        "fn skalieren(v: &mut Vec<f64>, f: f64) {\n"
        "    for i in 0..v.len() {\n"
        "        v[i] = v[i] * f;\n"
        "    }\n"
        "}\n\n"
        "fn main() {\n"
        "    let mut u = vec![1.0, 2.0, 3.0, 4.0];\n"
        "    println!(\"vorher  {:.1}\", summe(&u));\n"
        "    skalieren(&mut u, 2.5);\n"
        "    println!(\"nachher {:.1}\", summe(&u));\n"
        "}\n",
        [
            mc("Welche Kombination von Ausleihen auf dieselbe Variable ist "
               "erlaubt?",
               ["Drei `&` gleichzeitig.",
                "Ein `&` und ein `&mut` gleichzeitig.",
                "Zwei `&mut` gleichzeitig.",
                "Ein `&mut` und zwei `&` gleichzeitig."], 0,
               "Lesen schließt sich nicht gegenseitig aus -- beliebig "
               "viele `&` sind kein Problem. Sobald einer schreibt, darf "
               "sonst niemand hinsehen.\n\n"
               "Das ist genau die Bedingung, unter der ein Programm auch "
               "auf mehreren Kernen richtig bleibt: Die Regel, die hier "
               "einen Fehler im Einprozessorprogramm verhindert, ist "
               "dieselbe, die Datenrennen unmöglich macht. Deshalb sagt "
               "man in Rust „fearless concurrency“ -- nicht, weil "
               "Nebenläufigkeit einfach wäre, sondern weil dieselbe "
               "Prüfung sie mit abdeckt."),
            predict("Was schreibt dieses Programm?",
                    "fn verdoppeln(x: &mut f64) {\n"
                    "    *x = *x * 2.0;\n"
                    "}\n\n"
                    "fn main() {\n"
                    "    let mut a = 2.5;\n"
                    "    verdoppeln(&mut a);\n"
                    "    println!(\"{}\", a);\n"
                    "}\n",
                    "5",
                    "Der Stern löst den Verweis auf, genau wie in C -- "
                    "`*x = *x * 2.0` schreibt in die Variable des "
                    "Aufrufers. Beim Lesen in Rechnungen darf er meist "
                    "entfallen, beim Schreiben nie.\n\n"
                    "Ausgegeben wird `5` und nicht `5.0`: Der "
                    "Anzeigedruck `{}` schreibt die kürzeste Form, die "
                    "die Zahl zurückliest. Wer `5.0` sehen will, nimmt "
                    "`{:.1}`."),
            code("Schreibe `fn groesster(v: &Vec<f64>) -> f64`, die den "
                 "größten Wert liefert, und gib ihn mit einer "
                 "Nachkommastelle aus. Fang beim ersten Element an, nicht "
                 "bei null.",
                 "fn groesster(v: &Vec<f64>) -> f64 {\n"
                 "    let m = v[0];\n"
                 "    m\n"
                 "}\n\n"
                 "fn main() {\n"
                 "    let u = vec![3.0, 9.0, 2.0, 7.0];\n"
                 "    println!(\"{:.1}\", groesster(&u));\n"
                 "}\n",
                 "9.0",
                 "fn groesster(v: &Vec<f64>) -> f64 {\n"
                 "    let mut m = v[0];\n"
                 "    for i in 1..v.len() {\n"
                 "        if v[i] > m {\n"
                 "            m = v[i];\n"
                 "        }\n"
                 "    }\n"
                 "    m\n"
                 "}\n\n"
                 "fn main() {\n"
                 "    let u = vec![3.0, 9.0, 2.0, 7.0];\n"
                 "    println!(\"{:.1}\", groesster(&u));\n"
                 "}\n",
                 "Derselbe Anfangswert wie in C: `v[0]`, nicht `0.0` -- "
                 "sonst wäre das Maximum eines Feldes aus lauter negativen "
                 "Werten null.\n\n"
                 "Zwei Rust-Eigenheiten stecken darin: `m` braucht `mut`, "
                 "weil es sich ändert, und die letzte Zeile hat kein "
                 "Semikolon. Ein Block **ist** in Rust ein Ausdruck; sein "
                 "Wert ist die letzte Zeile ohne Semikolon, und genau das "
                 "wird zurückgegeben. `return m;` ginge auch und wird "
                 "meist nur für den vorzeitigen Ausstieg benutzt."),
        ],
        output="vorher  10.0\nnachher 25.0\n"),
])


# ---------------------------------------------------------------------------
# 13 -- Rust: ein Loeser
# ---------------------------------------------------------------------------

K15 = chapter("rs-loeser", "Rust: ein Löser", 15, "rust",
              "Dieselbe Wärmeleitung und dieselbe Feder wie in den "
              "C-Kapiteln — Zeile für Zeile vergleichbar, mit denselben "
              "Zahlen am Ende. Was sich ändert, ist, was der Übersetzer "
              "dabei mitprüft.", [

    lesson("rs-vec", "Vec, zwei Felder und der Tausch", ["vec", "swap"],
        "`Vec<f64>` ist das Gitter: ein zusammenhängender Block Kommazahlen "
        "mit bekannter Länge, der sich beim Verlassen des Blocks selbst "
        "freigibt. Es ist dasselbe wie `std::vector<double>` in C++ -- und "
        "dasselbe, was man in C aus `malloc`, einer mitgeschleppten Länge "
        "und einem `free` an jedem Ausgang zusammenbaut.\n\n"
        "    let mut u = vec![0.0; n];   // n Zellen, alle 0.0\n"
        "    u[n / 2] = 1.0;\n"
        "    for i in 0..u.len() { ... }\n\n"
        "**Der Index ist geprüft.** `u[41]` bei 41 Zellen bricht das "
        "Programm mit einer klaren Meldung ab, statt fremden Speicher zu "
        "beschreiben. Das kostet einen Vergleich je Zugriff -- in der "
        "inneren Schleife eines Lösers spürbar, aber nicht so spürbar, wie "
        "die meisten annehmen, weil der Übersetzer die Prüfung oft aus der "
        "Schleife herausziehen kann. Wer sie wirklich los sein muss, hat "
        "Wege dafür; sie beginnen alle damit, dass man zeigt, warum der "
        "Index nicht danebenliegen kann.\n\n"
        "**Der Tausch.** Der explizite Löser braucht zwei Felder und "
        "schreibt das neue über das alte. In C tauscht man zwei Zeiger; in "
        "Rust tut das `std::mem::swap(&mut u, &mut w)` -- zwei "
        "veränderliche Ausleihen auf zwei verschiedene Variablen, und "
        "getauscht werden die Innereien, nicht der Inhalt. Kostet nichts, "
        "egal wie groß das Gitter ist.\n\n"
        "**Warum `&mut u` und `&mut w` zugleich erlaubt sind:** Es sind "
        "zwei verschiedene Variablen. Verboten wären zwei `&mut` auf "
        "**dieselbe** Sache -- und genau deshalb kann `swap` sicher sein: "
        "Die Signatur verlangt zwei veränderliche Ausleihen, und die "
        "Sprache garantiert, dass es dann nicht zweimal dasselbe Feld ist. "
        "In C ist `swap(&a, &a)` ein Aufruf, den niemand aufhält.\n\n"
        "**Die Ränder** bleiben wie in Kapitel 6 stehen: Die Schleife läuft "
        "von 1 bis n-2, die Zellen 0 und n-1 behalten ihren Wert. Das "
        "Ergebnis ist Zahl für Zahl dasselbe wie im C-Kapitel -- "
        "Fließkomma rechnet in jeder Sprache gleich.",
        "fn schritt(u: &Vec<f64>, w: &mut Vec<f64>, r: f64) {\n"
        "    let n = u.len();\n"
        "    for i in 1..n - 1 {\n"
        "        w[i] = u[i] + r * (u[i - 1] - 2.0 * u[i] + u[i + 1]);\n"
        "    }\n"
        "}\n\n"
        "fn main() {\n"
        "    let n = 41;\n"
        "    let r = 0.4;\n"
        "    let mut u = vec![0.0; n];\n"
        "    let mut w = vec![0.0; n];\n"
        "    u[n / 2] = 1.0;\n\n"
        "    for _schritt in 0..200 {\n"
        "        schritt(&u, &mut w, r);\n"
        "        std::mem::swap(&mut u, &mut w);\n"
        "    }\n\n"
        "    let mut summe = 0.0;\n"
        "    for i in 0..n {\n"
        "        summe = summe + u[i];\n"
        "    }\n"
        "    println!(\"Mitte {:.6}  Summe {:.6}\", u[n / 2], summe);\n"
        "}\n",
        [
            mc("Warum nimmt `schritt` das alte Feld als `&Vec<f64>` und "
               "das neue als `&mut Vec<f64>`?",
               ["Weil aus dem alten nur gelesen und in das neue nur "
                "geschrieben wird -- die Signatur sagt es.",
                "Weil `&mut` schneller ist.",
                "Weil Rust zwei Parameter verlangt.",
                "Weil sonst kopiert würde."], 0,
               "Die Signatur ist hier die Dokumentation: Wer sie liest, "
               "weiß, welches Feld der Schritt anfasst, ohne den Rumpf zu "
               "lesen. In C steht dort zweimal `double *`, und man muss "
               "nachsehen.\n\n"
               "Nebenbei fällt damit ein ganzer Fehler weg: `schritt(&u, "
               "&mut u, r)` -- altes und neues Feld dasselbe -- wird "
               "abgelehnt, weil `&` und `&mut` auf dieselbe Variable nicht "
               "zusammen gehen. Genau dieser Aufruf ist in C erlaubt und "
               "ergibt still das Gauß-Seidel-Verfahren statt des "
               "expliziten."),
            predict("Was schreibt dieses Programm?",
                    "fn main() {\n"
                    "    let mut a = vec![1.0, 2.0];\n"
                    "    let mut b = vec![9.0, 9.0];\n"
                    "    std::mem::swap(&mut a, &mut b);\n"
                    "    println!(\"{} {}\", a[0], b[0]);\n"
                    "}\n",
                    "9 1",
                    "`swap` vertauscht die beiden Gitter vollständig -- "
                    "danach steht in `a`, was in `b` war. Kopiert wird "
                    "dabei nichts: Getauscht werden Zeiger, Länge und "
                    "Platz, die drei Zahlen, aus denen ein `Vec` besteht.\n\n"
                    "Deshalb ist der Tausch in einer Zeitschleife über "
                    "Millionen Schritte kostenlos, während `u = w.clone()` "
                    "das ganze Gitter jedes Mal kopieren würde."),
            code("Baue den Wärmeleitungsschritt in `schritt` ein: die "
                 "inneren Zellen aus dem Drei-Punkt-Stern, die Ränder "
                 "bleiben. Dann läuft das Programm 200 Schritte und gibt "
                 "Mitte und Summe mit sechs Stellen aus.",
                 "fn schritt(u: &Vec<f64>, w: &mut Vec<f64>, r: f64) {\n"
                 "    let n = u.len();\n"
                 "    for i in 1..n - 1 {\n"
                 "        w[i] = u[i];\n"
                 "    }\n"
                 "}\n\n"
                 "fn main() {\n"
                 "    let n = 41;\n"
                 "    let mut u = vec![0.0; n];\n"
                 "    let mut w = vec![0.0; n];\n"
                 "    u[n / 2] = 1.0;\n"
                 "    for _s in 0..200 {\n"
                 "        schritt(&u, &mut w, 0.4);\n"
                 "        std::mem::swap(&mut u, &mut w);\n"
                 "    }\n"
                 "    let mut summe = 0.0;\n"
                 "    for i in 0..n {\n"
                 "        summe = summe + u[i];\n"
                 "    }\n"
                 "    println!(\"{:.6} {:.6}\", u[n / 2], summe);\n"
                 "}\n",
                 "0.031086 0.771801",
                 "fn schritt(u: &Vec<f64>, w: &mut Vec<f64>, r: f64) {\n"
                 "    let n = u.len();\n"
                 "    for i in 1..n - 1 {\n"
                 "        w[i] = u[i] + r * (u[i - 1] - 2.0 * u[i] + u[i + 1]);\n"
                 "    }\n"
                 "}\n\n"
                 "fn main() {\n"
                 "    let n = 41;\n"
                 "    let mut u = vec![0.0; n];\n"
                 "    let mut w = vec![0.0; n];\n"
                 "    u[n / 2] = 1.0;\n"
                 "    for _s in 0..200 {\n"
                 "        schritt(&u, &mut w, 0.4);\n"
                 "        std::mem::swap(&mut u, &mut w);\n"
                 "    }\n"
                 "    let mut summe = 0.0;\n"
                 "    for i in 0..n {\n"
                 "        summe = summe + u[i];\n"
                 "    }\n"
                 "    println!(\"{:.6} {:.6}\", u[n / 2], summe);\n"
                 "}\n",
                 "Dieselben Zahlen wie im C-Kapitel: 0.031086 und "
                 "0.771801. Dasselbe Verfahren, dieselbe Fließkommaarith"
                 "metik -- die Sprache ändert am Ergebnis nichts.\n\n"
                 "Was sie ändert, ist die Fehlersuche davor: `2.0` muss "
                 "`2.0` heißen und nicht `2`, das alte Feld ist als `&` "
                 "erkennbar nur zum Lesen da, und ein Index daneben bricht "
                 "mit Meldung ab, statt still eine fremde Variable zu "
                 "beschreiben.",
                 seconds=25),
        ],
        output="Mitte 0.031086  Summe 0.771801\n"),

    lesson("rs-struct", "Strukturen und die Feder", ["struct", "methoden"],
        "Eine `struct` fasst zusammen, was zusammengehört -- wie in C, nur "
        "ohne das vorangestellte Wort `struct` bei jeder Benutzung:\n\n"
        "    struct Teilchen {\n"
        "        x: f64,\n"
        "        v: f64,\n"
        "    }\n"
        "    let p = Teilchen { x: 1.0, v: 0.0 };\n\n"
        "**Jedes Feld wird gesetzt.** Es gibt keine halb gefüllte Struktur "
        "und keinen Zufallsinhalt: Wer ein Feld vergisst, bekommt einen "
        "Fehler (E0063). Das ist dieselbe Linie wie beim Besitz -- "
        "uninitialisierter Speicher ist in Rust kein Zustand, den ein "
        "Programm erreichen kann.\n\n"
        "**Zugriff mit dem Punkt, auch durch Verweise.** In C braucht man "
        "den Pfeil (`p->x`), sobald ein Zeiger im Spiel ist. Rust löst den "
        "Verweis beim Punkt von selbst auf: `p.x` schreibt sich gleich, ob "
        "`p` eine Struktur ist oder eine Ausleihe darauf. Der Pfeil "
        "entfällt ersatzlos.\n\n"
        "**Eine Funktion, die die Struktur ändert,** nimmt `&mut Teilchen` "
        "-- und an der Aufrufstelle steht `schritt(&mut p, 0.05)`. Wieder "
        "sieht man am Aufruf, dass etwas verändert wird.\n\n"
        "**Was hier bewusst fehlt:** In echtem Rust schreibt man solche "
        "Funktionen als Methoden in einen `impl`-Block, also "
        "`p.schritt(0.05)`, wobei der erste Parameter `&mut self` heißt. "
        "Das ist Zucker um genau dieselbe Sache -- und der Deuter dieser "
        "App kennt es nicht, weil es am Verständnis nichts ändert und der "
        "Aufwand groß wäre. Wer draußen Rust liest, wird `impl` aber "
        "überall sehen; dass es nur eine andere Schreibweise für die "
        "Funktion mit `&mut` als erstem Parameter ist, ist das Wichtige "
        "daran.\n\n"
        "**Das Ergebnis am Ende ist dasselbe wie in Kapitel 3:** 0.4912 "
        "nach 400 Schritten mit dem symplektischen Verfahren -- erst die "
        "Geschwindigkeit, dann der Ort. Die Reihenfolge der beiden Zeilen "
        "entscheidet auch hier über die Energie, und keine Sprache der "
        "Welt nimmt einem diese Entscheidung ab.",
        "struct Teilchen {\n"
        "    x: f64,\n"
        "    v: f64,\n"
        "}\n\n"
        "fn schritt(p: &mut Teilchen, dt: f64) {\n"
        "    let a = -p.x;\n"
        "    p.v = p.v + a * dt;\n"
        "    p.x = p.x + p.v * dt;\n"
        "}\n\n"
        "fn energie(p: &Teilchen) -> f64 {\n"
        "    0.5 * p.v * p.v + 0.5 * p.x * p.x\n"
        "}\n\n"
        "fn main() {\n"
        "    let mut p = Teilchen { x: 1.0, v: 0.0 };\n"
        "    println!(\"Energie am Anfang {:.4}\", energie(&p));\n"
        "    for _i in 0..400 {\n"
        "        schritt(&mut p, 0.05);\n"
        "    }\n"
        "    println!(\"Energie am Ende   {:.4}\", energie(&p));\n"
        "}\n",
        [
            mc("Warum nimmt `energie` ein `&Teilchen` und nicht ein "
               "`Teilchen`?",
               ["Weil sie nur liest -- mit `Teilchen` wäre der Besitz weg "
                "und `p` danach unbenutzbar.",
                "Weil Strukturen immer als Verweis übergeben werden.",
                "Weil `f64` zurückgegeben wird.",
                "Weil sie sonst langsamer wäre."], 0,
               "Eine eigene Struktur ist nicht `Copy`. `energie(p)` würde "
               "sie verschieben, und die nächste Zeile in `main` wäre ein "
               "Fehler.\n\n"
               "Der Nebeneffekt ist derselbe wie bei `const&` in C++: Es "
               "wird nichts kopiert. Bei zwei Kommazahlen wäre das egal, "
               "bei einer Struktur mit einem Gitter darin nicht -- und die "
               "Regel ist dieselbe, egal wie groß die Struktur ist."),
            parsons("Setze einen symplektischen Schritt zusammen: erst die "
                    "Beschleunigung, dann die Geschwindigkeit, dann der "
                    "Ort mit dem **neuen** v.",
                    ["fn schritt(p: &mut Teilchen, dt: f64) {",
                     "    let a = -p.x;",
                     "    p.v = p.v + a * dt;",
                     "    p.x = p.x + p.v * dt;",
                     "}"],
                    "Genau die Reihenfolge aus Kapitel 3: Wer den Ort "
                    "zuerst fortschreibt, hat das explizite Euler-Verfahren "
                    "und eine Energie, die davonläuft.\n\n"
                    "Rust hilft hier nicht -- es ist kein Fehler der "
                    "Sprache, sondern des Verfahrens. Was es hilft: `p` ist "
                    "als `&mut` gekennzeichnet, also weiß der Leser sofort, "
                    "dass diese Funktion den Zustand verändert, und muss "
                    "nicht nach einer versteckten Zuweisung suchen.",
                    distractors=["    p.x = p.x + p.v * dt;  // vor v",
                                 "    let p = Teilchen { x: 0.0, v: 0.0 };"]),
            code("Erweitere das Teilchen um ein Feld `m` für die Masse und "
                 "rechne die Beschleunigung als `-p.x / p.m`. Nimm "
                 "`m = 2.0`, 400 Schritte, `dt = 0.05`, und gib die Energie "
                 "`0.5*m*v*v + 0.5*x*x` am Ende mit vier Stellen aus.",
                 "struct Teilchen {\n"
                 "    x: f64,\n"
                 "    v: f64,\n"
                 "    m: f64,\n"
                 "}\n\n"
                 "fn schritt(p: &mut Teilchen, dt: f64) {\n"
                 "    let a = -p.x;\n"
                 "    p.v = p.v + a * dt;\n"
                 "    p.x = p.x + p.v * dt;\n"
                 "}\n\n"
                 "fn main() {\n"
                 "    let mut p = Teilchen { x: 1.0, v: 0.0, m: 2.0 };\n"
                 "    for _i in 0..400 {\n"
                 "        schritt(&mut p, 0.05);\n"
                 "    }\n"
                 "    println!(\"{:.4}\", 0.5 * p.m * p.v * p.v + 0.5 * p.x * p.x);\n"
                 "}\n",
                 "0.5004",
                 "struct Teilchen {\n"
                 "    x: f64,\n"
                 "    v: f64,\n"
                 "    m: f64,\n"
                 "}\n\n"
                 "fn schritt(p: &mut Teilchen, dt: f64) {\n"
                 "    let a = -p.x / p.m;\n"
                 "    p.v = p.v + a * dt;\n"
                 "    p.x = p.x + p.v * dt;\n"
                 "}\n\n"
                 "fn main() {\n"
                 "    let mut p = Teilchen { x: 1.0, v: 0.0, m: 2.0 };\n"
                 "    for _i in 0..400 {\n"
                 "        schritt(&mut p, 0.05);\n"
                 "    }\n"
                 "    println!(\"{:.4}\", 0.5 * p.m * p.v * p.v + 0.5 * p.x * p.x);\n"
                 "}\n",
                 "Mit der doppelten Masse schwingt dieselbe Feder "
                 "langsamer -- die Kreisfrequenz ist `sqrt(k/m)` --, und "
                 "die Energie bleibt wieder nahe bei 0.5.\n\n"
                 "Beachte, dass `p.m` in der Struktur steht und nicht als "
                 "zweiter Parameter durchgereicht wird. Genau dafür sind "
                 "Strukturen da: Was physikalisch zu einem Teilchen "
                 "gehört, steht an einer Stelle, und die Signatur von "
                 "`schritt` bleibt kurz, auch wenn später Ladung, Radius "
                 "und Kraftgesetz dazukommen.",
                 seconds=25),
        ],
        output="Energie am Anfang 0.5000\nEnergie am Ende   0.4912\n"),
])


CHAPTERS = [K1, K2, K3, K6, K7, K8, K9, K4, K5, K10, K11, K12, K13, K14, K15]

# What the course is meant to cover once it is finished. The placement test
# already scores against these topics, so it can say what to work on even
# where the chapter is still being written.
PLAN = [
    ("c-werte", "Werte und Typen", 1, "c", True),
    ("c-fluss", "Schleifen und Verzweigungen", 2, "c", True),
    ("c-bewegung", "Bewegung integrieren", 3, "c", True),
    ("cpp-grund", "C++: was es bringt", 8, "cpp", True),
    ("py-numpy", "Python und NumPy", 9, "python", True),
    ("cpp-template", "C++: Templates", 12, "cpp", True),
    ("rs-werte", "Rust: Werte und Typen", 13, "rust", True),
    ("rs-besitz", "Rust: Besitz und Ausleihen", 14, "rust", True),
    ("rs-loeser", "Rust: ein Löser", 15, "rust", True),
]


def chapter_by_id(ident):
    for item in CHAPTERS:
        if item["id"] == ident:
            return item
    return None


def lesson_by_id(ident):
    for item in CHAPTERS:
        for entry in item["lessons"]:
            if entry["id"] == ident:
                return item, entry
    return None, None


def all_lessons():
    out = []
    for item in CHAPTERS:
        for entry in item["lessons"]:
            out.append((item, entry))
    return out
