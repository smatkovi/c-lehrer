// Das Gedaechtnis pruefen -- die Datei, die Korrektur und das
// Zusammenfuehren. Ohne Netz und ohne Telefon: die Abdruecke werden hier
// von Hand gesetzt, damit jede Zahl vorhersagbar ist.
//
// Gebaut von tools/build-nachlernentest.sh, druckt am Ende "alles gut".
#include "Nachlernen.h"

#include <QBuffer>
#include <QCoreApplication>
#include <QDataStream>
#include <QFile>
#include <QDir>
#include <QImage>
#include <QTextStream>
#include <QVector>

#include <cmath>
#include <cstdlib>

namespace {

QTextStream aus(stdout);
int fehler = 0;

void pruefen(bool bedingung, const QString &was)
{
    if (!bedingung) {
        aus << "FEHLER: " << was << "\n";
        ++fehler;
    }
}

void nahe(float ist, float soll, const QString &was, float toleranz = 1e-4f)
{
    if (std::fabs(ist - soll) > toleranz) {
        aus << "FEHLER: " << was << " -- " << ist << " statt " << soll << "\n";
        ++fehler;
    }
}

const int kGroesse = 8;         // kurzer Abdruck, damit sich rechnen laesst
const int kKante = 16;

QStringList klassen()
{
    QStringList k;
    k << QLatin1String("cu-humilis") << QLatin1String("stratocumulus")
      << QLatin1String("cirrus");
    return k;
}

/* Ein Einheitsvektor, der in Richtung `richtung` zeigt, mit etwas
   Beimischung -- so sind die Klassen unterscheidbar, aber nicht orthogonal,
   wie im echten Merkmalsraum. */
QVector<float> abdruck(int richtung, float rauschen = 0.f)
{
    QVector<float> v(kGroesse, 0.f);
    v[richtung % kGroesse] = 1.f;
    v[(richtung + 1) % kGroesse] = rauschen;
    double quadrat = 0.0;
    for (int i = 0; i < v.size(); ++i)
        quadrat += (double)v[i] * v[i];
    const float norm = (float)(1.0 / std::sqrt(quadrat));
    for (int i = 0; i < v.size(); ++i)
        v[i] *= norm;
    return v;
}

/* Ein Bild, das sich von jedem anderen unterscheidet -- gleiche Bilder
   wuerde das Gedaechtnis zusammenlegen. */
QImage bild(int nummer)
{
    QImage b(kKante, kKante, QImage::Format_RGB32);
    for (int y = 0; y < kKante; ++y)
        for (int x = 0; x < kKante; ++x)
            b.setPixel(x, y, qRgb((x * 7 + nummer * 13) & 0xff,
                                  (y * 11 + nummer * 29) & 0xff,
                                  (nummer * 37) & 0xff));
    return b;
}

QVector<float> gleichverteilt()
{
    QVector<float> p(3);
    for (int i = 0; i < 3; ++i)
        p[i] = 1.f / 3.f;
    return p;
}

void fuellen(Nachlernen *g, int jeKlasse)
{
    int n = 0;
    for (int k = 0; k < 3; ++k)
        for (int i = 0; i < jeKlasse; ++i, ++n)
            g->merken(klassen().at(k), Nachlernen::Einig, 3, bild(n),
                      abdruck(k, 0.1f * i), 12.f);
}

}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    /* Mit einem Pfad: nur diese Datei laden und sagen, was drin ist --
       zum Nachsehen, ob eine echte Gelerntes-Datei vom Geraet lesbar ist. */
    if (argc > 1) {
        Nachlernen g;
        QString f;
        if (!g.laden(QString::fromLocal8Bit(argv[1]), &f)) {
            aus << "nicht lesbar: " << f << "\n";
            return 1;
        }
        aus << g.anzahl() << " Eintraege, " << g.brauchtNeurechnung().size()
            << " nachzurechnen\n";
        const QVariantList liste = g.eintraege();
        for (int i = 0; i < liste.size(); ++i) {
            const QVariantMap e = liste.at(i).toMap();
            aus << "  " << e.value(QLatin1String("klasse")).toString()
                << " quelle " << e.value(QLatin1String("quelle")).toInt()
                << " sicherheit " << e.value(QLatin1String("sicherheit")).toInt() << "\n";
        }
        return 0;
    }
    const QString ordner = QDir::tempPath() + QLatin1String("/nachlernentest");
    QDir().mkpath(ordner);
    const QString pfad = ordner + QLatin1String("/gelerntes.bin");
    QFile::remove(pfad);

    aus << "-- Leeres Gedaechtnis\n";
    {
        Nachlernen g;
        g.netzSetzen(QLatin1String("abc123"), klassen());
        QString f;
        pruefen(g.laden(pfad, &f), QLatin1String("fehlende Datei ist kein Fehler"));
        pruefen(g.anzahl() == 0, QLatin1String("leer"));
        pruefen(!g.wirksam(), QLatin1String("leer wirkt nicht"));
        pruefen(g.fehlende() == 20, QLatin1String("zwanzig fehlen"));
        const QVector<float> p = gleichverteilt();
        const QVector<float> q = g.korrigieren(p, abdruck(0));
        pruefen(q == p, QLatin1String("ohne Eintraege bleibt alles, wie es ist"));
    }

    aus << "-- Unter der Schwelle bleibt die Korrektur aus\n";
    {
        Nachlernen g;
        g.netzSetzen(QLatin1String("abc123"), klassen());
        fuellen(&g, 5);                   // 15 Eintraege
        pruefen(g.anzahl() == 15, QLatin1String("fuenfzehn gemerkt"));
        pruefen(!g.wirksam(), QLatin1String("fuenfzehn wirken noch nicht"));
        pruefen(g.fehlende() == 5, QLatin1String("fuenf fehlen"));
        pruefen(g.korrigieren(gleichverteilt(), abdruck(0)) == gleichverteilt(),
                QLatin1String("unter der Schwelle unveraendert"));
    }

    aus << "-- Ueber der Schwelle zieht die gemerkte Klasse\n";
    {
        Nachlernen g;
        g.netzSetzen(QLatin1String("abc123"), klassen());
        fuellen(&g, 8);                   // 24 Eintraege
        pruefen(g.anzahl() == 24, QLatin1String("vierundzwanzig gemerkt"));
        pruefen(g.wirksam(), QLatin1String("vierundzwanzig wirken"));
        pruefen(g.anzahlJeKlasse(klassen().at(1)) == 8, QLatin1String("acht je Klasse"));

        /* Ein Foto, das genau wie die gemerkten Stratocumulus aussieht,
           muss Stratocumulus anheben -- obwohl das Netz nichts weiss. */
        const QVector<float> q = g.korrigieren(gleichverteilt(), abdruck(1));
        pruefen(q.size() == 3, QLatin1String("drei Klassen heraus"));
        pruefen(q.at(1) > q.at(0) && q.at(1) > q.at(2),
                QLatin1String("die aehnliche Klasse fuehrt"));
        double summe = 0.0;
        for (int i = 0; i < q.size(); ++i)
            summe += q.at(i);
        nahe((float)summe, 1.f, QLatin1String("Summe eins"));

        /* Das Gewicht: 24 Eintraege, Halbwert 30 -> w = 24/54 = 0,444.
           Die Netzausgabe bleibt also mit 0,556 drin. Setzt man das Netz
           ganz auf eine andere Klasse, darf das Gedaechtnis es nicht
           einfach ueberstimmen. */
        QVector<float> sicher(3);
        sicher[0] = 0.98f; sicher[1] = 0.01f; sicher[2] = 0.01f;
        const QVector<float> r = g.korrigieren(sicher, abdruck(1));
        pruefen(r.at(0) > r.at(1), QLatin1String("ein sicheres Netz behaelt recht"));

        aus << "-- Schreiben und wieder lesen\n";
        QString f;
        pruefen(g.speichern(pfad, &f), QLatin1String("speichern: ") + f);
        Nachlernen h;
        h.netzSetzen(QLatin1String("abc123"), klassen());
        pruefen(h.laden(pfad, &f), QLatin1String("laden: ") + f);
        pruefen(h.anzahl() == 24, QLatin1String("alle Eintraege zurueck"));
        pruefen(h.nutzbare() == 24, QLatin1String("alle nutzbar"));
        pruefen(h.brauchtNeurechnung().isEmpty(), QLatin1String("nichts nachzurechnen"));
        /* Die Abdruecke sind int8-quantisiert, also nicht bitgenau, aber
           das Ergebnis muss praktisch dasselbe sein. */
        const QVector<float> q2 = h.korrigieren(gleichverteilt(), abdruck(1));
        for (int i = 0; i < q.size(); ++i)
            nahe(q2.at(i), q.at(i), QLatin1String("Korrektur nach dem Laden"), 0.01f);
        pruefen(!h.bildDaten(0).isEmpty(), QLatin1String("Bild ist mitgekommen"));
        pruefen(h.bildDaten(0).startsWith("\xff\xd8"), QLatin1String("Bild ist ein JPEG"));
        pruefen(h.eintraege().size() == 24, QLatin1String("Liste fuer die Oberflaeche"));
        pruefen(h.eintraege().first().toMap()
                .value(QLatin1String("nummer")).toInt() == 23,
                QLatin1String("das Neueste zuerst"));
    }

    aus << "-- Anderes Netz: Bilder bleiben, Abdruecke gehen\n";
    {
        Nachlernen g;
        g.netzSetzen(QLatin1String("ganz-anders"), klassen());
        QString f;
        pruefen(g.laden(pfad, &f), QLatin1String("laden: ") + f);
        /* laden() setzt den Fingerabdruck aus der Datei; netzSetzen danach
           verwirft die Abdruecke, weil sie nicht passen. */
        g.netzSetzen(QLatin1String("ganz-anders"), klassen());
        pruefen(g.anzahl() == 24, QLatin1String("Eintraege bleiben"));
        pruefen(g.nutzbare() == 0, QLatin1String("keiner nutzbar ohne Abdruck"));
        pruefen(g.brauchtNeurechnung().size() == 24, QLatin1String("alle nachzurechnen"));
        pruefen(!g.wirksam(), QLatin1String("ohne Abdruecke keine Korrektur"));
        pruefen(!g.bildDaten(5).isEmpty(), QLatin1String("Bild noch da"));

        // Nachrechnen, wie es die App beim ersten Start tun wuerde.
        for (int i = 0; i < 24; ++i)
            g.abdruckSetzen(i, abdruck(i / 8, 0.1f * (i % 8)), 12.f);
        pruefen(g.nutzbare() == 24, QLatin1String("nach dem Nachrechnen nutzbar"));
        pruefen(g.wirksam(), QLatin1String("wirkt wieder"));
    }

    aus << "-- Klasse, die das Netz nicht kennt\n";
    {
        Nachlernen g;
        QStringList weniger;
        weniger << QLatin1String("cu-humilis") << QLatin1String("cirrus");
        g.netzSetzen(QLatin1String("abc123"), weniger);
        QString f;
        pruefen(g.laden(pfad, &f), QLatin1String("laden: ") + f);
        g.netzSetzen(QLatin1String("abc123"), weniger);
        pruefen(g.anzahl() == 24, QLatin1String("alle Eintraege bleiben in der Datei"));
        pruefen(g.nutzbare() == 16, QLatin1String("nur die bekannten zaehlen"));
        const QVector<float> p(2, 0.5f);
        const QVector<float> q = g.korrigieren(p, abdruck(0));
        pruefen(q.size() == 2, QLatin1String("so viele Klassen wie das Netz hat"));
    }

    aus << "-- Zusammenfuehren zweier Geraete\n";
    {
        Nachlernen zweites;
        zweites.netzSetzen(QLatin1String("abc123"), klassen());
        for (int i = 0; i < 6; ++i)
            zweites.merken(klassen().at(2), Nachlernen::Leser, 0, bild(100 + i),
                           abdruck(2, 0.05f * i), 12.f);
        const QString pfad2 = ordner + QLatin1String("/zweites.bin");
        QString f;
        pruefen(zweites.speichern(pfad2, &f), QLatin1String("zweites speichern: ") + f);

        Nachlernen g;
        g.netzSetzen(QLatin1String("abc123"), klassen());
        pruefen(g.laden(pfad, &f), QLatin1String("laden: ") + f);
        const int neu = g.dazuladen(pfad2, &f);
        pruefen(neu == 6, QLatin1String("sechs neue Eintraege"));
        pruefen(g.anzahl() == 30, QLatin1String("dreissig insgesamt"));
        // Zweimal dasselbe dazuladen darf nichts verdoppeln.
        pruefen(g.dazuladen(pfad2, &f) == 0, QLatin1String("Doppelte werden erkannt"));
        pruefen(g.anzahl() == 30, QLatin1String("immer noch dreissig"));

        pruefen(g.vergessen(0), QLatin1String("einen vergessen"));
        pruefen(g.anzahl() == 29, QLatin1String("neunundzwanzig"));
        pruefen(!g.vergessen(999), QLatin1String("keine Nummer ausserhalb"));
        g.alleVergessen();
        pruefen(g.anzahl() == 0, QLatin1String("alles vergessen"));
    }

    aus << "-- Die letzte Schicht nachtrainieren\n";
    {
        Nachlernen g;
        g.netzSetzen(QLatin1String("abc123"), klassen());
        /* Eine ausgelieferte Schicht, die die Klassen GENAU VERTAUSCHT
           sieht: Richtung 0 heisst bei ihr Klasse 2 und umgekehrt.  Nach
           dem Nachtrainieren auf richtig beschrifteten Beispielen muss sie
           es anders herum haben. */
        QVector<float> w0(3 * kGroesse, 0.f), b0(3, 0.f);
        w0[0 * kGroesse + 2] = 1.f;      // Klasse 0 schaut auf Richtung 2
        w0[1 * kGroesse + 1] = 1.f;
        w0[2 * kGroesse + 0] = 1.f;      // Klasse 2 schaut auf Richtung 0
        g.kopfSetzen(w0, b0);
        pruefen(!g.kopfLohnt(), QLatin1String("leer lohnt sich nicht"));
        fuellen(&g, 14);                  // 42 Eintraege, ueber der Schwelle 40
        pruefen(g.kopfLohnt(), QLatin1String("42 Eintraege lohnen sich"));
        pruefen(!g.kopfAktiv(), QLatin1String("noch nicht nachtrainiert"));
        const int stand = g.stand();
        QVector<float> w, b;
        pruefen(g.kopfNachtrainieren(&w, &b), QLatin1String("nachtrainieren gelingt"));
        pruefen(w.size() == 3 * kGroesse && b.size() == 3, QLatin1String("Masse stimmen"));
        g.kopfUebernehmen(w, b, stand);
        pruefen(g.kopfAktiv(), QLatin1String("jetzt aktiv"));

        /* Das Netz sagt (mit der vertauschten Schicht) fuer Richtung 0
           Klasse 2; die nachtrainierte Schicht muss Klasse 0 sagen. */
        QVector<float> netz(3);
        netz[0] = 0.05f; netz[1] = 0.05f; netz[2] = 0.9f;
        const QVector<float> q = g.korrigieren(netz, abdruck(0));
        pruefen(q.at(0) > q.at(2) && q.at(0) > q.at(1),
                QLatin1String("nachtrainiert sieht Richtung 0 als Klasse 0"));

        // Ein neuer Eintrag macht die alte Schicht ungueltig.
        g.merken(klassen().at(1), Nachlernen::Leser, 0, bild(500), abdruck(1), 12.f);
        pruefen(!g.kopfAktiv(), QLatin1String("nach Aenderung nicht mehr aktiv"));
        // Ein zu altem Stand gerechnetes Ergebnis wird verworfen.
        g.kopfUebernehmen(w, b, stand);
        pruefen(!g.kopfAktiv(), QLatin1String("alter Stand wird verworfen"));
        QVector<float> w2, b2;
        pruefen(g.kopfNachtrainieren(&w2, &b2), QLatin1String("noch einmal"));
        g.kopfUebernehmen(w2, b2, g.stand());
        pruefen(g.kopfAktiv(), QLatin1String("mit neuem Stand aktiv"));

        // Die Laenge ueberlebt die Datei.
        QString f;
        const QString pfad3 = ordner + QLatin1String("/laenge.bin");
        pruefen(g.speichern(pfad3, &f), QLatin1String("speichern: ") + f);
        Nachlernen h;
        h.netzSetzen(QLatin1String("abc123"), klassen());
        h.kopfSetzen(w0, b0);
        pruefen(h.laden(pfad3, &f), QLatin1String("laden: ") + f);
        pruefen(h.kopfLohnt(), QLatin1String("nach dem Laden lohnt es sich wieder"));
        QVector<float> w3, b3;
        pruefen(h.kopfNachtrainieren(&w3, &b3), QLatin1String("und geht"));
    }

    aus << "-- Fassung 1 der Datei (ohne Laenge) wird noch gelesen\n";
    {
        /* So schrieb Segelflug 2.11 / Sailfish 1.18.x: der Abdruck ohne
           seine Laenge.  Die Eintraege muessen ankommen, die Abdruecke
           nicht -- die rechnet die App aus den Bildern nach. */
        const QString alt = ordner + QLatin1String("/fassung1.bin");
        QFile a(alt);
        pruefen(a.open(QIODevice::WriteOnly | QIODevice::Truncate),
                QLatin1String("Fassung 1 schreiben"));
        QDataStream s(&a);
        s.setByteOrder(QDataStream::LittleEndian);
        s.setFloatingPointPrecision(QDataStream::SinglePrecision);
        s.writeRawData("WOLKENG1", 8);
        const QByteArray kopf("{\"abdruck\":8,\"eintraege\":2,\"format\":1,"
                              "\"klassen\":[\"cu-humilis\",\"stratocumulus\",\"cirrus\"],"
                              "\"modell\":\"abc123\"}");
        s << (quint32)kopf.size();
        s.writeRawData(kopf.constData(), kopf.size());
        for (int i = 0; i < 2; ++i) {
            const QByteArray kennung("stratocumulus");
            s << (quint16)kennung.size();
            s.writeRawData(kennung.constData(), kennung.size());
            s << (quint8)0 << (quint8)2 << (qint64)1761580800;
            QByteArray jpeg;
            QBuffer puffer(&jpeg);
            puffer.open(QIODevice::WriteOnly);
            bild(100 + i).save(&puffer, "JPEG", 85);
            puffer.close();
            s << (quint32)jpeg.size();
            s.writeRawData(jpeg.constData(), jpeg.size());
            s << (quint8)1;
            QByteArray roh(kGroesse, '\0');
            roh[i] = 127;
            s.writeRawData(roh.constData(), kGroesse);
            s << (float)(1.f / 127.f);      // Massstab -- und keine Laenge
        }
        a.close();

        Nachlernen g;
        g.netzSetzen(QLatin1String("abc123"), klassen());
        QString f;
        pruefen(g.laden(alt, &f), QLatin1String("Fassung 1 laden: ") + f);
        pruefen(g.anzahl() == 2, QLatin1String("beide Eintraege da"));
        pruefen(g.brauchtNeurechnung().size() == 2,
                QLatin1String("Abdruecke ohne Laenge werden nachgerechnet"));
        pruefen(g.bildDaten(0).startsWith("\xff\xd8"), QLatin1String("Bilder sind da"));
        for (int i = 0; i < 2; ++i)
            g.abdruckSetzen(i, abdruck(1, 0.1f * i), 12.f);
        pruefen(g.nutzbare() == 2, QLatin1String("nach dem Nachrechnen nutzbar"));

        const QString neu = ordner + QLatin1String("/fassung2.bin");
        pruefen(g.speichern(neu, &f), QLatin1String("wieder speichern: ") + f);
        QFile n(neu);
        n.open(QIODevice::ReadOnly);
        const QByteArray geschrieben = n.readAll();
        n.close();
        pruefen(geschrieben.contains("\"format\":2"), QLatin1String("geschrieben wird Fassung 2"));
        Nachlernen h;
        h.netzSetzen(QLatin1String("abc123"), klassen());
        pruefen(h.laden(neu, &f), QLatin1String("Fassung 2 laden: ") + f);
        pruefen(h.anzahl() == 2 && h.brauchtNeurechnung().isEmpty(),
                QLatin1String("mit Laenge: nichts nachzurechnen"));

        // Eine Fassung aus der Zukunft wird abgelehnt, nicht geraten.
        QByteArray zukunft = geschrieben;
        zukunft.replace("\"format\":2", "\"format\":3");
        const QString spaeter = ordner + QLatin1String("/fassung3.bin");
        QFile z(spaeter);
        z.open(QIODevice::WriteOnly | QIODevice::Truncate);
        z.write(zukunft);
        z.close();
        Nachlernen k;
        k.netzSetzen(QLatin1String("abc123"), klassen());
        pruefen(!k.laden(spaeter, &f), QLatin1String("Fassung 3 scheitert"));
        pruefen(f.contains(QLatin1String("Fassung")), QLatin1String("und sagt warum"));
    }

    aus << "-- Kaputte Dateien\n";
    {
        const QString kaputt = ordner + QLatin1String("/kaputt.bin");
        QFile a(kaputt);
        a.open(QIODevice::WriteOnly | QIODevice::Truncate);
        a.write("NICHTDAS");
        a.write(QByteArray(40, 'x'));
        a.close();
        Nachlernen g;
        g.netzSetzen(QLatin1String("abc123"), klassen());
        QString f;
        pruefen(!g.laden(kaputt, &f), QLatin1String("falsche Kennung scheitert"));
        pruefen(!f.isEmpty(), QLatin1String("und sagt warum"));

        // Abgeschnitten mitten im Eintrag.
        QFile voll(pfad);
        voll.open(QIODevice::ReadOnly);
        const QByteArray alles = voll.readAll();
        voll.close();
        const QString halb = ordner + QLatin1String("/halb.bin");
        QFile b(halb);
        b.open(QIODevice::WriteOnly | QIODevice::Truncate);
        b.write(alles.left(alles.size() / 2));
        b.close();
        Nachlernen h;
        h.netzSetzen(QLatin1String("abc123"), klassen());
        pruefen(!h.laden(halb, &f), QLatin1String("abgeschnitten scheitert"));
        pruefen(h.anzahl() == 0, QLatin1String("und laesst nichts halb Gelesenes stehen"));
    }

    if (fehler) {
        aus << fehler << " Fehler\n";
        aus.flush();
        return 1;
    }
    aus << "alles gut\n";
    aus.flush();
    return 0;
}
