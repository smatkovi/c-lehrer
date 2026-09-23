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

var titleSize = 30;
var headSize  = 22;
var bodySize  = 19;
var smallSize = 16;
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
    out = out.replace(/\n\n/g, "<br><br>");
    out = out.replace(/\n/g, "<br>");
    return out;
}
