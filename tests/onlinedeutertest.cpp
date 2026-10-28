// Was der Online-Blick zusichert, geprueft gegen tests/scheinserver.py
// statt gegen die echte API -- ohne Schluessel, ohne Netz, ohne Kosten:
//   * Die Anfrage traegt die drei Kopfzeilen und einen Rumpf mit einem
//     JPEG-Block (der Scheinserver prueft beides und sagt sonst, was fehlt).
//   * Die Antwort wird tolerant gelesen: Nachdenk-Block davor, Prosa um das
//     JSON herum, "high" statt "hoch".
//   * Ein 401 kommt als ok=false mit der Meldung der API an -- und ohne den
//     Schluessel darin.
//   * abbrechen() unterdrueckt fertig().
//   * schluesselAusProfil() liest die export-Zeile aus ~/.profile.
//
// Uebersetzt mit tools/build-onlinedeutertest.sh.  Qt 5 genuegt; auf
// Harmattan laeuft der andere Zweig, den nur der Cross-Build prueft.
#include "OnlineDeuter.h"
#include "Klassifizierer.h"

#include <QCoreApplication>
#include <QDir>
#include <QEventLoop>
#include <QFile>
#include <QImage>
#include <QProcess>
#include <QTimer>
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

/* Attrappe fuer Klassifizierer.cpp, das hier nicht mitgebaut wird: laedt
   das Bild schlicht und verkleinert es wie das Original. */
QImage Klassifizierer::bildLaden(const QString &pfad, int kante, QString *fehlerText)
{
    QImage bild(pfad);
    if (bild.isNull()) {
        if (fehlerText)
            *fehlerText = QLatin1String("laden");
        return bild;
    }
    if (bild.width() > kante || bild.height() > kante)
        bild = bild.scaled(kante, kante, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    return bild;
}

static QVariantMap karte(const char *id, const char *name)
{
    QVariantMap m;
    m.insert(QLatin1String("id"), QString::fromUtf8(id));
    m.insert(QLatin1String("name"), QString::fromUtf8(name));
    return m;
}

/* Wartet auf fertig() oder das Zeitlimit; gibt zurueck, ob fertig() kam. */
class Empfaenger : public QObject
{
    Q_OBJECT
public:
    QVariantMap antwort;
    int anzahl;
    Empfaenger() : anzahl(0) {}

    bool warten(OnlineDeuter *deuter, int ms)
    {
        QEventLoop schleife;
        QTimer uhr;
        uhr.setSingleShot(true);
        connect(deuter, SIGNAL(fertig(QVariantMap)), this, SLOT(angekommen(QVariantMap)));
        connect(this, SIGNAL(weiter()), &schleife, SLOT(quit()));
        connect(&uhr, SIGNAL(timeout()), &schleife, SLOT(quit()));
        const int vorher = anzahl;
        uhr.start(ms);
        schleife.exec();
        disconnect(deuter, 0, this, 0);
        return anzahl > vorher;
    }

signals:
    void weiter();

private slots:
    void angekommen(const QVariantMap &a)
    {
        antwort = a;
        ++anzahl;
        emit weiter();
    }
};

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);
    const QString server = argc > 1 ? QString::fromLocal8Bit(argv[1])
                                    : QString::fromLatin1("tests/scheinserver.py");
    const QString ablage = QDir::tempPath() + QLatin1String("/onlinedeutertest");
    QDir().mkpath(ablage);

    // Schluessel aus ~/.profile -- mit einem eigenen HOME, das Jolla hat keins.
    {
        QFile profil(ablage + QLatin1String("/.profile"));
        profil.open(QIODevice::WriteOnly | QIODevice::Truncate);
        profil.write("# Kommentar\nexport PATH=$PATH:/opt/bin\n"
                     "export ANTHROPIC_API_KEY=\"sk-schein-123\"\n");
        profil.close();
        qputenv("HOME", ablage.toLocal8Bit());
        pruefe(OnlineDeuter::schluesselAusProfil() == QLatin1String("sk-schein-123"),
               "schluesselAusProfil liest die export-Zeile");
        QFile::remove(profil.fileName());
        pruefe(OnlineDeuter::schluesselAusProfil().isEmpty(),
               "schluesselAusProfil ohne Datei ist leer");
    }

    // Ein kleines Foto: Verlauf von Blau nach Weiss, als JPEG.
    const QString foto = ablage + QLatin1String("/himmel.jpg");
    {
        QImage bild(96, 64, QImage::Format_RGB32);
        for (int y = 0; y < bild.height(); ++y)
            for (int x = 0; x < bild.width(); ++x)
                bild.setPixel(x, y, qRgb(80 + x, 120 + x, 220));
        pruefe(bild.save(foto, "JPEG", 85), "Testfoto als JPEG gespeichert");
        QFile f(foto);
        f.open(QIODevice::ReadOnly);
        const QByteArray kopf = f.read(2);
        pruefe(kopf == QByteArray("\xff\xd8", 2), "JPEG-Erkennung im Prozess (qjpeg laedt)");
    }

    QVariantList klassen;
    klassen << karte("cu-humilis", "Cumulus humilis")
            << karte("cirrus", "Cirrus")
            << karte("stratus", "Stratus");

    // Den Scheinserver starten und seinen Port lesen.
    QProcess schein;
    schein.setProcessChannelMode(QProcess::ForwardedErrorChannel);
    schein.start(QLatin1String("python3"), QStringList() << server);
    pruefe(schein.waitForStarted(5000), "Scheinserver startet");
    pruefe(schein.waitForReadyRead(10000), "Scheinserver nennt seinen Port");
    const QString port = QString::fromLatin1(schein.readLine()).trimmed();
    pruefe(!port.isEmpty(), "Port gelesen");
    const QString basis = QLatin1String("http://127.0.0.1:") + port;
    const QString schluessel = QLatin1String("sk-geheim-ABC");

    OnlineDeuter deuter;
    Empfaenger empf;
    pruefe(OnlineDeuter::verfuegbar(), "verfuegbar() auf Qt 5");
    pruefe(!deuter.laeuft(), "laeuft() vor der Anfrage falsch");

    // 1. Der gute Fall.
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/v1/messages")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("de"), schluessel);
    pruefe(deuter.laeuft(), "laeuft() waehrend der Anfrage wahr");
    pruefe(empf.warten(&deuter, 20000), "fertig() kommt");
    pruefe(!deuter.laeuft(), "laeuft() danach falsch");
    if (!empf.antwort.value(QLatin1String("ok")).toBool())
        std::printf("  Fehlertext: %s\n",
                    empf.antwort.value(QLatin1String("fehler")).toString().toUtf8().constData());
    pruefe(empf.antwort.value(QLatin1String("ok")).toBool(), "ok im guten Fall");
    pruefe(empf.antwort.value(QLatin1String("klasse")).toString() == QLatin1String("cirrus"),
           "klasse cirrus");
    pruefe(empf.antwort.value(QLatin1String("sicherheit")).toString() == QLatin1String("hoch"),
           "sicherheit hoch aus dem Werkzeug");
    pruefe(empf.antwort.value(QLatin1String("begruendung")).toString().contains(QLatin1String("Schleier")),
           "begruendung uebernommen");
    pruefe(empf.antwort.value(QLatin1String("fehler")).toString().isEmpty(),
           "fehler leer im guten Fall");

    // 1b. Der alte Weg: JSON zwischen Prosa im Textblock.
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/text")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("de"), schluessel);
    pruefe(empf.warten(&deuter, 20000), "fertig() kommt bei Text");
    pruefe(empf.antwort.value(QLatin1String("ok")).toBool(), "ok bei JSON im Text");
    pruefe(empf.antwort.value(QLatin1String("klasse")).toString() == QLatin1String("cirrus"),
           "klasse cirrus aus dem Text");
    pruefe(empf.antwort.value(QLatin1String("sicherheit")).toString() == QLatin1String("hoch"),
           "sicherheit 'high' wird zu hoch");

    // 1c. Nur Prosa: nicht lesbar, mit dem Anfang des Textes -- und der
    //     Rumpf liegt zum Nachlesen da.
    const QString protokoll = ablage + QLatin1String("/letzte-antwort.json");
    QFile::remove(protokoll);
    OnlineDeuter::protokollSetzen(protokoll);
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/prosa")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("de"), schluessel);
    pruefe(empf.warten(&deuter, 20000), "fertig() kommt bei Prosa");
    pruefe(!empf.antwort.value(QLatin1String("ok")).toBool(), "ok falsch bei Prosa");
    {
        const QString m = empf.antwort.value(QLatin1String("fehler")).toString();
        pruefe(m.contains(QLatin1String("nicht lesbar")) && m.contains(QLatin1String("Hope that")),
               "Meldung nennt den Anfang der Prosa");
        QFile pf(protokoll);
        pruefe(pf.open(QIODevice::ReadOnly) && pf.readAll().contains("lovely sky"),
               "Rumpf im Protokoll");
        pruefe((pf.permissions() & (QFile::ReadGroup | QFile::ReadOther)) == 0,
               "Protokoll nur fuer den Benutzer lesbar");
    }

    // 1d. Abgeschnitten.
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/abgeschnitten")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("en"), schluessel);
    pruefe(empf.warten(&deuter, 20000), "fertig() kommt bei Abschnitt");
    pruefe(empf.antwort.value(QLatin1String("fehler")).toString().contains(QLatin1String("cut off")),
           "abgeschnitten wird benannt");
    OnlineDeuter::protokollSetzen(QString());
    QFile::remove(protokoll);

    // 1e. Fable nicht zu haben: dieselbe Anfrage noch einmal mit Opus.
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/fable-aus")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("de"), schluessel);
    pruefe(empf.warten(&deuter, 20000), "fertig() kommt nach dem Rueckfall");
    pruefe(empf.antwort.value(QLatin1String("ok")).toBool(), "ok ueber Opus");
    pruefe(empf.antwort.value(QLatin1String("klasse")).toString() == QLatin1String("cirrus"),
           "klasse cirrus von Opus");
    pruefe(empf.antwort.value(QLatin1String("modell")).toString().startsWith(QLatin1String("Opus")),
           "Karte nennt Opus");
    pruefe(empf.antwort.value(QLatin1String("modell")).toString().contains(QLatin1String("Fable")),
           "und sagt, dass Fable fehlte");
    // Der gute Fall nennt Fable.
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/v1/messages")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("de"), schluessel);
    pruefe(empf.warten(&deuter, 20000), "fertig() kommt (Fable)");
    pruefe(empf.antwort.value(QLatin1String("modell")).toString() == QLatin1String("Fable"),
           "Karte nennt Fable");

    // 2. Der 401-Fall.
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/fehler")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("en"), schluessel);
    pruefe(empf.warten(&deuter, 20000), "fertig() kommt bei 401");
    pruefe(!empf.antwort.value(QLatin1String("ok")).toBool(), "ok falsch bei 401");
    const QString meldung = empf.antwort.value(QLatin1String("fehler")).toString();
    pruefe(meldung.contains(QLatin1String("invalid x-api-key")), "Meldung der API im fehler");
    pruefe(!meldung.contains(schluessel), "Schluessel nicht im fehler");
    pruefe(empf.antwort.value(QLatin1String("klasse")).toString().isEmpty(), "klasse leer bei 401");

    // 3. Foto, das es nicht gibt: ok falsch, aber fertig() kommt trotzdem
    //    (und erst aus der Schleife heraus, nicht aus anfragen()).
    {
        const int vorher = empf.anzahl;
        deuter.anfragen(ablage + QLatin1String("/nix.jpg"), klassen, QLatin1String("de"), schluessel);
        pruefe(empf.anzahl == vorher, "fertig() feuert nicht aus anfragen() heraus");
        pruefe(empf.warten(&deuter, 5000), "fertig() kommt bei unlesbarem Foto");
        pruefe(!empf.antwort.value(QLatin1String("ok")).toBool(), "ok falsch bei unlesbarem Foto");
    }

    // 4. Abbruch: der langsame Endpunkt, Abbruch sofort danach -- kein fertig().
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/langsam")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("de"), schluessel);
    pruefe(deuter.laeuft(), "laeuft() vor dem Abbruch wahr");
    deuter.abbrechen();
    pruefe(!deuter.laeuft(), "laeuft() nach dem Abbruch falsch");
    pruefe(!empf.warten(&deuter, 3500), "kein fertig() nach abbrechen()");

    // 5. Nach dem Abbruch geht eine neue Anfrage wieder.
    qputenv("SEGELFLUG_API_URL", (basis + QLatin1String("/v1/messages")).toLatin1());
    deuter.anfragen(foto, klassen, QLatin1String("en"), schluessel);
    pruefe(empf.warten(&deuter, 20000), "fertig() nach einem Abbruch wieder");
    pruefe(empf.antwort.value(QLatin1String("ok")).toBool(), "ok nach einem Abbruch");

    schein.kill();
    schein.waitForFinished(3000);
    QFile::remove(foto);

    std::printf(fehler ? "%d Fehler\n" : "alles gut\n", fehler);
    return fehler ? 1 : 0;
}

#include "onlinedeutertest.moc"
