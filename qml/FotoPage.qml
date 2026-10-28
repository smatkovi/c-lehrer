import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style
import "worte.js" as W

// Foto deuten: ein eigenes Himmelsfoto, erst der eigene Tipp, dann das
// Netz im Geraet -- und auf Wunsch Claude dazu.
//
// Die Reihenfolge ist der Zweck der Seite. Das Netz ist meist schon
// fertig, bevor der Leser die Ratetafel ueberhaupt gelesen hat; stuende
// sein Ergebnis da, tippte niemand mehr selbst. Also bleibt es verborgen,
// bis ein Tipp steht (course.photo.geraten), und erst dann erscheinen
// beide Urteile nebeneinander, das eigene ausdruecklich darunter.
//
// Alles, was entschieden wird, entscheidet Course: Die Seite liest
// course.photo und ruft classifyPhoto, guessPhoto, askOnline.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }

    property variant foto: course.photo
    // Die Hinweise zum Fotografieren; fehlt die Eigenschaft im Programm,
    // bleibt die Liste leer statt die Seite zu verlieren.
    property variant tipps: course.classifierTips === undefined
                            ? [] : course.classifierTips
    // Die Kamera ist auf Harmattan ein Versuch: Gibt es eine ladbare
    // KameraPage.qml, erscheint die Taste, sonst nicht. Das Element aus
    // QtMultimediaKit 1.1 bleibt auf N9 und N950 schwarz (siehe
    // ces-chor/ScannerPage.qml), darum liegt hier vorerst keine.
    property variant kameraBauplan: null
    property bool kameraDa: false
    // Woran man es sieht, aufgeklappt?
    property bool mehr: false
    // Die Tafel zum Richtigstellen, aufgeklappt?
    property bool richtig: false

    Connections {
        target: course
        onPhotoChanged: page.foto = course.photo
    }

    Component.onCompleted: {
        var k = Qt.createComponent(Qt.resolvedUrl("KameraPage.qml"));
        if (k.status === Component.Ready) {
            page.kameraBauplan = k;
            page.kameraDa = true;
        }
    }

    // Das Foto gehoert zu dieser Seite; wer zurueckgeht, faengt beim
    // naechsten Mal leer an.
    Component.onDestruction: course.clearPhoto()

    function sicherheitsWort(s) {
        if (s === "hoch") return W.w("hoch", course.language);
        if (s === "mittel") return W.w("mittel", course.language);
        if (s === "niedrig") return W.w("niedrig", course.language);
        return s === undefined ? "" : s;
    }

    Rectangle { anchors.fill: parent; color: Style.bg }

    Flickable {
        id: lauf
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
                text: course.classifierTitle
                font.pixelSize: Style.titleSize
                color: Style.accent
            }
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                visible: page.foto.leer
                text: course.classifierSubtitle
                font.pixelSize: Style.smallSize
                color: Style.dim
            }

            // ---- Foto holen --------------------------------------------
            Row {
                width: parent.width
                spacing: Style.gap

                Button {
                    width: page.kameraDa
                           ? (parent.width - Style.gap) / 2 : parent.width
                    text: W.w("Foto wählen", course.language)
                    onClicked: {
                        page.mehr = false;
                        pageStack.push(Qt.resolvedUrl("FotoWahlPage.qml"));
                    }
                }
                Button {
                    width: (parent.width - Style.gap) / 2
                    visible: page.kameraDa
                    text: W.w("Foto aufnehmen", course.language)
                    onClicked: {
                        page.mehr = false;
                        pageStack.push(page.kameraBauplan);
                    }
                }
            }

            // ---- so gelingt das Foto (nur solange keins da ist) ---------
            Panel {
                width: parent.width
                height: tippBlock.height + 2 * Style.pad
                visible: page.foto.leer && page.tipps.length > 0

                Column {
                    id: tippBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 6

                    Text {
                        text: W.w("So gelingt das Foto", course.language)
                        font.pixelSize: Style.headSize
                        color: Style.text
                    }
                    Repeater {
                        model: page.tipps
                        Text {
                            width: tippBlock.width
                            wrapMode: Text.WordWrap
                            text: "• " + modelData
                            font.pixelSize: Style.smallSize
                            color: Style.dim
                            lineHeight: 1.2
                            lineHeightMode: Text.ProportionalHeight
                        }
                    }
                }
            }

            // ---- das Foto ----------------------------------------------
            // Klein dekodiert (sourceSize 640): Die Kamera liefert acht
            // Millionen Bildpunkte, und die voll zu entpacken kostet auf
            // dem N9 Sekunden und den halben Speicher. Die Hoehe kommt
            // aus den Massen des geladenen Bildes, nicht aus
            // implicitHeight -- das waere die Bindungsschleife aus
            // Bild.qml.
            Rectangle {
                id: rahmen
                width: spalte.width
                /* Feste Hoehe im Verhaeltnis 4:3, nicht aus dem Bild
                   gerechnet.  Qt 4.7.4 gibt `sourceSize.height` als 0
                   zurueck, wenn nur `sourceSize.width` gesetzt ist -- der
                   Rahmen waere dann 0 Pixel hoch und das Foto unsichtbar
                   (am Pruefstand gemessen).  Und eine Hoehe, die am
                   geladenen Bild haengt, ist der Ringschluss aus Bild.qml.
                   Also ein Kasten, in den das Bild hineinpasst. */
                height: Math.round(width * 0.75)
                visible: !page.foto.leer
                color: Style.codeBg
                border.color: Style.panelEdge
                border.width: 1
                radius: 4
                clip: true

                Image {
                    id: bild
                    anchors.centerIn: parent
                    /* Hochkant geschossene Fotos: Qt 4 dreht QML-Bilder
                       nicht nach EXIF, waehrend das Netz sie gedreht sieht
                       (Klassifizierer::bildLaden).  Also hier selbst
                       drehen -- und bei 90 oder 270 Grad Breite und Hoehe
                       tauschen, sonst steht das Bild aus dem Rahmen. */
                    property bool quer: page.foto.drehung === 90
                                        || page.foto.drehung === 270
                    width: (quer ? rahmen.height : rahmen.width) - 2
                    height: (quer ? rahmen.width : rahmen.height) - 2
                    rotation: page.foto.drehung === undefined ? 0 : page.foto.drehung
                    source: page.foto.leer ? "" : "file://" + page.foto.pfad
                    sourceSize.width: 640
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                    asynchronous: true
                }

                BusyIndicator {
                    anchors.centerIn: parent
                    running: bild.status === Image.Loading
                    visible: running
                }
            }

            // ---- Fehler beim Laden oder Rechnen ------------------------
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                visible: !page.foto.leer && page.foto.fehler !== ""
                text: page.foto.fehler === undefined ? "" : page.foto.fehler
                font.pixelSize: Style.bodySize
                color: Style.bad
            }

            // ---- der eigene Tipp ---------------------------------------
            Text {
                width: parent.width
                wrapMode: Text.WordWrap
                visible: !page.foto.leer && page.foto.geraten === ""
                         && page.foto.fehler === ""
                text: W.w("Was siehst du?", course.language)
                font.pixelSize: Style.headSize
                color: Style.text
            }

            Grid {
                id: tafel
                width: parent.width
                columns: 2
                spacing: Style.gap
                visible: !page.foto.leer && page.foto.geraten === ""
                         && page.foto.fehler === ""

                Repeater {
                    model: tafel.visible ? course.classifierClasses : []
                    Rectangle {
                        width: (tafel.width - Style.gap) / 2
                        height: wahl.paintedHeight + 24
                        radius: 6
                        border.width: 1
                        border.color: Style.panelEdge
                        color: druck.pressed ? Style.panelEdge : Style.panel

                        Text {
                            id: wahl
                            x: 12
                            y: 12
                            width: parent.width - 24
                            wrapMode: Text.WordWrap
                            text: modelData.name
                            font.pixelSize: Style.bodySize
                            color: Style.text
                        }
                        MouseArea {
                            id: druck
                            anchors.fill: parent
                            onClicked: course.guessPhoto(modelData.id)
                        }
                    }
                }
            }

            Button {
                width: parent.width
                visible: tafel.visible
                text: W.w("Weiß nicht", course.language)
                onClicked: course.guessPhoto("")
            }

            // Das Netz rechnet noch -- dezent, der Tipp geht vor.
            Row {
                spacing: Style.gap
                visible: !page.foto.leer && page.foto.laeuft === true
                BusyIndicator {
                    running: parent.visible
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    text: W.w("Das Netz rechnet …", course.language)
                    font.pixelSize: Style.smallSize
                    color: Style.faint
                }
            }

            // ---- das Netz sagt -----------------------------------------
            Panel {
                width: parent.width
                height: netzBlock.height + 2 * Style.pad
                visible: !page.foto.leer && page.foto.geraten !== ""
                         && page.foto.fertig === true && page.foto.fehler === ""

                Column {
                    id: netzBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 8

                    Text {
                        text: W.w("Das Netz sagt", course.language)
                        font.pixelSize: Style.headSize
                        color: Style.text
                    }

                    Repeater {
                        model: (page.foto.ergebnis === undefined || !netzBlock.visible)
                               ? [] : page.foto.ergebnis
                        Column {
                            width: netzBlock.width
                            spacing: 3

                            Row {
                                width: parent.width
                                Text {
                                    width: parent.width - 80
                                    wrapMode: Text.WordWrap
                                    text: modelData.name
                                    font.pixelSize: Style.bodySize
                                    font.bold: index === 0
                                    color: index === 0 ? Style.accent : Style.text
                                }
                                Text {
                                    width: 80
                                    horizontalAlignment: Text.AlignRight
                                    text: modelData.prozent + " %"
                                    font.pixelSize: Style.bodySize
                                    font.bold: index === 0
                                    color: index === 0 ? Style.accent : Style.dim
                                }
                            }
                            Rectangle {
                                width: parent.width
                                height: 8
                                radius: 4
                                color: Style.codeBg
                                Rectangle {
                                    width: Math.round(parent.width * modelData.prozent / 100)
                                    height: parent.height
                                    radius: 4
                                    color: index === 0 ? Style.accent : Style.panelEdge
                                }
                            }
                            // Die Bedeutung fuers Fliegen, nur beim ersten.
                            Text {
                                width: parent.width
                                wrapMode: Text.WordWrap
                                visible: index === 0 && modelData.sinn !== undefined
                                         && modelData.sinn !== ""
                                text: "→ " + modelData.sinn
                                font.pixelSize: Style.bodySize
                                color: Style.good
                            }
                        }
                    }

                    // Woran man es sieht und was es heisst: aufklappbar,
                    // weil beide Texte lang sind und die Prozente sonst
                    // vom Bildschirm schieben.
                    Text {
                        text: page.mehr ? W.w("Weniger", course.language)
                                        : W.w("Woran erkennt man das?", course.language)
                        font.pixelSize: Style.smallSize
                        color: Style.accent
                        MouseArea {
                            anchors.fill: parent
                            anchors.margins: -8
                            onClicked: page.mehr = !page.mehr
                        }
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.mehr
                        text: (page.foto.ergebnis === undefined
                               || page.foto.ergebnis.length === 0)
                              ? "" : page.foto.ergebnis[0].erkennen
                        font.pixelSize: Style.smallSize
                        color: Style.dim
                        lineHeight: 1.2
                        lineHeightMode: Text.ProportionalHeight
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.mehr
                        text: (page.foto.ergebnis === undefined
                               || page.foto.ergebnis.length === 0)
                              ? "" : page.foto.ergebnis[0].bedeutet
                        font.pixelSize: Style.smallSize
                        color: Style.dim
                        lineHeight: 1.2
                        lineHeightMode: Text.ProportionalHeight
                    }

                    // Das Gelernte hat die Reihenfolge gedreht -- sonst
                    // waere nicht zu sehen, dass es etwas tut.
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.gelernt !== undefined
                                 && page.foto.gelernt.korrigiert === true
                        text: W.w("Das Gelernte hat dieses Urteil geändert.", course.language)
                        font.pixelSize: Style.smallSize
                        color: Style.accent
                    }

                    // Rueckmeldung zum eigenen Tipp. Bei "weiss nicht"
                    // gibt es nichts zu bewerten.
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.geraten !== "?"
                        text: page.foto.treffer === true
                              ? W.w("Richtig geraten", course.language)
                              : W.w("Du hattest auf ", course.language)
                                + page.foto.geratenName
                                + W.w(" getippt", course.language) + "."
                        font.pixelSize: Style.bodySize
                        font.bold: true
                        color: page.foto.treffer === true ? Style.good : Style.warn
                    }
                }
            }

            // ---- Claude dazu -------------------------------------------
            // Nur wenn es einen Weg ins Netz gibt; ohne Schluessel steht
            // davor das Feld dafuer. Der Schluessel geht an Course und
            // nirgendwohin sonst.
            Column {
                width: parent.width
                spacing: Style.gap
                visible: course.onlineAvailable && !page.foto.leer
                         && page.foto.geraten !== "" && page.foto.fertig === true
                         && page.foto.fehler === ""
                         && page.foto.online.laeuft !== true
                         && (page.foto.online.fertig !== true
                             || page.foto.online.ok !== true)

                TextField {
                    id: schluessel
                    width: parent.width
                    visible: !course.hasApiKey
                    echoMode: TextInput.Password
                    placeholderText: W.w("Anthropic-Schlüssel", course.language)
                    inputMethodHints: Qt.ImhNoPredictiveText | Qt.ImhNoAutoUppercase
                }
                Button {
                    width: parent.width
                    visible: !course.hasApiKey
                    enabled: schluessel.text.length > 0
                    text: W.w("Speichern", course.language)
                    onClicked: {
                        course.setApiKey(schluessel.text);
                        schluessel.text = "";
                    }
                }
                Button {
                    width: parent.width
                    visible: course.hasApiKey
                    text: W.w("Claude fragen", course.language)
                    onClicked: course.askOnline()
                }
                Text {
                    width: parent.width
                    wrapMode: Text.WordWrap
                    visible: page.foto.online.fertig !== true
                    text: W.w("Das Foto wird an Anthropic geschickt.", course.language)
                    font.pixelSize: Style.smallSize
                    color: Style.faint
                }
            }

            Panel {
                width: parent.width
                height: claudeBlock.height + 2 * Style.pad
                visible: !page.foto.leer && page.foto.geraten !== ""
                         && (page.foto.online.laeuft === true
                             || page.foto.online.fertig === true)

                Column {
                    id: claudeBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 8

                    Text {
                        text: W.w("Claude sagt", course.language)
                        font.pixelSize: Style.headSize
                        color: Style.text
                    }

                    Row {
                        spacing: Style.gap
                        visible: page.foto.online.laeuft === true
                        BusyIndicator {
                            running: parent.visible
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            text: W.w("Claude schaut …", course.language)
                            font.pixelSize: Style.smallSize
                            color: Style.faint
                        }
                    }

                    // Fertig und gut: Klasse, Sicherheit, Begruendung,
                    // Bedeutung.
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.online.fertig === true
                                 && page.foto.online.ok === true
                        text: (page.foto.online.name === undefined
                               || page.foto.online.name === "")
                              ? W.w("Keine der Klassen", course.language)
                              : page.foto.online.name
                        font.pixelSize: Style.bodySize
                        font.bold: true
                        color: Style.accent
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.online.fertig === true
                                 && page.foto.online.ok === true
                        text: W.w("Sicherheit: ", course.language)
                              + page.sicherheitsWort(page.foto.online.sicherheit)
                              + (page.foto.online.modell === undefined || page.foto.online.modell === ""
                                 ? "" : " · " + page.foto.online.modell)
                        font.pixelSize: Style.smallSize
                        color: Style.dim
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.online.fertig === true
                                 && page.foto.online.ok === true
                        text: page.foto.online.begruendung === undefined
                              ? "" : page.foto.online.begruendung
                        /* Der Text kommt vom Server: als PlainText, nicht als
                           AutoText -- sonst deutet Qt ein <img src="http://...">
                           darin als Auszeichnung und holt das Bild wirklich ab. */
                        textFormat: Text.PlainText
                        font.pixelSize: Style.bodySize
                        color: Style.text
                        lineHeight: 1.2
                        lineHeightMode: Text.ProportionalHeight
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.online.fertig === true
                                 && page.foto.online.ok === true
                                 && page.foto.online.sinn !== undefined
                                 && page.foto.online.sinn !== ""
                        text: "→ " + page.foto.online.sinn
                        font.pixelSize: Style.bodySize
                        color: Style.good
                    }
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.online.fertig === true
                                 && page.foto.online.ok === true
                        text: page.foto.online.einig === true
                              ? W.w("Netz und Claude sind sich einig.", course.language)
                              : W.w("Claude sieht es anders als das Netz.", course.language)
                        font.pixelSize: Style.smallSize
                        color: page.foto.online.einig === true ? Style.good : Style.warn
                    }

                    // Fertig und schief: der Grund.
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.online.fertig === true
                                 && page.foto.online.ok !== true
                        text: page.foto.online.fehler === undefined
                              ? "" : page.foto.online.fehler
                        /* Der Text kommt vom Server: als PlainText, nicht als
                           AutoText -- sonst deutet Qt ein <img src="http://...">
                           darin als Auszeichnung und holt das Bild wirklich ab. */
                        textFormat: Text.PlainText
                        font.pixelSize: Style.bodySize
                        color: Style.bad
                    }
                }
            }

            // ---- Dazulernen --------------------------------------------
            // Stimmen Claudes Urteil und der eigene Tipp ueberein, hat
            // Course das Foto schon gemerkt (GELERNTES.md). Gehen sie
            // auseinander, entscheidet hier der Leser -- und wer es besser
            // weiss, stellt ohnehin richtig.
            Panel {
                width: parent.width
                height: lernBlock.height + 2 * Style.pad
                visible: page.foto.gelernt !== undefined
                         && page.foto.gelernt.merkbar === true
                         && page.foto.geraten !== ""

                Column {
                    id: lernBlock
                    x: Style.pad
                    y: Style.pad
                    width: parent.width - 2 * Style.pad
                    spacing: 8

                    Text {
                        text: W.w("Dazulernen", course.language)
                        font.pixelSize: Style.headSize
                        color: Style.text
                    }

                    // Schon gemerkt: was und wie viel insgesamt.
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.gelernt.gemerkt !== ""
                        text: W.w("Gemerkt als ", course.language)
                              + page.foto.gelernt.gemerktName + "."
                        font.pixelSize: Style.bodySize
                        color: Style.good
                    }

                    // Claude und der eigene Tipp gehen auseinander: wer hat recht?
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        visible: page.foto.gelernt.gemerkt === ""
                                 && page.foto.online.fertig === true
                                 && page.foto.online.ok === true
                                 && page.foto.online.einig !== true
                        text: W.w("Wessen Urteil soll das Netz lernen?", course.language)
                        font.pixelSize: Style.bodySize
                        color: Style.text
                    }
                    Row {
                        width: parent.width
                        spacing: Style.gap
                        visible: page.foto.gelernt.gemerkt === ""
                                 && page.foto.online.fertig === true
                                 && page.foto.online.ok === true
                                 && page.foto.online.einig !== true
                                 && page.foto.online.klasse !== undefined
                                 && page.foto.online.klasse !== ""
                        Button {
                            width: (parent.width - Style.gap) / 2
                            text: W.w("Claude", course.language)
                            onClicked: course.rememberPhoto(page.foto.online.klasse, 1)
                        }
                        Button {
                            width: (parent.width - Style.gap) / 2
                            visible: page.foto.geraten !== "?"
                            text: W.w("Mein Tipp", course.language)
                            onClicked: course.rememberPhoto(page.foto.geraten, 2)
                        }
                    }

                    // Richtigstellen: die eigene Klasse waehlen, auch ohne Claude.
                    Text {
                        text: page.richtig ? W.w("Weniger", course.language)
                                           : W.w("Es ist etwas anderes", course.language)
                        font.pixelSize: Style.smallSize
                        color: Style.accent
                        MouseArea {
                            anchors.fill: parent
                            anchors.margins: -8
                            onClicked: page.richtig = !page.richtig
                        }
                    }
                    Grid {
                        id: richtigTafel
                        width: parent.width
                        columns: 2
                        spacing: 6
                        visible: page.richtig

                        Repeater {
                            model: page.richtig ? course.classifierClasses : []
                            Rectangle {
                                width: (richtigTafel.width - 6) / 2
                                height: richtigWahl.paintedHeight + 18
                                radius: 6
                                border.width: 1
                                border.color: Style.panelEdge
                                color: richtigDruck.pressed ? Style.panelEdge : Style.codeBg
                                Text {
                                    id: richtigWahl
                                    x: 9
                                    y: 9
                                    width: parent.width - 18
                                    wrapMode: Text.WordWrap
                                    text: modelData.name
                                    font.pixelSize: Style.smallSize
                                    color: Style.text
                                }
                                MouseArea {
                                    id: richtigDruck
                                    anchors.fill: parent
                                    onClicked: {
                                        course.rememberPhoto(modelData.id, 2);
                                        page.richtig = false;
                                    }
                                }
                            }
                        }
                    }

                    // Wie weit das Gedaechtnis ist.
                    Text {
                        width: parent.width
                        wrapMode: Text.WordWrap
                        text: page.foto.gelernt.wirksam === true
                              ? W.w("Gelernt: ", course.language)
                                + page.foto.gelernt.anzahl
                                + W.w(" Fotos — das Netz zieht sie mit ein.", course.language)
                              : W.w("Gelernt: ", course.language)
                                + page.foto.gelernt.anzahl
                                + W.w(" Fotos. Ab ", course.language)
                                + (page.foto.gelernt.anzahl + page.foto.gelernt.fehlende)
                                + W.w(" zieht das Netz sie mit ein.", course.language)
                        font.pixelSize: Style.smallSize
                        color: Style.dim
                    }
                    Button {
                        width: parent.width
                        visible: page.foto.gelernt.anzahl > 0
                        text: W.w("Gelerntes ansehen", course.language)
                        onClicked: pageStack.push(Qt.resolvedUrl("GelerntesPage.qml"))
                    }
                }
            }

            Item { width: 1; height: Style.pad }
        }
    }

    ScrollDecorator { flickableItem: lauf }
}
