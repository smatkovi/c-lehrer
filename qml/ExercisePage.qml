import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// The exercises, in rising order of effort: read and predict, fill a gap,
// assemble from given lines, write it yourself. That order is not a matter
// of taste -- a worked example faded out step by step teaches a beginner
// more than being dropped in front of an empty editor, and on a phone
// keyboard tapping lines into place is the difference between an exercise
// someone does and one they skip.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }


    property variant aufgabe: course.exercise
    property variant loesungsZeilen: []      // parsons: was zusammengebaut wurde
    property variant vorratsZeilen: []       // parsons: was noch übrig ist
    property string editorText: ""
    property bool editorGefuellt: false

    Connections {
        target: course
        onLessonChanged: page.uebernehmen()
    }

    Component.onCompleted: uebernehmen()

    // Was "die richtige Loesung" heisst, haengt an der Art der Aufgabe: bei
    // der Auswahl die richtige Moeglichkeit, bei der Vorhersage die Ausgabe,
    // bei der Luecke das fehlende Stueck, beim Ordnen die Reihenfolge.
    function loesungstext() {
        var a = page.aufgabe;
        if (a.leer)
            return "";
        if (a.art === "mc")
            return W.w("Richtig: ", course.language) + a.optionen[a.antwort];
        if (a.art === "predict")
            return "Richtig wäre:\n" + (a.antwort === undefined ? "" : a.antwort);
        if (a.art === "blank")
            return W.w("Richtig: ", course.language) + (a.antworten === undefined ? "" : a.antworten.join("   "));
        if (a.art === "parsons")
            return "Richtige Reihenfolge:\n"
                   + (a.zeilen === undefined ? "" : a.zeilen.join("\n"));
        return "";
    }

    // Vor einem zweiten Anlauf wird geleert, was sonst die alte Antwort
    // stehen laesst. Die zusammengebauten Zeilen der Ordnungsaufgabe
    // bleiben: dort will man umstellen, nicht von vorn anfangen.
    function zuruecksetzen() {
        if (page.aufgabe.art === "predict")
            vorhersage.text = "";
    }

    function uebernehmen() {
        aufgabe = course.exercise;
        if (aufgabe.leer)
            return;
        if (aufgabe.art === "parsons" && loesungsZeilen.length === 0
                && vorratsZeilen.length === 0) {
            vorratsZeilen = aufgabe.gemischt;
        }
        if (aufgabe.art === "code" && !editorGefuellt) {
            editorText = aufgabe.vorlage;
            editorGefuellt = true;
        }
    }

    function weiter() {
        loesungsZeilen = [];
        vorratsZeilen = [];
        editorGefuellt = false;
        editorText = "";
        vorhersage.text = "";
        course.nextExercise();
        uebernehmen();
        if (!course.exercise.leer && course.exercise.art === "parsons")
            vorratsZeilen = course.exercise.gemischt;
        if (!course.exercise.leer && course.exercise.art === "code") {
            editorText = course.exercise.vorlage;
            editorGefuellt = true;
        }
    }

    Rectangle { anchors.fill: parent; color: Style.bg }

    Flickable {
        id: flick
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

            // ---- fertig ---------------------------------------------------
            Column {
                width: parent.width
                spacing: Style.gap
                visible: page.aufgabe.leer

                Text {
                    text: W.w("Lektion geschafft", course.language)
                    font.pixelSize: Style.titleSize
                    color: Style.good
                }
                Text {
                    width: parent.width
                    wrapMode: Text.WordWrap
                    text: page.aufgabe.leer && page.aufgabe.beantwortet > 0
                          ? (page.aufgabe.richtigGesamt + " von "
                             + page.aufgabe.beantwortet + " Aufgaben auf Anhieb richtig. "
                             + W.w("Die Begriffe dieser Lektion kommen in ein paar Tagen ", course.language)
                             + W.w("zur Auffrischung wieder.", course.language))
                          : ""
                    font.pixelSize: Style.bodySize
                    color: Style.dim
                }
                Button {
                    width: parent.width
                    text: W.w("Weiter", course.language)
                    onClicked: { pageStack.pop(); pageStack.pop(); }
                }
            }

            // ---- Kopf -----------------------------------------------------
            Text {
                visible: !page.aufgabe.leer
                text: W.w("Aufgabe ", course.language) + (page.aufgabe.leer ? "" : page.aufgabe.nummer)
                      + " von " + (page.aufgabe.leer ? "" : page.aufgabe.gesamt)
                font.pixelSize: Style.smallSize
                color: Style.faint
            }
            Text {
                visible: !page.aufgabe.leer
                width: parent.width
                wrapMode: Text.WordWrap
                text: page.aufgabe.leer ? "" : Style.rich(page.aufgabe.frage)
                textFormat: Text.RichText
                font.pixelSize: Style.headSize
                color: Style.text
            }

            Bild {
                width: parent.width
                name: (page.aufgabe.leer || page.aufgabe.bild === undefined)
                      ? "" : page.aufgabe.bild
            }

            CodeBlock {
                width: parent.width
                visible: !page.aufgabe.leer && page.aufgabe.art !== "code"
                         && page.aufgabe.art !== "parsons"
                         && page.aufgabe.code !== undefined
                         && page.aufgabe.code !== ""
                code: (page.aufgabe.leer || page.aufgabe.code === undefined)
                      ? "" : page.aufgabe.code
            }

            // ---- Auswahl --------------------------------------------------
            Repeater {
                model: (!page.aufgabe.leer && page.aufgabe.art === "mc")
                       ? page.aufgabe.optionen : []
                Rectangle {
                    width: spalte.width
                    height: wahlText.paintedHeight + 24
                    radius: 6
                    border.width: 1
                    // Die richtige Moeglichkeit wird erst gruen, wenn die
                    // Loesung aufgedeckt ist -- sonst waere der zweite
                    // Anlauf keiner. Die eigene falsche Wahl steht dagegen
                    // sofort da: Man soll sehen, was man geantwortet hat.
                    border.color: {
                        if (!page.aufgabe.geprueft) return Style.panelEdge;
                        if ((page.aufgabe.loesungZeigen || page.aufgabe.richtig)
                                && index === page.aufgabe.antwort) return Style.good;
                        if (index === page.aufgabe.gewaehlt && !page.aufgabe.richtig)
                            return Style.bad;
                        return Style.panelEdge;
                    }
                    color: {
                        if (!page.aufgabe.geprueft)
                            return wahlDruck.pressed ? Style.panelEdge : Style.panel;
                        if ((page.aufgabe.loesungZeigen || page.aufgabe.richtig)
                                && index === page.aufgabe.antwort) return "#1c3a24";
                        if (index === page.aufgabe.gewaehlt && !page.aufgabe.richtig)
                            return "#3a1c1c";
                        return Style.panel;
                    }
                    Text {
                        id: wahlText
                        x: 12; y: 12
                        width: parent.width - 24
                        wrapMode: Text.WordWrap
                        text: modelData
                        font.pixelSize: Style.bodySize
                        color: Style.text
                    }
                    MouseArea {
                        id: wahlDruck
                        anchors.fill: parent
                        enabled: !page.aufgabe.geprueft
                        onClicked: course.answerChoice(index)
                    }
                }
            }

            // ---- Vorhersage -----------------------------------------------
            Column {
                width: parent.width
                spacing: 8
                visible: !page.aufgabe.leer && page.aufgabe.art === "predict"

                Text {
                    text: W.w("Was schreibt das Programm?", course.language)
                    font.pixelSize: Style.smallSize
                    color: Style.dim
                }
                TextArea {
                    id: vorhersage
                    width: parent.width
                    height: 110
                    font.family: Style.mono
                    font.pixelSize: Style.codeSize
                    enabled: !page.aufgabe.geprueft
                    inputMethodHints: Qt.ImhNoAutoUppercase | Qt.ImhNoPredictiveText
                    placeholderText: W.w("Deine Vorhersage", course.language)
                }
                Row {
                    spacing: Style.gap
                    Button {
                        text: W.w("Prüfen", course.language)
                        width: course.lesson.laeuft === true
                               ? spalte.width - 140 : spalte.width
                        enabled: !page.aufgabe.geprueft
                        onClicked: course.answerText(vorhersage.text)
                    }
                    Button {
                        // Bei C++ gibt es auf diesem Gerät nichts
                        // auszuführen; ein Knopf, hinter dem nichts läuft,
                        // wäre eine Zusage, die die App nicht hält.
                        text: W.w("Laufen", course.language)
                        width: 128
                        visible: course.lesson.laeuft === true
                        enabled: !course.running
                        onClicked: course.runCode(page.aufgabe.code, 30)
                    }
                }
            }

            // ---- eine Zahl ausrechnen -------------------------------------
            Column {
                width: parent.width
                spacing: 8
                visible: !page.aufgabe.leer && page.aufgabe.art === "zahl"

                Row {
                    spacing: 10
                    TextField {
                        id: zahlenfeld
                        width: spalte.width - 150
                        enabled: !page.aufgabe.geprueft
                        inputMethodHints: Qt.ImhFormattedNumbersOnly
                        placeholderText: W.w("Zahl", course.language)
                    }
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        width: 130
                        wrapMode: Text.WordWrap
                        text: page.aufgabe.einheit === undefined
                              ? "" : page.aufgabe.einheit
                        font.pixelSize: Style.smallSize
                        color: Style.dim
                    }
                }
                Button {
                    width: parent.width
                    text: W.w("Prüfen", course.language)
                    enabled: !page.aufgabe.geprueft && zahlenfeld.text !== ""
                    onClicked: course.answerNumber(
                                   parseFloat(zahlenfeld.text.replace(",", ".")))
                }
                Text {
                    width: parent.width
                    wrapMode: Text.WordWrap
                    visible: page.aufgabe.geprueft && !page.aufgabe.richtig
                             && page.aufgabe.loesungZeigen
                    text: W.w("Richtig wäre etwa ", course.language) + (page.aufgabe.antwort === undefined
                                                  ? "" : page.aufgabe.antwort)
                          + " " + (page.aufgabe.einheit === undefined
                                   ? "" : page.aufgabe.einheit)
                    font.pixelSize: Style.bodySize
                    color: Style.good
                }
            }

            // ---- Lücken ---------------------------------------------------
            Column {
                id: luecken
                width: parent.width
                spacing: 8
                visible: !page.aufgabe.leer && page.aufgabe.art === "blank"

                property variant felder: []

                Repeater {
                    id: lueckenRepeater
                    model: (!page.aufgabe.leer && page.aufgabe.art === "blank")
                           ? page.aufgabe.luecken : 0
                    Row {
                        spacing: 8
                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            text: W.w("Lücke ", course.language) + (index + 1)
                            font.pixelSize: Style.smallSize
                            color: Style.dim
                            width: 90
                        }
                        TextField {
                            width: luecken.width - 100
                            font.family: Style.mono
                            enabled: !page.aufgabe.geprueft
                            inputMethodHints: Qt.ImhNoAutoUppercase | Qt.ImhNoPredictiveText
                            onTextChanged: {
                                var alle = luecken.felder;
                                alle[index] = text;
                                luecken.felder = alle;
                            }
                        }
                    }
                }
                Button {
                    width: parent.width
                    text: W.w("Prüfen", course.language)
                    enabled: !page.aufgabe.geprueft
                    onClicked: course.answerBlanks(luecken.felder)
                }
            }

            // ---- Zeilen ordnen --------------------------------------------
            Column {
                width: parent.width
                spacing: 8
                visible: !page.aufgabe.leer && page.aufgabe.art === "parsons"

                Text {
                    text: W.w("Deine Lösung – tippe eine Zeile an, um sie zurückzulegen", course.language)
                    font.pixelSize: Style.smallSize
                    color: Style.dim
                }
                Rectangle {
                    width: parent.width
                    height: Math.max(50, gebaut.height + 16)
                    color: Style.codeBg
                    border.color: Style.panelEdge
                    border.width: 1
                    radius: 4

                    Column {
                        id: gebaut
                        x: 8; y: 8
                        width: parent.width - 16
                        Repeater {
                            model: page.loesungsZeilen
                            Rectangle {
                                width: gebaut.width
                                height: 34
                                color: "transparent"
                                Text {
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: modelData
                                    font.family: Style.mono
                                    font.pixelSize: Style.codeSize
                                    color: Style.text
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    enabled: !page.aufgabe.geprueft
                                    onClicked: {
                                        var l = page.loesungsZeilen.slice();
                                        var v = page.vorratsZeilen.slice();
                                        v.push(l[index]);
                                        l.splice(index, 1);
                                        page.loesungsZeilen = l;
                                        page.vorratsZeilen = v;
                                    }
                                }
                            }
                        }
                    }
                }

                Text {
                    text: W.w("Bausteine", course.language)
                    font.pixelSize: Style.smallSize
                    color: Style.dim
                }
                Repeater {
                    model: page.vorratsZeilen
                    Rectangle {
                        width: spalte.width
                        height: 40
                        radius: 4
                        color: vorratDruck.pressed ? Style.panelEdge : Style.panel
                        border.color: Style.panelEdge
                        border.width: 1
                        Text {
                            x: 10
                            anchors.verticalCenter: parent.verticalCenter
                            width: parent.width - 20
                            elide: Text.ElideRight
                            text: modelData
                            font.family: Style.mono
                            font.pixelSize: Style.codeSize
                            color: Style.text
                        }
                        MouseArea {
                            id: vorratDruck
                            anchors.fill: parent
                            enabled: !page.aufgabe.geprueft
                            onClicked: {
                                var l = page.loesungsZeilen.slice();
                                var v = page.vorratsZeilen.slice();
                                l.push(v[index]);
                                v.splice(index, 1);
                                page.loesungsZeilen = l;
                                page.vorratsZeilen = v;
                            }
                        }
                    }
                }
                Button {
                    width: parent.width
                    text: W.w("Prüfen", course.language)
                    enabled: !page.aufgabe.geprueft && page.loesungsZeilen.length > 0
                    onClicked: course.answerParsons(page.loesungsZeilen)
                }
            }

            // ---- selbst schreiben -----------------------------------------
            Column {
                width: parent.width
                spacing: 8
                visible: !page.aufgabe.leer && page.aufgabe.art === "code"

                TextArea {
                    id: editor
                    width: parent.width
                    height: 320
                    text: page.editorText
                    font.family: Style.mono
                    font.pixelSize: Style.codeSize
                    inputMethodHints: Qt.ImhNoAutoUppercase | Qt.ImhNoPredictiveText
                    onTextChanged: page.editorText = text
                }

                // The on-screen keyboard hides braces three layers deep, and
                // these five characters are most of C.
                Row {
                    spacing: 6
                    Repeater {
                        model: ["{", "}", "(", ")", ";", "*", "[", "]"]
                        Rectangle {
                            width: (spalte.width - 42) / 8
                            height: 44
                            radius: 4
                            color: zeichenDruck.pressed ? Style.accent : Style.panel
                            border.color: Style.panelEdge
                            border.width: 1
                            Text {
                                anchors.centerIn: parent
                                text: modelData
                                font.family: Style.mono
                                font.pixelSize: Style.bodySize
                                color: Style.text
                            }
                            MouseArea {
                                id: zeichenDruck
                                anchors.fill: parent
                                onClicked: {
                                    var pos = editor.cursorPosition;
                                    editor.text = editor.text.substring(0, pos)
                                                + modelData
                                                + editor.text.substring(pos);
                                    editor.cursorPosition = pos + 1;
                                }
                            }
                        }
                    }
                }

                Row {
                    spacing: Style.gap
                    Button {
                        text: course.running ? W.w("läuft …", course.language) : W.w("Ausführen", course.language)
                        width: spalte.width - 140
                        enabled: !course.running
                        onClicked: {
                            course.keepCode(editor.text);
                            course.runCode(editor.text,
                                           page.aufgabe.sekunden ? page.aufgabe.sekunden : 10);
                        }
                    }
                    Button {
                        text: W.w("Stopp", course.language)
                        width: 128
                        enabled: course.running
                        onClicked: course.stopRun()
                    }
                }

                Button {
                    width: parent.width
                    text: W.w("Als Antwort prüfen", course.language)
                    enabled: !course.running && course.output !== ""
                    onClicked: course.checkRun()
                }

                Text {
                    width: parent.width
                    wrapMode: Text.WordWrap
                    visible: page.aufgabe.erwartet !== undefined
                             && page.aufgabe.erwartet !== ""
                    text: W.w("Erwartet: ", course.language) + (page.aufgabe.erwartet === undefined
                                          ? "" : page.aufgabe.erwartet)
                    font.family: Style.mono
                    font.pixelSize: Style.smallSize
                    color: Style.faint
                }
            }

            // ---- Ausgabe eines Laufs ---------------------------------------
            OutputBlock {
                width: parent.width
                visible: !page.aufgabe.leer
            }

            // ---- Rückmeldung -----------------------------------------------
            Panel {
                width: parent.width
                height: rueckBlock.height + 2 * Style.pad
                visible: !page.aufgabe.leer && page.aufgabe.geprueft

                Column {
                    id: rueckBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 8

                    Text {
                        text: page.aufgabe.richtig ? W.w("Richtig", course.language) : W.w("Noch nicht", course.language)
                        font.pixelSize: Style.headSize
                        color: page.aufgabe.richtig ? Style.good : Style.warn
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: page.aufgabe.leer ? "" : Style.rich(page.aufgabe.warum)
                        textFormat: Text.RichText
                        font.pixelSize: Style.bodySize
                        color: Style.text
                        lineHeight: 1.25
                        lineHeightMode: Text.ProportionalHeight
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.aufgabe.loesungZeigen && !page.aufgabe.richtig
                                 && page.aufgabe.art !== "code"
                                 && page.aufgabe.art !== "zahl"
                        text: page.loesungstext()
                        font.family: page.aufgabe.art === "mc" ? undefined : Style.mono
                        font.pixelSize: Style.codeSize
                        color: Style.good
                    }
                    // Die richtige Loesung steht nicht von selbst da -- wer
                    // sie sofort liest, denkt nicht mehr nach. Auf Anfrage
                    // gehoert sie aber hin: eine falsche Antwort ohne
                    // Aufloesung ist nur eine Niederlage.
                    // Der zweite Anlauf steht vor der Aufloesung: Wer die
                    // richtige Antwort liest und nickt, behaelt deutlich
                    // weniger als wer sie nach einem Fehlschlag noch einmal
                    // selbst sucht.
                    Button {
                        width: parent.width
                        text: W.w("Nochmal versuchen", course.language)
                        visible: !page.aufgabe.richtig && page.aufgabe.versuche < 2
                        onClicked: {
                            page.zuruecksetzen();
                            course.retryExercise();
                        }
                    }
                    Button {
                        width: parent.width
                        text: W.w("Lösung anzeigen", course.language)
                        visible: !page.aufgabe.richtig && !page.aufgabe.loesungZeigen
                        onClicked: course.showSolution()
                    }
                    CodeBlock {
                        width: parent.width
                        visible: page.aufgabe.loesungZeigen && page.aufgabe.art === "code"
                        code: page.aufgabe.loesung === undefined ? "" : page.aufgabe.loesung
                    }
                }
            }

            Button {
                width: parent.width
                visible: !page.aufgabe.leer && page.aufgabe.geprueft
                text: page.aufgabe.nummer === page.aufgabe.gesamt
                      ? W.w("Lektion abschließen", course.language) : W.w("Nächste Aufgabe", course.language)
                onClicked: page.weiter()
            }

            Button {
                width: parent.width
                visible: !page.aufgabe.leer && !page.aufgabe.geprueft
                text: W.w("Überspringen", course.language)
                onClicked: page.weiter()
            }

            Item { width: 1; height: Style.pad }
        }
    }
}
