"""Builds the logo masters: primary wordmark, mark (standard and small cut) and the expressive shared-O lockup."""
import sys, os, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make8 as k, cairosvg
import bigo11  # shared-O lockup
D = sys.argv[1]; NAVY, LIGHT, BLUE, DEEP = k.NAVY, k.LIGHT, k.BLUE, "#0096DB"
face = k.Face("InterDisplay-SemiBold.otf")

OPEN = dict(gap_k=0.30, rise_k=0.0, bar_end=0.46, bar_k=0.88)          # refined top opening (option C)
wm = k.wordmark(face, **OPEN); pad = 0.6 * wm["stem"]; top = k.bounds(wm["bars"][0])[1]
vb = (-pad, top - pad, wm["width"] + 2 * pad, wm["base"] + 24 * wm["s"] - top + 2 * pad)
k.svg(f"{D}/more-power-wordmark.svg", k.wordmark_parts(wm, accent=DEEP, power=DEEP), vb)
k.svg(f"{D}/more-power-wordmark-reversed.svg", k.wordmark_parts(wm, ink=LIGHT, reversed_=True, power=BLUE), vb)
import mark_v2                                                   # two identical rings, one deliberate core
mk = mark_v2.build(style="protected")
mark_v2.save(f"{D}/more-power-mark.svg", mk)
mark_v2.save(f"{D}/more-power-mark-reversed.svg", mk, ink=LIGHT, blue=BLUE, core=LIGHT)
small = mark_v2.build(style="node", w_k=0.36, gap_k=0.36, bar_k=0.95)   # 24–48 px: core dropped, overlap left open
mark_v2.save(f"{D}/more-power-mark-small.svg", small)
mark_v2.save(f"{D}/more-power-mark-small-reversed.svg", small, ink=LIGHT, blue=BLUE)
for dark in (False, True):
    parts, v = bigo11.build("split", dark=dark, **OPEN)
    k.svg(f"{D}/more-power-shared-o{'-reversed' if dark else ''}.svg", parts, v)

print("ok")
