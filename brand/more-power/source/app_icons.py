"""App icons and social avatars, mark only (no words): iOS, Android (adaptive + legacy) and social profiles."""
import os, re, sys
import cairosvg
ROOT = sys.argv[1]; NAVY = "#0B1E3A"; WHITE = "#FFFFFF"
def art(name):
    s = open(os.path.join(ROOT, "logo", f"more-power-{name}.svg")).read()
    v = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    return re.search(r'</title>(.*)</svg>', s, re.S).group(1), v
def tile(path, px, bg, name, mark_w, corner=0.0, nudge=-0.02, circle=False):
    """Square canvas `px`, background `bg` (None = transparent), mark centred at `mark_w` of the width."""
    body, (x0, y0, w, h) = art(name); S = 1000; sc = mark_w * S / w
    tx = (S - w * sc) / 2 - x0 * sc; ty = (S - h * sc) / 2 - y0 * sc + nudge * S
    bgsvg = "" if bg is None else (f'<circle cx="500" cy="500" r="500" fill="{bg}"/>' if circle else
                                   f'<rect width="{S}" height="{S}" rx="{corner * S}" fill="{bg}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{px}" height="{px}">{bgsvg}'
           f'<g transform="translate({tx:.2f},{ty:.2f}) scale({sc:.5f})">{body}</g></svg>')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path, output_width=px, output_height=px)
    if path.endswith("-1024.png") or path.endswith("master.png"):
        open(path[:-4] + ".svg", "w").write(svg)
A = os.path.join(ROOT, "app-icons")
# iOS: full-bleed square (the system applies the corner mask); small sizes use the heavier small cut
for px in (1024, 180, 167, 152, 120, 87, 80, 76, 60, 58, 40, 29, 20):
    tile(os.path.join(A, "ios", f"ios-icon-{px}.png"), px, NAVY, "mark-reversed" if px >= 152 else "mark-small-reversed", 0.72 if px >= 152 else 0.78)
# Android adaptive icon: 432 px layers (108 dp @4x); the mark stays inside the 66 % safe circle
tile(os.path.join(A, "android", "adaptive-foreground-432.png"), 432, None, "mark-reversed", 0.50)
tile(os.path.join(A, "android", "adaptive-background-432.png"), 432, NAVY, "mark-reversed", 0.0001)
for px, dens in ((48, "mdpi"), (72, "hdpi"), (96, "xhdpi"), (144, "xxhdpi"), (192, "xxxhdpi")):
    tile(os.path.join(A, "android", f"ic_launcher-{dens}-{px}.png"), px, NAVY, "mark-small-reversed" if px < 96 else "mark-reversed", 0.66, corner=0.22)
tile(os.path.join(A, "android", "play-store-512.png"), 512, NAVY, "mark-reversed", 0.70)
# Social avatars: circle-crop safe (mark within 62 % of the diameter); navy and white versions
for px in (400, 800, 1080):
    tile(os.path.join(A, "social", f"avatar-navy-{px}.png"), px, NAVY, "mark-reversed", 0.60, nudge=-0.015)
    tile(os.path.join(A, "social", f"avatar-white-{px}.png"), px, WHITE, "mark", 0.60, nudge=-0.015)
print("ok")
