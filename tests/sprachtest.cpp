/* Prueft ohne Geraet, dass in der englischen Fassung nichts Deutsches
   uebrigbleibt: Plan und die Themen der Einstufung.
 *
 * Auf dem Rechner bauen (Qt 5 reicht, der JSON-Leser steckt hier drin):
 *
 *   g++ -std=c++17 -fPIC -Isrc $(pkg-config --cflags Qt5Core) \
 *       -o sprachtest tests/sprachtest.cpp src/Curriculum.cpp \
 *       $(pkg-config --libs Qt5Core)
 *   ./sprachtest ~/ps/segelflug/data/kurs.json
 *
 * "roh" heisst: `Curriculum::plan()` gibt das {de,en}-Woerterbuch heraus
 * statt eines Textes - wer das an die Oberflaeche reicht, zeigt dem
 * englischen Leser Deutsch.  Genau das war der Fehler; `Course::plan()`
 * uebersetzt jetzt beim Anzeigen. */
#include "Curriculum.h"
#include "Json.h"
#include <QFile>
#include <QJsonDocument>

/* Auf dem Geraet liest QtScript die JSON; hier steht nur Qt5 zur Verfuegung,
   also dieselbe Schnittstelle mit QJsonDocument dahinter - der Test prueft
   den Kurs und die Sprachwahl, nicht den Leser. */
namespace Json {
QVariant parseFile(const QString &path, QString *error)
{
    QFile f(path);
    if (!f.open(QIODevice::ReadOnly)) {
        if (error) *error = QStringLiteral("nicht lesbar");
        return QVariant();
    }
    QJsonParseError e;
    const QJsonDocument doc = QJsonDocument::fromJson(f.readAll(), &e);
    if (doc.isNull()) {
        if (error) *error = e.errorString();
        return QVariant();
    }
    return doc.toVariant();
}
QVariant parse(const QString &, QString *) { return QVariant(); }
QString stringify(const QVariant &, bool) { return QString(); }
bool writeFile(const QString &, const QVariant &) { return false; }
}

#include <QCoreApplication>
#include <QDebug>
#include <cstdio>
#define SAG(...) do { std::printf(__VA_ARGS__); std::printf("\n"); } while (0)
#include <QStringList>

static bool istDeutsch(const QVariant &v)
{
    return v.type() == QVariant::Map;      /* noch ein {de,en}-Paar */
}

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);
    Curriculum k;
    QString fehler;
    if (!k.load(QString::fromLocal8Bit(argv[1]), &fehler)) {
        SAG("Laden schlug fehl: %s", qPrintable(fehler));
        return 1;
    }
    for (const QString &sprache : k.languages()) {
        k.setLanguage(sprache);
        SAG("== Sprache %s", qPrintable(sprache));
        int roh = 0;
        for (const QVariant &p : k.plan()) {
            const QVariantMap e = p.toMap();
            if (istDeutsch(e.value("titel"))) ++roh;
        }
        SAG("   Plan: %d Eintraege, %d davon roh (Woerterbuch statt Text)", int(k.plan().size()), roh);
        QStringList titel;
        for (const QVariant &p : k.plan())
            titel << k.text(p.toMap().value("titel"));
        SAG("   erste drei: %s", qPrintable(titel.mid(0, 3).join(" | ")));
        QStringList themen;
        const QVariantMap t = k.topics();
        for (auto it = t.constBegin(); it != t.constEnd(); ++it)
            themen << k.text(it.value());
        SAG("   Themen: %s", qPrintable(themen.mid(0, 5).join(" | ")));
    }
    return 0;
}
