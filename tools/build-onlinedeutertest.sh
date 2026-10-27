#!/bin/sh
# Den Online-Blick pruefen -- hier auf dem Rechner, gegen tests/scheinserver.py
# statt gegen die echte API (kein Schluessel, kein Netz).
#
# Uebersetzt wird die Sailfish-Kopie in harbour-lehrer/src, nicht der Text
# hier: beide sind byteidentisch (das prueft dieses Skript), aber Json.cpp
# braucht hier QtScript, das auf dem Jolla fehlt, und dort QJsonDocument.
# Die Sailfish-Kopie ist ohnehin das Qt-5-Ziel.  Klassifizierer.h kommt aus
# src/, Klassifizierer.cpp wird nicht gebaut -- der Test bringt eine
# Attrappe von bildLaden mit.
set -e
cd "$(dirname "$0")/.."
SFOS=../harbour-lehrer/src
cmp src/OnlineDeuter.cpp "$SFOS/OnlineDeuter.cpp"
cmp src/OnlineDeuter.h "$SFOS/OnlineDeuter.h"

MOC=$(pkg-config --variable=host_bins Qt5Core)/moc
[ -x "$MOC" ] || MOC=moc-qt5
INC=$(pkg-config --cflags Qt5Core Qt5Gui Qt5Network)
LIB=$(pkg-config --libs Qt5Core Qt5Gui Qt5Network)
BAU=${TMPDIR:-/tmp}/onlinedeutertest.bau
mkdir -p "$BAU"
"$MOC" "$PWD/src/OnlineDeuter.h" -o "$BAU/moc_OnlineDeuter.cpp"
"$MOC" "$PWD/tests/onlinedeutertest.cpp" -o "$BAU/onlinedeutertest.moc"
g++ -std=c++11 -Wall -Wextra -Wno-unused-parameter -Wno-deprecated-copy -fPIC \
    -I "$SFOS" -I src -I "$BAU" $INC \
    "$SFOS/OnlineDeuter.cpp" "$SFOS/Json.cpp" "$BAU/moc_OnlineDeuter.cpp" \
    tests/onlinedeutertest.cpp -o "$BAU/onlinedeutertest" $LIB
"$BAU/onlinedeutertest" "$PWD/tests/scheinserver.py"
