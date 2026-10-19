"""Stacked lockup: MORE above POWER, flush left (for square and vertical formats, and entrance signs)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make8 as k
OUT = sys.argv[1]; NAVY, LIGHT, BLUE, DEEP = k.NAVY, k.LIGHT, k.BLUE, "#0096DB"
OPEN = dict(gap_k=0.30, rise_k=0.0, bar_end=0.46, bar_k=0.88)
face = k.Face("InterDisplay-SemiBold.otf"); size = 120; s = size / face.upm; cap = 1490 * s

def word(text, base, ink, ring, bar, letters):
    wm = k.wordmark(face, size=size, x0=0, base=base, text=text, **OPEN)
    return wm, [(letters, wm["letters"]), (ring, wm["rings"][0]), (bar, wm["bars"][0])]

def stacked(dark=False):
    ink = LIGHT if dark else NAVY; pw = BLUE if dark else DEEP
    b1 = 0; b2 = cap * 1.36                                   # line gap = 0.36 cap height
    wM, p1 = word("MORE", b1, ink, ink, pw, ink)
    wP, p2 = word("POWER", b2, ink, pw, ink, pw)
    if dark:
        t = 0.03 * wM["stem"]; p1 = [(c, k.thin(p, t)) for c, p in p1]; p2 = [(c, k.thin(p, t)) for c, p in p2]
    top = b1 - 1514 * s; bot = b2 + 24 * s; pad = 0.6 * face.stem * s
    return p1 + p2, (-pad, top - pad, wP["width"] + 2 * pad, bot - top + 2 * pad)

for dark in (False, True):
    parts, vb = stacked(dark)
    k.svg(os.path.join(OUT, f"more-power-stacked{'-reversed' if dark else ''}.svg"), parts, vb)
print("ok")
