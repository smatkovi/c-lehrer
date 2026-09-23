import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// The lesson itself: one idea, a worked example that actually runs, then
// the exercises. Running the example before being asked anything is the
// point -- the learner sees what the code does before having to predict it.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }


    property variant lektion: course.lesson

    Connections {
        target: course
        onLessonChanged: page.lektion = course.lesson
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
                text: page.lektion.leer ? "" : page.lektion.kapitel
                font.pixelSize: Style.smallSize
                color: Style.faint
            }
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                text: page.lektion.leer ? "" : page.lektion.titel
                font.pixelSize: Style.titleSize
                color: Style.accent
            }

            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                text: page.lektion.leer ? "" : Style.rich(page.lektion.text)
                textFormat: Text.RichText
                font.pixelSize: Style.bodySize
                color: Style.text
                lineHeight: 1.25
                lineHeightMode: Text.ProportionalHeight
            }

            Bild {
                width: parent.width
                name: page.lektion.leer || page.lektion.bild === undefined
                      ? "" : page.lektion.bild
            }

            Text {
                text: W.w("Beispiel", course.language)
                font.pixelSize: Style.headSize
                color: Style.text
                visible: !page.lektion.leer && page.lektion.beispiel !== ""
            }

            CodeBlock {
                width: parent.width
                visible: !page.lektion.leer && page.lektion.beispiel !== ""
                code: page.lektion.leer ? "" : page.lektion.beispiel
            }

            Row {
                spacing: Style.gap
                visible: !page.lektion.leer && page.lektion.beispiel !== ""
                Button {
                    text: course.running ? W.w("läuft …", course.language) : W.w("Ausführen", course.language)
                    enabled: !course.running
                    width: spalte.width - 140
                    onClicked: course.runCode(page.lektion.beispiel, 30)
                }
                Button {
                    text: W.w("Stopp", course.language)
                    width: 128
                    enabled: course.running
                    onClicked: course.stopRun()
                }
            }

            OutputBlock { width: parent.width }

            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                visible: course.output === "" && course.error === "" && !course.running
                          && !page.lektion.leer && page.lektion.ausgabe !== ""
                text: W.w("Erwartete Ausgabe:\n", course.language) + (page.lektion.leer ? "" : page.lektion.ausgabe)
                font.family: Style.mono
                font.pixelSize: Style.codeSize
                color: Style.faint
            }

            Button {
                width: parent.width
                text: W.w("Zu den Aufgaben (", course.language) + (page.lektion.leer ? 0 : page.lektion.aufgaben) + ")"
                onClicked: {
                    course.toExercises();
                    pageStack.push(Qt.resolvedUrl("ExercisePage.qml"));
                }
            }

            Item { width: 1; height: Style.pad }
        }
    }
}
