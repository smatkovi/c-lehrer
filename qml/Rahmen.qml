import QtQuick 1.1
import "style.js" as Style

// Wovon eine Aufgabe ausgeht und worauf sie hinauswill.
//
// Steht ueber der Frage und nicht in der Rueckmeldung: Eine Aufgabe ohne
// genannte Annahmen ist ein Raetsel -- wer nicht weiss, dass die Masse 1 kg
// ist oder dass `int` hier 32 Bit hat, raet nicht schlechter, nur an einer
// anderen Stelle. Verraten wird damit nichts: Es sind die Zahlen und
// Gleichungen, mit denen gerechnet wird, nicht das Ergebnis.
//
// Die Reihenfolge ist Absicht. Zuerst **Mathematisch**: die Gleichung, das
// Gebiet, Anfangs- und Randbedingungen, die Diskretisierung, die Bedingung,
// unter der das Verfahren haelt. Dann **Physikalisch**: woher die Gleichung
// kommt und was weggelassen wurde. Dann der Rest, dann das Ziel. Wer die
// Physik zuerst liest, sucht in der Mathematik danach; umgekehrt nicht.
//
// Jedes Feld ist einzeln entbehrlich -- eine Aufgabe ueber `printf` hat
// keine Physik, und ein "Ziel: Sag voraus, was das Programm schreibt" unter
// der Frage "Was schreibt dieses Programm?" waere Laerm.
Rectangle {
    id: rahmen

    property string mathematisch: ""
    property string physikalisch: ""
    property string annahmen: ""
    property string ziel: ""
    property string sprache: "de"

    color: Style.panel
    border.color: Style.panelEdge
    border.width: 1
    radius: 6
    visible: mathematisch !== "" || physikalisch !== ""
             || annahmen !== "" || ziel !== ""
    height: visible ? spalte.height + 24 : 0

    Column {
        id: spalte
        x: 12; y: 12
        width: parent.width - 24
        spacing: 12

        RahmenBlock {
            width: spalte.width
            sprache: rahmen.sprache
            titel: "Mathematisch"
            inhalt: rahmen.mathematisch
        }
        RahmenBlock {
            width: spalte.width
            sprache: rahmen.sprache
            titel: "Physikalisch"
            inhalt: rahmen.physikalisch
        }
        RahmenBlock {
            width: spalte.width
            sprache: rahmen.sprache
            titel: "Annahmen"
            inhalt: rahmen.annahmen
        }
        RahmenBlock {
            width: spalte.width
            sprache: rahmen.sprache
            titel: "Ziel"
            inhalt: rahmen.ziel
        }
    }
}
