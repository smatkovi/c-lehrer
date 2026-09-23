#!/bin/sh
# Baut "rrun", den Rust-Deuter, fuer das N9/N950.
#
# Warum ein eigener Deuter und nicht rustc: siehe den Kopf von
# rust/rrun.cpp. Gebaut wird mit derselben GCC-14-Kreuzkette wie die App
# selbst -- das Programm haelt seine C++-Laufzeit statisch bei sich, damit
# es neben dem alten libstdc++ des Geraets keinen Streit gibt.
#
#   tools/build-rrun.sh          # -> bin/rrun
set -e
cd "$(dirname "$0")/.."

REMOTE=/tmp/c-lehrer-rust
HOST=$(sh "$HOME/ps/nfsshift-sfos/tools/buildhost.sh")
echo "== Build-Rechner: $HOST"

ssh "$HOST" "mkdir -p $REMOTE"
scp -q rust/rrun.cpp "$HOST:$REMOTE/"

cat > /tmp/rrun-remote.sh <<'REMOTE_EOF'
set -e
SRC=/tmp/c-lehrer-rust
XGCC=${XGCC:-/tmp/xgcc-harmattan}
SYSROOT=${SYSROOT:-$HOME/QtSDK/Madde/sysroots/harmattan_sysroot_10.2011.34-1_slim}
CXX=$XGCC/bin/arm-none-linux-gnueabi-g++
[ -x "$CXX" ] || { echo "Cross-Compiler fehlt: $CXX -- erst tools/build.sh" >&2; exit 1; }

cd "$SRC"
# Ganz statisch, wie crun: dann braucht das Geraet weder eine passende
# libstdc++ noch den Lader, und derselbe Binaerbau laeuft unter qemu-arm
# auf dem Baurechner -- das ist die Bedingung dafuer, dass die Kursprobe
# ihn dort pruefen kann.
$CXX --sysroot=$SYSROOT -std=gnu++11 -O2 -Wall -static \
     -o rrun rrun.cpp -lm
$XGCC/bin/arm-none-linux-gnueabi-strip rrun
ls -l rrun

# Gleich hier die Gegenprobe: der Deuter muss unter qemu-arm dasselbe
# sagen wie auf dem Baurechner, sonst stimmt etwas mit der Kreuzkette
# nicht.
cat > /tmp/rrun-probe.rs <<'RS'
fn main() {
    let mut x = 1.0;
    let mut v = 0.0;
    for _i in 0..400 {
        v = v + (-x) * 0.05;
        x = x + v * 0.05;
    }
    println!("{:.4}", 0.5 * v * v + 0.5 * x * x);
}
RS
echo "== Probe unter qemu-arm:"
qemu-arm ./rrun /tmp/rrun-probe.rs
REMOTE_EOF

scp -q /tmp/rrun-remote.sh "$HOST:/tmp/"
ssh "$HOST" 'sh /tmp/rrun-remote.sh'
mkdir -p bin
scp -q "$HOST:$REMOTE/rrun" bin/
ls -l bin/rrun
echo "== bin/rrun fertig"
