// Colours and sizes in one place.
//
// QtQuick 1.1 has no singletons -- "pragma Singleton" arrived with QtQuick 2
// -- and com.nokia.meego exports a "Theme" of its own that beats any context
// property of that name. A plain JS library sidesteps both.
.pragma library

var bg        = "#0e0e12";
var panel     = "#191920";
var panelEdge = "#2a2a34";
var codeBg    = "#0a0a0e";
var text      = "#e4e4ec";
var dim       = "#9a9aa8";
var faint     = "#6a6a78";
var accent    = "#5aa9ff";
var good      = "#7ee787";
var bad       = "#ff6b6b";
var warn      = "#ffb14e";

var mono      = "Andale Mono";

var pad       = 16;
var gap       = 12;

// Wo die gesetzten Formeln liegen. main.qml traegt es beim Start ein --
// eine Bibliothek kennt ihre eigene Adresse nicht, und rich() wird von
// zwei Dutzend Stellen aufgerufen, die alle keinen Pfad kennen sollen.
var bilderPfad = "";
// Breiter als die Seite darf kein Formelbild werden; main.qml traegt die
// Breite ein, die zwischen den Seitenraendern bleibt. Die Bilder kommen in
// natuerlicher Groesse, verkleinert wird erst hier -- so bleibt dieselbe
// Formel auf einem breiten Schirm gross und wird nur hier klein.
var breiteMax = 0;

// Wie gross eine gesetzte Formel neben der Schrift steht; main.qml traegt
// es beim Start ein. Die Formeln sind fuer 17 Punkt bei 100 dpi gesetzt
// (tools/formeln.py), ein Geviert misst also 23,6 Bildpunkte bei Skala 1 --
// ohne diese Zeile stand jede Formel in der Groesse, in der sie gesetzt
// wurde, und nicht in der Groesse der Zeile, in der sie steht.
var skala = 1.0;

// Etwas groesser als die Schrift daneben, weil Brueche, Indizes und
// Exponenten im Bild kleiner ausfallen als die Grundlinie -- bei gleicher
// Hoehe wirkt ein Bruch im Satz winzig. Dieselbe Rechnung wie in
// harbour-lehrer/qml/stil.js, damit beide Fassungen gleich aussehen.
var GEVIERT = 17 * 100 / 72;

function skalaFuer(schriftgroesse) {
    return 1.15 * schriftgroesse / GEVIERT;
}

// Breite und Hoehe eines gesetzten Bildes auf diesem Geraet: skaliert, und
// wenn es dann breiter waere als die Seite, auf die Seite verkleinert.
function bildmasse(b, h) {
    var f = skala;
    if (breiteMax > 0 && b * f > breiteMax)
        f = breiteMax / b;
    return { breite: Math.round(b * f), hoehe: Math.round(h * f) };
}

// Die Lesegroessen sind Harmattans eigene: 24 Punkte fuer den Fliesstext.
// Mit 19 war der ganze Kurs klein gesetzt -- und die gesetzten Formeln
// standen mit ihm klein da, weil sie an der Schrift haengen (skalaFuer).
// Programmtext bleibt bei 16: er soll in die Zeile passen, nicht gelesen
// werden wie Prosa.
var titleSize = 36;
var headSize  = 28;
var bodySize  = 24;
var smallSize = 20;
var codeSize  = 16;

// Turns the little bit of markup the course text uses into rich text.
// Deliberately tiny: **bold**, *italic*, `code`, and paragraphs. A full
// markdown renderer would be a lot of QML for four constructs.
//
// Bold is replaced before italic, or the two asterisks of **bold** would be
// eaten one at a time and leave a stray one behind.
function rich(source) {
    if (!source)
        return "";
    var out = source.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    // Ueberschriften. Die Herleitungen sind lang genug, dass sie
    // Zwischenstufen brauchen -- ohne diese Zeile stand "## Herleitung"
    // woertlich im Text.
    out = out.replace(/^##\s*(.+)$/gm,
                      "<b style='color:" + accent + "'>$1</b>");
    out = out.replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
    out = out.replace(/\*([^*\n]+)\*/g, "<i>$1</i>");
    out = out.replace(/`([^`]+)`/g,
                      "<span style='font-family:" + mono + "; color:" + accent + "'>$1</span>");
    // Gesetzte Formeln im Fliesstext. make-kurs.py hat $...$ durch
    // [[formel:<name>:<breite>:<hoehe>]] ersetzt; hier wird daraus ein
    // Bild in der Zeile. Breite und Hoehe stehen im Marker, weil Rich Text
    // ein Bild ohne Masse erst nach dem Laden setzt und der Absatz dann
    // springt.
    out = out.replace(/\[\[formel:([A-Za-z0-9_-]+):(\d+):(\d+)\]\]/g,
                      function (ganz, name, b, h) {
                          var m = bildmasse(b, h);
                          return "<img src='" + bilderPfad + name + ".png' width='"
                                 + m.breite + "' height='" + m.hoehe + "'>";
                      });
    out = out.replace(/\n\n/g, "<br><br>");
    out = out.replace(/\n/g, "<br>");
    return out;
}
