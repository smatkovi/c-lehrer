import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style

// Every question of the placement test again, with the answer given, the
// right one, and why. Asked for explicitly: a test you cannot look back at
// teaches nothing, it only sorts you.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }


    Rectangle { anchors.fill: parent; color: Style.bg }

    ListView {
        id: liste
        anchors.fill: parent
        model: course.placementReview()
        spacing: Style.gap
        cacheBuffer: 2000
        clip: true
        pressDelay: 140

        header: Item {
            width: liste.width
            height: kopf.height + 2 * Style.pad
            Text {
                id: kopf
                x: Style.pad
                y: Style.pad
                width: liste.width - 2 * Style.pad
                wrapMode: Text.WordWrap
                text: "Einstufung: alle Antworten"
                font.pixelSize: Style.titleSize
                color: Style.accent
            }
        }

        delegate: Item {
            width: liste.width
            height: karte.height + Style.gap

            Panel {
                id: karte
                x: Style.pad
                width: liste.width - 2 * Style.pad
                height: inhalt.height + 2 * Style.pad

                Column {
                    id: inhalt
                    x: Style.pad
                    y: Style.pad
                    width: karte.width - 2 * Style.pad
                    spacing: 8

                    Row {
                        spacing: 8
                        Rectangle {
                            width: 26; height: 26; radius: 13
                            color: modelData.korrekt ? Style.good : Style.bad
                            Text {
                                anchors.centerIn: parent
                                text: modelData.korrekt ? "✓" : "✗"
                                color: Style.bg
                                font.pixelSize: 17
                                font.bold: true
                            }
                        }
                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            text: modelData.thema + " · Stufe " + modelData.stufe
                            font.pixelSize: Style.smallSize
                            color: Style.faint
                        }
                    }

                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: modelData.frage
                        font.pixelSize: Style.bodySize
                        color: Style.text
                    }

                    CodeBlock {
                        width: parent.width
                        code: modelData.code
                        visible: modelData.code !== ""
                    }

                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: !modelData.korrekt
                        text: "Deine Antwort: " + modelData.optionen[modelData.gewaehlt]
                        font.pixelSize: Style.smallSize
                        color: Style.bad
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: "Richtig: " + modelData.optionen[modelData.richtig]
                        font.pixelSize: Style.smallSize
                        color: Style.good
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: Style.rich(modelData.warum)
                        textFormat: Text.RichText
                        font.pixelSize: Style.smallSize
                        color: Style.dim
                    }
                }
            }
        }

        footer: Item {
            width: liste.width
            height: 90
            Button {
                x: Style.pad
                y: Style.pad
                width: liste.width - 2 * Style.pad
                text: "Zurück"
                onClicked: pageStack.pop()
            }
        }
    }
}
