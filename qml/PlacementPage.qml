import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style

// One tap answers and the next question appears -- no second tap to
// continue. A test that needs two taps per question feels twice as long.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }


    property variant frage: course.placementQuestion
    property variant ergebnis: course.placementResult

    Connections {
        target: course
        onPlacementChanged: {
            page.frage = course.placementQuestion;
            page.ergebnis = course.placementResult;
        }
    }

    Rectangle { anchors.fill: parent; color: Style.bg }

    // ---- die Fragen -------------------------------------------------------
    Flickable {
        anchors.fill: parent
        contentHeight: fragenSpalte.height + 2 * Style.pad
        visible: !course.placementDone
        pressDelay: 140
        clip: true

        Column {
            id: fragenSpalte
            x: Style.pad
            y: Style.pad
            width: page.width - 2 * Style.pad
            spacing: Style.gap

            Text {
                text: "Frage " + (page.frage.leer ? "" : page.frage.nummer)
                font.pixelSize: Style.smallSize
                color: Style.faint
            }

            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                text: page.frage.leer ? "" : page.frage.frage
                font.pixelSize: Style.headSize
                color: Style.text
            }

            Bild {
                width: parent.width
                name: (page.frage.leer || page.frage.bild === undefined)
                      ? "" : page.frage.bild
            }

            CodeBlock {
                width: parent.width
                code: page.frage.leer ? "" : page.frage.code
                visible: !page.frage.leer && page.frage.code !== ""
            }

            Repeater {
                model: page.frage.leer ? [] : page.frage.optionen
                Rectangle {
                    width: fragenSpalte.width
                    height: optionText.paintedHeight + 24
                    color: druck.pressed ? Style.panelEdge : Style.panel
                    border.color: Style.panelEdge
                    border.width: 1
                    radius: 6

                    Text {
                        id: optionText
                        x: 12
                        y: 12
                        width: parent.width - 24
                        wrapMode: Text.WordWrap
                        text: modelData
                        font.pixelSize: Style.bodySize
                        color: Style.text
                    }
                    MouseArea {
                        id: druck
                        anchors.fill: parent
                        onClicked: course.answerPlacement(index)
                    }
                }
            }

            Item { width: 1; height: Style.pad }
        }
    }

    // ---- das Ergebnis -----------------------------------------------------
    Flickable {
        anchors.fill: parent
        contentHeight: ergebnisSpalte.height + 2 * Style.pad
        visible: course.placementDone
        pressDelay: 140
        clip: true

        Column {
            id: ergebnisSpalte
            x: Style.pad
            y: Style.pad
            width: page.width - 2 * Style.pad
            spacing: Style.gap

            Text {
                text: "Stufe " + (page.ergebnis.leer ? "" : page.ergebnis.level)
                font.pixelSize: Style.titleSize
                color: Style.accent
            }
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                font.pixelSize: Style.bodySize
                color: Style.dim
                text: page.ergebnis.leer ? ""
                      : (page.ergebnis.richtig + " von " + page.ergebnis.gesamt
                         + " Fragen richtig.")
            }

            Panel {
                width: parent.width
                height: weiterBlock.height + 2 * Style.pad
                visible: !page.ergebnis.leer && page.ergebnis.weiterId !== undefined
                         && page.ergebnis.weiterId !== ""

                Column {
                    id: weiterBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: Style.gap

                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        font.pixelSize: Style.bodySize
                        color: Style.text
                        text: page.ergebnis.leer ? ""
                              : ("Der Kurs geht weiter bei:\n"
                                 + page.ergebnis.weiterKapitel + " – "
                                 + page.ergebnis.weiterLektion)
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        font.pixelSize: Style.smallSize
                        color: Style.warn
                        visible: !page.ergebnis.leer && page.ergebnis.ueberStoff === true
                        text: "Du liegst über dem, was bisher geschrieben ist. "
                              + "Die höheren Kapitel kommen noch; bis dahin "
                              + "findest du hier das, was es schon gibt."
                    }
                    Button {
                        width: parent.width
                        text: "Dort weiterlernen"
                        onClicked: {
                            course.startLesson(page.ergebnis.weiterId);
                            pageStack.pop();
                            pageStack.push(Qt.resolvedUrl("LessonPage.qml"));
                        }
                    }
                }
            }

            Panel {
                width: parent.width
                height: schwachSpalte.height + 2 * Style.pad
                visible: !page.ergebnis.leer && page.ergebnis.schwach !== undefined
                         && page.ergebnis.schwach.length > 0

                Column {
                    id: schwachSpalte
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 6
                    Text {
                        text: "Daran solltest du arbeiten"
                        font.pixelSize: Style.headSize
                        color: Style.text
                    }
                    Repeater {
                        model: (page.ergebnis.leer || page.ergebnis.schwach === undefined)
                               ? [] : page.ergebnis.schwach
                        Text {
                            width: schwachSpalte.width
                            wrapMode: Text.WordWrap
                            text: "• " + modelData
                            font.pixelSize: Style.bodySize
                            color: Style.warn
                        }
                    }
                }
            }

            Button {
                width: parent.width
                text: "Antworten ansehen"
                onClicked: pageStack.push(Qt.resolvedUrl("ReviewPage.qml"))
            }
            Button {
                width: parent.width
                text: "Zur Übersicht"
                onClicked: pageStack.pop()
            }

            Item { width: 1; height: Style.pad }
        }
    }
}
