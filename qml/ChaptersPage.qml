import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style

Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }


    property variant kapitel: course.chapters()
    property variant plan: course.plan()

    Connections {
        target: course
        onChanged: page.kapitel = course.chapters()
    }

    Rectangle { anchors.fill: parent; color: Style.bg }

    function zeichen(stand) {
        if (stand === "fertig") return "✓";
        if (stand === "bekannt") return "•";
        return "";
    }
    function farbe(stand) {
        if (stand === "fertig") return Style.good;
        if (stand === "bekannt") return Style.faint;
        return Style.text;
    }

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
                text: "Kapitel"
                font.pixelSize: Style.titleSize
                color: Style.accent
            }

            Repeater {
                model: page.kapitel
                Panel {
                    width: spalte.width
                    height: kapitelSpalte.height + 2 * Style.pad

                    property variant daten: modelData

                    Column {
                        id: kapitelSpalte
                        x: Style.pad
                        y: Style.pad
                        width: parent.width - 2 * Style.pad
                        spacing: 8

                        Text {
                            width: parent.width
                            wrapMode: Text.WordWrap
                            text: daten.stufe + ". " + daten.titel
                            font.pixelSize: Style.headSize
                            color: Style.text
                        }
                        Text {
                            width: parent.width
                            wrapMode: Text.WordWrap
                            text: daten.text
                            font.pixelSize: Style.smallSize
                            color: Style.dim
                        }

                        Repeater {
                            model: daten.lektionen
                            Rectangle {
                                width: kapitelSpalte.width
                                height: 46
                                color: tipp.pressed ? Style.panelEdge : "transparent"
                                radius: 4

                                Text {
                                    x: 4
                                    anchors.verticalCenter: parent.verticalCenter
                                    width: parent.width - 40
                                    elide: Text.ElideRight
                                    text: modelData.titel
                                    font.pixelSize: Style.bodySize
                                    color: page.farbe(modelData.stand)
                                }
                                Text {
                                    anchors.right: parent.right
                                    anchors.rightMargin: 4
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: page.zeichen(modelData.stand)
                                    font.pixelSize: Style.bodySize
                                    color: page.farbe(modelData.stand)
                                }
                                MouseArea {
                                    id: tipp
                                    anchors.fill: parent
                                    onClicked: {
                                        course.startLesson(modelData.id);
                                        pageStack.push(Qt.resolvedUrl("LessonPage.qml"));
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // ---- was noch kommt -------------------------------------------
            // topPadding is a QtQuick 2 property: assigning it here makes
            // the whole file fail to load, and a page that does not load is
            // simply a button that does nothing.
            Item { width: 1; height: Style.pad }
            Text {
                text: "Geplant"
                font.pixelSize: Style.headSize
                color: Style.faint
            }
            Repeater {
                model: page.plan
                Text {
                    width: spalte.width
                    wrapMode: Text.WordWrap
                    visible: !modelData.fertig
                    text: modelData.stufe + ". " + modelData.titel
                          + (modelData.sprache === "cpp" ? "  (C++)" : "")
                    font.pixelSize: Style.smallSize
                    color: Style.faint
                }
            }

            Button {
                width: parent.width
                text: "Zurück"
                onClicked: pageStack.pop()
            }
            Item { width: 1; height: Style.pad }
        }
    }
}
