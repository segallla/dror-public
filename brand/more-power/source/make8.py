"""MORE POWER — polished build. Rings are cut from the real Inter Display O; booleans via skia-pathops."""
import math, os, sys
import pathops, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

NAVY, BLUE, LIGHT = "#0B1E3A", "#00B0FF", "#F8FAFC"
FONT_DIR = "/usr/share/fonts/opentype/inter/"
f2 = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")

def to_d(p):
    pen = SVGPathPen(None, ntos=f2); p.draw(pen); return pen.getCommands()
def bounds(p):
    b = BoundsPen(None); p.draw(b); return b.bounds
def rect(x0, y0, x1, y1):
    p = pathops.Path(); p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close(); return p
def capsule(cx, y_top, y_bot, w):
    """Vertical bar with round ends (y grows downward)."""
    r = w / 2; k = 0.5523 * r; p = pathops.Path()
    p.moveTo(cx - r, y_top + r)
    p.cubicTo(cx - r, y_top + r - k, cx - k, y_top, cx, y_top); p.cubicTo(cx + k, y_top, cx + r, y_top + r - k, cx + r, y_top + r)
    p.lineTo(cx + r, y_bot - r)
    p.cubicTo(cx + r, y_bot - r + k, cx + k, y_bot, cx, y_bot); p.cubicTo(cx - k, y_bot, cx - r, y_bot - r + k, cx - r, y_bot - r)
    p.close(); return p
def op(a, b, kind): return pathops.op(a, b, kind)
U, D, X = pathops.PathOp.UNION, pathops.PathOp.DIFFERENCE, pathops.PathOp.XOR
def shift(p, dx, dy=0):
    q = pathops.Path(); p.draw(TransformPen(q.getPen(), (1, 0, 0, 1, dx, dy))); return q
def thin(p, t):
    """Erode a shape by t (for reversed artwork): subtract a stroke of width 2t centred on its outline."""
    s = pathops.Path(); p.draw(s.getPen()); s.stroke(2 * t, pathops.LineCap.BUTT_CAP, pathops.LineJoin.MITER_JOIN, 4); s.convertConicsToQuads()
    return op(p, s, D)

class Face:
    def __init__(self, file):
        self.file = FONT_DIR + file; self.tt = TTFont(self.file); self.gs = self.tt.getGlyphSet()
        self.upm = self.tt["head"].unitsPerEm; self.cap = self.tt["OS/2"].sCapHeight
        b = BoundsPen(self.gs); self.gs["I"].draw(b); self.stem = b.bounds[2] - b.bounds[0]
        blob = hb.Blob.from_file_path(self.file); self.hbf = hb.Font(hb.Face(blob))
    def glyph_path(self, name, s, x, base):
        p = pathops.Path(); self.gs[name].draw(TransformPen(p.getPen(), (s, 0, 0, -s, x, base))); return p
    def layout(self, text, size, track_em=0.0, space_em=None):
        """Shape with HarfBuzz (kerning on), add tracking; returns [(glyph name, x)] in px and total width."""
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(self.hbf, buf, {"kern": True})
        s = size / self.upm; x = 0; out = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.hbf.glyph_to_string(info.codepoint)
            out.append((name, x + pos.x_offset * s))
            adv = pos.x_advance * s
            if name == "space" and space_em is not None: adv = space_em * size
            x += adv + track_em * size
        return out, x - track_em * size

def ellipse(cx, cy, rx, ry, reverse=False):
    k = 0.5523; p = pathops.Path()
    pts = [(cx + rx, cy), (cx, cy + ry), (cx - rx, cy), (cx, cy - ry)]
    if reverse: pts = pts[::-1]
    p.moveTo(*pts[0])
    for i in range(4):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % 4]
        if x0 == cx:  c1 = (x0 + (x1 - cx) * k, y0); c2 = (x1, y1 + (y0 - cy) * k)
        else:         c1 = (x0, y0 + (y1 - cy) * k); c2 = (x1 + (x0 - cx) * k, y1)
        p.cubicTo(*c1, *c2, x1, y1)
    p.close(); return p

def ring_geo(face, s, cx, base, ar=0.97, st=None):
    """Geometric O matched to the font: same overshoot as its O, sides = stem, top/bottom 8% thinner."""
    top, bot = base - 1514 * s, base + 24 * s          # Inter Display O overshoot (font units)
    ry = (bot - top) / 2; rx = ry * ar; cy = (top + bot) / 2; st = st or face.stem * s
    return op(ellipse(cx, cy, rx, ry), ellipse(cx, cy, rx - st, ry - 0.92 * st), D), (cx - rx, top, cx + rx, bot)

def power_o(face, s, cx, base, gap, bar_w, rise, st=None, bar_end=0.54):
    """Geometric O opened at the top with a switch bar. Returns (ring, bar, bbox)."""
    O, (x0, y0, x1, y1) = ring_geo(face, s, cx, base, st=st); cy = (y0 + y1) / 2
    h = bar_w / 2 + gap
    ring = op(O, rect(cx - h, y0 - 10, cx + h, cy), D)
    return ring, capsule(cx, y0 - rise, y0 + bar_end * (y1 - y0), bar_w), (x0, y0, x1, y1)

def wordmark(face, size=120, track_em=0.035, space_em=0.24, x0=0, base=None, rise_k=0.3, gap_k=0.5, bar_k=0.92, o_fit=0.7, text="MORE POWER", bar_end=0.54):
    s = size / face.upm; base = base if base is not None else face.cap * s + 0.5 * face.stem * s + 8
    stem = face.stem * s; gap, bar_w, rise = gap_k * stem, bar_k * stem, rise_k * stem
    glyphs, width = face.layout(text, size, track_em, space_em)
    letters = pathops.Path(); letters2 = pathops.Path(); rings, bars = [], []; word = 0
    extra = (1538 * 0.97 - (1460 - 72)) * s * o_fit; extra_total = 0     # geometric O is wider than the font O
    for name, gx in glyphs:
        if name == "space": word = 1; continue
        if name == "O":
            o_c = x0 + gx + extra_total + (72 + 1460) / 2 * s + extra / 2   # font O centre + half the extra width
            r_, b_, _ = power_o(face, s, o_c, base, gap, bar_w, rise, bar_end=bar_end); rings.append(r_); bars.append(b_)
            extra_total += extra
        else:
            g = face.glyph_path(name, s, x0 + gx + extra_total, base)
            if word: letters2 = op(letters2, g, U)
            else: letters = op(letters, g, U)
    return dict(letters=letters, letters2=letters2, rings=rings, bars=bars, width=width + extra_total, base=base, stem=stem, gap=gap, s=s)

def mark(face, size=420, d_k=1.42, stroke_k=0.27, gap_k=0.42, rise_k=0.3, bar_k=0.95, bar_end=0.54):
    """Two Os back to back: left (navy ring, blue bar) in front; right (blue ring, navy bar) cut back by `gap`.
    The mark is a display cut: its stroke is set relative to the ring (stroke_k * radius), lighter than the
    wordmark's Os, so the overlap reads at large sizes; gap, bar and rise all derive from that stroke."""
    s = size / face.upm; ry = (1514 + 24) / 2 * s; stem = stroke_k * ry; gap = gap_k * stem
    base = 1514 * s + rise_k * stem + 4
    L_ring, L_bar, (ax0, ay0, ax1, ay1) = power_o(face, s, 0, base, gap, bar_k * stem, rise_k * stem, st=stem, bar_end=bar_end)
    half_w = (ax1 - ax0) / 2; dx = d_k * half_w
    R_ring, R_bar, _ = power_o(face, s, dx, base, gap, bar_k * stem, rise_k * stem, st=stem, bar_end=bar_end)
    st = pathops.Path(); L_ring.draw(st.getPen())
    st.stroke(2 * gap, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4); st.convertConicsToQuads()
    clear = op(L_ring, st, U)                     # the front ring plus its clearance
    R_ring = op(R_ring, clear, D)
    allp = op(op(L_ring, R_ring, U), op(L_bar, R_bar, U), U); bx0, by0, bx1, by1 = bounds(allp)
    return dict(L_ring=L_ring, L_bar=L_bar, R_ring=R_ring, R_bar=R_bar, bbox=(bx0, by0, bx1, by1), stem=stem)

def svg(path, parts, vb, title="MORE POWER"):
    x, y, w, h = vb
    body = "\n  ".join(f'<path fill="{c}" d="{to_d(p)}"/>' for c, p in parts)
    open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f2(x)} {f2(y)} {f2(w)} {f2(h)}" '
                          f'width="{f2(w)}" height="{f2(h)}" role="img">\n  <title>{title}</title>\n  {body}\n</svg>\n')

def wordmark_parts(wm, ink=NAVY, accent=BLUE, reversed_=False, power=None):
    """`power` colours the letters of POWER (default: same as `ink`)."""
    l1, l2, rings, bars = wm["letters"], wm["letters2"], list(wm["rings"]), list(wm["bars"])
    if reversed_:
        t = 0.03 * wm["stem"]; l1, l2 = thin(l1, t), thin(l2, t)
        rings = [thin(r, t) for r in rings]; bars = [thin(b, t) for b in bars]
    return [(ink, l1), (ink, rings[0]), (accent, bars[0]), (power or ink, l2), (accent, rings[1]), (ink, bars[1])]

def mark_parts(mk, ink=NAVY, accent=BLUE):
    return [(accent, mk["R_ring"]), (ink, mk["R_bar"]), (ink, mk["L_ring"]), (accent, mk["L_bar"])]

def mark_svg(path, mk, ink=NAVY, accent=BLUE, reversed_=False, pad_k=0.08):
    parts = mark_parts(mk, ink, accent)
    if reversed_:
        t = 0.03 * mk["stem"]; parts = [(c, thin(p, t)) if c == ink else (c, p) for c, p in parts]
    x0, y0, x1, y1 = mk["bbox"]; p = pad_k * (x1 - x0)
    svg(path, parts, (x0 - p, y0 - p, x1 - x0 + 2 * p, y1 - y0 + 2 * p))

if __name__ == "__main__":
    OUT = sys.argv[1]; face = Face("InterDisplay-SemiBold.otf")
    wm = wordmark(face); pad = 0.6 * wm["stem"]; top = bounds(wm["bars"][0])[1]
    vb = (-pad, top - pad, wm["width"] + 2 * pad, wm["base"] + 24 * wm["s"] - top + 2 * pad)
    svg(f"{OUT}/more-power-wordmark.svg", wordmark_parts(wm), vb)
    svg(f"{OUT}/more-power-wordmark-reversed.svg", wordmark_parts(wm, ink=LIGHT, reversed_=True), vb)
    mk = mark(face)
    mark_svg(f"{OUT}/more-power-mark.svg", mk)
    mark_svg(f"{OUT}/more-power-mark-reversed.svg", mk, ink=LIGHT, reversed_=True)
    small = mark(face, stroke_k=0.38, d_k=1.56, gap_k=0.5, rise_k=0.18, bar_k=1.0)
    mark_svg(f"{OUT}/more-power-mark-small.svg", small, pad_k=0.04)
    print("ok")
