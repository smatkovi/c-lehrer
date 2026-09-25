import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// Karteikarten mit wachsenden Abständen.
//
// Nur Fragen mit einer eindeutigen Antwort kommen hier vor — Auswahl und
// Zahl. Etwas zusammenzusetzen oder Code zu schreiben gehört in die
// Lektion: eine Karte soll in Sekunden beantwortet sein, sonst wiederholt
// man am Tag zwanzig statt zweihundert.
//
// Richtig beantwortet schiebt die Karte weiter hinaus (1 Tag, 3 Tage, dann
// mit dem Faktor mal), falsch holt sie auf morgen zurück. Genau dieses
// Zurückholen ist der Lerneffekt, nicht das Wiederlesen.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }

    property variant karte: course.card

    Connections {
        target: course
        onCardChanged: page.karte = course.card
    }

    Component.onCompleted: course.startCards()

    Rectangle { anchors.fill: parent; color: Style.bg }

    // ---- alles durch ------------------------------------------------------
    Column {
        anchors.centerIn: parent
        width: page.width - 2 * Style.pad
        spacing: Style.gap
        visible: page.karte.leer === true

        Text {
            width: parent.width
            wrapMode: Text.WordWrap
            text: W.w("Für jetzt durch", course.language)
            font.pixelSize: Style.titleSize
            color: Style.good
        }
        Text {
            width: parent.width
            wrapMode: Text.WordWrap
            font.pixelSize: Style.bodySize
            color: Style.dim
            text: (page.karte.erledigt === undefined ? 0 : page.karte.erledigt)
                  + " Karten bearbeitet. Was du richtig hattest, kommt in "
                  + "ein paar Tagen wieder; was nicht saß, schon morgen."
        }
        Button {
            width: parent.width
            text: W.w("Zurück", course.language)
            onClicked: pageStack.pop()
        }
    }

    // ---- die Karte --------------------------------------------------------
    Flickable {
        anchors.fill: parent
        contentHeight: spalte.height + 2 * Style.pad
        visible: page.karte.leer === false
        pressDelay: 140
        clip: true

        Column {
            id: spalte
            x: Style.pad
            y: Style.pad
            width: page.width - 2 * Style.pad
            spacing: Style.gap

            Row {
                width: parent.width
                Text {
                    width: parent.width - 110
                    elide: Text.ElideRight
                    text: page.karte.kapitel === undefined ? "" : page.karte.kapitel
                    font.pixelSize: Style.smallSize
                    color: Style.faint
                }
                Text {
                    width: 110
                    horizontalAlignment: Text.AlignRight
                    text: page.karte.neu === true
                          ? "neu"
                          : W.w("noch ", course.language) + (page.karte.offen === undefined ? 0 : page.karte.offen)
                    font.pixelSize: Style.smallSize
                    color: page.karte.neu === true ? Style.accent : Style.faint
                }
            }

            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                text: page.karte.frage === undefined ? "" : Style.rich(page.karte.frage)
                textFormat: Text.RichText
                font.pixelSize: Style.headSize
                color: Style.text
            }

            Rahmen {
                width: parent.width
                sprache: course.language
                mathematisch: (page.karte.leer || page.karte.mathematisch === undefined)
                                  ? "" : page.karte.mathematisch
                physikalisch: (page.karte.leer || page.karte.physikalisch === undefined)
                                  ? "" : page.karte.physikalisch
                annahmen: (page.karte.leer || page.karte.annahmen === undefined)
                              ? "" : page.karte.annahmen
                ziel: (page.karte.leer || page.karte.ziel === undefined)
                          ? "" : page.karte.ziel
            }

            Bild {
                width: parent.width
                name: page.karte.bild === undefined ? "" : page.karte.bild
            }

            CodeBlock {
                width: parent.width
                visible: page.karte.code !== undefined && page.karte.code !== ""
                code: page.karte.code === undefined ? "" : page.karte.code
            }

            // ---- Auswahl ---------------------------------------------------
            Repeater {
                model: (page.karte.art === "mc" && page.karte.optionen !== undefined)
                       ? page.karte.optionen : []
                Rectangle {
                    width: spalte.width
                    height: wahl.paintedHeight + 24
                    radius: 6
                    border.width: 1
                    border.color: (page.karte.geprueft === true
                                   && index === page.karte.antwort)
                                  ? Style.good : Style.panelEdge
                    color: {
                        if (page.karte.geprueft !== true)
                            return druck.pressed ? Style.panelEdge : Style.panel;
                        if (index === page.karte.antwort) return "#1c3a24";
                        return Style.panel;
                    }
                    Text {
                        id: wahl
                        x: 12; y: 12
                        width: parent.width - 24
                        wrapMode: Text.WordWrap
                        text: modelData
                        font.pixelSize: Style.bodySize
                        color: Style.text
                    }
                    MouseArea {
                        id: druck
                        anchors.fill: parent
                        enabled: page.karte.geprueft !== true
                        onClicked: course.answerCard(index)
                    }
                }
            }

            // ---- Zahl ------------------------------------------------------
            Column {
                width: parent.width
                spacing: 8
                visible: page.karte.art === "zahl"

                Row {
                    spacing: 10
                    TextField {
                        id: zahl
                        width: spalte.width - 150
                        enabled: page.karte.geprueft !== true
                        inputMethodHints: Qt.ImhFormattedNumbersOnly
                        placeholderText: W.w("Zahl", course.language)
                    }
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        width: 130
                        wrapMode: Text.WordWrap
                        text: page.karte.einheit === undefined ? "" : page.karte.einheit
                        font.pixelSize: Style.smallSize
                        color: Style.dim
                    }
                }
                Button {
                    width: parent.width
                    text: W.w("Prüfen", course.language)
                    enabled: page.karte.geprueft !== true && zahl.text !== ""
                    onClicked: course.answerCardNumber(
                                   parseFloat(zahl.text.replace(",", ".")))
                }
            }

            // ---- Rückmeldung ------------------------------------------------
            Panel {
                width: parent.width
                height: rueck.height + 2 * Style.pad
                visible: page.karte.geprueft === true

                Column {
                    id: rueck
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 8

                    Row {
                        spacing: 10
                        Text {
                            text: page.karte.richtig === true ? W.w("Richtig", course.language) : W.w("Daneben", course.language)
                            font.pixelSize: Style.headSize
                            color: page.karte.richtig === true ? Style.good : Style.warn
                        }
                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            text: page.karte.richtig === true
                                  ? W.w("wieder in ", course.language) + (page.karte.tage === undefined
                                                    ? 1 : page.karte.tage)
                                    + " Tagen"
                                  : W.w("morgen wieder", course.language)
                            font.pixelSize: Style.smallSize
                            color: Style.faint
                        }
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.karte.art === "zahl" && page.karte.richtig !== true
                        text: W.w("Richtig wäre etwa ", course.language) + (page.karte.antwort === undefined
                                                      ? "" : page.karte.antwort)
                        font.pixelSize: Style.bodySize
                        color: Style.good
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: page.karte.warum === undefined ? "" : Style.rich(page.karte.warum)
                        textFormat: Text.RichText
                        font.pixelSize: Style.bodySize
                        color: Style.text
                        lineHeight: 1.25
                        lineHeightMode: Text.ProportionalHeight
                    }
                    // Die Herleitung gehoert auf die Rueckseite der Karte.
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.karte.herleitung !== undefined
                                 && page.karte.herleitung !== ""
                        text: page.karte.herleitung === undefined
                              ? "" : Style.rich(page.karte.herleitung)
                        textFormat: Text.RichText
                        font.pixelSize: Style.bodySize
                        color: Style.text
                        lineHeight: 1.25
                        lineHeightMode: Text.ProportionalHeight
                    }
                    Bild {
                        width: parent.width
                        name: page.karte.skizze === undefined
                              ? "" : page.karte.skizze
                    }
                }
            }

            Button {
                width: parent.width
                visible: page.karte.geprueft === true
                text: W.w("Nächste Karte", course.language)
                onClicked: course.nextCard()
            }

            Button {
                width: parent.width
                visible: page.karte.geprueft !== true && page.karte.art === "mc"
                text: W.w("Überspringen", course.language)
                onClicked: course.nextCard()
            }

            Item { width: 1; height: Style.pad }
        }
    }
}
