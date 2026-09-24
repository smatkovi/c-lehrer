import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

Page {
    id: page
    orientationLock: PageOrientation.Automatic

    // Die Startseite ist die unterste: kein Zurueck, aber die Leiste bleibt
    // sichtbar, damit die Seiten nicht bei jedem Wechsel springen.
    tools: ToolBarLayout { }


    property variant weiter: course.nextLesson()
    property variant zahlen: course.stats

    function auffrischen() {
        weiter = course.nextLesson();
        zahlen = course.stats;
    }

    Connections {
        target: course
        onChanged: page.auffrischen()
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

            // Titel und Untertitel kommen aus dem Kurs, nicht aus dem
            // Programm: dasselbe Binaer traegt mehrere Kurse.
            Text {
                text: course.courseTitle
                font.pixelSize: Style.titleSize
                color: Style.accent
            }
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                font.pixelSize: Style.smallSize
                color: Style.dim
                visible: course.courseSubtitle !== ""
                text: course.courseSubtitle
            }

            // ---- noch kein Einstufungstest --------------------------------
            Panel {
                width: parent.width
                height: einstufungsBlock.height + 2 * Style.pad
                visible: course.needsPlacement

                Column {
                    id: einstufungsBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: Style.gap

                    Text {
                        text: W.w("Einstufungstest", course.language)
                        font.pixelSize: Style.headSize
                        color: Style.text
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        font.pixelSize: Style.bodySize
                        color: Style.dim
                        text: W.w("Etwa zehn Fragen, ein Fingertipp je Frage. ", course.language)
                              + W.w("Danach geht der Kurs genau dort weiter, wo dein ", course.language)
                              + W.w("Wissen aufhört -- nichts, was du schon kannst.", course.language)
                    }
                    Button {
                        width: parent.width
                        text: W.w("Test beginnen", course.language)
                        onClicked: {
                            course.startPlacement();
                            pageStack.push(Qt.resolvedUrl("PlacementPage.qml"));
                        }
                    }
                }
            }

            // ---- eingestuft -----------------------------------------------
            Panel {
                width: parent.width
                height: standBlock.height + 2 * Style.pad
                visible: !course.needsPlacement

                Column {
                    id: standBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: Style.gap

                    Row {
                        spacing: Style.gap
                        Text {
                            text: W.w("Stufe ", course.language) + course.level
                            font.pixelSize: Style.headSize
                            color: Style.accent
                        }
                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            text: page.zahlen.fertig + " "
                                  + W.w("von", course.language) + " "
                                  + page.zahlen.gesamt + " "
                                  + W.w("Lektionen", course.language)
                            font.pixelSize: Style.smallSize
                            color: Style.dim
                        }
                    }

                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        font.pixelSize: Style.bodySize
                        color: Style.text
                        visible: !page.weiter.leer
                        text: W.w("Weiter: ", course.language) + page.weiter.kapitel + " – " + page.weiter.titel
                    }

                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        font.pixelSize: Style.smallSize
                        color: Style.warn
                        visible: page.zahlen.level > page.zahlen.hoechstesKapitel
                        text: W.w("Du liegst über dem, was bisher geschrieben ist ", course.language)
                              + W.w("(bis Stufe ", course.language) + page.zahlen.hoechstesKapitel
                              + W.w("). Die höheren Kapitel kommen noch – ", course.language)
                              + W.w("unten steht der Plan.", course.language)
                    }

                    Button {
                        width: parent.width
                        text: W.w("Weiterlernen", course.language)
                        visible: !page.weiter.leer
                        onClicked: {
                            course.startLesson(page.weiter.id);
                            pageStack.push(Qt.resolvedUrl("LessonPage.qml"));
                        }
                    }

                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        font.pixelSize: Style.smallSize
                        color: Style.warn
                        visible: page.zahlen.faellig > 0
                        text: page.zahlen.faellig
                              + W.w(" Lektion(en) sind zur ", course.language)
                              + W.w("Auffrischung fällig – Wiederholen nach Abstand ", course.language)
                              + W.w("ist der halbe Lernerfolg.", course.language)
                    }
                }
            }

            // Nur zeigen, wenn der Kurs mehr als eine Sprache mitbringt --
            // beim C-Kurs wäre der Schalter sonst eine leere Zusage.
            Row {
                spacing: Style.gap
                visible: course.languages.length > 1
                Repeater {
                    model: course.languages
                    Rectangle {
                        width: 92
                        height: 52
                        radius: 6
                        color: modelData === course.language
                               ? Style.accent : Style.panel
                        border.color: Style.panelEdge
                        border.width: 1
                        Text {
                            anchors.centerIn: parent
                            text: modelData === "de" ? W.w("Deutsch", course.language)
                                  : modelData === "en" ? W.w("English", course.language) : modelData
                            font.pixelSize: Style.smallSize
                            color: modelData === course.language
                                   ? Style.bg : Style.text
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: course.language = modelData
                        }
                    }
                }
            }

            Button {
                width: parent.width
                text: {
                    var z = course.cardStats;
                    return z.faellig > 0
                           ? W.w("Karteikarten (", course.language) + z.faellig + " fällig)"
                           : W.w("Karteikarten", course.language);
                }
                // Auch vor dem Einstufungstest: Karten sind gerade am
                // Anfang nützlich, und wer nur abfragen will, soll nicht
                // erst einen Test machen müssen.
                visible: course.cardStats.gesamt > 0
                onClicked: pageStack.push(Qt.resolvedUrl("CardPage.qml"))
            }

            Button {
                width: parent.width
                text: W.w("Kapitel", course.language)
                onClicked: pageStack.push(Qt.resolvedUrl("ChaptersPage.qml"))
            }

            Button {
                width: parent.width
                text: W.w("Spielwiese: eigenen Code laufen lassen", course.language)
                visible: course.canRun
                onClicked: pageStack.push(Qt.resolvedUrl("PlaygroundPage.qml"))
            }

            Button {
                width: parent.width
                text: W.w("Einstufung ansehen", course.language)
                visible: !course.needsPlacement
                onClicked: pageStack.push(Qt.resolvedUrl("ReviewPage.qml"))
            }

            Button {
                width: parent.width
                text: course.needsPlacement ? "" : W.w("Neu einstufen", course.language)
                visible: !course.needsPlacement
                onClicked: {
                    course.startPlacement();
                    pageStack.push(Qt.resolvedUrl("PlacementPage.qml"));
                }
            }

            // ---- Schwächen aus dem Test -----------------------------------
            Panel {
                width: parent.width
                height: schwachBlock.height + 2 * Style.pad
                visible: course.weakTopics.length > 0

                Column {
                    id: schwachBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 6

                    Text {
                        text: W.w("Woran es noch hakt", course.language)
                        font.pixelSize: Style.headSize
                        color: Style.text
                    }
                    Repeater {
                        model: course.weakTopics
                        Text {
                            width: schwachBlock.width
                            wrapMode: Text.WordWrap
                            text: "• " + modelData
                            font.pixelSize: Style.bodySize
                            color: Style.warn
                        }
                    }
                }
            }

            Item { width: 1; height: Style.pad }
        }
    }
}
