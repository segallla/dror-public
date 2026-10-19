"""Print files from the SVG masters: CMYK PDFs, Pantone spot-colour PDFs, one-colour PDFs and EPS.

These are vector PDFs with exact CMYK / spot values. They are not certified PDF/X-4 (no output-intent ICC
profile is embedded); a print vendor can export PDF/X-4 from them in their own prepress tool.
"""
import os, re, sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor, CMYKColorSep
from reportlab.graphics.shapes import Drawing, Path, Group
from reportlab.graphics import renderPS
ROOT = sys.argv[1]; MM = 72 / 25.4
# HEX -> (CMYK, Pantone)
INKS = {"#0b1e3a": ((1.00, 0.78, 0.30, 0.55), "PANTONE 289 C"),
        "#0096db": ((0.85, 0.25, 0.00, 0.00), "PANTONE 2925 C"),
        "#00b0ff": ((0.70, 0.10, 0.00, 0.00), "PANTONE 2995 C"),
        "#f8fafc": ((0.00, 0.00, 0.00, 0.00), None),            # reversed artwork: paper white / white ink
        "#000000": ((0.00, 0.00, 0.00, 1.00), None),
        "#ffffff": ((0.00, 0.00, 0.00, 0.00), None)}
TOK = re.compile(r"[MLHVCQZmlhvcqz]|-?\d*\.?\d+(?:e-?\d+)?")

def read_svg(path):
    s = open(path).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    shapes = [(c.lower(), d) for c, d in re.findall(r'<path fill="(#[0-9A-Fa-f]{6})" d="([^"]+)"', s)]
    return vb, shapes

def segments(d):
    """Yield ('M',x,y) ('L',x,y) ('C',x1,y1,x2,y2,x,y) ('Z',) in absolute coordinates; quads become cubics."""
    t = TOK.findall(d); i = 0; cmd = None; x = y = sx = sy = 0.0
    def num():
        nonlocal i; i += 1; return float(t[i - 1])
    while i < len(t):
        if t[i].isalpha(): cmd = t[i]; i += 1
        if cmd == "M": x, y = num(), num(); sx, sy = x, y; yield ("M", x, y); cmd = "L"
        elif cmd == "L": x, y = num(), num(); yield ("L", x, y)
        elif cmd == "H": x = num(); yield ("L", x, y)
        elif cmd == "V": y = num(); yield ("L", x, y)
        elif cmd == "C": a = [num() for _ in range(6)]; x, y = a[4], a[5]; yield ("C", *a)
        elif cmd == "Q":
            qx, qy, ex, ey = num(), num(), num(), num()
            yield ("C", x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y), ex + 2 / 3 * (qx - ex), ey + 2 / 3 * (qy - ey), ex, ey)
            x, y = ex, ey
        elif cmd in "Zz": x, y = sx, sy; yield ("Z",)
        else: raise ValueError(f"unsupported path command {cmd}")

def colour(hexc, mode):
    cmyk, spot = INKS[hexc]
    if mode == "spot" and spot: return CMYKColorSep(*cmyk, spotName=spot)
    if mode == "black": return CMYKColor(0, 0, 0, 1)
    if mode == "navy-spot": return CMYKColorSep(*INKS["#0b1e3a"][0], spotName="PANTONE 289 C")
    return CMYKColor(*cmyk)

def pdf(svg_path, out, width_mm, mode="cmyk", title=""):
    (x0, y0, w, h), shapes = read_svg(svg_path); sc = width_mm * MM / w
    c = canvas.Canvas(out, pagesize=(w * sc, h * sc)); c.setTitle(title); c.setAuthor("MORE POWER"); c.setCreator("MORE POWER logo kit")
    c.translate(0, h * sc); c.scale(sc, -sc); c.translate(-x0, -y0)
    for hexc, d in shapes:
        if mode in ("black", "navy-spot") and hexc in ("#f8fafc", "#ffffff"): continue
        c.setFillColor(colour(hexc, mode)); p = c.beginPath()
        for sg in segments(d):
            if sg[0] == "M": p.moveTo(*sg[1:])
            elif sg[0] == "L": p.lineTo(*sg[1:])
            elif sg[0] == "C": p.curveTo(*sg[1:])
            else: p.close()
        c.drawPath(p, stroke=0, fill=1, fillMode=1)       # non-zero winding, as in the SVG masters
    c.showPage(); c.save()

def eps(svg_path, out, width_mm):
    (x0, y0, w, h), shapes = read_svg(svg_path); sc = width_mm * MM / w
    dr = Drawing(w * sc, h * sc); g = Group(); g.transform = (sc, 0, 0, -sc, -x0 * sc, (h + y0) * sc)
    for hexc, d in shapes:
        p = Path(fillColor=colour(hexc, "cmyk"), strokeColor=None, fillMode=1)
        for sg in segments(d):
            if sg[0] == "M": p.moveTo(*sg[1:])
            elif sg[0] == "L": p.lineTo(*sg[1:])
            elif sg[0] == "C": p.curveTo(*sg[1:])
            else: p.closePath()
        g.add(p)
    dr.add(g); renderPS.drawToFile(dr, out)

if __name__ == "__main__":
    ART = [("wordmark", 200), ("wordmark-reversed", 200), ("stacked", 120), ("stacked-reversed", 120),
           ("mark", 100), ("mark-reversed", 100), ("mark-small", 60), ("shared-o", 160), ("shared-o-reversed", 160)]
    for sub in ("cmyk", "spot", "one-colour", "eps", "production"): os.makedirs(os.path.join(ROOT, "print", sub), exist_ok=True)
    for name, wmm in ART:
        src = os.path.join(ROOT, "logo", f"more-power-{name}.svg")
        pdf(src, os.path.join(ROOT, "print", "cmyk", f"more-power-{name}-cmyk.pdf"), wmm, "cmyk", f"MORE POWER {name} CMYK")
        pdf(src, os.path.join(ROOT, "print", "spot", f"more-power-{name}-pantone.pdf"), wmm, "spot", f"MORE POWER {name} Pantone")
        eps(src, os.path.join(ROOT, "print", "eps", f"more-power-{name}-cmyk.eps"), wmm)
        if "reversed" not in name:
            pdf(src, os.path.join(ROOT, "print", "one-colour", f"more-power-{name}-black.pdf"), wmm, "black", f"MORE POWER {name} black")
            pdf(src, os.path.join(ROOT, "print", "one-colour", f"more-power-{name}-navy-289C.pdf"), wmm, "navy-spot", f"MORE POWER {name} navy")
    print("ok")
