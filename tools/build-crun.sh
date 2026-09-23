#!/bin/sh
# Cross-builds "crun", the C interpreter the app runs the learner's code with.
#
# It is picoc (New BSD), built with MADDE's gcc 4.4.1 against the Harmattan
# sysroot and linked -static, so the phone needs nothing installed. An
# interpreter rather than a compiler on purpose: nothing has to write an
# executable and ask Aegis to run it, and a runaway loop in someone's first
# program kills a child process, not the app.
#
# Two changes to the source, both in the patch beside this script:
#   * USE_READLINE is tied to NO_FP upstream -- we need floating point and
#     have no readline in the sysroot, so the define goes.
#   * -O2 instead of the stock -g: picoc walks its syntax tree for every
#     statement, and on a 1 GHz Cortex-A8 that is the difference between a
#     lesson that answers and one the learner waits out.
#
#   tools/build-crun.sh          # -> bin/crun
set -e
cd "$(dirname "$0")/.."

REMOTE=/tmp/c-lehrer-build
HOST=$(sh "$HOME/ps/nfsshift-sfos/tools/buildhost.sh")
echo "== build host: $HOST"

cat > /tmp/crun-build-remote.sh <<'REMOTE_EOF'
set -e
TC=$HOME/QtSDK/Madde/toolchains/arm-2009q3-67-arm-none-linux-gnueabi-x86_64-unknown-linux-gnu/arm-2009q3-67
SR=$HOME/QtSDK/Madde/sysroots/harmattan_sysroot_10.2011.34-1_slim
CC=$TC/bin/arm-none-linux-gnueabi-gcc
REMOTE=/tmp/c-lehrer-build

mkdir -p $REMOTE && cd $REMOTE
if [ ! -d picoc ]; then
    git clone --depth 1 https://gitlab.com/zsaleeba/picoc.git picoc 2>/dev/null ||
    git clone --depth 1 https://github.com/zsaleeba/picoc.git picoc
fi
cd picoc

# readline is switched on by the floating-point branch of platform.h; we want
# the one without the other.
if grep -q '^#  define USE_READLINE' platform.h; then
    sed -i 's|^#  define USE_READLINE$|/* USE_READLINE removed: upstream ties it to NO_FP, and the sysroot has\n    no readline. The interpreter is only ever run on a file here. */|' platform.h
fi

make CC="$CC --sysroot=$SR -static" \
     CFLAGS='-Wall -O2 -fomit-frame-pointer -DUNIX_HOST -DVER=\"2.1\"' \
     LIBS="-lm" clean all

$TC/bin/arm-none-linux-gnueabi-strip -o crun picoc
ls -la crun
REMOTE_EOF

scp -q /tmp/crun-build-remote.sh "$HOST":/tmp/
ssh "$HOST" 'sh /tmp/crun-build-remote.sh'
mkdir -p bin
scp -q "$HOST":$REMOTE/picoc/crun bin/crun
chmod 755 bin/crun
echo "== bin/crun fertig"
ls -la bin/crun
