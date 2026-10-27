import QtQuick 1.1
import com.nokia.meego 1.0
import Qt.labs.folderlistmodel 1.0
import "style.js" as Style
import "worte.js" as W

// Ein Foto aus den Bilderordnern waehlen -- die eigene Galerie.
//
// **Nicht ueber die Galerie des Systems.** QtMobilitys DocumentGalleryModel
// liest den Tracker-Index aus ~/.cache/tracker, und das Verzeichnis gehoert
// `metadata-users` mit Modus d---rwx---: als `user` liefert jede Abfrage 0
// Treffer (am N950 nachgemessen, siehe harbour-sagswien/meego). Die Dateien
// selbst sind lesbar, also geht es ueber das Dateisystem: zwei Ordner, in
// denen auf diesem Geraet Bilder liegen, das Neueste zuerst.
//
// Qt 4.7s FolderListModel kennt keine Rolle, an der sich ein Ordner von
// einer Datei unterscheiden liesse -- darum zwei feste Ordner statt eines
// Baums.
Page {
    id: page
    orientationLock: PageOrientation.Automatic

    tools: ToolBarLayout {
        ToolIcon {
            platformIconId: "toolbar-back"
            onClicked: pageStack.pop()
        }
    }

    property string wurzel: "file:///home/user/MyDocs"

    Rectangle { anchors.fill: parent; color: Style.bg }

    Column {
        id: kopf
        x: Style.pad
        y: Style.pad
        width: page.width - 2 * Style.pad
        spacing: Style.gap

        Text {
            text: W.w("Foto wählen", course.language)
            font.pixelSize: Style.titleSize
            color: Style.accent
        }

        // Die Ordner als Umschalter, im Stil des Sprachschalters auf der
        // Startseite.
        Row {
            spacing: Style.gap
            Repeater {
                model: [
                    { name: "Kamera", pfad: "/DCIM" },
                    { name: "Bilder", pfad: "/Pictures" }
                ]
                Rectangle {
                    width: 140
                    height: 52
                    radius: 6
                    color: bilder.folder === page.wurzel + modelData.pfad
                           ? Style.accent : Style.panel
                    border.color: Style.panelEdge
                    border.width: 1
                    Text {
                        anchors.centerIn: parent
                        text: W.w(modelData.name, course.language)
                        font.pixelSize: Style.smallSize
                        color: bilder.folder === page.wurzel + modelData.pfad
                               ? Style.bg : Style.text
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: bilder.folder = page.wurzel + modelData.pfad
                    }
                }
            }
        }
    }

    GridView {
        id: raster
        anchors.top: kopf.bottom
        anchors.topMargin: Style.gap
        anchors.bottom: parent.bottom
        x: Style.pad
        width: page.width - 2 * Style.pad
        cellWidth: Math.floor(width / 3)
        cellHeight: cellWidth
        clip: true
        cacheBuffer: 0

        model: FolderListModel {
            id: bilder
            folder: page.wurzel + "/DCIM"
            nameFilters: ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG"]
            showDirs: false
            showDotAndDotDot: false
            // Das Neueste zuerst: wer deuten will, hat das Foto meist
            // gerade eben geschossen.
            sortField: FolderListModel.Time
            sortReversed: false
        }

        delegate: Item {
            width: raster.cellWidth
            height: raster.cellHeight

            Rectangle {
                anchors.fill: parent
                anchors.margins: 2
                color: Style.panel
            }

            Image {
                anchors.fill: parent
                anchors.margins: 2
                fillMode: Image.PreserveAspectCrop
                clip: true
                asynchronous: true
                // Klein dekodieren -- ein volles Foto je Kachel bringt
                // das N9 ins Schwitzen.
                sourceSize.width: 160
                sourceSize.height: 160
                // filePath ist hier schon eine URL ("file:///home/user/..."),
                // kein nackter Pfad -- am Geraet nachgesehen. Ein
                // vorangestelltes "file://" ergaebe ein leeres Bild.
                source: filePath
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    // Course will einen Dateipfad (QImage), das Modell
                    // gibt eine URL -- also abschneiden.
                    var s = String(filePath);
                    course.classifyPhoto(s.indexOf("file://") === 0
                                         ? s.substring(7) : s);
                    pageStack.pop();
                }
            }
        }
    }

    ScrollDecorator { flickableItem: raster }

    Text {
        anchors.centerIn: raster
        width: raster.width - 2 * Style.pad
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
        visible: raster.count === 0
        text: W.w("In diesem Ordner liegen keine Bilder.", course.language)
        font.pixelSize: Style.bodySize
        color: Style.dim
    }
}
