"""Simplified one-colour artwork for embroidery, engraving, laser and vinyl cutting.

The mark drops its core (the gaps around it are too fine for thread or a cutter) and uses heavier rings,
wider openings and rounder joins. Use these files for physical production, the standard masters elsewhere.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mark_v2 as v, make8 as k
ROOT = sys.argv[1]; OUT = os.path.join(ROOT, "print", "production"); os.makedirs(OUT, exist_ok=True)
m = v.build(style="node", w_k=0.40, gap_k=0.45, bar_k=1.0, overlap_k=0.87)
x0, y0, x1, y1 = m["bbox"]; p = 0.05 * (x1 - x0)
k.svg(os.path.join(OUT, "more-power-mark-production.svg"),
      [("#000000", m["L"]), ("#000000", m["Lbar"]), ("#000000", m["R"]), ("#000000", m["Rbar"])],
      (x0 - p, y0 - p, x1 - x0 + 2 * p, y1 - y0 + 2 * p))
import re
src = open(os.path.join(ROOT, "logo", "more-power-wordmark.svg")).read()
open(os.path.join(OUT, "more-power-wordmark-production.svg"), "w").write(re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="#000000"', src))
sys.argv = [sys.argv[0], ROOT]
import print_files as pf
for n, wmm in (("mark-production", 100), ("wordmark-production", 200)):
    pf.pdf(os.path.join(OUT, f"more-power-{n}.svg"), os.path.join(OUT, f"more-power-{n}.pdf"), wmm, "black", f"MORE POWER {n}")
print("ok")
