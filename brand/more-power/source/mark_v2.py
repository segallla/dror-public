"""Mark v2: two identical power rings whose overlap is one deliberate shape (a vesica 'core').

Geometry: rings of outer radius R and stroke w, centres d = 2R - w apart. At exactly that distance the two
stroke bands meet in a single lens as wide as the stroke itself, with no slivers or triangles anywhere else.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make8 as k
P = k.pathops; op, U, D, I = k.op, k.U, k.D, P.PathOp.INTERSECTION
NAVY, LIGHT, BLUE, DEEP = k.NAVY, k.LIGHT, k.BLUE, "#0096DB"

def disc(cx, cy, r): return k.ellipse(cx, cy, r, r)
def dilate(p, g):
    st = P.Path(); p.draw(st.getPen()); st.stroke(2 * g, P.LineCap.ROUND_CAP, P.LineJoin.ROUND_JOIN, 4); st.convertConicsToQuads()
    return op(p, st, U)
def erode(p, g):
    st = P.Path(); p.draw(st.getPen()); st.stroke(2 * g, P.LineCap.BUTT_CAP, P.LineJoin.ROUND_JOIN, 4); st.convertConicsToQuads()
    return op(p, st, D)

def build(R=100, w_k=0.28, gap_k=0.30, bar_k=0.92, bar_end=0.46, style="core", core_gap_k=0.28):
    w = w_k * R; r = R - w; d = 2 * R - w; cy = R + 4
    c1, c2 = R + 4, R + 4 + d
    gap = gap_k * w; bw = bar_k * w; h = bw / 2 + gap
    def ring(cx):
        a = op(disc(cx, cy, R), disc(cx, cy, r), D)
        return op(a, k.rect(cx - h, cy - R - 10, cx + h, cy), D)
    def bar(cx): return k.capsule(cx, cy - R, cy - R + bar_end * 2 * R, bw)
    L, Rr = ring(c1), ring(c2)
    lens = op(disc(c1, cy, R), disc(c2, cy, R), I)
    out = {"L": L, "R": Rr, "Lbar": bar(c1), "Rbar": bar(c2), "core": None}
    if style == "core":          # the overlap is its own colour
        out["L"], out["R"], out["core"] = op(L, lens, D), op(Rr, lens, D), lens
    elif style == "node":        # the overlap is empty: a light node between the rings
        out["L"], out["R"] = op(L, lens, D), op(Rr, lens, D)
    elif style == "protected":   # a smaller core, held by both rings with a clear gap around it
        g = core_gap_k * w; core = erode(lens, g * 0.5)
        cut = dilate(core, g)
        out["L"], out["R"], out["core"] = op(L, cut, D), op(Rr, cut, D), core
    elif style == "front":       # previous version for comparison: left ring in front, right ring cut back
        g = 0.42 * w; out["R"] = op(Rr, dilate(L, g), D)
    allp = op(op(out["L"], out["R"], U), op(out["Lbar"], out["Rbar"], U), U)
    out["bbox"] = k.bounds(allp); out["w"] = w
    return out

def parts(m, ink=NAVY, blue=DEEP, core=None):
    core = core or (BLUE if blue == DEEP else LIGHT)
    ps = [(ink, m["L"]), (blue, m["Lbar"]), (blue, m["R"]), (ink, m["Rbar"])]
    if m["core"] is not None: ps.append((core, m["core"]))
    return ps

def save(path, m, **kw):
    x0, y0, x1, y1 = m["bbox"]; p = 0.08 * (x1 - x0)
    k.svg(path, parts(m, **kw), (x0 - p, y0 - p, x1 - x0 + 2 * p, y1 - y0 + 2 * p))
