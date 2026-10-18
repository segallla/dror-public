"""The favourite, rebuilt as one system: one-line wordmark (POWER in blue), two-ring mark, shared-O secondary."""
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
mk = k.mark(face, gap_k=0.25, rise_k=0.0, bar_end=0.46, bar_k=0.91)
k.mark_svg(f"{D}/more-power-mark.svg", mk, accent=DEEP)
k.mark_svg(f"{D}/more-power-mark-reversed.svg", mk, ink=LIGHT, reversed_=True)
small = k.mark(face, stroke_k=0.38, d_k=1.56, gap_k=0.36, rise_k=0.0, bar_k=0.95, bar_end=0.48)
k.mark_svg(f"{D}/more-power-mark-small.svg", small, accent=DEEP, pad_k=0.04)
k.mark_svg(f"{D}/more-power-mark-small-reversed.svg", small, ink=LIGHT, pad_k=0.04)
for dark in (False, True):
    parts, v = bigo11.build("split", dark=dark, **OPEN)
    k.svg(f"{D}/more-power-shared-o{'-reversed' if dark else ''}.svg", parts, v)

def inner(p):
    s = open(p).read(); v = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    return re.search(r'</title>(.*)</svg>', s, re.S).group(1), v
def place(p, cx, cy, maxw, maxh):
    b, v = inner(p); sc = min(maxw / v[2], maxh / v[3]); w, h = v[2] * sc, v[3] * sc
    return f'<g transform="translate({cx - w / 2:.1f},{cy - h / 2:.1f}) scale({sc:.5f}) translate({-v[0]:.2f},{-v[1]:.2f})">{b}</g>'
def at(p, x, y, w):
    b, v = inner(p); sc = w / v[2]
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({sc:.5f}) translate({-v[0]:.2f},{-v[1]:.2f})">{b}</g>'
T = lambda x, y, t, c="#5b6b82": f'<text x="{x}" y="{y}" font-family="Inter" font-size="18" font-weight="600" letter-spacing="1.5" fill="{c}">{t}</text>'
card = lambda x, y, w, h, fill="#fff": f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}"/>'
F = lambda n: f"{D}/more-power-{n}.svg"
W, H = 1600, 1660
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#F4F5F7"/>',
     '<text x="60" y="78" font-family="Inter Display" font-size="40" font-weight="700" fill="#0B1E3A">MORE POWER</text>',
     '<text x="60" y="114" font-family="Inter" font-size="20" fill="#5b6b82">Primary wordmark, mark and the shared-O secondary lockup, as one system.</text>']
s += [card(60, 150, 1480, 360), T(90, 186, "PRIMARY"), place(F("wordmark"), 800, 340, 1240, 220)]
s += [card(60, 530, 960, 300, NAVY), T(90, 566, "PRIMARY · ON NAVY", "#8fa3bf"), place(F("wordmark-reversed"), 540, 690, 820, 200)]
s += [card(1040, 530, 500, 300), T(1070, 566, "MARK"), place(F("mark"), 1290, 690, 380, 210)]
s += [card(60, 850, 720, 400), T(90, 886, "SECONDARY · SHARED O"), place(F("shared-o"), 420, 1060, 560, 270)]
s += [card(800, 850, 740, 400, NAVY), T(830, 886, "SECONDARY · ON NAVY", "#8fa3bf"), place(F("shared-o-reversed"), 1170, 1060, 560, 270)]
s += [card(60, 1270, 720, 360), T(90, 1306, "SMALL SIZES · TRUE SIZE")]
x = 100
for px in (64, 32, 24, 16):
    s.append(at(F("mark-small"), x, 1400 - px * 0.36, px)); s.append(f'<text x="{x}" y="1460" font-family="Inter" font-size="15" fill="#5b6b82">{px}</text>'); x += px + 44
s += [at(F("wordmark"), 100, 1500, 320), at(F("wordmark"), 100, 1570, 160), at(F("wordmark"), 300, 1576, 110)]
s += [card(800, 1270, 740, 360), T(830, 1306, "APP ICON · AVATAR")]
s.append(f'<rect x="900" y="1350" width="200" height="200" rx="44" fill="{NAVY}"/>'); s.append(place(F("mark-small-reversed"), 1000, 1448, 140, 120))
s.append(f'<circle cx="1260" cy="1450" r="100" fill="{NAVY}"/>'); s.append(place(F("shared-o-reversed"), 1260, 1452, 150, 110))
s.append('<rect x="1400" y="1410" width="80" height="80" rx="18" fill="#fff" stroke="#dde2ea"/>'); s.append(place(F("mark-small"), 1440, 1450, 60, 50))
s.append("</svg>"); cairosvg.svg2png(bytestring="".join(s).encode(), write_to=os.path.join(D, "..", "boards", "more-power-system.png"))
print("ok")
