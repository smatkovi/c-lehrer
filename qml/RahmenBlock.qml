import QtQuick 1.1
import "style.js" as Style
import "worte.js" as W

// Ein Block im Annahmenkasten: Ueberschrift und Text.
//
// Eigene Datei statt Repeater: In QtQuick 1.1 ist ein Modell aus
// JavaScript-Objekten ein Grenzfall, der auf dem Geraet schweigend nichts
// anzeigt statt zu meckern -- und das Geraet steht zum Nachsehen nicht immer
// bereit. Vier gleiche Zeilen sind das wert.
Column {
    property string titel: ""
    property string inhalt: ""
    property string sprache: "de"

    visible: inhalt !== ""
    height: visible ? kopf.height + leib.height + spacing : 0
    spacing: 4

    Text {
        id: kopf
        text: W.w(titel, sprache)
        font.pixelSize: Style.smallSize
        font.bold: true
        color: Style.faint
    }
    Text {
        id: leib
        width: parent.width
        wrapMode: Text.WordWrap
        text: Style.rich(inhalt)
        textFormat: Text.RichText
        font.pixelSize: Style.bodySize
        color: Style.dim
    }
}
