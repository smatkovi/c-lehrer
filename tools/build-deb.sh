#!/bin/sh
# Packs the built binary, the interpreter, the course and the QML into a .deb.
#
# Architecture is armel, not "all": the app is native C++ and carries the C
# interpreter with it. Both the N9 and the N950 are the same armel, so one
# package covers them.
#
# No versioned dependency anywhere on purpose. "libqt4-gui (>= 4.7.4)" looks
# harmless and is not: the installed Qt is 4.7.4~git20120327, and "~" sorts
# BELOW the empty string in Debian ordering, so that dependency can never be
# satisfied. The package then stays half-installed and the launcher draws a
# red exclamation mark over the icon.
#
#   tools/build-deb.sh [version]
set -e
cd "$(dirname "$0")/.."

VERSION=${1:-0.1}
STAGE=build/stage
rm -rf "$STAGE"

mkdir -p "$STAGE/opt/c-lehrer/bin" "$STAGE/opt/c-lehrer/qml" \
         "$STAGE/opt/c-lehrer/data" "$STAGE/opt/c-lehrer/bilder" "$STAGE/usr/share/applications" \
         "$STAGE/usr/share/icons/hicolor/80x80/apps" "$STAGE/DEBIAN"

[ -x build/c-lehrer ] || { echo "build/c-lehrer fehlt -- erst tools/build.sh" >&2; exit 1; }
[ -x bin/crun ] || { echo "bin/crun fehlt -- erst tools/build-crun.sh" >&2; exit 1; }
[ -x bin/rrun ] || { echo "bin/rrun fehlt -- erst tools/build-rrun.sh" >&2; exit 1; }

cp build/c-lehrer "$STAGE/opt/c-lehrer/bin/"
cp bin/crun "$STAGE/opt/c-lehrer/bin/"
cp bin/rrun "$STAGE/opt/c-lehrer/bin/"
cp qml/*.qml qml/*.js "$STAGE/opt/c-lehrer/qml/"
cp data/kurs.json "$STAGE/opt/c-lehrer/data/"
# Die gesetzten Formeln. Ohne sie bleibt die Codezeile stehen und nur das
# Bild fehlt -- aber dann war tools/formeln.py nicht gelaufen.
cp bilder/*.png "$STAGE/opt/c-lehrer/bilder/"
cp c-lehrer.desktop "$STAGE/usr/share/applications/"
cp icons/icon-80.png "$STAGE/usr/share/icons/hicolor/80x80/apps/c-lehrer.png"
chmod 755 "$STAGE/opt/c-lehrer/bin/c-lehrer" "$STAGE/opt/c-lehrer/bin/crun" \
          "$STAGE/opt/c-lehrer/bin/rrun"

python3 - "$VERSION" <<'PY'
import base64, io, sys, textwrap
version = sys.argv[1]
icon = base64.b64encode(open("icons/icon-64.png", "rb").read()).decode("ascii")
text = io.open("control.in", encoding="utf-8").read()
text = text.replace("@VERSION@", version)
text = text.replace("@ICON@",
                    "\n".join(" " + line for line in textwrap.wrap(icon, 76)))
io.open("build/stage/DEBIAN/control", "w", encoding="utf-8").write(text)
PY

OUT="c-lehrer_${VERSION}_armel.deb"
python3 tools/mkdeb.py "$STAGE" "$OUT"
