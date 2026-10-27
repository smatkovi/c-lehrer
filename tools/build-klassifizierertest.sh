#!/bin/sh
# Das Wolkennetz pruefen -- hier auf dem Rechner, ohne Telefon.
#
# Qt5Core + Qt5Gui genuegen.  Json.cpp kommt aus harbour-lehrer (QJsonDocument);
# die Harmattan-Fassung braucht QtScript, das es hier nicht gibt --
# Klassifizierer.cpp sieht nur Json.h, es ist also derselbe Text im Test.
#
# Ablauf: tests/winzig-modell.py schreibt ein kleines Modell samt Referenz
# nach $AUS, der Pruefstand rechnet nach, die Logits muessen auf < 1e-4
# stimmen; dazu die drei kaputten Dateien (sauberer Fehler, Exit != 0) und,
# wenn ein Foto da ist, die EXIF-Drehprobe.
#
#   tools/build-klassifizierertest.sh [foto.jpg]
#
# Ohne Argument nimmt es ein erk-*.jpg aus ../segelflug/bilder, wenn das
# da liegt.  Ausgaben landen in $TMPDIR (nie im Baum).
set -e
cd "$(dirname "$0")/.."
WURZEL=$(pwd)
# -isystem statt -I: die Qt-Kopfdateien selbst loesen unter -Wextra
# Warnungen aus (deprecated-copy), die nichts mit diesem Text zu tun haben.
INC=$(pkg-config --cflags Qt5Core Qt5Gui | sed "s/-I/-isystem /g")
LIB=$(pkg-config --libs Qt5Core Qt5Gui)
AUS=${TMPDIR:-/tmp}/klassifizierertest
BIN=$AUS/klassifizierertest
JSON_CPP=$WURZEL/../harbour-lehrer/src/Json.cpp
mkdir -p "$AUS"

g++ -std=c++11 -O2 -Wall -Wextra -fPIC -I src \
    $INC src/Klassifizierer.cpp "$JSON_CPP" tests/klassifizierertest.cpp \
    -o "$BIN" $LIB

FOTO=${1:-}
if [ -z "$FOTO" ]; then
    FOTO=$(ls "$WURZEL"/../segelflug/bilder/erk-*.jpg 2>/dev/null | head -n 1 || true)
fi

python3 tests/winzig-modell.py "$AUS" $FOTO

echo "-- Logits gegen die Referenz"
"$BIN" "$AUS/modell.bin" "$AUS/eingabe.rgb" > "$AUS/ergebnis.txt"
python3 - "$AUS" <<'EOF'
import json, sys
aus = sys.argv[1]
erwartet = json.load(open(aus + "/erwartet.json"))["eingabe.rgb"]["logits"]
zeilen = [z for z in open(aus + "/ergebnis.txt").read().split("\n")]
assert zeilen[0].endswith("eingabe.rgb"), zeilen[0]
bekommen = [float(z) for z in zeilen[1:1 + len(erwartet)]]
delta = max(abs(a - b) for a, b in zip(erwartet, bekommen))
print("  erwartet:", " ".join("%.6f" % x for x in erwartet))
print("  bekommen:", " ".join("%.6f" % x for x in bekommen))
print("  max |delta| = %.3g" % delta)
if delta >= 1e-4:
    print("  FEHLER: Abweichung zu gross")
    sys.exit(1)
EOF

echo "-- Kaputte Dateien muessen sauber scheitern"
for k in kennung-falsch kopf-abgeschnitten offset-ausserhalb; do
    if "$BIN" "$AUS/$k.bin" "$AUS/eingabe.rgb" > /dev/null 2> "$AUS/$k.err"; then
        echo "  FEHLER: $k.bin wurde angenommen"
        exit 1
    fi
    echo "  $k: $(cat "$AUS/$k.err")"
done
if "$BIN" "$AUS/eingabe.rgb" "$AUS/eingabe.rgb" > /dev/null 2> "$AUS/kein-modell.err"; then
    echo "  FEHLER: eine .rgb-Datei wurde als Modell angenommen"
    exit 1
fi
echo "  kein-modell: $(cat "$AUS/kein-modell.err")"

echo "-- Zeit (Winzigmodell)"
"$BIN" --zeit "$AUS/modell.bin" "$AUS/eingabe.rgb"

if [ -n "$FOTO" ]; then
    echo "-- bildLaden + bewerten: $FOTO"
    "$BIN" --bild "$AUS/modell.bin" "$FOTO" | tee "$AUS/bild.txt"
    MASSE=$(head -n 1 "$AUS/bild.txt")
    B=${MASSE#Bild }; W=${B%x*}; H=${B#*x}
    echo "-- EXIF-Drehprobe"
    for n in 6 8 3; do
        M=$("$BIN" --bild "$AUS/modell.bin" "$AUS/gedreht-$n.jpg" | head -n 1)
        case $n in
            3) SOLL="Bild ${W}x${H}" ;;
            *) SOLL="Bild ${H}x${W}" ;;
        esac
        if [ "$M" != "$SOLL" ]; then
            echo "  FEHLER: Orientation $n ergab '$M', erwartet '$SOLL'"
            exit 1
        fi
        echo "  Orientation $n: $M"
    done
fi

echo "GRUEN"
