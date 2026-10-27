import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// Das Glossar: jedes Fachwort des Kurses an einer Stelle, alphabetisch.
//
// Gebraucht wird es mitten in einer Lektion ("was war Spreizung?"), und
// dann hilft kein Scrollen durch hundert Woerter -- darum steht das
// Suchfeld oben und bleibt stehen. Es liegt ausdruecklich NICHT im
// header der ListView: der wird beim Neufuellen des Modells mit
// angefasst, und ein Feld, das beim Tippen die Eingabe verliert, ist
// schlimmer als keines.
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

    // Die Liste kommt uebersetzt und sortiert aus Course::glossary(); hier
    // wird sie nur gefiltert. Sie liegt in einem ListModel und nicht als
    // JS-Feld am Modell, weil section.property einen Rollennamen braucht --
    // bei einem Feld aus Objekten gibt es nur modelData, und die
    // Abschnittsbuchstaben blieben leer. Die Rolle heisst "kennung" und
    // nicht "id": "id" ist in einem Delegate schon vergeben.
    ListModel { id: gefundene }

    // Umlaute zaehlen unter ihrem Grundbuchstaben, damit "Überentwicklung"
    // bei U steht und nicht in einem eigenen Abschnitt hinter Z -- dieselbe
    // Rechnung wie beim Sortieren in Course::glossary().
    function anfangsbuchstabe(wort) {
        var z = wort.substring(0, 1).toUpperCase();
        if (z === "Ä") return "A";
        if (z === "Ö") return "O";
        if (z === "Ü") return "U";
        return z;
    }

    // Gesucht wird nach Wortanfang UND Teilwort: wer "spreiz" tippt, will
    // die Spreizung, und wer "nimbus" tippt, will auch Cumulonimbus finden.
    // Die Reihenfolge bleibt dabei alphabetisch -- sonst sprengen die
    // Abschnittsbuchstaben auseinander und stehen zweimal da.
    function fuellen() {
        var alle = course.glossary;
        var suche = feld.text.toLowerCase();
        gefundene.clear();
        for (var i = 0; i < alle.length; i++) {
            var wort = alle[i].wort;
            if (suche !== "" && wort.toLowerCase().indexOf(suche) < 0)
                continue;
            gefundene.append({ kennung: alle[i].id, wort: wort,
                               buchstabe: page.anfangsbuchstabe(wort) });
        }
    }

    Component.onCompleted: page.fuellen()

    // Beim Sprachwechsel sind die Woerter andere und anders sortiert.
    Connections {
        target: course
        onChanged: page.fuellen()
    }

    Column {
        id: kopf
        x: Style.pad
        y: Style.pad
        width: page.width - 2 * Style.pad
        spacing: Style.gap

        Text {
            text: W.w("Glossar", course.language)
            font.pixelSize: Style.titleSize
            color: Style.accent
        }
        Text {
            text: course.glossary.length + " " + W.w("Begriffe", course.language)
            font.pixelSize: Style.smallSize
            color: Style.faint
        }
        TextField {
            id: feld
            width: parent.width
            placeholderText: W.w("Wort suchen", course.language)
            onTextChanged: page.fuellen()
        }
    }

    ListView {
        id: liste
        anchors.top: kopf.bottom
        anchors.topMargin: Style.gap
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        model: gefundene
        clip: true
        pressDelay: 140
        cacheBuffer: 2000

        section.property: "buchstabe"
        section.criteria: ViewSection.FullString
        section.delegate: Item {
            width: liste.width
            height: 44
            Text {
                x: Style.pad
                anchors.verticalCenter: parent.verticalCenter
                text: section
                font.pixelSize: Style.headSize
                color: Style.accent
            }
            Rectangle {
                anchors.bottom: parent.bottom
                x: Style.pad
                width: liste.width - 2 * Style.pad
                height: 1
                color: Style.panelEdge
            }
        }

        delegate: Item {
            width: liste.width
            height: zeile.height + Style.gap

            Text {
                id: zeile
                x: Style.pad
                y: Style.gap / 2
                width: liste.width - 2 * Style.pad
                wrapMode: Text.WordWrap
                text: wort
                font.pixelSize: Style.bodySize
                color: Style.text
            }

            MouseArea {
                anchors.fill: parent
                onClicked: pageStack.push(Qt.resolvedUrl("BegriffPage.qml"),
                                          { kennung: kennung })
            }
        }
    }

    ScrollDecorator { flickableItem: liste }

    Text {
        anchors.centerIn: parent
        visible: gefundene.count === 0
        text: W.w("Nichts gefunden", course.language)
        font.pixelSize: Style.bodySize
        color: Style.faint
    }
}
