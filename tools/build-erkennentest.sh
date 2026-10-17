#!/bin/sh
# Den Erkennungsmodus pruefen -- hier auf dem Rechner, ohne Telefon.
# Qt5 genuegt: Erkennen.cpp kennt nur QVariant und QMap.
set -e
cd "$(dirname "$0")/.."
INC=$(pkg-config --cflags Qt5Core)
LIB=$(pkg-config --libs Qt5Core)
OUT=${TMPDIR:-/tmp}/erkennentest
g++ -std=c++11 -Wall -Wextra -Wno-unused-parameter -fPIC -I src \
    $INC src/Erkennen.cpp tests/erkennentest.cpp -o "$OUT" $LIB
"$OUT"
