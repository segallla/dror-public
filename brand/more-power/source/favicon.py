"""Single-O favicon source for 16–24 px: the O of MORE, heavier, filling the square."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make8 as k
OUT = sys.argv[1]
R, cx, cy = 112, 128, 134
st = 0.36 * R; gap = 0.26 * st; bw = 0.9 * st; h = bw / 2 + gap
ring = k.op(k.ellipse(cx, cy, R, R), k.ellipse(cx, cy, R - st, R - 0.94 * st), k.D)
ring = k.op(ring, k.rect(cx - h, cy - R - 10, cx + h, cy), k.D)
bar = k.capsule(cx, cy - R, cy, bw)
k.svg(os.path.join(OUT, "more-power-favicon-source.svg"), [(k.NAVY, ring), ("#0096DB", bar)], (0, 0, 256, 256))
