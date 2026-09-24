import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// A blank page with a compiler behind it. Half of learning to program is
// trying something small just to see what happens, and that needs no
// lesson attached.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    // Die Spielwiese hat ihre eigene Sprache. Vorher lief ihr Quelltext mit
    // der Sprache der zuletzt geoeffneten Lektion -- wer aus dem
    // NumPy-Kapitel herkam, bekam auf sein C-Programm einen Syntaxfehler
    // von Python.
    property string sprache: "c"

    property variant vorlagen: {
        "c": "#include <stdio.h>\n#include <math.h>\n\n"
             + "int main()\n{\n    int i;\n\n"
             + "    for (i = 0; i < 100; i++) {\n"
             + "        double t = i * 0.1;\n"
             + "        printf(\"plot %.3f %.5f\\n\", t, sin(t) / (1 + t));\n"
             + "    }\n    return 0;\n}\n",
        "cpp": "#include <cstdio>\n#include <cmath>\n\n"
               + "int main()\n{\n"
               + "    for (int i = 0; i < 100; i++) {\n"
               + "        double t = i * 0.1;\n"
               + "        std::printf(\"plot %.3f %.5f\\n\", t, std::sin(t) / (1 + t));\n"
               + "    }\n    return 0;\n}\n",
        "python": "import math\n\n"
                  + "for i in range(100):\n"
                  + "    t = i * 0.1\n"
                  + "    print('plot %.3f %.5f' % (t, math.sin(t) / (1 + t)))\n",
        "rust": "fn main() {\n"
                + "    for i in 0..100 {\n"
                + "        let t = i as f64 * 0.1;\n"
                + "        println!(\"plot {:.3} {:.5}\", t, t.sin() / (1.0 + t));\n"
                + "    }\n}\n"
    }

    // Gedeutet oder übersetzt? Das erklärt die Wartezeit, die man hier
    // tatsächlich sieht: C und Rust laufen sofort los, Python braucht einen
    // Augenblick zum Hochkommen, C++ fast eine Sekunde zum Übersetzen. Ohne
    // einen Satz dazu sieht das wie eine Aussage über die Sprachen aus — und
    // das wäre falsch.
    property variant artZeile: {
        "c": "C läuft hier gedeutet: picoc liest deinen Text und tut, was dort steht. Kein Übersetzen, also geht es sofort los.",
        "cpp": "C++ wird übersetzt: g++ macht erst Maschinencode daraus und bindet ihn, dann läuft er. Das kostet die Sekunden vor der Ausgabe.",
        "rust": "Rust läuft hier gedeutet: rrun liest deinen Text und tut, was dort steht. Kein Übersetzen, also geht es sofort los.",
        "python": "Python wird gedeutet: CPython liest deinen Text. Der Deuter selbst muss aber erst hochkommen, und das sind die paar Zehntel vor der Ausgabe."
    }

    property string artErklaerung:
        "**Gedeutet** heißt: ein Programm liest deinen Text und tut Zeile für Zeile, was dort steht. Es gibt nichts zu übersetzen, also fängt es sofort an — dafür ist der Deuter beim Laufen die ganze Zeit dabei und kostet Zeit an jeder Zeile.\n\n"
      + "**Übersetzt** heißt: ein Übersetzer macht aus deinem Text einmal Maschinencode, den der Prozessor unmittelbar ausführt. Die Arbeit fällt **vorher** an, dafür läuft das Ergebnis danach schnell.\n\n"
      + "Bei kurzen Programmen sieht man deshalb fast nur das Übersetzen und kaum das Laufen. Bei C++ kommt dazu, dass eine einzige Zeile wie `#include <iostream>` rund 37 000 Zeilen Schablonen hereinholt, die der Übersetzer jedes Mal neu liest — das ist der größte Teil der Wartezeit, nicht dein Programm.\n\n"
      + "Und das sagt nichts darüber, welche Sprache schnell ist: C ist hier nur deshalb sofort da, weil diese App einen kleinen C-Deuter mitbringt. Richtig übersetztes C läuft schneller als alles andere hier — man wartet nur vorher."

    property bool artOffen: false

    property variant zeichen: {
        "c": ["{", "}", "(", ")", ";", "*", "[", "]"],
        "cpp": ["{", "}", "(", ")", ";", "*", "[", "]"],
        // Python hat weder Klammern um Bloecke noch Strichpunkte; was hier
        // fehlt, ist der Doppelpunkt und die Einrueckung.
        "python": [":", "(", ")", "[", "]", "=", "%", "    "],
        // Rust braucht die geschweiften Klammern wie C, dazu das
        // kaufmaennische Und fuer Ausleihen und das Ausrufezeichen der
        // Makros.
        "rust": ["{", "}", "(", ")", ";", "&", "!", "    "]
    }

    function sprachwechsel(neu) {
        if (page.sprache === neu)
            return;
        // Eigenen Text nicht wegwerfen -- nur die unveraenderte Vorlage.
        if (editor.text === page.vorlagen[page.sprache])
            editor.text = page.vorlagen[neu];
        page.sprache = neu;
    }

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }


    Rectangle { anchors.fill: parent; color: Style.bg }

    Flickable {
        anchors.fill: parent
        contentHeight: spalte.height + 2 * Style.pad
        pressDelay: 140
        clip: true

        Column {
            id: spalte
            x: Style.pad
            y: Style.pad
            width: page.width - 2 * Style.pad
            spacing: Style.gap

            Text {
                text: W.w("Spielwiese", course.language)
                font.pixelSize: Style.titleSize
                color: Style.accent
            }
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                font.pixelSize: Style.smallSize
                color: Style.dim
                text: page.sprache === "python"
                      ? W.w("Zeilen, die mit plot beginnen, werden gezeichnet: ", course.language)
                        + W.w("print('plot %f %f' % (t, x)) ergibt eine Kurve, ", course.language)
                        + W.w("print('plot name %f %f' % ...) mehrere.", course.language)
                      : page.sprache === "rust"
                      ? W.w("Zeilen, die mit plot beginnen, werden gezeichnet: ", course.language)
                        + "println!(\"plot {} {}\", t, x); ergibt eine Kurve, "
                        + "println!(\"plot name {} {}\", ...) mehrere."
                      : W.w("Zeilen, die mit plot beginnen, werden gezeichnet: ", course.language)
                        + "printf(\"plot %f %f\\n\", t, x); ergibt eine Kurve, "
                        + "printf(\"plot name %f %f\\n\", ...) mehrere."
            }

            // Die Sprachwahl. Angeboten wird nur, was auf diesem Geraet auch
            // laufen kann -- ohne das Zusatzpaket gibt es kein C++, ohne
            // Python unter /opt kein Python.
            Row {
                spacing: 6
                Repeater {
                    model: [["c", "C"], ["cpp", "C++"], ["rust", "Rust"],
                            ["python", "Python"]]
                    Rectangle {
                        visible: course.canRunLanguage(modelData[0])
                        width: (spalte.width - 18) / 4
                        height: 48
                        radius: 4
                        color: page.sprache === modelData[0] ? Style.accent : Style.panel
                        border.color: Style.panelEdge
                        border.width: 1
                        Text {
                            anchors.centerIn: parent
                            text: modelData[1]
                            font.pixelSize: Style.bodySize
                            color: page.sprache === modelData[0] ? Style.bg : Style.text
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: page.sprachwechsel(modelData[0])
                        }
                    }
                }
            }

            // ---- Gedeutet oder übersetzt? -------------------------------
            Column {
                width: parent.width
                spacing: 6

                Text {
                    width: parent.width
                    wrapMode: Text.WordWrap
                    font.pixelSize: Style.smallSize
                    color: Style.accent
                    text: W.w(page.artZeile[page.sprache], course.language)
                }

                Text {
                    id: artSchalter
                    width: parent.width
                    wrapMode: Text.WordWrap
                    font.pixelSize: Style.smallSize
                    color: Style.dim
                    text: (page.artOffen ? "▾ " : "▸ ")
                          + W.w("Was heißt gedeutet und übersetzt?", course.language)
                    MouseArea {
                        anchors.fill: parent
                        onClicked: page.artOffen = !page.artOffen
                    }
                }

                Text {
                    width: parent.width
                    visible: page.artOffen
                    wrapMode: Text.WordWrap
                    textFormat: Text.RichText
                    font.pixelSize: Style.smallSize
                    color: Style.dim
                    text: Style.rich(W.w(page.artErklaerung, course.language))
                }
            }

            TextArea {
                id: editor
                width: parent.width
                height: 340
                font.family: Style.mono
                font.pixelSize: Style.codeSize
                inputMethodHints: Qt.ImhNoAutoUppercase | Qt.ImhNoPredictiveText
                text: page.vorlagen[page.sprache]
            }

            Row {
                spacing: 6
                Repeater {
                    model: page.zeichen[page.sprache]
                    Rectangle {
                        width: (spalte.width - 42) / 8
                        height: 44
                        radius: 4
                        color: druck.pressed ? Style.accent : Style.panel
                        border.color: Style.panelEdge
                        border.width: 1
                        Text {
                            anchors.centerIn: parent
                            // Die Einrueckung ist vier Leerzeichen; als
                            // Beschriftung waere sie unsichtbar.
                            text: modelData === "    " ? "␣␣" : modelData
                            font.family: Style.mono
                            font.pixelSize: Style.bodySize
                            color: Style.text
                        }
                        MouseArea {
                            id: druck
                            anchors.fill: parent
                            onClicked: {
                                var pos = editor.cursorPosition;
                                editor.text = editor.text.substring(0, pos) + modelData
                                            + editor.text.substring(pos);
                                editor.cursorPosition = pos + modelData.length;
                            }
                        }
                    }
                }
            }

            Row {
                spacing: Style.gap
                Button {
                    text: course.running ? W.w("läuft …", course.language) : W.w("Ausführen", course.language)
                    width: spalte.width - 140
                    enabled: !course.running
                    onClicked: course.runCode(editor.text, 30, page.sprache)
                }
                Button {
                    text: W.w("Stopp", course.language)
                    width: 128
                    enabled: course.running
                    onClicked: course.stopRun()
                }
            }

            OutputBlock { width: parent.width }

            Button {
                width: parent.width
                text: W.w("Zurück", course.language)
                onClicked: pageStack.pop()
            }
            Item { width: 1; height: Style.pad }
        }
    }
}
