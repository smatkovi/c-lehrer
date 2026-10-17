import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// Wolken erkennen: ein Foto, zwei Fragen, und das viele Male.
//
// Anders als die Einstufung gibt diese Seite nach jedem Tipp Antwort.
// Beim Einstufen waere das falsch -- dort wird gemessen, und wer die
// Loesung sieht, lernt waehrend der Messung dazu. Hier ist das Lernen der
// Zweck: Ohne den Satz "daran haettest du es gesehen" bleibt vom
// Danebentippen nur das Danebentippen.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }

    property variant frage: course.recognitionQuestion
    property variant ergebnis: course.recognitionResult

    Connections {
        target: course
        onRecognitionChanged: {
            page.frage = course.recognitionQuestion;
            page.ergebnis = course.recognitionResult;
        }
    }

    Rectangle { anchors.fill: parent; color: Style.bg }

    // ---- die Uebung -------------------------------------------------------
    Flickable {
        id: lauf
        anchors.fill: parent
        contentHeight: spalte.height + 2 * Style.pad
        visible: !course.recognitionDone
        pressDelay: 140
        clip: true

        Column {
            id: spalte
            x: Style.pad
            y: Style.pad
            width: page.width - 2 * Style.pad
            spacing: Style.gap

            Text {
                text: page.frage.leer ? ""
                      : W.w("Bild ", course.language) + page.frage.nummer
                        + W.w(" von ", course.language) + page.frage.gesamt
                font.pixelSize: Style.smallSize
                color: Style.faint
            }

            // Das Foto. Die Hoehe kommt aus den mitgelieferten Massen,
            // nicht aus implicitHeight -- das waere die Bindungsschleife
            // aus Bild.qml.
            Rectangle {
                id: rahmen
                width: spalte.width
                height: {
                    if (page.frage.leer || page.frage.foto === undefined
                            || !page.frage.foto.breite)
                        return Math.round(spalte.width * 0.7);
                    return Math.round(spalte.width * page.frage.foto.hoehe
                                      / page.frage.foto.breite);
                }
                color: Style.codeBg
                border.color: Style.panelEdge
                border.width: 1
                radius: 4
                clip: true

                Image {
                    anchors.fill: parent
                    anchors.margins: 1
                    source: (page.frage.leer || page.frage.foto === undefined)
                            ? "" : Style.bilderPfad + page.frage.foto.datei
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                    asynchronous: true
                }
            }

            // Urheber und Lizenz. Die Fotos stehen unter CC BY und CC BY-SA;
            // beide verlangen genau diese Zeile, auch hier.
            Text {
                width: spalte.width
                wrapMode: Text.WordWrap
                text: (page.frage.leer || page.frage.foto === undefined) ? ""
                      : page.frage.foto.autor + " · " + page.frage.foto.lizenz
                        + " · Wikimedia Commons"
                font.pixelSize: Style.smallSize - 2
                color: Style.faint
            }

            Text {
                width: spalte.width
                wrapMode: Text.WordWrap
                text: page.frage.leer ? ""
                      : (page.frage.stufe === 0
                         ? W.w("Was für eine Wolke ist das?", course.language)
                         : W.w("Und was heißt sie fürs Segelfliegen?",
                               course.language))
                font.pixelSize: Style.headSize
                color: Style.text
            }

            Repeater {
                model: page.frage.leer ? [] : page.frage.optionen
                Rectangle {
                    width: spalte.width
                    height: wahl.paintedHeight + 24
                    radius: 6
                    border.width: 1
                    border.color: (page.frage.geprueft
                                   && index === page.frage.antwort)
                                  ? Style.good
                                  : ((page.frage.geprueft
                                      && index === page.frage.gewaehlt)
                                     ? Style.bad : Style.panelEdge)
                    color: {
                        if (!page.frage.geprueft)
                            return druck.pressed ? Style.panelEdge : Style.panel;
                        if (index === page.frage.antwort) return "#1c3a24";
                        if (index === page.frage.gewaehlt) return "#3a1c1c";
                        return Style.panel;
                    }

                    Text {
                        id: wahl
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
                        enabled: !page.frage.geprueft
                        onClicked: course.answerRecognition(index)
                    }
                }
            }

            // ---- woran man es sieht ---------------------------------------
            Panel {
                width: spalte.width
                height: rueck.height + 2 * Style.pad
                visible: !page.frage.leer && page.frage.geprueft

                Column {
                    id: rueck
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 6

                    Text {
                        text: page.frage.richtig
                              ? W.w("Richtig", course.language)
                              : W.w("Daneben", course.language)
                        font.pixelSize: Style.bodySize
                        font.bold: true
                        color: page.frage.richtig ? Style.good : Style.bad
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: page.frage.geprueft ? page.frage.name : ""
                        font.pixelSize: Style.bodySize
                        color: Style.accent
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: page.frage.geprueft ? page.frage.erklaerung : ""
                        font.pixelSize: Style.bodySize
                        color: Style.dim
                        lineHeight: 1.2
                        lineHeightMode: Text.ProportionalHeight
                    }
                }
            }

            Button {
                width: spalte.width
                visible: !page.frage.leer && page.frage.geprueft
                text: page.frage.stufe === 0
                      ? W.w("Und was heißt das?", course.language)
                      : W.w("Nächstes Bild", course.language)
                onClicked: {
                    course.nextRecognition();
                    lauf.contentY = 0;
                }
            }

            Item { width: 1; height: Style.pad }
        }
    }

    // ---- das Ergebnis -----------------------------------------------------
    Flickable {
        anchors.fill: parent
        contentHeight: endeSpalte.height + 2 * Style.pad
        visible: course.recognitionDone
        pressDelay: 140
        clip: true

        Column {
            id: endeSpalte
            x: Style.pad
            y: Style.pad
            width: page.width - 2 * Style.pad
            spacing: Style.gap

            Text {
                text: W.w("Durch", course.language)
                font.pixelSize: Style.titleSize
                color: Style.accent
            }
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                text: W.w("Wolke erkannt: ", course.language)
                      + page.ergebnis.art + W.w(" von ", course.language)
                      + page.ergebnis.gesamt + ". "
                      + W.w("Bedeutung gewusst: ", course.language)
                      + page.ergebnis.sinn + W.w(" von ", course.language)
                      + page.ergebnis.gesamt + "."
                font.pixelSize: Style.bodySize
                color: Style.text
            }

            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                visible: page.ergebnis.schwach !== undefined
                         && page.ergebnis.schwach.length > 0
                text: W.w("Das sieh dir noch einmal an:", course.language)
                font.pixelSize: Style.bodySize
                color: Style.dim
            }

            Repeater {
                model: page.ergebnis.schwach === undefined
                       ? [] : page.ergebnis.schwach
                Panel {
                    width: endeSpalte.width
                    height: schwachBlock.height + 2 * Style.pad

                    Column {
                        id: schwachBlock
                        x: Style.pad
                        y: Style.pad
                        width: parent.width - 2 * Style.pad
                        spacing: 4

                        Text {
                            width: parent.width
                            wrapMode: Text.WordWrap
                            text: modelData.name + "  (" + modelData.richtig
                                  + "/" + modelData.gesamt + ")"
                            font.pixelSize: Style.bodySize
                            color: Style.warn
                        }
                        Text {
                            width: parent.width
                            wrapMode: Text.WordWrap
                            text: modelData.erkennen
                            font.pixelSize: Style.smallSize
                            color: Style.dim
                        }
                    }
                }
            }

            Button {
                width: parent.width
                text: W.w("Noch einmal", course.language)
                onClicked: course.startRecognition(0)
            }
            Button {
                width: parent.width
                text: W.w("Zurück", course.language)
                onClicked: pageStack.pop()
            }

            Item { width: 1; height: Style.pad }
        }
    }
}
