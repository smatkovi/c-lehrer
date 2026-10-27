import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// Ein Glossareintrag: das Wort, die Zeichnung dazu, die Erklaerung und die
// Nachbarbegriffe.
//
// Die Seite liegt auf dem Stapel, nicht als Blase ueber der Lektion: Wer
// von "Spreizung" zu "Taupunkt" und von dort zur "Basis" weiterliest, soll
// mit Zurueck Schritt fuer Schritt denselben Weg zurueckgehen und am Ende
// wieder in seiner Lektion stehen.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }

    // Die Kennung kommt beim Oeffnen mit (pageStack.push mit Eigenschaften).
    property string kennung: ""
    property variant eintrag: page.leererEintrag()

    function leererEintrag() {
        return { leer: true, wort: "", definition: "", bild: "", siehe: [] };
    }

    function laden() {
        page.eintrag = page.kennung === "" ? page.leererEintrag()
                                           : course.glossaryEntry(page.kennung);
    }

    // Geladen wird in einer Funktion und nicht als Bindung: beim
    // Sprachwechsel aendert sich die Kennung nicht, wohl aber der Text,
    // und eine Bindung auf glossaryEntry(kennung) merkte das nicht.
    Component.onCompleted: page.laden()
    onKennungChanged: page.laden()

    Connections {
        target: course
        onChanged: page.laden()
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
                width: parent.width
                wrapMode: Text.WordWrap
                text: page.eintrag.leer ? "" : page.eintrag.wort
                font.pixelSize: Style.titleSize
                color: Style.accent
            }

            // Dieselbe Zeichnung wie in der Lektion, in denselben Massen:
            // Bild rechnet seine Hoehe aus der Breite und ausdruecklich
            // nicht aus der implicitHeight des Bildes -- das waere auf
            // Harmattan ein Ringschluss, und der Rahmen blieb null hoch.
            Bild {
                width: parent.width
                name: page.eintrag.leer || page.eintrag.bild === undefined
                      ? "" : page.eintrag.bild
            }

            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                text: page.eintrag.leer ? "" : Style.rich(page.eintrag.definition)
                textFormat: Text.RichText
                font.pixelSize: Style.bodySize
                color: Style.text
                lineHeight: 1.25
                lineHeightMode: Text.ProportionalHeight
                // Auch eine Definition verweist weiter -- dann einen
                // Eintrag tiefer auf den Stapel, wie von der Lektion aus.
                onLinkActivated: {
                    if (link.indexOf("begriff:") === 0)
                        pageStack.push(Qt.resolvedUrl("BegriffPage.qml"),
                                       { kennung: link.substring(8) });
                }
            }

            Text {
                text: W.w("Siehe auch", course.language)
                font.pixelSize: Style.headSize
                color: Style.text
                visible: !page.eintrag.leer && page.eintrag.siehe.length > 0
            }

            Repeater {
                model: page.eintrag.leer ? [] : page.eintrag.siehe
                Button {
                    width: spalte.width
                    text: modelData.wort
                    onClicked: pageStack.push(Qt.resolvedUrl("BegriffPage.qml"),
                                              { kennung: modelData.id })
                }
            }

            Item { width: 1; height: Style.pad }
        }
    }
}
