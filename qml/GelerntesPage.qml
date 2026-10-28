import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// Was die App dazugelernt hat -- und wie man es loswird oder mitnimmt.
//
// Jeder Eintrag ist ein Foto, das der Leser deuten liess, mit der Klasse,
// auf die sich Claude und sein eigener Tipp geeinigt haben. Hier steht
// alles sichtbar nebeneinander: Wer nachsieht, was das Netz gelernt hat,
// findet auch die Fotos, die es falsch gelernt hat, und kann sie
// einzeln wegnehmen. Das Format und warum es so wirkt, steht in
// segelflug/tools/GELERNTES.md.
//
// Die Vorschau ist das gespeicherte Netzbild (160 Pixel); Qt 4.7 kann
// kein JPEG aus dem Speicher anzeigen, darum legt Course es beim ersten
// Hinsehen in den Zwischenspeicher und gibt den Pfad zurueck.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }

    property variant gelernt: course.learned
    property string meldung: ""

    Connections {
        target: course
        onLearnedChanged: page.gelernt = course.learned
    }

    function quellenWort(q) {
        if (q === 0) return W.w("Claude und ich", course.language);
        if (q === 1) return W.w("Claude", course.language);
        return W.w("von mir richtiggestellt", course.language);
    }

    Rectangle { anchors.fill: parent; color: Style.bg }

    Column {
        id: kopf
        x: Style.pad
        y: Style.pad
        width: page.width - 2 * Style.pad
        spacing: 6

        Text {
            text: W.w("Gelerntes", course.language)
            font.pixelSize: Style.titleSize
            color: Style.accent
        }
        Text {
            width: parent.width
            wrapMode: Text.WordWrap
            text: page.gelernt.wirksam === true
                  ? W.w("", course.language) + page.gelernt.anzahl
                    + W.w(" Fotos, die das Netz mit einbezieht.", course.language)
                  : W.w("", course.language) + page.gelernt.anzahl
                    + W.w(" Fotos. Ab ", course.language)
                    + (page.gelernt.anzahl + page.gelernt.fehlende)
                    + W.w(" zieht das Netz sie mit ein.", course.language)
            font.pixelSize: Style.smallSize
            color: Style.dim
        }
        // Ab vierzig Eintraegen wird die letzte Schicht des Netzes selbst
        // nachtrainiert -- dann steht es hier.
        Text {
            width: parent.width
            wrapMode: Text.WordWrap
            visible: page.gelernt.anzahl > 0
            text: page.gelernt.kopf === true
                  ? W.w("Die letzte Schicht des Netzes ist nachtrainiert.", course.language)
                  : W.w("Ab ", course.language) + page.gelernt.kopfAb
                    + W.w(" Fotos wird auch die letzte Schicht des Netzes nachtrainiert.", course.language)
            font.pixelSize: Style.smallSize
            color: page.gelernt.kopf === true ? Style.good : Style.dim
        }
        // Auch ohne eigenen Tipp von Claude lernen (nur bei "hoch").
        Row {
            width: parent.width
            spacing: Style.gap
            Switch {
                id: vonClaude
                anchors.verticalCenter: parent.verticalCenter
                checked: course.learnFromClaude
                onCheckedChanged: if (checked !== course.learnFromClaude) course.learnFromClaude = checked
            }
            Text {
                width: parent.width - vonClaude.width - Style.gap
                anchors.verticalCenter: parent.verticalCenter
                wrapMode: Text.WordWrap
                text: W.w("Von Claude lernen, unabhängig von meinem Tipp", course.language)
                      + "\n" + W.w("Sobald Fable „hoch“ sagt, auch gegen meinen Tipp; bei Opus nur per Knopf.", course.language)
                font.pixelSize: Style.smallSize
                color: Style.text
            }
        }
        Text {
            width: parent.width
            wrapMode: Text.WordWrap
            visible: page.meldung !== ""
            text: page.meldung
            font.pixelSize: Style.smallSize
            color: Style.text
        }

        Row {
            width: parent.width
            spacing: Style.gap
            Button {
                width: (parent.width - Style.gap) / 2
                text: W.w("Sichern", course.language)
                onClicked: page.meldung = course.exportLearned()
            }
            Button {
                width: (parent.width - Style.gap) / 2
                text: W.w("Laden", course.language)
                onClicked: page.meldung = course.importLearned("")
            }
        }
    }

    ListView {
        id: liste
        anchors.top: kopf.bottom
        anchors.topMargin: Style.gap
        anchors.bottom: fuss.top
        anchors.bottomMargin: Style.gap
        x: Style.pad
        width: page.width - 2 * Style.pad
        clip: true
        spacing: 6
        cacheBuffer: 0

        model: page.gelernt.eintraege === undefined ? [] : page.gelernt.eintraege

        delegate: Rectangle {
            width: liste.width
            height: 84
            radius: 4
            color: Style.panel
            border.color: Style.panelEdge
            border.width: 1

            Image {
                id: vorschau
                x: 6
                y: 6
                width: 72
                height: 72
                asynchronous: true
                fillMode: Image.PreserveAspectCrop
                clip: true
                /* Nur EIN Mass: mit beiden staucht Qt 4.7.4 statt zu
                   beschneiden (siehe FotoWahlPage). */
                sourceSize.height: 144
                source: "file://" + course.learnedImage(modelData.nummer)
            }

            Column {
                anchors.left: vorschau.right
                anchors.leftMargin: 10
                anchors.right: weg.left
                anchors.rightMargin: 6
                anchors.verticalCenter: parent.verticalCenter
                spacing: 3

                Text {
                    width: parent.width
                    elide: Text.ElideRight
                    text: modelData.name
                    font.pixelSize: Style.bodySize
                    color: modelData.bekannt === true ? Style.text : Style.dim
                }
                Text {
                    width: parent.width
                    elide: Text.ElideRight
                    text: page.quellenWort(modelData.quelle)
                    font.pixelSize: Style.smallSize
                    color: Style.dim
                }
                // Eine Klasse, die dieses Netz nicht kennt, zaehlt nicht
                // mit -- das muss dastehen, sonst sucht man den Fehler
                // woanders.
                Text {
                    width: parent.width
                    wrapMode: Text.WordWrap
                    visible: modelData.bekannt !== true
                    text: W.w("Diese Klasse kennt das Netz nicht.", course.language)
                    font.pixelSize: Style.smallSize
                    color: Style.warn
                }
            }

            ToolIcon {
                id: weg
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                platformIconId: "toolbar-delete"
                onClicked: {
                    course.forgetLearned(modelData.nummer);
                    page.meldung = W.w("Eintrag gelöscht.", course.language);
                }
            }
        }
    }

    ScrollDecorator { flickableItem: liste }

    Column {
        id: fuss
        anchors.bottom: parent.bottom
        anchors.bottomMargin: Style.pad
        x: Style.pad
        width: page.width - 2 * Style.pad
        spacing: 6

        Text {
            width: parent.width
            wrapMode: Text.WordWrap
            visible: liste.count === 0
            text: W.w("Noch nichts gelernt. Lass ein Foto von Claude deuten; "
                      + "stimmt sein Urteil mit deinem Tipp überein, merkt es "
                      + "die App.", course.language)
            font.pixelSize: Style.bodySize
            color: Style.dim
        }
        Button {
            width: parent.width
            visible: liste.count > 0
            text: W.w("Alles vergessen", course.language)
            onClicked: {
                course.forgetAllLearned();
                page.meldung = W.w("Alles vergessen.", course.language);
            }
        }
    }
}
