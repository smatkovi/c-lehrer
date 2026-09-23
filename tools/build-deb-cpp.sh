#!/bin/sh
# Packt den mitgelieferten C++-Compiler als eigenes .deb.
#
# Getrennt vom Hauptpaket, weil der Baum 30 MB wiegt und die App auch ohne
# ihn sinnvoll ist: die C++-Lektionen bleiben lesbar, nur der Knopf zum
# Ausfuehren fehlt.
#
# Der Baum stammt aus den offiziellen SDK-Paketen (gcc-4.4, g++-4.4, cpp-4.4,
# libstdc++6-4.4-dev, libc6-dev, binutils, linux-kernel-headers), mit
# dpkg-deb -x ausgepackt. Bewusst NICHT installiert: libc6-dev verlangt genau
# das aeltere libc6, das Geraet hat aber das neuere aus PR1.3. Erzwingen
# waere der falsche Weg -- gebraucht werden aus dem Paket ohnehin nur die
# Kopfdateien und crt*.o, die eigentlichen Bibliotheken kommen vom Geraet.
#
# Keine versionierten Abhaengigkeiten, aus demselben Grund wie im Hauptpaket.
#
#   tools/build-deb-cpp.sh [version] [pfad/zum/toolchain-baum]
set -e
cd "$(dirname "$0")/.."

VERSION=${1:-0.1}
BAUM=${2:-toolchain/tree}
STAGE=build/stage-cpp
rm -rf "$STAGE"

[ -d "$BAUM/usr/bin" ] || { echo "Toolchain-Baum fehlt: $BAUM" >&2; exit 1; }
[ -x "$BAUM/usr/bin/g++-4.4" ] || { echo "g++-4.4 fehlt in $BAUM" >&2; exit 1; }

mkdir -p "$STAGE/opt/c-lehrer/bin" "$STAGE/opt/c-lehrer/toolchain" "$STAGE/DEBIAN"
cp -a "$BAUM/." "$STAGE/opt/c-lehrer/toolchain/"
# Das Linkerskript muss auf den Installationspfad zeigen, nicht auf den Baum,
# in dem gebaut wurde. make-toolchain.sh schreibt es schon richtig, wenn
# INSTALL gesetzt war -- hier sicherheitshalber noch einmal.
cat > "$STAGE/opt/c-lehrer/toolchain/usr/lib/libc.so" <<EOF
/* GNU ld script
   Die gemeinsame Bibliothek kommt vom Geraet, einige Funktionen stecken nur
   in der statischen -- die liegt im mitgelieferten Baum. */
OUTPUT_FORMAT(elf32-littlearm)
GROUP ( /lib/libc.so.6 /opt/c-lehrer/toolchain/usr/lib/libc_nonshared.a AS_NEEDED ( /lib/ld-linux.so.3 ) )
EOF
cp toolchain/crunxx "$STAGE/opt/c-lehrer/bin/crunxx"
chmod 755 "$STAGE/opt/c-lehrer/bin/crunxx"

python3 - "$VERSION" <<'PY'
import io, sys
text = io.open("control-cpp.in", encoding="utf-8").read()
io.open("build/stage-cpp/DEBIAN/control", "w", encoding="utf-8").write(
    text.replace("@VERSION@", sys.argv[1]))
PY

OUT="c-lehrer-cpp_${VERSION}_armel.deb"
python3 tools/mkdeb.py "$STAGE" "$OUT"
