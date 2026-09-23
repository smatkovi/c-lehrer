import QtQuick 1.1
import com.nokia.meego 1.0
import "style.js" as Style

// C-Lehrer -- C und C++ lernen, mit Blick auf Simulation.
PageStackWindow {
    id: app
    showStatusBar: true
    // Die Leiste traegt den Zurueck-Knopf. Ohne sie gibt es auf Harmattan
    // keinen Weg zurueck ausser einem Knopf am Ende der Seite -- und auf
    // einer langen, scrollenden Seite findet den niemand.
    showToolBar: true
    initialPage: StartPage { }

    Component.onCompleted: theme.inverted = true

    Rectangle {
        // The components draw their own background per page; this one keeps
        // the colour steady during page transitions.
        anchors.fill: parent
        color: Style.bg
        z: -1
    }
}
