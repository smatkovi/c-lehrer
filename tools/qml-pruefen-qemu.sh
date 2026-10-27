#!/bin/sh
# Jede QML-Seite gegen das ECHTE Harmattan-Qt laden -- ohne Geraet.
#
#   tools/qml-pruefen-qemu.sh [<kurs-verzeichnis>]
#
# Warum das etwas anderes ist als der Pruefer auf dem Rechner: Der laeuft
# gegen ein Desktop-Qt ohne com.nokia.meego und filtert deshalb genau die
# Meldungen weg, die eine Eigenschaft oder Komponente betreffen, die es in
# dieser Fassung der Bibliothek nicht gibt ("Switch hat kein clicked", am
# 09.10.2026 bei Sag's Wien). Hier laeuft die gebaute ARM-Binaerdatei unter
# qemu-arm mit dem MADDE-Sysroot, also mit Qt 4.7.4 und com.nokia.meego 1.0
# in genau der Fassung des N9/N950 -- und --qml-pruefen (main.cpp) laesst
# QDeclarativeComponent jede Datei uebersetzen.
#
# Gebraucht wird auf dem Baurechner: qemu-arm, xvfb-run (die meego-
# Grafikschicht will einen Bildschirm, auch ohne Fenster), das Sysroot und
# eine frische build/c-lehrer aus tools/build.sh.
set -e
cd "$(dirname "$0")/.."
QUELLE=$(pwd)
KURS=${1:-$HOME/ps/segelflug}

HOST=$(sh "$HOME/ps/nfsshift-sfos/tools/buildhost.sh")
FERN=/tmp/qmlprobe
echo "== Pruefrechner: $HOST"

ssh "$HOST" "mkdir -p $FERN/qml $FERN/bin $FERN/data $FERN/bilder"
rsync -r --no-perms --no-owner --no-group "$QUELLE/qml/" "$HOST:$FERN/qml/"
rsync --no-perms --no-owner --no-group "$KURS/data/kurs.json" "$HOST:$FERN/data/kurs.json"
# Das Netz ist zweieinhalb Megabyte und wird zum Laden der Seiten nicht
# gebraucht; Course meldet dann nur "Kein Wolkennetz".
[ -f "$KURS/data/modell.bin" ] && echo "   (modell.bin bleibt hier -- fuer die Seiten unnoetig)"

ssh "$HOST" "set -e
SYS=\${SYSROOT:-\$HOME/QtSDK/Madde/sysroots/harmattan_sysroot_10.2011.34-1_slim}
[ -d \"\$SYS\" ] || { echo 'Sysroot fehlt' >&2; exit 1; }
cp /tmp/c-lehrer-src/build/c-lehrer $FERN/bin/segelflug
cd $FERN
HOME=$FERN QML_IMPORT_PATH=/usr/lib/qt4/imports QT_PLUGIN_PATH=/usr/lib/qt4/plugins \
    xvfb-run -a qemu-arm -L \"\$SYS\" bin/segelflug --qml-pruefen 2>&1 \
    | grep -v 'Fontconfig warning\|ThemeDaemonClient\|GConf Error\|Failed to activate configuration server\|graphics system\|^ *$'"
