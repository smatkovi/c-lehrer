#!/usr/bin/env python3
"""Runs every piece of C in the course and checks it says what it claims.

This is the test suite. A lesson whose example does not run, or a model
solution whose output no longer matches, is worse than a missing lesson --
so nothing ships without going through here first.

The learner's crun is an ARM binary, so the running happens on the build
host under qemu-arm.

    tools/test-curriculum.py            # all of it
    tools/test-curriculum.py c-bewegung # one chapter
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import curriculum
import check

REMOTE = "/tmp/c-lehrer-test"


def build_host():
    out = subprocess.check_output(
        ["sh", os.path.expanduser("~/ps/nfsshift-sfos/tools/buildhost.sh")])
    return out.decode().strip()


def collect(only=None):
    """Everything that has to run, as (name, code, expected, language).

    C++ used to be excluded: there is no C++ interpreter, and the lessons
    were read-and-predict with authored outputs. Since c-lehrer-cpp ships
    the g++ 4.4 from the Harmattan SDK, those programs are compiled and run
    on the phone like everything else -- and against that compiler, not a
    modern one, which would wave through things GCC 4.4 refuses.
    """
    jobs = []
    for chapter in curriculum.CHAPTERS:
        if only and chapter["id"] != only:
            continue
        if chapter["lang"] not in ("c", "cpp", "python", "rust"):
            continue
        lang = chapter["lang"]
        for lesson in chapter["lessons"]:
            name = "%s/%s" % (chapter["id"], lesson["id"])
            if lesson["example"]:
                jobs.append((name + " [Beispiel]", lesson["example"],
                             lesson["output"], lang))
            for index, task in enumerate(lesson["exercises"]):
                tag = "%s [%d %s]" % (name, index + 1, task["kind"])
                if task["kind"] == "predict":
                    if task.get("run", True):
                        jobs.append((tag, task["code"], task["answer"], lang))
                elif task["kind"] == "code":
                    jobs.append((tag, task["solution"], task["expect"], lang))
                    # The starter must at least be valid, or the editor opens
                    # on something that cannot even be run once.
                    jobs.append((tag + " Vorlage", task["starter"], None, lang))
                elif task["kind"] == "blank":
                    filled = task["code"]
                    for answer in task["answers"]:
                        filled = filled.replace("___", answer, 1)
                    jobs.append((tag + " ausgefuellt", filled, None, lang))
    return jobs


def strip_plots(text):
    keep = []
    for line in text.split("\n"):
        if line.strip().startswith("plot "):
            continue
        keep.append(line)
    return "\n".join(keep).strip()


def run_batch(jobs, runner, header):
    """Ship a batch of programs somewhere and bring the outputs back."""
    if not jobs:
        return {}
    print("== %d %s" % (len(jobs), header))
    payload = []
    for index, job in enumerate(jobs):
        payload.append("===== %d\n%s" % (index, job[1]))
    open("/tmp/bundle.txt", "w", encoding="utf-8").write("\n".join(payload))
    raw = runner()
    results = {}
    current, buffer_ = None, []
    for line in raw.split("\n"):
        if line.startswith("--RUN prog"):
            current = int(line[len("--RUN prog"):].split(".")[0])
            buffer_ = []
        elif line.startswith("--END"):
            if current is not None:
                results[current] = "\n".join(buffer_)
            current = None
        elif current is not None:
            buffer_.append(line)
    return results


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    jobs = collect(only)
    host = build_host()
    print("== %d Programme, Build-Rechner %s" % (len(jobs), host))

    # C laeuft unter qemu-arm auf dem Build-Rechner; Python muss aufs
    # Geraet, weil nur dort das Python 3.11 mit NumPy steht, gegen das die
    # Loesungen geschrieben sind.
    c_jobs = [(i, j) for i, j in enumerate(jobs) if j[3] == "c"]
    py_jobs = [(i, j) for i, j in enumerate(jobs) if j[3] == "python"]
    # C++ muss ebenfalls aufs Geraet: der Compiler ist der mitgelieferte
    # g++ 4.4 aus c-lehrer-cpp, und genau gegen den sind die Lektionen
    # geschrieben. Ein moderner Cross-g++ wuerde Dinge durchgehen lassen,
    # die auf dem Geraet nicht uebersetzen.
    cxx_jobs = [(i, j) for i, j in enumerate(jobs) if j[3] == "cpp"]
    # Rust laeuft wie C auf dem Baurechner unter qemu-arm: rrun ist statisch
    # gebunden, also genuegt dieselbe ARM-Datei, die auch aufs Geraet geht.
    rs_jobs = [(i, j) for i, j in enumerate(jobs) if j[3] == "rust"]

    script_c = """
set -e
mkdir -p %(remote)s && cd %(remote)s
rm -f prog*.c
python3 - <<'SPLIT'
raw = open("bundle.txt", encoding="utf-8").read()
for block in raw.split("===== ")[1:]:
    head, body = block.split("\\n", 1)
    open("prog%%s.c" %% head.strip(), "w", encoding="utf-8").write(body)
SPLIT
for f in prog*.c; do
    echo "--RUN $f"
    timeout 60 qemu-arm %(crun)s "$f" 2>&1 || echo "--RC $?"
    echo "--END"
done
""" % {"remote": REMOTE, "crun": "/tmp/c-lehrer-build/picoc/crun"}

    script_rs = """
set -e
mkdir -p %(remote)s && cd %(remote)s
rm -f prog*.rs
python3 - <<'SPLIT'
raw = open("bundle.txt", encoding="utf-8").read()
for block in raw.split("===== ")[1:]:
    head, body = block.split("\\n", 1)
    open("prog%%s.rs" %% head.strip(), "w", encoding="utf-8").write(body)
SPLIT
for f in prog*.rs; do
    echo "--RUN $f"
    timeout 60 qemu-arm %(rrun)s "$f" 2>&1 || echo "--RC $?"
    echo "--END"
done
""" % {"remote": REMOTE + "-rust", "rrun": "/tmp/c-lehrer-rust/rrun"}

    script_py = """
set -e
mkdir -p /home/user/kurstest && cd /home/user/kurstest
rm -f prog*.py
/opt/wunderw/bin/python3.11 - <<'SPLIT'
raw = open("bundle.txt", encoding="utf-8").read()
for block in raw.split("===== ")[1:]:
    head, body = block.split("\\n", 1)
    open("prog%s.py" % head.strip(), "w", encoding="utf-8").write(body)
SPLIT
for f in prog*.py; do
    echo "--RUN $f"
    /opt/wunderw/bin/python3.11 "$f" 2>&1 || echo "--RC $?"
    echo "--END"
done
"""

    script_cxx = """
set -e
mkdir -p /home/user/kurstest && cd /home/user/kurstest
rm -f prog*.cpp
/opt/wunderw/bin/python3.11 - <<'SPLIT'
raw = open("bundle.txt", encoding="utf-8").read()
for block in raw.split("===== ")[1:]:
    head, body = block.split("\\n", 1)
    open("prog%s.cpp" % head.strip(), "w", encoding="utf-8").write(body)
SPLIT
for f in prog*.cpp; do
    echo "--RUN $f"
    /opt/c-lehrer/bin/crunxx "$f" 2>&1 || echo "--RC $?"
    echo "--END"
done
"""

    results = {}

    def auf_host(skript, name, verzeichnis):
        open("/tmp/" + name, "w").write(skript)
        subprocess.check_call(["ssh", host, "mkdir -p " + verzeichnis])
        subprocess.check_call(["scp", "-q", "/tmp/bundle.txt",
                               host + ":" + verzeichnis + "/"])
        subprocess.check_call(["scp", "-q", "/tmp/" + name, host + ":/tmp/"])
        return subprocess.check_output(["ssh", host, "sh /tmp/" + name],
                                       stderr=subprocess.STDOUT).decode("utf-8", "replace")

    def run_on_host():
        return auf_host(script_c, "runall.sh", REMOTE)

    def run_rust_on_host():
        # Der Deuter muss dort liegen, wo das Skript ihn sucht -- gebaut
        # wird er mit tools/build-rrun.sh, und genau von dort kommt er.
        subprocess.check_call(["ssh", host, "mkdir -p /tmp/c-lehrer-rust"])
        subprocess.check_call(["scp", "-q", os.path.join(ROOT, "bin", "rrun"),
                               host + ":/tmp/c-lehrer-rust/rrun"])
        subprocess.check_call(["ssh", host, "chmod 755 /tmp/c-lehrer-rust/rrun"])
        return auf_host(script_rs, "runall-rs.sh", REMOTE + "-rust")

    def geraet(skript, name):
        """Schickt ein Bundel aufs Geraet und laesst es dort laufen."""
        key = ["-oHostKeyAlgorithms=+ssh-rsa", "-oPubkeyAcceptedAlgorithms=+ssh-rsa",
               "-i", os.path.expanduser("~/.ssh/id_rsa_n9")]
        target = "user@" + os.environ.get("N9_HOST", "192.168.1.8")
        open("/tmp/" + name, "w").write(skript)
        subprocess.check_call(["ssh"] + key + [target, "mkdir -p /home/user/kurstest"])
        subprocess.check_call(["scp", "-q"] + key + ["/tmp/bundle.txt",
                                                     target + ":/home/user/kurstest/"])
        subprocess.check_call(["scp", "-q"] + key + ["/tmp/" + name,
                                                     target + ":/home/user/"])
        return subprocess.check_output(["ssh"] + key + [target, "sh /home/user/" + name],
                                       stderr=subprocess.STDOUT).decode("utf-8", "replace")

    def run_on_device():
        return geraet(script_py, "runall-py.sh")

    def run_cxx_on_device():
        return geraet(script_cxx, "runall-cxx.sh")

    for batch, runner, header in ((c_jobs, run_on_host, "C-Programme unter qemu-arm"),
                                  (rs_jobs, run_rust_on_host,
                                   "Rust-Programme unter qemu-arm (rrun)"),
                                  (cxx_jobs, run_cxx_on_device,
                                   "C++-Programme auf dem Geraet (g++ 4.4)"),
                                  (py_jobs, run_on_device, "Python-Programme auf dem Geraet")):
        if not batch:
            continue
        local = run_batch([j for _, j in batch], runner, header)
        for position, (index, _) in enumerate(batch):
            results[index] = local.get(position, "")

    bad = 0
    for index, (name, code, expected, lang) in enumerate(jobs):
        got = results.get(index, "")
        failed = "--RC" in got
        got_clean = strip_plots(got.replace("--RC 1", "").strip())
        if failed:
            print("FEHLER  %s\n        %s" % (name, got_clean.split("\n")[-1][:90]))
            bad += 1
            continue
        if expected is None:
            continue
        want = strip_plots(expected)
        if "plot ..." in expected:
            want = "\n".join(l for l in expected.split("\n")
                             if not l.startswith("plot ...")).strip()
        if not check.output_matches(got_clean, want):
            print("ABWEICHUNG %s\n   erwartet: %r\n   bekommen: %r"
                  % (name, want[:120], got_clean[:120]))
            bad += 1

    print("== %d von %d in Ordnung" % (len(jobs) - bad, len(jobs)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
