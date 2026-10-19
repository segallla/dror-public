"""Overview board of the logo system (boards/more-power-system.png)."""
import os, re, sys
import cairosvg
ROOT = sys.argv[1]; NAVY = "#0B1E3A"
F = lambda n: os.path.join(ROOT, "logo", f"more-power-{n}.svg")
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
W, H = 1600, 2060
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#F4F5F7"/>',
     '<text x="60" y="78" font-family="Inter Display" font-size="40" font-weight="700" fill="#0B1E3A">MORE POWER</text>',
     '<text x="60" y="114" font-family="Inter" font-size="20" fill="#5b6b82">Two words. Two power switches. One connected system.</text>']
s += [card(60, 150, 1480, 360), T(90, 186, "1 · PRIMARY"), place(F("wordmark"), 800, 340, 1240, 220)]
s += [card(60, 530, 960, 300, NAVY), T(90, 566, "2 · PRIMARY REVERSED", "#8fa3bf"), place(F("wordmark-reversed"), 540, 690, 820, 200)]
s += [card(1040, 530, 500, 300), T(1070, 566, "4 · MARK"), place(F("mark"), 1290, 690, 380, 200)]
s += [card(60, 850, 720, 400), T(90, 886, "3 · STACKED"), place(F("stacked"), 420, 1065, 420, 260)]
s += [card(800, 850, 740, 400, NAVY), T(830, 886, "3 · STACKED REVERSED", "#8fa3bf"), place(F("stacked-reversed"), 1170, 1065, 420, 260)]
s += [card(60, 1270, 1480, 360), T(90, 1306, "5 · EXPRESSIVE · CAMPAIGNS, COVERS, POSTERS, ANIMATION")]
s += [place(F("shared-o"), 430, 1460, 560, 230), f'<rect x="820" y="1330" width="680" height="270" rx="16" fill="{NAVY}"/>', place(F("shared-o-reversed"), 1160, 1465, 520, 210)]
s += [card(60, 1650, 720, 380), T(90, 1686, "SMALL SIZES · TRUE SIZE")]
x = 100
for name, px in (("mark", 64), ("mark-small", 40), ("mark-small", 28), ("favicon-source", 20), ("favicon-source", 16)):
    s.append(at(F(name), x, 1790 - px * (0.33 if "mark" in name else 0.5), px)); s.append(f'<text x="{x}" y="1840" font-family="Inter" font-size="15" fill="#5b6b82">{px}</text>'); x += px + 44
s += [at(F("wordmark"), 100, 1880, 300), at(F("wordmark"), 100, 1950, 160), at(F("wordmark"), 300, 1956, 130)]
s += [card(800, 1650, 740, 380), T(830, 1686, "6 · APP ICON · AVATAR · FAVICON (MARK ONLY)")]
s.append(f'<rect x="880" y="1730" width="200" height="200" rx="44" fill="{NAVY}"/>'); s.append(place(F("mark-reversed"), 980, 1830, 150, 110))
s.append(f'<circle cx="1220" cy="1830" r="100" fill="{NAVY}"/>'); s.append(place(F("mark-reversed"), 1220, 1832, 140, 100))
s.append('<rect x="1380" y="1790" width="80" height="80" rx="18" fill="#fff" stroke="#dde2ea"/>'); s.append(place(F("mark-small"), 1420, 1830, 60, 44))
s.append('<rect x="1475" y="1814" width="32" height="32" rx="6" fill="#fff" stroke="#dde2ea"/>'); s.append(place(F("favicon-source"), 1491, 1830, 20, 20))
s.append("</svg>")
os.makedirs(os.path.join(ROOT, "boards"), exist_ok=True)
cairosvg.svg2png(bytestring="".join(s).encode(), write_to=os.path.join(ROOT, "boards", "more-power-system.png")); print("ok")
