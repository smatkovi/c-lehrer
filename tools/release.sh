#!/bin/sh
# Haengt die Pakete einer Fassung an ein Release dieses Repos.
#
#   tools/release.sh <version> <paket> [<paket> ...]
#
# gh ist auf dem Arch-Rechner angemeldet, nicht auf dem Telefon, also gehen
# die Dateien zuerst dorthin. Ein zweiter Aufruf mit weiteren Dateien haengt
# sie an das schon vorhandene Release an.
set -e
VERSION=$1
shift 2>/dev/null || true
if [ -z "$VERSION" ] || [ $# -eq 0 ]; then
    echo "Aufruf: tools/release.sh <version> <paket> [<paket> ...]" >&2
    exit 2
fi
for DATEI in "$@"; do
    [ -f "$DATEI" ] || { echo "keine solche Datei: $DATEI" >&2; exit 2; }
done

if [ -n "$BUILD_HOST" ]; then
    HOST=$BUILD_HOST
elif ssh -o BatchMode=yes -o ConnectTimeout=4 sebastian@192.168.1.21 true 2>/dev/null; then
    HOST=sebastian@192.168.1.21
else
    HOST=arch
fi
REPO=${REPO:-smatkovi/c-lehrer}
TAG=v$VERSION
WORK=/tmp/c-lehrer-release

ssh "$HOST" "rm -rf $WORK && mkdir -p $WORK"
for DATEI in "$@"; do
    scp -q "$DATEI" "$HOST:$WORK/"
done
if [ -f "$(dirname "$0")/../NOTIZ.md" ]; then
    scp -q "$(dirname "$0")/../NOTIZ.md" "$HOST:$WORK/notiz.md"
else
    ssh "$HOST" "printf 'C-Lehrer %s\n' $VERSION > $WORK/notiz.md"
fi

NAMEN=""
for DATEI in "$@"; do
    NAMEN="$NAMEN $WORK/$(basename "$DATEI")"
done

ssh "$HOST" "cd $WORK && \
    if gh release view $TAG --repo $REPO >/dev/null 2>&1; then \
        gh release upload $TAG $NAMEN --repo $REPO --clobber; \
    else \
        gh release create $TAG $NAMEN --repo $REPO --title 'C-Lehrer $VERSION' \
            --notes-file notiz.md; \
    fi"
echo "== Release $TAG: https://github.com/$REPO/releases/tag/$TAG"
