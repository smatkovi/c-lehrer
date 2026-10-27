#!/usr/bin/env python3
"""Ein winziges Modell nach segelflug/tools/MODELL.md, samt naiver Referenz.

Reines Python ohne numpy -- auf dem Jolla gibt es keins, und der Pruefstand
soll ohne das echte Modell auskommen, das parallel auf arch entsteht.

Der Graph deckt jede Schichtart und jeden Parameterfall ab, den
Klassifizierer.cpp unterscheidet: Schritt 1 und 2, Rand 0 und 1, Gruppen 1,
2 und = ein, relu6 an und aus, ein add mit Restpfad, dessen erste Quelle
mehrere Schichten zurueckliegt (prueft die Letztverwendung), mittel und
linear.  Gewichte und Eingabe kommen aus einem eigenen LCG mit fester Saat;
die Referenz-Logits rechnen in double mit denselben float32-Gewichten.

Aufruf: winzig-modell.py <ausgabeordner> [foto.jpg]
Schreibt modell.bin, eingabe.rgb, erwartet.json sowie drei absichtlich
kaputte Dateien (kennung-falsch.bin, kopf-abgeschnitten.bin,
offset-ausserhalb.bin).  Mit foto.jpg zusaetzlich gedreht-<n>.jpg: dasselbe
Bild mit einem eingeschobenen EXIF-Block, Orientation n (6 in II-, 8 in
MM-Reihenfolge, 3 in II), fuer die Drehprobe von bildLaden().
"""
import json
import os
import struct
import sys

EINGABE = 12
KLASSEN = ["alpha", "beta", "gamma", "delta", "epsilon"]
MITTEL = [0.485, 0.456, 0.406]
STREUUNG = [0.229, 0.224, 0.225]


class LCG:
    def __init__(self, saat):
        self.z = saat & 0xFFFFFFFF

    def naechste(self):
        self.z = (self.z * 1103515245 + 12345) & 0xFFFFFFFF
        return self.z >> 16

    def int8(self):
        # -127..127, symmetrisch wie die Quantisierung
        return self.naechste() % 255 - 127

    def einheit(self):
        return self.naechste() / 65536.0


def f32(x):
    """Auf float32 runden -- so liegen die Werte in der Datei."""
    return struct.unpack("<f", struct.pack("<f", x))[0]


# ---- Graph ---------------------------------------------------------------
# (art, parameter); conv: ein, aus, kern, schritt, rand, gruppen, relu6
SCHICHTEN = [
    dict(art="conv", quelle=0, ein=3, aus=4, kern=3, schritt=2, rand=1, gruppen=1, relu6=True),   # -> T1 4x6x6
    dict(art="conv", quelle=1, ein=4, aus=4, kern=3, schritt=1, rand=1, gruppen=4, relu6=True),   # -> T2 tiefenweise
    dict(art="conv", quelle=2, ein=4, aus=6, kern=1, schritt=1, rand=0, gruppen=1, relu6=False),  # -> T3 1x1 ohne relu
    dict(art="conv", quelle=3, ein=6, aus=4, kern=1, schritt=1, rand=0, gruppen=1, relu6=True),   # -> T4 1x1 mit relu
    dict(art="conv", quelle=4, ein=4, aus=4, kern=3, schritt=1, rand=1, gruppen=4, relu6=True),   # -> T5 tiefenweise
    dict(art="conv", quelle=5, ein=4, aus=6, kern=1, schritt=1, rand=0, gruppen=1, relu6=False),  # -> T6 Projektion
    dict(art="add", quellen=[3, 6]),                                                               # -> T7 (T3 lag 4 Schichten zurueck)
    dict(art="conv", quelle=7, ein=6, aus=4, kern=3, schritt=1, rand=0, gruppen=2, relu6=True),   # -> T8 4x4x4, Rand 0, Gruppen 2
    dict(art="conv", quelle=8, ein=4, aus=4, kern=3, schritt=2, rand=1, gruppen=4, relu6=False),  # -> T9 4x2x2, tiefenweise Schritt 2
    dict(art="conv", quelle=9, ein=4, aus=8, kern=1, schritt=1, rand=0, gruppen=2, relu6=True),   # -> T10 8x2x2, 1x1 mit Gruppen
    dict(art="mittel", quelle=10),                                                                 # -> T11 [8]
    dict(art="linear", quelle=11, ein=8, aus=len(KLASSEN)),                                        # -> T12 [5]
]


def ausgabeform(form, s):
    c, h, w = form
    ah = (h + 2 * s["rand"] - s["kern"]) // s["schritt"] + 1
    aw = (w + 2 * s["rand"] - s["kern"]) // s["schritt"] + 1
    return (s["aus"], ah, aw)


def gewichte_erzeugen(lcg):
    """Fuellt jede conv/linear-Schicht mit q (int8), skalen, bias."""
    for s in SCHICHTEN:
        if s["art"] not in ("conv", "linear"):
            continue
        if s["art"] == "conv":
            je_aus = (s["ein"] // s["gruppen"]) * s["kern"] * s["kern"]
        else:
            je_aus = s["ein"]
        s["q"] = [lcg.int8() for _ in range(s["aus"] * je_aus)]
        # Skala so, dass die Aktivierungen in der Groessenordnung 1 bleiben:
        # |w| <= 127*skala, Summe ueber je_aus Abgriffe.
        s["skalen"] = [f32((0.5 + lcg.einheit()) / (127.0 * (je_aus ** 0.5))) for _ in range(s["aus"])]
        s["bias"] = [f32(lcg.einheit() - 0.5) for _ in range(s["aus"])]
        s["w"] = [f32(q * s["skalen"][o // je_aus]) for o, q in enumerate(s["q"])]
        s["je_aus"] = je_aus


# ---- naive Referenz -------------------------------------------------------
def conv(s, ein, form):
    c, h, w = form
    aus_c, ah, aw = ausgabeform(form, s)
    g = s["gruppen"]
    ein_je = c // g
    aus_je = aus_c // g
    k = s["kern"]
    z = [0.0] * (aus_c * ah * aw)
    for o in range(aus_c):
        gr = o // aus_je
        for oy in range(ah):
            for ox in range(aw):
                summe = s["bias"][o]
                for ci in range(ein_je):
                    cc = gr * ein_je + ci
                    for ky in range(k):
                        iy = oy * s["schritt"] - s["rand"] + ky
                        if iy < 0 or iy >= h:
                            continue
                        for kx in range(k):
                            ix = ox * s["schritt"] - s["rand"] + kx
                            if ix < 0 or ix >= w:
                                continue
                            summe += s["w"][((o * ein_je + ci) * k + ky) * k + kx] * ein[(cc * h + iy) * w + ix]
                if s["relu6"]:
                    summe = min(max(summe, 0.0), 6.0)
                z[(o * ah + oy) * aw + ox] = summe
    return z, (aus_c, ah, aw)


def referenz(rgb):
    e = EINGABE
    t0 = [0.0] * (3 * e * e)
    for c in range(3):
        for p in range(e * e):
            t0[c * e * e + p] = (rgb[p * 3 + c] / 255.0 - MITTEL[c]) / STREUUNG[c]
    tensoren = [(t0, (3, e, e))]
    for s in SCHICHTEN:
        if s["art"] == "conv":
            q, form = tensoren[s["quelle"]]
            tensoren.append(conv(s, q, form))
        elif s["art"] == "add":
            a, fa = tensoren[s["quellen"][0]]
            b, fb = tensoren[s["quellen"][1]]
            assert fa == fb
            tensoren.append(([x + y for x, y in zip(a, b)], fa))
        elif s["art"] == "mittel":
            q, (c, h, w) = tensoren[s["quelle"]]
            tensoren.append(([sum(q[k * h * w:(k + 1) * h * w]) / (h * w) for k in range(c)], (c, 0, 0)))
        elif s["art"] == "linear":
            q, (c, _, _) = tensoren[s["quelle"]]
            z = [s["bias"][o] + sum(s["w"][o * c + i] * q[i] for i in range(c)) for o in range(s["aus"])]
            tensoren.append((z, (s["aus"], 0, 0)))
    return tensoren[-1][0]


# ---- Datei ----------------------------------------------------------------
def modell_schreiben(pfad, kopf_aendern=None):
    blob = bytearray()
    kopf_schichten = []
    for s in SCHICHTEN:
        eintrag = {k: v for k, v in s.items() if k in ("art", "quelle", "quellen", "ein", "aus", "kern", "schritt", "rand", "gruppen", "relu6")}
        if s["art"] in ("conv", "linear"):
            while len(blob) % 4:
                blob.append(0)
            eintrag["gewichte"] = len(blob)
            blob += struct.pack("<%db" % len(s["q"]), *s["q"])
            while len(blob) % 4:
                blob.append(0)
            eintrag["skalen"] = len(blob)
            blob += struct.pack("<%df" % len(s["skalen"]), *s["skalen"])
            eintrag["bias"] = len(blob)
            blob += struct.pack("<%df" % len(s["bias"]), *s["bias"])
        kopf_schichten.append(eintrag)
    kopf = dict(format=1, eingabe=EINGABE, mittel=MITTEL, streuung=STREUUNG,
                klassen=KLASSEN, bytes=len(blob), schichten=kopf_schichten)
    if kopf_aendern:
        kopf_aendern(kopf)
    text = json.dumps(kopf).encode("utf-8")
    while (12 + len(text)) % 4:
        text += b" "
    with open(pfad, "wb") as f:
        f.write(b"WOLKEN01")
        f.write(struct.pack("<I", len(text)))
        f.write(text)
        f.write(bytes(blob))


def exif_block(orientierung, gross):
    """Ein minimaler APP1-Block mit nur dem Orientation-Tag."""
    bo = ">" if gross else "<"
    tiff = (b"MM" if gross else b"II") + struct.pack(bo + "HI", 0x2A, 8)
    ifd = struct.pack(bo + "H", 1)
    ifd += struct.pack(bo + "HHI", 0x0112, 3, 1) + struct.pack(bo + "H", orientierung) + b"\0\0"
    ifd += struct.pack(bo + "I", 0)
    nutzlast = b"Exif\0\0" + tiff + ifd
    return b"\xff\xe1" + struct.pack(">H", len(nutzlast) + 2) + nutzlast


def jpeg_mit_exif(quelle, ziel, orientierung, gross):
    with open(quelle, "rb") as f:
        daten = f.read()
    assert daten[:2] == b"\xff\xd8"
    # Vorhandene APP1-Bloecke fliegen raus, sonst gewinnt der erste.
    rest = daten[2:]
    teile = []
    while rest[:2] not in (b"\xff\xda", b"") and rest[0:1] == b"\xff":
        marker = rest[1]
        if marker == 0xD8 or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            teile.append(rest[:2])
            rest = rest[2:]
            continue
        laenge = struct.unpack(">H", rest[2:4])[0]
        if marker != 0xE1:
            teile.append(rest[:2 + laenge])
        rest = rest[2 + laenge:]
    with open(ziel, "wb") as f:
        f.write(b"\xff\xd8" + exif_block(orientierung, gross) + b"".join(teile) + rest)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__)
        return 2
    ordner = sys.argv[1]
    os.makedirs(ordner, exist_ok=True)

    lcg = LCG(20261027)
    gewichte_erzeugen(lcg)
    rgb = bytes(lcg.naechste() % 256 for _ in range(EINGABE * EINGABE * 3))

    modell_schreiben(os.path.join(ordner, "modell.bin"))
    with open(os.path.join(ordner, "eingabe.rgb"), "wb") as f:
        f.write(rgb)
    logits = referenz(rgb)
    with open(os.path.join(ordner, "erwartet.json"), "w") as f:
        json.dump({"eingabe.rgb": {"klassen": KLASSEN, "logits": logits}}, f, indent=1)

    # Drei kaputte Fassungen fuer die Fehlerpfade.
    pfad = os.path.join(ordner, "modell.bin")
    with open(pfad, "rb") as f:
        gut = f.read()
    with open(os.path.join(ordner, "kennung-falsch.bin"), "wb") as f:
        f.write(b"WOLKEN02" + gut[8:])
    with open(os.path.join(ordner, "kopf-abgeschnitten.bin"), "wb") as f:
        f.write(gut[:40])

    def offset_kaputt(kopf):
        kopf["schichten"][3]["gewichte"] = kopf["bytes"] + 4
    modell_schreiben(os.path.join(ordner, "offset-ausserhalb.bin"), offset_kaputt)

    if len(sys.argv) > 2:
        foto = sys.argv[2]
        jpeg_mit_exif(foto, os.path.join(ordner, "gedreht-6.jpg"), 6, False)
        jpeg_mit_exif(foto, os.path.join(ordner, "gedreht-8.jpg"), 8, True)
        jpeg_mit_exif(foto, os.path.join(ordner, "gedreht-3.jpg"), 3, False)

    print("Logits:", " ".join("%.6f" % x for x in logits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
