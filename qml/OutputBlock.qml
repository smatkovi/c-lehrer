import QtQuick 1.1
import "style.js" as Style

// What a run produced: the text, the picture, or the complaint.
Column {
    id: block
    property bool zeigeBild: true
    spacing: 8

    Text {
        width: parent.width
        wrapMode: Text.WordWrap
        visible: course.error !== ""
        text: course.error + (course.errorLine > 0
                              ? "  (Zeile " + course.errorLine + ")" : "")
        font.pixelSize: Style.smallSize
        color: Style.bad
    }

    Rectangle {
        width: parent.width
        height: ausgabe.paintedHeight + 16
        visible: course.output !== ""
        color: Style.codeBg
        border.color: Style.panelEdge
        border.width: 1
        radius: 4

        Text {
            id: ausgabe
            x: 8
            y: 8
            width: parent.width - 16
            wrapMode: Text.Wrap
            text: course.output
            font.family: Style.mono
            font.pixelSize: Style.codeSize
            color: Style.good
        }
    }

    Image {
        width: parent.width
        height: width * 0.62
        fillMode: Image.PreserveAspectFit
        visible: block.zeigeBild && course.hasPlot
        // The revision in the URL is what makes QML fetch a new picture --
        // it caches by URL, and the provider's path never changes.
        source: course.hasPlot ? "image://plot/" + course.plotRevision : ""
        sourceSize.width: parent.width
        sourceSize.height: parent.width * 0.62
    }

    Text {
        visible: course.seconds > 0
        text: course.seconds.toFixed(2) + " s"
        font.pixelSize: Style.smallSize
        color: Style.faint
    }
}
