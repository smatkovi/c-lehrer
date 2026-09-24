import QtQuick 1.1
import "style.js" as Style

// A picture belonging to a lesson or an exercise.
//
// The name in the course data is bare ("cu-humilis"); the file lives in
// <app>/bilder/<name>.png, and the QML sits in <app>/qml, so one step up
// resolves it. Keeping the path out of the course data means the same
// course file works wherever the app is installed.
//
// The height comes from a plain ratio, NOT from the image's own
// implicitHeight. Deriving it from the image while the image fills this
// item is a binding loop: QML detects it, drops the height binding, and the
// frame stays zero pixels tall -- a picture that is present, correct and
// completely invisible.
Rectangle {
    id: rahmen

    property string name: ""
    property real verhaeltnis: 300 / 440      // the drawings' own shape

    visible: name !== ""
    height: visible ? Math.round(width * verhaeltnis) : 0
    color: Style.codeBg
    border.color: Style.panelEdge
    border.width: 1
    radius: 4
    clip: true

    // Zeichnungen tragen ihre Beschriftung im Bild -- in der englischen
    // Fassung muss also ein anderes Bild her. Es heisst <name>.en.png und
    // liegt neben dem deutschen; gibt es keines, bleibt das deutsche stehen
    // (besser ein Bild mit fremder Beschriftung als gar keines).
    Image {
        id: bild
        anchors.fill: parent
        anchors.margins: 1
        property bool zurueckgefallen: false
        source: rahmen.name === "" ? ""
                : Qt.resolvedUrl("../bilder/" + rahmen.name
                                 + (course.language !== "de" && !zurueckgefallen
                                    ? "." + course.language : "") + ".png")
        onStatusChanged: {
            if (status === Image.Error && !zurueckgefallen)
                zurueckgefallen = true;
        }
        onSourceChanged: if (course.language === "de") zurueckgefallen = false
        fillMode: Image.PreserveAspectFit
        smooth: true
        asynchronous: true
    }
}
