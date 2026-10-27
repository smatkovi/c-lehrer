// Der Pruefstand fuer das Wolkennetz, ohne Telefon.
//
//   klassifizierertest <modell.bin> <datei.rgb> [weitere .rgb]
//       je Datei: Name, dann ein Logit je Zeile, dann eine Leerzeile
//   klassifizierertest --bild <modell.bin> <foto.jpg>
//       Bildmasse nach bildLaden() und die drei wahrscheinlichsten Klassen
//   klassifizierertest --zeit <modell.bin> <datei.rgb>
//       Millisekunden fuer fuenf Durchlaeufe von logits()
//
// Exit-Code 0 nur, wenn alles gelesen und gerechnet wurde; der Fehltext
// geht auf stderr.  Die Referenzwerte liefert tests/winzig-modell.py
// (oder training/vergleichen.py fuers echte Modell); den Vergleich macht
// tools/build-klassifizierertest.sh.
//
// QCoreApplication reicht fuer die Bildleser-Plugins; eine QGuiApplication
// wuerde auf dem Jolla ein Fenstersystem anfassen, das niemand will.
#include "Klassifizierer.h"

#include <QCoreApplication>
#include <QElapsedTimer>
#include <QFile>
#include <QStringList>

#include <clocale>
#include <cstdio>

static int fehlschlag(const QString &text)
{
    std::fprintf(stderr, "FEHLER %s\n", qPrintable(text));
    return 1;
}

static bool modellLaden(Klassifizierer &netz, const QString &pfad)
{
    QString fehler;
    if (!netz.laden(pfad, &fehler)) {
        fehlschlag(QString::fromUtf8("%1: %2").arg(pfad).arg(fehler));
        return false;
    }
    return true;
}

static bool rgbLesen(const QString &pfad, int kante, QByteArray *puffer)
{
    QFile datei(pfad);
    if (!datei.open(QIODevice::ReadOnly)) {
        fehlschlag(QString::fromUtf8("%1 laesst sich nicht oeffnen").arg(pfad));
        return false;
    }
    *puffer = datei.readAll();
    if (puffer->size() != kante * kante * 3) {
        fehlschlag(QString::fromUtf8("%1 hat %2 Byte, erwartet %3")
                   .arg(pfad).arg(puffer->size()).arg(kante * kante * 3));
        return false;
    }
    return true;
}

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);
    /* QCoreApplication zieht die Sprache aus der Umgebung; die Logits
       sollen aber mit Punkt kommen, sonst liest sie das Vergleichsskript
       nicht. */
    std::setlocale(LC_NUMERIC, "C");
    const QStringList args = app.arguments();
    if (args.size() < 3)
        return fehlschlag(QString::fromUtf8("Aufruf: klassifizierertest [--bild|--zeit] <modell.bin> <datei...>"));

    Klassifizierer netz;

    if (args.at(1) == QLatin1String("--bild")) {
        if (args.size() != 4)
            return fehlschlag(QString::fromUtf8("--bild braucht Modell und Foto"));
        if (!modellLaden(netz, args.at(2)))
            return 1;
        QString fehler;
        const QImage bild = Klassifizierer::bildLaden(args.at(3), 640, &fehler);
        if (bild.isNull())
            return fehlschlag(QString::fromUtf8("%1: %2").arg(args.at(3)).arg(fehler));
        std::printf("Bild %dx%d\n", bild.width(), bild.height());
        QElapsedTimer uhr;
        uhr.start();
        const QVector<float> anteile = netz.bewerten(bild);
        const qint64 ms = uhr.elapsed();
        if (anteile.isEmpty())
            return fehlschlag(QString::fromUtf8("bewerten() lieferte nichts"));
        const QStringList klassen = netz.klassen();
        if (anteile.size() != klassen.size())
            return fehlschlag(QString::fromUtf8("%1 Anteile fuer %2 Klassen").arg(anteile.size()).arg(klassen.size()));
        float summe = 0.f;
        for (int i = 0; i < anteile.size(); ++i)
            summe += anteile.at(i);
        if (summe < 0.999f || summe > 1.001f)
            return fehlschlag(QString::fromUtf8("Softmax summiert auf %1").arg(summe));
        QVector<bool> genommen(anteile.size(), false);
        for (int rang = 0; rang < 3 && rang < anteile.size(); ++rang) {
            int bester = -1;
            for (int i = 0; i < anteile.size(); ++i)
                if (!genommen.at(i) && (bester < 0 || anteile.at(i) > anteile.at(bester)))
                    bester = i;
            genommen[bester] = true;
            std::printf("%d. %s %.4f\n", rang + 1, qPrintable(klassen.at(bester)), anteile.at(bester));
        }
        std::printf("bewerten: %lld ms\n", (long long)ms);
        return 0;
    }

    if (args.at(1) == QLatin1String("--zeit")) {
        if (args.size() != 4)
            return fehlschlag(QString::fromUtf8("--zeit braucht Modell und .rgb"));
        if (!modellLaden(netz, args.at(2)))
            return 1;
        QByteArray rgb;
        if (!rgbLesen(args.at(3), netz.eingabeGroesse(), &rgb))
            return 1;
        const unsigned char *p = reinterpret_cast<const unsigned char *>(rgb.constData());
        QElapsedTimer uhr;
        uhr.start();
        for (int lauf = 0; lauf < 5; ++lauf)
            if (netz.logits(p).isEmpty())
                return fehlschlag(QString::fromUtf8("logits() lieferte nichts"));
        const qint64 ms = uhr.elapsed();
        std::printf("5 Durchlaeufe: %lld ms (%lld ms je Bild)\n", (long long)ms, (long long)(ms / 5));
        return 0;
    }

    if (!modellLaden(netz, args.at(1)))
        return 1;
    for (int a = 2; a < args.size(); ++a) {
        QByteArray rgb;
        if (!rgbLesen(args.at(a), netz.eingabeGroesse(), &rgb))
            return 1;
        const QVector<float> l = netz.logits(reinterpret_cast<const unsigned char *>(rgb.constData()));
        if (l.size() != netz.klassen().size())
            return fehlschlag(QString::fromUtf8("%1 Logits fuer %2 Klassen").arg(l.size()).arg(netz.klassen().size()));
        std::printf("%s\n", qPrintable(args.at(a)));
        for (int i = 0; i < l.size(); ++i)
            std::printf("%.7g\n", l.at(i));
        std::printf("\n");
    }
    return 0;
}
