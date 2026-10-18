"""One large O shared by both lines:  M ◯ RE / P ◯ WER."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make8 as k
D = sys.argv[1]; NAVY, LIGHT, BLUE, DEEP = k.NAVY, k.LIGHT, k.BLUE, "#0096DB"
face = k.Face("InterDisplay-SemiBold.otf"); P = k.pathops; op, U, Dif, I = k.op, k.U, k.D, P.PathOp.INTERSECTION
size = 120; s = size / face.upm; cap = 1490 * s; stem = face.stem * s; track = 0.035 * size

def run(text, x, base):
    glyphs, w = face.layout(text, size, 0.035)
    p = P.Path()
    for name, gx in glyphs: p = op(p, face.glyph_path(name, s, x + gx, base), U)
    return p, w

def build(scheme="navy", dark=False, stroke_k=1.5, line_k=1.34, gap_k=0.5, rise_k=0.3, bar_end=0.54, bar_k=0.92):
    ink = LIGHT if dark else NAVY; pw = BLUE if dark else DEEP
    b1 = 0; b2 = b1 + cap * line_k
    top, bot = b1 - cap - 24 * s, b2 + 24 * s                 # O spans cap line of MORE to baseline of POWER
    ry = (bot - top) / 2; rx = ry * 0.97; st = stroke_k * stem
    gap = gap_k * st; bar_w = bar_k * st; rise = rise_k * st
    # left column: M over P, both set flush right against the O
    mP, mw = run("M", 0, b1); pP, pw_ = run("P", 0, b2)
    colw = max(mw, pw_)
    M = k.shift(mP, colw - mw); Pp = k.shift(pP, colw - pw_)
    fit = 0.55 * st                                           # optical space between letters and the big O
    cx = colw + fit + rx; cy = (top + bot) / 2
    ring = op(k.ellipse(cx, cy, rx, ry), k.ellipse(cx, cy, rx - st, ry - 0.92 * st), Dif)
    h = bar_w / 2 + gap
    ring = op(ring, k.rect(cx - h, top - 10, cx + h, cy), Dif)
    bar = k.capsule(cx, top - rise, top + bar_end * (bot - top), bar_w)
    xr = cx + rx + fit
    RE, rw = run("RE", xr, b1); WER, ww = run("WER", xr, b2)
    parts = [(ink, M), (ink, RE), (pw, Pp), (pw, WER)]
    if scheme == "navy":  parts += [(ink, ring), (pw, bar)]
    elif scheme == "blue": parts += [(pw, ring), (ink, bar)]
    elif scheme == "split":   # upper half belongs to MORE, lower half to POWER
        split = (b1 + (b2 - cap)) / 2
        up = op(ring, k.rect(cx - 2 * rx, top - 50, cx + 2 * rx, split), I)
        lo = op(ring, k.rect(cx - 2 * rx, split, cx + 2 * rx, bot + 50), I)
        parts += [(ink, up), (pw, lo), (pw, bar)]
    width = xr + max(rw, ww); pad = 0.6 * stem
    vb = (-pad, top - rise - pad, width + 2 * pad, bot - top + rise + 2 * pad)
    return parts, vb

if __name__ == "__main__":
  for sch in ("navy", "blue", "split"):
    parts, vb = build(sch); k.svg(f"{D}/bigo-{sch}.svg", parts, vb)
    parts, vb = build(sch, dark=True); k.svg(f"{D}/bigo-{sch}-reversed.svg", parts, vb)
print("ok")
