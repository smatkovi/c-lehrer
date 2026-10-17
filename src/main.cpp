// C-Lehrer: C und C++ lernen, mit Blick auf Simulation.
//
// Native C++ over Qt 4.7 and QtQuick 1.1 -- the combination this device has.
// The only part that is not this binary is bin/crun, the C interpreter the
// learner's own programs run in, as a child process.

#include <QApplication>
#include <QDeclarativeComponent>
#include <QDeclarativeContext>
#include <QDeclarativeEngine>
#include <QDeclarativeError>
#include <QDeclarativeView>
#include <QDir>
#include <QFileInfo>
#include <QTextCodec>

#include "Course.h"
#include "Curriculum.h"
#include "Plotter.h"

int main(int argc, char **argv)
{
    QApplication app(argc, argv);
    // The binary's own name, so a second course installed beside this one
    // keeps its own progress file instead of sharing it.
    app.setOrganizationName(QLatin1String("lernapps"));
    app.setApplicationName(QFileInfo(app.applicationFilePath()).fileName());

    // Qt 4 defaults to Latin-1 for QString::fromAscii; the course is German
    // and full of umlauts, so say it once here rather than wrapping every
    // literal.
    QTextCodec::setCodecForCStrings(QTextCodec::codecForName("UTF-8"));
    QTextCodec::setCodecForTr(QTextCodec::codecForName("UTF-8"));

    // The binary sits in <root>/bin, the course and the QML beside it.
    const QString root = QFileInfo(QFileInfo(app.applicationFilePath())
                                   .absolutePath()).absolutePath();

    Curriculum curriculum;
    QString error;
    if (!curriculum.load(root + QLatin1String("/data/kurs.json"), &error)) {
        qWarning("Kurs nicht lesbar: %s", qPrintable(error));
        return 1;
    }

    Plotter *plotter = new Plotter();          // the view takes ownership
    Course course(&curriculum, plotter);

    /* "--qml-pruefen": jede QML-Datei einmal uebersetzen und sagen, welche
       nicht laedt. Der Pruefer auf dem Entwicklungsrechner hilft hier nur
       halb -- com.nokia.meego gibt es dort nicht, und gerade dessen
       Elemente ("Switch hat kein clicked") fallen erst am Geraet auf.
       Also am Geraet, ohne Fenster, in zwei Sekunden. */
    if (argc > 1 && QLatin1String(argv[1]) == QLatin1String("--qml-pruefen")) {
        QDeclarativeEngine engine;
        engine.addImageProvider(QLatin1String("plot"), plotter);
        engine.rootContext()->setContextProperty(QLatin1String("course"), &course);
        const QDir qmlDir(root + QLatin1String("/qml"));
        int schlecht = 0;
        const QStringList dateien = qmlDir.entryList(
                QStringList() << QLatin1String("*.qml"), QDir::Files, QDir::Name);
        for (const QString &name : dateien) {
            QDeclarativeComponent teil(&engine,
                                       QUrl::fromLocalFile(qmlDir.filePath(name)));
            if (teil.isError()) {
                ++schlecht;
                for (const QDeclarativeError &e : teil.errors())
                    qWarning("FEHLER %s: %s", qPrintable(name),
                             qPrintable(e.toString()));
            }
        }
        qWarning("%d QML-Dateien, %d mit Fehler", dateien.size(), schlecht);
        return schlecht ? 1 : 0;
    }

    QDeclarativeView view;
    view.setResizeMode(QDeclarativeView::SizeRootObjectToView);
    view.engine()->addImageProvider(QLatin1String("plot"), plotter);
    view.rootContext()->setContextProperty(QLatin1String("course"), &course);
    view.setSource(QUrl::fromLocalFile(root + QLatin1String("/qml/main.qml")));
    if (view.status() == QDeclarativeView::Error) {
        for (const QDeclarativeError &e : view.errors())
            qWarning("QML: %s", qPrintable(e.toString()));
        return 1;
    }
    view.showFullScreen();
    return app.exec();
}
