import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style

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
                text: "Spielwiese"
                font.pixelSize: Style.titleSize
                color: Style.accent
            }
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                font.pixelSize: Style.smallSize
                color: Style.dim
                text: page.sprache === "python"
                      ? "Zeilen, die mit plot beginnen, werden gezeichnet: "
                        + "print('plot %f %f' % (t, x)) ergibt eine Kurve, "
                        + "print('plot name %f %f' % ...) mehrere."
                      : page.sprache === "rust"
                      ? "Zeilen, die mit plot beginnen, werden gezeichnet: "
                        + "println!(\"plot {} {}\", t, x); ergibt eine Kurve, "
                        + "println!(\"plot name {} {}\", ...) mehrere."
                      : "Zeilen, die mit plot beginnen, werden gezeichnet: "
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
                    text: course.running ? "läuft …" : "Ausführen"
                    width: spalte.width - 140
                    enabled: !course.running
                    onClicked: course.runCode(editor.text, 30, page.sprache)
                }
                Button {
                    text: "Stopp"
                    width: 128
                    enabled: course.running
                    onClicked: course.stopRun()
                }
            }

            OutputBlock { width: parent.width }

            Button {
                width: parent.width
                text: "Zurück"
                onClicked: pageStack.pop()
            }
            Item { width: 1; height: Style.pad }
        }
    }
}
