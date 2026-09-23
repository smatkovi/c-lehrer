// Checks the one path the unit tests cannot reach: starting the interpreter,
// splitting its output into text and curves, and painting the picture.
//
// Runs on the device over ssh, so it needs no taps and no screen watching.
// DISPLAY must be set because QPainter's font handling wants a QApplication.

#include <QApplication>
#include <QDir>
#include <QEventLoop>
#include <QImage>
#include <QTextStream>
#include <QTimer>

#include "Checker.h"
#include "Plotter.h"
#include "Runner.h"

static QTextStream out(stdout);

static RunResult runOnce(Runner &runner, const QString &code, int seconds,
                         const QString &language = QLatin1String("c"))
{
    QEventLoop loop;
    QObject::connect(&runner, SIGNAL(finished()), &loop, SLOT(quit()));
    runner.start(code, seconds, language);
    QTimer::singleShot((seconds + 5) * 1000, &loop, SLOT(quit()));
    loop.exec();
    return runner.result();
}

int main(int argc, char **argv)
{
    QApplication app(argc, argv);

    Runner runner;
    runner.setInterpreter(QLatin1String("c"),
                          QLatin1String("/opt/c-lehrer/bin/crun"),
                          QLatin1String(".c"));
    runner.setInterpreter(QLatin1String("python"),
                          QLatin1String("/opt/wunderw/bin/python3.11"),
                          QLatin1String(".py"));
    runner.setWorkingDirectory(QDir::homePath() + QLatin1String("/.cache/c-lehrer"));

    int bad = 0;

    // 1 -- plain output
    {
        const RunResult r = runOnce(runner,
            "#include <stdio.h>\nint main(){ printf(\"%.4f\\n\", 3.5*2); return 0; }\n", 10);
        out << "1 Text:      \"" << r.output << "\"  Fehler=\"" << r.error
            << "\"  " << QString::number(r.seconds, 'f', 2) << " s\n";
        if (!Checker::outputMatches(r.output, QLatin1String("7.0000"))) { out << "   FEHLT\n"; ++bad; }
    }

    // 2 -- two curves and a line of text, the shape the lessons use
    {
        const RunResult r = runOnce(runner,
            "#include <stdio.h>\n#include <math.h>\n"
            "int main(){ int i; double t;\n"
            "  for (i = 0; i < 200; i++) { t = i * 0.05;\n"
            "    printf(\"plot euler %.3f %.5f\\n\", t, sin(t) * (1 + 0.004 * i));\n"
            "    printf(\"plot verlet %.3f %.5f\\n\", t, sin(t)); }\n"
            "  printf(\"fertig %.4f\\n\", t); return 0; }\n", 20);
        out << "2 Kurven:    " << r.curves.size() << "  Punkte="
            << (r.curves.isEmpty() ? 0 : r.curves.at(0).points.size())
            << "  Namen=";
        for (const Curve &c : r.curves) out << c.name << " ";
        out << " Text=\"" << r.output << "\"  "
            << QString::number(r.seconds, 'f', 2) << " s\n";
        if (r.curves.size() != 2) { out << "   FEHLT: zwei Kurven erwartet\n"; ++bad; }

        Plotter plotter;
        plotter.setCurves(r.curves);
        QSize size;
        const QImage image = plotter.requestImage(QLatin1String("1"), &size, QSize(620, 380));
        const QString path = QDir::homePath() + QLatin1String("/plot-test.png");
        if (!image.save(path, "PNG")) { out << "   FEHLT: Bild nicht schreibbar\n"; ++bad; }
        else out << "   Bild " << size.width() << "x" << size.height()
                 << " -> " << path << "\n";
    }

    // 3 -- a program that does not end
    {
        const RunResult r = runOnce(runner,
            "#include <stdio.h>\nint main(){ while (1) { } return 0; }\n", 3);
        out << "3 Endlos:    abgebrochen=" << (r.timedOut ? "ja" : "NEIN")
            << "  nach " << QString::number(r.seconds, 'f', 2) << " s\n";
        if (!r.timedOut) { out << "   FEHLT: haette abbrechen muessen\n"; ++bad; }
    }

    // 4 -- a syntax error, with its line
    {
        const RunResult r = runOnce(runner,
            "#include <stdio.h>\nint main(){ printf(\"x\")\n return 0; }\n", 10);
        out << "4 Fehler:    \"" << r.error << "\"  Zeile=" << r.errorLine << "\n";
        if (r.error.isEmpty()) { out << "   FEHLT: Fehler erwartet\n"; ++bad; }
    }

    // 5 -- a later run must not be killed by an earlier run's timer
    {
        runOnce(runner, "#include <stdio.h>\nint main(){ printf(\"a\\n\"); return 0; }\n", 3);
        const RunResult r = runOnce(runner,
            "#include <stdio.h>\nint main(){ int i; double s = 0;\n"
            "  for (i = 0; i < 60000; i++) s += i;\n"
            "  printf(\"%.0f\\n\", s); return 0; }\n", 30);
        out << "5 Zeitgeber: \"" << r.output << "\"  abgebrochen="
            << (r.timedOut ? "JA" : "nein") << "  "
            << QString::number(r.seconds, 'f', 2) << " s\n";
        if (r.timedOut) { out << "   FEHLT: alter Zeitgeber hat zugeschlagen\n"; ++bad; }
    }

    // 6 -- Python, mit numpy: der Grund, warum das Rad gebaut wurde
    {
        const RunResult r = runOnce(runner,
            "import numpy as np\n"
            "u = np.zeros(101); u[50] = 1.0\n"
            "for _ in range(400):\n"
            "    u[1:-1] += 0.4 * (u[:-2] - 2*u[1:-1] + u[2:])\n"
            "for i in range(0, 101, 10):\n"
            "    print('plot %d %.6f' % (i, u[i]))\n"
            "print('%.6f' % u.sum())\n", 40, QLatin1String("python"));
        out << "6 Python:    \"" << r.output << "\"  Kurven=" << r.curves.size()
            << "  Fehler=\"" << r.error << "\"  "
            << QString::number(r.seconds, 'f', 2) << " s\n";
        if (!r.error.isEmpty() || r.curves.isEmpty()) { out << "   FEHLT\n"; ++bad; }
    }

    // 7 -- ein Python-Fehler mit Zeilennummer
    {
        const RunResult r = runOnce(runner,
            "x = 1\ny = 2\nprint(x + z)\n", 20, QLatin1String("python"));
        out << "7 Py-Fehler: \"" << r.error << "\"  Zeile=" << r.errorLine << "\n";
        if (r.error.isEmpty() || r.errorLine != 3) { out << "   FEHLT\n"; ++bad; }
    }

    out << (bad ? QString("== %1 Fehler\n").arg(bad) : QString("== alles in Ordnung\n"));
    out.flush();
    return bad ? 1 : 0;
}
