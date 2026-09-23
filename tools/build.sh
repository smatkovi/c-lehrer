#!/bin/sh
# Cross-builds the C-Lehrer binary for MeeGo Harmattan.
#
# Same recipe as harbour-snapszer/meego/build.sh, which is proven on this
# device: the GCC 14 cross toolchain from that project's toolchain.sh
# (/tmp/xgcc-harmattan) compiling against the MADDE Harmattan sysroot's
# Qt 4.7.4, with moc taken from the Qt Simulator's Qt -- the same 4.7.4.
#
# Two link details are not cosmetic:
#   * -Wl,--dynamic-linker=/lib/ld-linux.so.3 -- GCC would otherwise ask for
#     the armhf loader name, which Harmattan does not have.
#   * -static-libstdc++ -static-libgcc with --exclude-libs,ALL -- the binary
#     keeps the modern C++ runtime to itself instead of exporting it to Qt,
#     which is built against GCC 4.4's.
#
#   tools/build.sh        # -> build/c-lehrer
set -e
cd "$(dirname "$0")/.."

REMOTE=/tmp/c-lehrer-src
HOST=$(sh "$HOME/ps/nfsshift-sfos/tools/buildhost.sh")
echo "== build host: $HOST"

rsync -a --delete --exclude build --exclude '*.deb' --exclude stage \
    ./ "$HOST:$REMOTE/"

cat > /tmp/c-lehrer-remote.sh <<'REMOTE_EOF'
set -e
SRC=/tmp/c-lehrer-src
XGCC=${XGCC:-/tmp/xgcc-harmattan}
SYSROOT=${SYSROOT:-$HOME/QtSDK/Madde/sysroots/harmattan_sysroot_10.2011.34-1_slim}
SIMQT=${SIMQT:-$HOME/QtSDK/Simulator/Qt/gcc}
OUT=$SRC/build
mkdir -p "$OUT"

CXX=$XGCC/bin/arm-none-linux-gnueabi-g++
[ -x "$CXX" ] || { echo "Cross-Compiler fehlt: $CXX" >&2; exit 1; }
MOC=$SIMQT/bin/moc
QTINC=$SYSROOT/usr/include/qt4

CXXFLAGS="--sysroot=$SYSROOT -std=gnu++17 -O2 -Wall -Wno-register \
 -Wno-deprecated-declarations -Wno-nonnull -Wno-class-memaccess -DQT_NO_DEBUG -I$QTINC -I$SRC/src"
for m in QtCore QtGui QtScript QtDeclarative; do
    CXXFLAGS="$CXXFLAGS -I$QTINC/$m"
done
LDFLAGS="--sysroot=$SYSROOT -static-libstdc++ -static-libgcc -Wl,-O1 \
 -Wl,--as-needed -Wl,--exclude-libs,ALL -Wl,--dynamic-linker=/lib/ld-linux.so.3"
LIBS="-lQtDeclarative -lQtScript -lQtGui -lQtCore -lpthread"

SOURCES="Json Checker Curriculum Placement Engine Runner Plotter Course main"
MOC_HEADERS="Runner Course"

cd "$OUT"
OBJS=""
for h in $MOC_HEADERS; do
    $MOC "$SRC/src/$h.h" -o "moc_$h.cpp"
    $CXX $CXXFLAGS -c "moc_$h.cpp" -o "moc_$h.o"
    OBJS="$OBJS moc_$h.o"
done
for s in $SOURCES; do
    $CXX $CXXFLAGS -c "$SRC/src/$s.cpp" -o "$s.o"
    OBJS="$OBJS $s.o"
done
$CXX $LDFLAGS -o c-lehrer $OBJS $LIBS
$XGCC/bin/arm-none-linux-gnueabi-strip c-lehrer
ls -la c-lehrer
file c-lehrer

# The device-side test: the run path -- interpreter, output splitting,
# painting -- cannot be reached from a unit test on the build machine.
$CXX $CXXFLAGS -c "$SRC/tests/run_test.cpp" -o run_test.o
$CXX $LDFLAGS -o run_test run_test.o Runner.o Plotter.o Checker.o moc_Runner.o $LIBS
ls -la run_test
REMOTE_EOF

scp -q /tmp/c-lehrer-remote.sh "$HOST":/tmp/
ssh "$HOST" 'sh /tmp/c-lehrer-remote.sh'
mkdir -p build
scp -q "$HOST:$REMOTE/build/c-lehrer" build/c-lehrer
chmod 755 build/c-lehrer
echo "== build/c-lehrer fertig"
