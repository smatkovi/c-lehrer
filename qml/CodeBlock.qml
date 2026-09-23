import QtQuick 1.1
import "style.js" as Style

// A piece of program, shown the way a program should be shown: monospace,
// on its own ground, and scrollable sideways rather than wrapped -- wrapped
// C is unreadable, and guessing where a line really ends is exactly the
// confusion a beginner does not need.
Rectangle {
    id: block

    property string code: ""
    property int highlight: 0        // 1-based line to mark, 0 for none

    color: Style.codeBg
    border.color: Style.panelEdge
    border.width: 1
    radius: 4
    height: Math.min(flick.contentHeight + 16, 360)

    Flickable {
        id: flick
        anchors.fill: parent
        anchors.margins: 8
        contentWidth: Math.max(width, text.paintedWidth)
        contentHeight: text.paintedHeight
        clip: true
        flickableDirection: Flickable.HorizontalAndVerticalFlick
        // Without this the block never scrolls once a press lands on it.
        pressDelay: 120

        Rectangle {
            visible: block.highlight > 0
            color: "#40ff6b6b"
            width: flick.contentWidth
            height: text.font.pixelSize * 1.35
            y: (block.highlight - 1) * height
        }

        Text {
            id: text
            text: block.code
            font.family: Style.mono
            font.pixelSize: Style.codeSize
            lineHeight: 1.35
            lineHeightMode: Text.ProportionalHeight
            color: Style.text
            textFormat: Text.PlainText
        }
    }
}
