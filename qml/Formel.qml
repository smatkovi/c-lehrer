import QtQuick 1.1
import "style.js" as Style

// Eine Formel, zweimal: oben die Zeile so, wie sie im Beispielprogramm
// steht, darunter dieselbe Sache gesetzt.
//
// Das Gesetzte ist ein Bild, kein Text. QtQuick 1.1 kann Rich Text, aber
// keinen Bruchstrich und kein Summenzeichen mit Grenzen; gesetzt wird
// deshalb beim Bauen (tools/formeln.py), und hier haengt nur noch ein PNG.
//
// Die Groesse steht im Kurs, in Geraetepunkten. Sie aus dem Bild zu lesen
// waere eine Bindungsschleife: Die Hoehe haengt am Bild, das Bild an der
// Hoehe -- QML merkt das, wirft eine der Bindungen weg, und uebrig bleibt
// eine Formel mit null Pixeln Hoehe. Dieselbe Falle steht in Bild.qml.
Rectangle {
    id: rahmen

    property variant formel: undefined
    property real bildBreite: formel === undefined ? 0 : (formel.breite || 0)
    property real bildHoehe: formel === undefined ? 0 : (formel.hoehe || 0)
    // Breiter als der Platz wird verkleinert, schmaler bleibt es stehen:
    // eine kurze Formel auf Spaltenbreite aufzublasen sieht nach Plakat aus.
    property real skala: bildBreite > 0
                         ? Math.min(1.0, (width - 2 * 12) / bildBreite) : 1.0

    visible: formel !== undefined && formel.code !== undefined
    color: Style.codeBg
    border.color: Style.panelEdge
    border.width: 1
    radius: 4
    height: visible ? spalte.height + 16 : 0

    Column {
        id: spalte
        x: 12
        y: 8
        width: parent.width - 24
        spacing: 6

        Text {
            width: parent.width
            text: rahmen.formel === undefined ? "" : rahmen.formel.code
            font.family: Style.mono
            font.pixelSize: Style.codeSize
            color: Style.dim
            textFormat: Text.PlainText
            elide: Text.ElideRight
        }

        Image {
            visible: rahmen.bildBreite > 0
            width: Math.round(rahmen.bildBreite * rahmen.skala)
            height: Math.round(rahmen.bildHoehe * rahmen.skala)
            source: rahmen.formel === undefined || rahmen.formel.bild === undefined
                    ? "" : Qt.resolvedUrl("../bilder/" + rahmen.formel.bild + ".png")
            // Dreifach so gross gesetzt wie gezeigt -- ohne Glaetten waere
            // davon nichts zu merken.
            smooth: true
            asynchronous: true
        }

        Text {
            width: parent.width
            visible: text !== ""
            text: rahmen.formel === undefined ? "" : (rahmen.formel.untertitel || "")
            wrapMode: Text.WordWrap
            font.pixelSize: Style.smallSize
            color: Style.faint
        }
    }
}
