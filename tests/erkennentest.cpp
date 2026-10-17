// Was der Erkennungsmodus zusichert, und was sich ohne Geraet pruefen laesst.
//
// Drei Dinge, und alle drei waeren am Telefon muehsam zu bemerken:
//   * Die richtige Antwort steht nicht immer an derselben Stelle (beim
//     Schreiben steht sie vorn, gemischt wird erst hier).
//   * Die Auswahl der ersten Frage besteht aus wirklich verwechselbaren
//     Wolken, nicht aus irgendwelchen.
//   * Zwei Fotos derselben Klasse kommen nicht hintereinander.
//
// Uebersetzt mit tools/build-erkennentest.sh.
#include "Erkennen.h"

#include <QStringList>
#include <QVariantList>
#include <QVariantMap>

#include <cstdio>

static int fehler = 0;

static void pruefe(bool bedingung, const char *was)
{
    if (!bedingung) {
        std::printf("  FEHLER %s\n", was);
        ++fehler;
    }
}

static QVariantMap karte(const QString &id, const QString &name)
{
    QVariantMap m;
    m.insert(QLatin1String("id"), id);
    m.insert(QLatin1String("name"), name);
    return m;
}

int main()
{
    // Vier Klassen, drei Bedeutungen, je drei Fotos.
    QVariantList klassen;
    const char *ids[] = {"a", "b", "c", "d"};
    const char *sinn[] = {"gut", "gut", "schlecht", "egal"};
    for (int i = 0; i < 4; ++i) {
        QVariantMap k = karte(QLatin1String(ids[i]), QLatin1String(ids[i]));
        k.insert(QLatin1String("bedeutung"), QLatin1String(sinn[i]));
        QStringList nah;
        nah << QLatin1String(ids[(i + 1) % 4]);
        k.insert(QLatin1String("verwechselt"), nah);
        k.insert(QLatin1String("erkennen"), QLatin1String("so sieht es aus"));
        k.insert(QLatin1String("bedeutet"), QLatin1String("das heisst es"));
        klassen.append(k);
    }
    QVariantList bedeutungen;
    const char *bids[] = {"gut", "schlecht", "egal"};
    for (int i = 0; i < 3; ++i) {
        QVariantMap b = karte(QLatin1String(bids[i]), QLatin1String(bids[i]));
        bedeutungen.append(b);
    }
    QVariantList fotos;
    for (int i = 0; i < 4; ++i) {
        for (int n = 0; n < 3; ++n) {
            QVariantMap f;
            f.insert(QLatin1String("klasse"), QLatin1String(ids[i]));
            f.insert(QLatin1String("datei"),
                     QString(QLatin1String("%1-%2.jpg")).arg(QLatin1String(ids[i])).arg(n));
            fotos.append(f);
        }
    }

    // -- Durchlauf, zwei Stufen je Foto ------------------------------------
    Erkennen e;
    e.begin(fotos, klassen, bedeutungen, 0, 1234u);
    pruefe(e.total() == 12, "alle zwoelf Fotos im Stapel");

    QList<int> plaetze;
    QString vorige;
    int nebeneinander = 0;
    int durchlaeufe = 0;
    while (e.isRunning()) {
        const QString klasse = e.foto().value(QLatin1String("klasse")).toString();
        if (klasse == vorige)
            ++nebeneinander;
        vorige = klasse;
        ++durchlaeufe;

        // Stufe 0: Wolke
        pruefe(e.phase() == 0, "jedes Foto faengt mit der Wolke an");
        pruefe(e.options().size() == 4, "vier Auswahlmoeglichkeiten");
        pruefe(e.answerIndex() >= 0 && e.answerIndex() < 4,
               "die richtige Antwort ist dabei");
        plaetze.append(e.answerIndex());
        // Die richtige Klasse muss unter den Optionen stehen, und die
        // Nachbarklasse auch -- dafuer steht `verwechselt`.
        QStringList angeboten;
        for (const QVariant &v : e.options())
            angeboten << v.toMap().value(QLatin1String("id")).toString();
        pruefe(angeboten.contains(klasse), "die richtige Wolke steht zur Wahl");
        const int i = QString(QLatin1String("abcd")).indexOf(klasse);
        pruefe(angeboten.contains(QString(QChar(QLatin1Char('a' + (i + 1) % 4)))),
               "die verwechselbare Wolke steht zur Wahl");
        pruefe(!e.checked(), "vor dem Tippen ist nichts geprueft");

        e.answer(e.answerIndex());
        pruefe(e.checked() && e.wasRight(), "richtig getippt ist richtig");
        e.next();

        // Stufe 1: Bedeutung
        pruefe(e.phase() == 1, "danach kommt die Bedeutung");
        pruefe(e.options().size() == 3, "drei Bedeutungen, mehr gibt es nicht");
        const QString soll =
                e.klasse().value(QLatin1String("bedeutung")).toString();
        pruefe(e.options().at(e.answerIndex()).toMap()
                   .value(QLatin1String("id")).toString() == soll,
               "die Bedeutung der Klasse ist die richtige Antwort");
        e.answer((e.answerIndex() + 1) % 3);     // absichtlich daneben
        pruefe(!e.wasRight(), "daneben ist daneben");
        e.next();
    }
    pruefe(durchlaeufe == 12, "zwoelf Fotos durchlaufen");
    pruefe(e.done(), "danach ist es durch");
    pruefe(nebeneinander == 0, "keine zwei gleichen Klassen hintereinander");

    // Die richtige Antwort darf nicht immer an derselben Stelle stehen.
    bool verschieden = false;
    for (int i = 1; i < plaetze.size(); ++i)
        if (plaetze.at(i) != plaetze.at(0))
            verschieden = true;
    pruefe(verschieden, "die richtige Antwort wandert");

    const QVariantMap ergebnis = e.result();
    pruefe(ergebnis.value(QLatin1String("art")).toInt() == 12,
           "zwoelf Wolken richtig");
    pruefe(ergebnis.value(QLatin1String("sinn")).toInt() == 0,
           "keine Bedeutung richtig");
    pruefe(ergebnis.value(QLatin1String("schwach")).toList().isEmpty(),
           "wer alle Wolken trifft, hat keine schwache Klasse");

    // -- Begrenzter Durchlauf ----------------------------------------------
    Erkennen kurz;
    kurz.begin(fotos, klassen, bedeutungen, 5, 7u);
    pruefe(kurz.total() == 5, "auf fuenf Bilder begrenzt");

    // -- Zwei Laeufe, zwei Reihenfolgen ------------------------------------
    Erkennen a, b;
    a.begin(fotos, klassen, bedeutungen, 0, 1u);
    b.begin(fotos, klassen, bedeutungen, 0, 999u);
    pruefe(a.foto().value(QLatin1String("datei")).toString()
           != b.foto().value(QLatin1String("datei")).toString()
           || a.options().size() != b.options().size(),
           "zwei Saaten, zwei Laeufe");

    std::printf(fehler ? "%d Fehler\n" : "alles gut\n", fehler);
    return fehler ? 1 : 0;
}
