#!/bin/sh
# Das Gedaechtnis pruefen -- hier auf dem Rechner, ohne Telefon.
#
# Uebersetzt wird die Sailfish-Kopie in harbour-lehrer/src, nicht der Text
# hier: beide sind byteidentisch (das prueft dieses Skript), aber Json.cpp
# braucht hier QtScript, das auf dem Jolla fehlt, und dort QJsonDocument.
# Nachlernen.cpp selbst kennt nur QtCore, QtGui (QImage, QBuffer) und Json.h.
set -e
cd "$(dirname "$0")/.."
SFOS=../harbour-lehrer/src
cmp src/Nachlernen.cpp "$SFOS/Nachlernen.cpp"
cmp src/Nachlernen.h "$SFOS/Nachlernen.h"

# -isystem statt -I: die Qt-Kopfdateien loesen unter -Wextra eigene
# Warnungen aus, die nichts mit diesem Text zu tun haben.
INC=$(pkg-config --cflags Qt5Core Qt5Gui | sed "s/-I/-isystem /g")
LIB=$(pkg-config --libs Qt5Core Qt5Gui)
AUS=${TMPDIR:-/tmp}/nachlernentest
mkdir -p "$AUS"
g++ -std=c++11 -O2 -Wall -Wextra -fPIC -I "$SFOS" \
    $INC "$SFOS/Nachlernen.cpp" "$SFOS/Json.cpp" tests/nachlernentest.cpp \
    -o "$AUS/nachlernentest" $LIB
"$AUS/nachlernentest"
