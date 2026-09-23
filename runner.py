# -*- coding: utf-8 -*-
"""Runs the learner's C program and brings back what it said.

Three things matter here and none of them are optional:

* A time limit. The first loop anyone writes wrong is an endless one, and
  without a limit the app would simply hang with no way back.
* A separate process. picoc is an interpreter, but a program can still eat
  all memory or recurse until it dies -- in a child that is a message, in
  the app it is a crash.
* An output limit. "for(;;) printf" fills the flash otherwise.
"""
import os
import re
import subprocess
import threading

import config

TIMEOUT = 10.0
MAX_OUTPUT = 64 * 1024

# picoc says "file:line:col message"; the line number is worth showing in
# the editor rather than making people count.
ERROR = re.compile(r"^[^:]*:(\d+):(\d+)\s+(.*)$")

# A program draws by printing. "plot <x> <y>" is one point of one curve,
# "plot <name> <x> <y>" one point of a named curve, so a lesson can put
# Euler and Verlet in the same picture.
PLOT = re.compile(r"^plot\s+(.*)$")


class Result(object):
    def __init__(self):
        self.output = ""        # what the program printed, plot lines removed
        self.raw = ""           # everything, as it came
        self.error = ""         # compiler or runtime complaint
        self.line = 0           # where, if known
        self.series = []        # [(name, [(x, y), ...]), ...]
        self.timeout = False
        self.seconds = 0.0

    def ok(self):
        return not self.error and not self.timeout


def _split(raw):
    """Separates drawing instructions from ordinary output."""
    text, curves, order = [], {}, []
    for line in raw.split("\n"):
        hit = PLOT.match(line.strip())
        if not hit:
            text.append(line)
            continue
        parts = hit.group(1).split()
        if len(parts) == 2:
            name, nums = "", parts
        elif len(parts) >= 3:
            name, nums = parts[0], parts[1:3]
        else:
            text.append(line)
            continue
        try:
            point = (float(nums[0]), float(nums[1]))
        except ValueError:
            text.append(line)
            continue
        if name not in curves:
            curves[name] = []
            order.append(name)
        curves[name].append(point)
    series = []
    for name in order:
        series.append((name, curves[name]))
    return "\n".join(text).strip(), series


def run(code, seconds=TIMEOUT):
    """Writes the code out, runs it, and reads the answer."""
    import time
    result = Result()
    if not os.path.isdir(config.CACHE):
        os.makedirs(config.CACHE, 0755)
    path = os.path.join(config.CACHE, "lauf.c")
    fh = open(path, "w")
    try:
        fh.write(code.encode("utf-8") if isinstance(code, unicode) else code)
    finally:
        fh.close()

    if not os.path.exists(config.CRUN):
        result.error = "Der C-Ausführer fehlt (%s)." % config.CRUN
        return result

    started = time.time()
    try:
        proc = subprocess.Popen([config.CRUN, path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                cwd=config.CACHE)
    except OSError, exc:
        result.error = "Start fehlgeschlagen: %s" % exc
        return result

    # communicate() has no timeout in 2.6, so the clock runs beside it.
    killer = threading.Timer(seconds, _kill, [proc, result])
    killer.start()
    try:
        raw = proc.communicate()[0]
    finally:
        killer.cancel()
    result.seconds = time.time() - started

    if len(raw) > MAX_OUTPUT:
        raw = raw[:MAX_OUTPUT] + "\n... (Ausgabe abgeschnitten)"
    result.raw = raw
    result.output, result.series = _split(raw)

    if result.timeout:
        result.error = ("Das Programm lief länger als %d Sekunden und wurde "
                        "abgebrochen. Meist ist eine Schleife schuld, die "
                        "nicht endet." % int(seconds))
        return result

    # picoc reports its complaint on the last line and exits non-zero.
    if proc.returncode != 0:
        for line in reversed(result.raw.strip().split("\n")):
            if not line.strip():
                continue
            hit = ERROR.match(line.strip())
            if hit:
                result.line = int(hit.group(1))
                result.error = hit.group(3)
            else:
                result.error = line.strip()
            break
        if not result.error:
            result.error = "Das Programm wurde mit Fehler %d beendet." % proc.returncode
    return result


def _kill(proc, result):
    result.timeout = True
    try:
        proc.kill()
    except OSError:
        pass
