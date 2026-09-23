# -*- coding: utf-8 -*-
"""The placement test: find out where to start, in about twenty questions.

Adaptive rather than fixed: it starts in the middle, jumps two levels after
the first answers and one level once it has over- and undershot, and stops
when the estimate stops moving. That way a beginner is not walked through
fifteen questions about pointers to be told they are a beginner, and someone
experienced is not asked what printf does.

Every item is multiple choice on purpose -- a placement test is not the
place to fight a phone keyboard.

Levels match the chapter levels in curriculum.PLAN, so the result is
directly the place to carry on from.
"""
from __future__ import unicode_literals


def item(ident, level, topic, q, options, answer, why, code=""):
    return {"id": ident, "level": level, "topic": topic, "q": q,
            "code": code, "options": options, "answer": answer, "why": why}


TOPICS = {
    "grundlagen": "Werte, Typen, Ausgabe",
    "fluss": "Schleifen und Verzweigungen",
    "funktionen": "Funktionen und Fließkomma",
    "zeiger": "Felder und Zeiger",
    "speicher": "Strukturen und Speicher",
    "numerik": "Numerische Verfahren",
    "cpp": "C++",
    "stroemung": "Strömungsmechanik",
    "rust": "Rust: Besitz und Ausleihen",
}

ITEMS = [
    # --- Stufe 1 -----------------------------------------------------------
    item("p-printf", 1, "grundlagen",
         "Was schreibt dieses Programm?",
         ["Hallo", "Hallo mit Zeilenumbruch danach", "\\n", "Nichts"], 1,
         "`\\n` ist kein Text, sondern der Zeilenumbruch.",
         code='printf("Hallo\\n");'),
    item("p-typ", 1, "grundlagen",
         "Welcher Typ passt für eine Zeitschrittweite wie 0.001?",
         ["int", "double", "char", "void"], 1,
         "`int` kann nur ganze Zahlen; 0.001 würde zu 0.",
         code=""),
    # --- Stufe 2 -----------------------------------------------------------
    item("p-intdiv", 2, "grundlagen",
         "Was steht danach in `h`?",
         ["0.1", "0", "1", "Das Programm bricht ab"], 1,
         "Zwei `int` geteilt geben wieder `int`: 1/10 ist 0. Der Klassiker, "
         "der ganze Simulationen still tötet.",
         code="int n = 10;\ndouble h = 1 / n;"),
    item("p-schleife", 2, "fluss",
         "Wie oft läuft der Rumpf?",
         ["3 mal", "4 mal", "5 mal", "Endlos"], 1,
         "`i` nimmt 0, 1, 2, 3 an -- vier Werte. Geprüft wird vor jedem Durchlauf.",
         code="for (i = 0; i < 4; i++) { ... }"),
    # --- Stufe 3 -----------------------------------------------------------
    item("p-euler", 3, "numerik",
         "Eine reibungsfreie Feder wird mit diesem Schritt simuliert. Was "
         "passiert mit der Energie über viele Schwingungen?",
         ["Sie bleibt exakt erhalten", "Sie wächst stetig an",
          "Sie fällt stetig ab", "Sie springt zufällig"], 1,
         "Beide Größen aus den alten Werten fortzuschreiben ist das explizite "
         "Euler-Verfahren; bei Schwingungen pumpt es Energie hinein.",
         code="xn = x + v*dt;\nv  = v + a*dt;\nx  = xn;"),
    item("p-vergleich", 3, "fluss",
         "Welche Zeile prüft, ob `x` den Wert 2 hat?",
         ["if (x = 2)", "if (x == 2)", "if (x -> 2)", "if (x equals 2)"], 1,
         "`=` weist zu; `if (x = 2)` ist immer wahr und verändert `x`.",
         code=""),
    # --- Stufe 4 -----------------------------------------------------------
    item("p-funktion", 4, "funktionen",
         "Was gibt `f(3.0)` zurück?",
         ["6.0", "9.0", "3.0", "Nichts, die Funktion ist falsch"], 1,
         "`x*x` mit x = 3 ist 9.",
         code="double f(double x)\n{\n    return x * x;\n}"),
    item("p-rundung", 4, "funktionen",
         "Was ergibt der Vergleich in C?",
         ["Immer wahr", "Immer falsch", "Hängt vom Übersetzer ab",
          "Ein Übersetzungsfehler"], 1,
         "0.1 + 0.2 ist im Binärformat nicht exakt 0.3. Deshalb vergleicht "
         "man Fließkommazahlen nie mit `==`, sondern über einen Abstand.",
         code="0.1 + 0.2 == 0.3"),
    # --- Stufe 5 -----------------------------------------------------------
    item("p-array", 5, "zeiger",
         "Welcher Index ist der letzte gültige?",
         ["u[10]", "u[9]", "u[0]", "u[11]"], 1,
         "Ein Feld mit 10 Plätzen läuft von 0 bis 9. `u[10]` schreibt daneben "
         "-- und stürzt oft erst viel später ab.",
         code="double u[10];"),
    item("p-zeiger", 5, "zeiger",
         "Was steht nach diesen Zeilen in `a`?",
         ["1.0", "5.0", "Die Adresse von a", "Undefiniert"], 1,
         "`p` zeigt auf `a`, `*p = 5.0` schreibt also in `a`.",
         code="double a = 1.0;\ndouble *p = &a;\n*p = 5.0;"),
    # --- Stufe 6 -----------------------------------------------------------
    item("p-stencil", 6, "numerik",
         "Welcher Ausdruck ist die zweite Ableitung auf einem Gitter mit "
         "Abstand h?",
         ["(u[i+1] - u[i-1]) / (2*h)",
          "(u[i-1] - 2*u[i] + u[i+1]) / (h*h)",
          "(u[i+1] - u[i]) / h",
          "(u[i+1] + u[i-1]) / 2"], 1,
         "Der Drei-Punkt-Stern für die zweite Ableitung. Der erste Ausdruck "
         "ist die zentrale erste Ableitung.",
         code=""),
    item("p-cfl", 6, "numerik",
         "Explizite Wärmeleitung mit r = dt/h². Ab welchem r wird die "
         "Rechnung in 1D instabil?",
         ["r > 0.1", "r > 0.5", "r > 1.0", "Sie ist immer stabil"], 1,
         "Die von-Neumann-Analyse gibt r ≤ 1/2 für das explizite Verfahren "
         "in einer Dimension. Darüber wachsen kurze Wellen mit jedem Schritt.",
         code=""),
    # --- Stufe 7 -----------------------------------------------------------
    item("p-struct", 7, "speicher",
         "Wie greift man über den Zeiger `p` auf das Feld `x` zu?",
         ["p.x", "p->x", "*p.x", "&p.x"], 1,
         "`p->x` ist die Kurzschreibweise für `(*p).x`.",
         code="struct Teilchen *p;"),
    item("p-malloc", 7, "speicher",
         "Wie viel Speicher fordert diese Zeile an?",
         ["100 Byte", "100 double, also meist 800 Byte",
          "Einen Zeiger", "Das hängt vom Betriebssystem ab"], 1,
         "`sizeof(double)` ist auf dieser Maschine 8; `malloc` nimmt eine "
         "Anzahl **Bytes**, nicht Elemente.",
         code="double *u = malloc(100 * sizeof(double));"),
    item("p-2d", 7, "speicher",
         "Ein 2D-Gitter liegt flach im Speicher, `nx` Spalten. Wie kommt man "
         "an die Zelle (i, j)?",
         ["u[i][j]", "u[i * nx + j]", "u[i + j]", "u[j * j + i]"], 1,
         "Das ist die übliche Anordnung in Strömungscodes: eine Zeile nach "
         "der anderen, weil so der Zwischenspeicher der CPU mitspielt.",
         code="double *u = malloc(ny * nx * sizeof(double));"),
    # --- Stufe 8 -----------------------------------------------------------
    item("p-ref", 8, "cpp",
         "Was bewirkt das `&` im Parameter?",
         ["Es übergibt eine Kopie",
          "Es übergibt das Original, das die Funktion ändern kann",
          "Es übergibt die Adresse als Zahl",
          "Es ist in C++ nicht erlaubt"], 1,
         "Eine Referenz ist ein anderer Name für dasselbe Objekt -- ohne "
         "Kopie und ohne Zeigersyntax.",
         code="void schritt(Feld& f);"),
    item("p-raii", 8, "cpp",
         "Wann gibt ein `std::vector` seinen Speicher frei?",
         ["Wenn man delete aufruft",
          "Wenn er den Gültigkeitsbereich verlässt",
          "Am Programmende", "Wenn der Aufräumer läuft"], 1,
         "Das ist RAII: der Destruktor räumt auf, auch wenn eine Ausnahme "
         "den Block verlässt. Deshalb braucht C++-Simulationscode kaum "
         "noch `new` und `delete`.",
         code=""),
    # --- Stufe 9 -----------------------------------------------------------
    item("p-template", 9, "cpp",
         "Wofür steht `T` hier?",
         ["Für einen festen Typ, der später bestimmt wird",
          "Für einen Zeiger", "Für eine Konstante", "Für eine Klasse"], 0,
         "Ein Template wird für jeden benutzten Typ eigens erzeugt -- so "
         "rechnet derselbe Löser in float und in double, ohne Laufzeitkosten.",
         code="template <typename T>\nT quadrat(T x) { return x * x; }"),
    item("p-const-ref", 9, "cpp",
         "Warum nimmt man `const std::vector<double>&` statt "
         "`std::vector<double>` als Parameter?",
         ["Damit der Vektor schneller wächst",
          "Um die Kopie des ganzen Feldes zu vermeiden",
          "Weil vector sonst nicht übergeben werden kann",
          "Damit er automatisch freigegeben wird"], 1,
         "Ein Gitterfeld als Wert zu übergeben kopiert bei jedem Aufruf "
         "Megabyte. `const&` übergibt nichts und verspricht zugleich, nichts "
         "zu ändern.",
         code=""),
    # --- Stufe 10 ----------------------------------------------------------
    item("p-upwind", 10, "stroemung",
         "Advektion mit Geschwindigkeit u > 0. Welche Diskretisierung ist "
         "stabil?",
         ["zentral: (f[i+1] - f[i-1]) / (2h)",
          "stromaufwärts: (f[i] - f[i-1]) / h",
          "stromabwärts: (f[i+1] - f[i]) / h",
          "alle drei gleichermaßen"], 1,
         "Information kommt bei u > 0 von links. Der zentrale Ausdruck ist "
         "genauer, aber ohne Dämpfung instabil; stromabwärts ist immer "
         "instabil.",
         code=""),
    item("p-cfl2", 10, "stroemung",
         "Was besagt die CFL-Zahl u·dt/h ≤ 1 anschaulich?",
         ["Die Rechnung darf höchstens eine Stunde dauern",
          "In einem Zeitschritt darf die Strömung höchstens eine Zelle weit "
          "laufen",
          "Das Gitter muss quadratisch sein",
          "Die Dichte muss konstant bleiben"], 1,
         "Läuft die Information weiter als eine Zelle, holt das Verfahren "
         "sie nicht mehr ein -- kein explizites Schema kann das retten.",
         code=""),
    item("p-druck", 10, "stroemung",
         "Wozu dient der Druckschritt bei inkompressibler Strömung?",
         ["Er erhöht die Genauigkeit",
          "Er macht das Geschwindigkeitsfeld divergenzfrei",
          "Er bestimmt die Temperatur",
          "Er dämpft die Turbulenz"], 1,
         "Der Druck ist bei inkompressibler Strömung keine eigene "
         "Zustandsgröße, sondern genau die Kraft, die div u = 0 erzwingt. "
         "Deshalb steckt in jedem solchen Löser eine Poisson-Gleichung.",
         code=""),

    # --- Stufe 13 bis 15: Rust ---------------------------------------------
    #
    # Ohne Fragen auf diesen Stufen koennte die Einstufung nie in die
    # Rust-Kapitel zeigen -- sie rechnet in denselben Stufen wie der Plan.
    item("p-rs-typen", 13, "rust",
         "Was macht dieses Rust-Programm?",
         ["Es schreibt 0.1",
          "Es übersetzt nicht: i64 und f64 lassen sich nicht mischen",
          "Es schreibt 0",
          "Es schreibt 10"], 1,
         "Rust wandelt nie stillschweigend um. `1.0 / n` mit `n: i64` ist "
         "kein Rundungsfehler wie in C, sondern gar kein Programm -- "
         "gemeint ist `1.0 / n as f64`.",
         code="let n = 10;\nlet h = 1.0 / n;\nprintln!(\"{}\", h);"),
    item("p-rs-besitz", 14, "rust",
         "Was geschieht in der letzten Zeile?",
         ["Sie schreibt 5",
          "Sie ist ein Fehler: der Besitz ist zu b übergegangen",
          "Sie schreibt 0",
          "Sie kopiert das Gitter"], 1,
         "Ein `Vec` ist nicht `Copy`; die Zuweisung verschiebt ihn. Wer "
         "beides braucht, leiht mit `&a` aus oder kopiert mit "
         "`a.clone()` -- und sieht damit im Quelltext, was die Kopie "
         "kostet.",
         code="let a = vec![0.0; 5];\nlet b = a;\nprintln!(\"{}\", a.len());"),
    item("p-rs-ausleihe", 14, "rust",
         "Welche Ausleihen auf dieselbe Variable erlaubt Rust gleichzeitig?",
         ["Beliebig viele `&`",
          "Ein `&` und ein `&mut`",
          "Zwei `&mut`",
          "Beliebig viele `&mut`"], 0,
         "Lesen schließt sich nicht aus, Schreiben schon: entweder "
         "beliebig viele `&` oder genau ein `&mut`. Genau diese Regel "
         "macht Datenrennen unmöglich.",
         code=""),
    item("p-rs-swap", 15, "rust",
         "Wie tauscht ein expliziter Löser in Rust altes und neues Gitter?",
         ["u = w.clone();",
          "std::mem::swap(&mut u, &mut w);",
          "let u = w;",
          "u.copy_from(w);"], 1,
         "`swap` vertauscht Zeiger, Länge und Platz -- die drei Zahlen, "
         "aus denen ein `Vec` besteht. Das kostet nichts, während "
         "`clone()` das ganze Gitter je Zeitschritt kopieren würde.",
         code=""),
]


def by_level(level, used, reach=2):
    """An unused item near this level -- or nothing, if none is near.

    The "or nothing" matters: without it the test keeps handing a beginner
    ever harder questions simply because the easy ones are used up.
    """
    best, distance = None, 99
    for entry in ITEMS:
        if entry["id"] in used:
            continue
        gap = abs(entry["level"] - level)
        if gap < distance:
            best, distance = entry, gap
    if best is None or distance > reach:
        return None
    return best


def by_topic(topic, level, used):
    """An unused item of this topic, as close to the level as possible."""
    best, distance = None, 99
    for entry in ITEMS:
        if entry["id"] in used or entry["topic"] != topic:
            continue
        gap = abs(entry["level"] - level)
        if gap < distance:
            best, distance = entry, gap
    return best


MAX_QUESTIONS = 20
BREADTH = 3          # extra questions at the end, to fill in the profile


class Test(object):
    """Runs the adaptive test and remembers everything for the review.

    Two phases. First adaptive: start in the middle, step two levels while
    the estimate is far off, one once it has over- and undershot, stop as
    soon as it settles. That is usually five to eight questions.

    Then a short breadth phase: a few questions from topics the adaptive
    part never touched, at the level it found. Without it the profile of a
    quick run names two topics out of eight, which is no use for saying
    what to work on.
    """

    def __init__(self):
        self.level = 4.0
        self.step = 2.0
        self.used = []
        self.answers = []        # (item, chosen, correct)
        self.reversals = 0
        self.last_right = None
        self.streak = 0
        self.current = None
        self.phase = "adaptiv"

    def _settled(self):
        if len(self.answers) >= MAX_QUESTIONS:
            return True
        if self.reversals >= 4:
            return True
        # Pinned at an end and still going the same way: the answer is clear.
        if self.streak >= 3 and (self.level <= 1.0 or self.level >= 11.0):
            return True
        return False

    def _seen_topics(self):
        return [entry["topic"] for entry, _, _, _ in self.answers]

    def next_item(self):
        if self.phase == "adaptiv":
            if not self._settled():
                found = by_level(int(round(self.level)), self.used)
                if found is not None:
                    self.current = found
                    self.used.append(found["id"])
                    return found
            self.phase = "breite"
            self.breadth_left = BREADTH

        if self.phase == "breite" and self.breadth_left > 0:
            seen = self._seen_topics()
            for topic in ("grundlagen", "fluss", "funktionen", "zeiger",
                          "speicher", "numerik", "cpp", "stroemung"):
                if topic in seen:
                    continue
                found = by_topic(topic, int(round(self.level)), self.used)
                if found is not None:
                    self.breadth_left -= 1
                    self.current = found
                    self.used.append(found["id"])
                    return found

        self.current = None
        return None

    def answer(self, chosen):
        entry = self.current
        if entry is None:
            return False
        right = (chosen == entry["answer"])
        self.answers.append((entry, chosen, right, self.phase))
        if self.phase != "adaptiv":
            return right        # breadth questions do not move the estimate
        if self.last_right is not None and right != self.last_right:
            self.reversals += 1
            self.step = max(1.0, self.step - 1.0)
            self.streak = 1
        else:
            self.streak += 1
        self.last_right = right
        self.level += self.step if right else -self.step
        self.level = max(1.0, min(11.0, self.level))
        return right

    def done(self):
        return self.current is None and bool(self.answers)

    def asked(self):
        return len(self.answers)

    def result(self):
        """The level to carry on at, plus how each topic went."""
        right = sum(1 for _, _, ok, _ in self.answers if ok)
        solved = [entry["level"] for entry, _, ok, _ in self.answers if ok]
        level = max(solved) if solved else 1
        # Only the adaptive part decides the level. The breadth questions at
        # the end deliberately reach into topics the learner has not met, so
        # counting them would push everyone a level down.
        kern = [(ok) for _, _, ok, phase in self.answers if phase == "adaptiv"]
        share = (sum(1 for ok in kern if ok) / float(len(kern))) if kern else 0.0
        if share < 0.5:
            level = max(1, level - 1)
        level = int(max(1, min(15, level)))

        profile = {}
        for entry, _, ok, _ in self.answers:
            topic = entry["topic"]
            hits, total = profile.get(topic, (0, 0))
            profile[topic] = (hits + (1 if ok else 0), total + 1)
        scored = {}
        for topic in profile:
            hits, total = profile[topic]
            scored[topic] = hits / float(total)

        review = []
        for entry, chosen, ok, _ in self.answers:
            review.append({
                "frage": entry["q"], "code": entry["code"],
                "optionen": entry["options"], "richtig": entry["answer"],
                "gewaehlt": chosen, "korrekt": ok, "warum": entry["why"],
                "thema": TOPICS.get(entry["topic"], entry["topic"]),
                "stufe": entry["level"],
            })
        return {"level": level, "richtig": right, "gesamt": len(self.answers),
                "profil": scored, "rueckblick": review}
