#!/bin/sh
# Baut den mitgelieferten C++-Compiler-Baum aus den offiziellen SDK-Paketen.
#
#   tools/make-toolchain.sh [zielverzeichnis]      # Vorgabe: toolchain/tree
#
# Warum ausgepackt statt installiert: das SDK-Paket libc6-dev verlangt exakt
# libc6 2.10-0maemo18.1, auf dem Geraet liegt aber 2.10-0maemo20 aus PR1.3.
# Mit --force liesse sich das erzwingen -- man handelt sich damit aber ein
# Geraet ein, das nicht mehr bootet. Gebraucht werden aus dem Paket ohnehin
# nur Kopfdateien und Startobjekte; die eigentlichen Bibliotheken kommen vom
# Geraet, und dessen libstdc++6 ist mit 4.4.1-0maemo14+0m6 genau dieselbe
# Fassung wie das hier verwendete libstdc++6-4.4-dev. Kein ABI-Bruch moeglich.
#
# Nokias eigener Spiegel ist tot ("Coming Soon"); wunderwungiel.pl hat eine
# Kopie, ist aber langsam -- daher Wiederaufnahme und mehrere Anlaeufe.
set -e
cd "$(dirname "$0")/.."

ZIEL=${1:-toolchain/tree}
ROH=${ROH:-/tmp/cxx-debs}
AUS=/tmp/cxx-auspack
SPIEGEL=http://wunderwungiel.pl/MeeGo/harmattan-dev.nokia.com
# Endgueltiger Pfad auf dem Geraet -- steht im Linkerskript weiter unten.
INSTALL=${INSTALL:-/opt/c-lehrer/toolchain}

PAKETE="
pool/harmattan/free/k/kernel/linux-kernel-headers_2.6.32-20112910+0m6_armel.deb
pool/harmattan/free/e/eglibc/libc6-dev_2.10-0maemo18.1+0m6_armel.deb
pool/harmattan/free/b/binutils/binutils_2.19.51.20090709-0maemo10+0m6_armel.deb
pool/harmattan/free/g/gcc-4.4/cpp-4.4_4.4.1-0maemo14+0m6_armel.deb
pool/harmattan/free/g/gcc-4.4/gcc-4.4_4.4.1-0maemo14+0m6_armel.deb
pool/harmattan/free/g/gcc-4.4/libstdc++6-4.4-dev_4.4.1-0maemo14+0m6_armel.deb
pool/harmattan/free/g/gcc-4.4/g++-4.4_4.4.1-0maemo14+0m6_armel.deb
pool/harmattan/free/g/gmp/libgmp3c2_4.3.2+dfsg-1+maemo5+0m6_armel.deb
pool/harmattan/free/m/mpfr/libmpfr1ldbl_2.4.1-0maemo4+0m6_armel.deb
"

mkdir -p "$ROH"
for f in $PAKETE; do
    n=$(basename "$f")
    [ -s "$ROH/$n" ] && continue
    echo "hole $n"
    for versuch in 1 2 3 4 5 6 7 8; do
        curl -sSL -C - --max-time 900 -o "$ROH/$n" "$SPIEGEL/$f" && break
    done
done

rm -rf "$AUS"; mkdir -p "$AUS"
for d in "$ROH"/*.deb; do
    dpkg-deb -x "$d" "$AUS" 2>/dev/null || ar p "$d" data.tar.gz | tar xzf - -C "$AUS"
done

# --- trimmen -------------------------------------------------------------
# Raus fliegen: cc1 (C uebernimmt picoc), /usr/share (Doku, Uebersetzungen)
# und alle binutils-Werkzeuge ausser as und ld. 53 MB werden so zu 30 MB.
G=usr/lib/gcc/arm-linux-gnueabi/4.4
rm -rf "$ZIEL"; mkdir -p "$ZIEL/usr/bin" "$ZIEL/usr/lib" "$ZIEL/$G"

cp "$AUS/usr/bin/g++-4.4" "$AUS/usr/bin/as" "$AUS/usr/bin/ld" "$ZIEL/usr/bin/"
cp "$AUS/$G/cc1plus" "$AUS/$G/collect2" "$ZIEL/$G/"
cp "$AUS/$G"/*.o "$AUS/$G"/*.a "$ZIEL/$G/"
cp -a "$AUS/$G/libstdc++.so" "$ZIEL/$G/"
cp -a "$AUS/$G/include" "$AUS/$G/include-fixed" "$ZIEL/$G/"
cp "$AUS/usr/lib"/*.o "$AUS/usr/lib/libc_nonshared.a" "$ZIEL/usr/lib/"
cp -a "$AUS/usr/include" "$ZIEL/usr/"

# cc1plus haengt an gmp und mpfr -- die liegen nicht auf dem Geraet, also mit.
# (readelf -d cc1plus zeigt es; beim ersten Anlauf hatte ich die Ausgabe
# abgeschnitten und beide fuer entbehrlich gehalten.)
cp -a "$AUS/usr/lib"/libgmp.so.3* "$AUS/usr/lib"/libmpfr.so.1* "$ZIEL/usr/lib/"
# as und ld brauchen ihre eigenen Bibliotheken.
cp -a "$AUS/usr/lib"/libbfd*.so "$AUS/usr/lib"/libopcodes*.so "$ZIEL/usr/lib/"

# --- die vier Fallen -----------------------------------------------------
# 1) libm.so & Co. sind im Paket ABSOLUTE Symlinks nach /lib. Ein cp ohne -a
#    loest sie auf und legt die Bibliothek des BUILD-Rechners in den ARM-Baum
#    ("file format not recognized"). Also selbst setzen, auf die Gerätepfade.
for paar in libm.so:/lib/libm.so.6 libdl.so:/lib/libdl.so.2 \
            librt.so:/lib/librt.so.1 libutil.so:/lib/libutil.so.1 \
            libcrypt.so:/lib/libcrypt.so.1 libpthread.so:/lib/libpthread.so.0; do
    name=${paar%%:*}; pfad=${paar##*:}
    [ -f "$AUS/usr/lib/$name" ] && ! [ -L "$AUS/usr/lib/$name" ] \
        && cp "$AUS/usr/lib/$name" "$ZIEL/usr/lib/$name" && continue
    ln -sf "$pfad" "$ZIEL/usr/lib/$name"
done

# 2) -lgcc_s findet nichts: die gemeinsame libgcc steckt im Laufzeitpaket
#    libgcc1, nicht im Compilerpaket. Auf dem Geraet liegt sie in /lib.
ln -sf /lib/libgcc_s.so.1 "$ZIEL/$G/libgcc_s.so"

# 3) Das Linkerskript libc.so zeigt auf /usr/lib/libc_nonshared.a -- die gibt
#    es auf dem Geraet nicht, sie liegt in diesem Baum. Pfad umschreiben.
cat > "$ZIEL/usr/lib/libc.so" <<EOF
/* GNU ld script
   Die gemeinsame Bibliothek kommt vom Geraet, einige Funktionen stecken nur
   in der statischen -- die liegt im mitgelieferten Baum. */
OUTPUT_FORMAT(elf32-littlearm)
GROUP ( /lib/libc.so.6 $INSTALL/usr/lib/libc_nonshared.a AS_NEEDED ( /lib/ld-linux.so.3 ) )
EOF

# 4) Startdateien (crt1.o) sucht gcc ueber den -B-Pfad, nicht ueber -L.
#    Das steht in toolchain/crunxx, hier nur als Merkposten.

echo "== $ZIEL fertig: $(du -sh "$ZIEL" | cut -f1)"
