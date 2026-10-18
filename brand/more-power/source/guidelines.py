"""Builds the one-page usage guidelines (HTML) from the master SVG files."""
import os, re, sys
ROOT = sys.argv[1]
def svg(name, cls="", style=""):
    s = open(os.path.join(ROOT, "logo", name)).read()
    s = re.sub(r'<\?xml[^>]*>', "", s); s = re.sub(r'\swidth="[^"]+"\sheight="[^"]+"', "", s, count=1)
    return s.replace("<svg ", f'<svg class="{cls}" style="{style}" ', 1)
WM, WMR = "more-power-wordmark.svg", "more-power-wordmark-reversed.svg"
MK, MKR = "more-power-mark.svg", "more-power-mark-reversed.svg"
SO, SOR = "more-power-shared-o.svg", "more-power-shared-o-reversed.svg"
FAV = "more-power-favicon-source.svg"
COLOURS = [("Navy", "#0B1E3A", "11 30 58", "C100 M78 Y30 K55", "289 C", "MORE, text, dark backgrounds"),
           ("Deep blue", "#0096DB", "0 150 219", "C85 M25 Y0 K0", "2925 C", "POWER and switches on light backgrounds"),
           ("Electric blue", "#00B0FF", "0 176 255", "C70 M10 Y0 K0", "2995 C", "POWER and switches on dark backgrounds"),
           ("Off-white", "#F8FAFC", "248 250 252", "C2 M1 Y0 K0", "—", "Reversed artwork, light backgrounds")]
swatches = "".join(
    f'<div class="sw"><div class="chip" style="background:{h}"></div><b>{n}</b><code>{h}</code>'
    f'<span>RGB {r}</span><span>{c}</span><span>Pantone {p}</span><em>{u}</em></div>' for n, h, r, c, p, u in COLOURS)
donts = [("transform:scaleX(1.35)", "Don't stretch or squash"),
         ("filter:hue-rotate(140deg)", "Don't recolour"),
         ("filter:drop-shadow(4px 6px 3px rgba(0,0,0,.45))", "Don't add shadows or effects"),
         ("transform:rotate(-12deg)", "Don't rotate"),
         ("opacity:.35", "Don't fade or tint"),
         ("", "Don't place on busy or low-contrast backgrounds")]
dont_html = "".join(
    f'<figure class="dont{" busy" if i == 5 else ""}"><div class="dbox">{svg(WM, "d", st)}</div><figcaption>{t}</figcaption></figure>'
    for i, (st, t) in enumerate(donts))
files = [("logo/more-power-wordmark.svg", "Primary logo, light backgrounds"),
         ("logo/more-power-wordmark-reversed.svg", "Primary logo, dark backgrounds (strokes thinned 3%)"),
         ("logo/more-power-mark.svg · -reversed.svg", "Mark: icons, avatars, patterns"),
         ("logo/more-power-mark-small.svg · -reversed.svg", "Mark, heavier cut for 24–48 px"),
         ("logo/more-power-shared-o.svg · -reversed.svg", "Secondary lockup for square formats"),
         ("logo/more-power-favicon-source.svg", "Single O for 16–24 px (favicon)"),
         ("variants/", "Black, white and one-colour navy versions"),
         ("png/", "High-resolution transparent PNGs"),
         ("web/", "favicon.ico, PNG icons, webmanifest and head snippet"),
         ("animation/more-power-switch-on.html", "Switch-on animation (CSS only, 5 s loop)"),
         ("presentation/", "Presentation board and mockups"),
         ("source/", "Scripts that rebuild every file from the font")]
vbw = float(re.search(r'viewBox="([^"]+)"', open(os.path.join(ROOT, "logo", WM)).read()).group(1).split()[2])
X_RATIO = 0.5 * 1538 * 120 / 2048 / vbw      # X = half the O height, as a fraction of the artwork width
file_rows = "".join(f"<tr><td><code>{a}</code></td><td>{b}</td></tr>" for a, b in files)

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MORE POWER Guidelines</title>
<style>
:root{{--bg:#F4F5F7;--card:#fff;--ink:#0B1E3A;--muted:#5b6b82;--line:#dde2ea;--accent:#0096DB}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0a1424;--card:#111e33;--ink:#e8eef6;--muted:#9aaac0;--line:#24334d}}}}
:root[data-theme="dark"]{{--bg:#0a1424;--card:#111e33;--ink:#e8eef6;--muted:#9aaac0;--line:#24334d}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:40px 16px 80px}}
h1{{font:700 36px/1.15 "Inter Display",Inter,sans-serif;margin:0 0 6px}} h2{{font:700 22px/1.2 "Inter Display",Inter,sans-serif;margin:0 0 6px}}
.lead{{color:var(--muted);margin:0 0 32px;max-width:720px}} p{{max-width:760px}}
section{{background:var(--card);border-radius:18px;padding:28px;margin:0 0 20px}}
.sub{{color:var(--muted);margin:0 0 20px}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.tile{{border:1px solid var(--line);border-radius:14px;padding:28px 20px 16px;display:flex;flex-direction:column;align-items:center;gap:14px;background:#fff;color:#0B1E3A}}
.tile.dark{{background:#0B1E3A;color:#e8eef6;border-color:#0B1E3A}} .tile small{{color:inherit;opacity:.7}}
.tile svg{{width:100%;max-height:110px}}
.hero{{background:#fff;border-radius:14px;padding:48px 24px;display:flex;justify-content:center}} .hero svg{{width:min(760px,100%)}}
.cs{{--w:min(560px,70vw);--x:calc(var(--w) * {X_RATIO:.4f});position:relative;display:inline-block;padding:var(--x);border:1.5px dashed #0096DB;background:repeating-linear-gradient(45deg,rgba(0,150,219,.07) 0 8px,transparent 8px 16px)}}
.cs .inner{{background:#fff;display:block}} .cs svg{{display:block;width:var(--w)}}
.cs .x{{position:absolute;left:0;top:50%;transform:translateY(-50%);width:var(--x);text-align:center;font:600 13px Inter;color:#0096DB}}
.sizes{{display:flex;gap:32px;align-items:flex-end;flex-wrap:wrap}} .sizes figure{{margin:0}} .sizes figcaption{{color:var(--muted);font-size:13px;margin-top:8px}}
.sw{{border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:2px;font-size:14px}}
.chip{{height:84px;border-radius:10px;margin-bottom:10px;border:1px solid var(--line)}} .sw code{{font-size:14px}} .sw span{{color:var(--muted)}} .sw em{{margin-top:6px;font-style:normal}}
.dont{{margin:0}} .dbox{{background:#fff;border:1px solid var(--line);border-radius:14px;height:130px;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}}
.dbox::after{{content:"";position:absolute;inset:0;background:linear-gradient(to top right,transparent calc(50% - 1.5px),#e5484d calc(50% - 1.5px),#e5484d calc(50% + 1.5px),transparent calc(50% + 1.5px))}}
.dbox svg{{width:72%}} .busy .dbox{{background:repeating-linear-gradient(60deg,#7fb8d8 0 14px,#2a6f97 14px 28px)}}
.dont figcaption{{font-size:14px;margin-top:8px}}
table{{width:100%;border-collapse:collapse;font-size:14px}} td{{padding:8px 6px;border-top:1px solid var(--line);vertical-align:top}} td code{{font-size:13px}}
ul{{margin:0;padding-left:20px}} li{{margin:4px 0}}
@media (max-width:560px){{section{{padding:20px}} h1{{font-size:28px}}}}
</style></head><body><main>
<h1>MORE POWER · Logo guidelines</h1>
<p class="lead">How to use the logo, its colours and its files. Keep this page next to the logo files.</p>

<section><h2>1. The idea</h2>
<p class="sub">Each O in the name is a power switch. MORE is navy with a blue switch; POWER is blue with a navy switch. The mark puts the same two Os back to back, overlapping like a transformer.</p>
<div class="hero">{svg(WM)}</div></section>

<section><h2>2. Versions</h2><p class="sub">Use the primary logo wherever it fits. The other versions are for the formats named under each one.</p>
<div class="grid">
<div class="tile">{svg(WM)}<small>Primary · headers, documents, signage</small></div>
<div class="tile dark">{svg(WMR)}<small>Primary reversed · dark backgrounds</small></div>
<div class="tile">{svg(SO)}<small>Secondary · square formats, entrance signs</small></div>
<div class="tile">{svg(MK)}<small>Mark · app icon, avatar, patterns</small></div>
<div class="tile dark">{svg(MKR)}<small>Mark reversed</small></div>
<div class="tile">{svg(FAV, style="max-height:80px")}<small>Single O · favicon, 16–24 px only</small></div>
</div></section>

<section><h2>3. Clear space</h2><p class="sub">Keep a free margin of <b>X</b> on every side, where X is half the height of the O. Nothing else, including text, other logos or the edge of the page, goes inside it.</p>
<div class="cs"><span class="x">X</span><span class="inner">{svg(WM)}</span></div></section>

<section><h2>4. Minimum size</h2><p class="sub">Below these sizes the switches stop reading. Switch to the smaller version listed instead.</p>
<div class="sizes">
<figure>{svg(WM, style="width:120px")}<figcaption>Primary: 120 px / 30 mm wide</figcaption></figure>
<figure>{svg(SO, style="width:80px")}<figcaption>Secondary: 80 px / 22 mm wide</figcaption></figure>
<figure>{svg(MK, style="width:40px")}<figcaption>Mark: 40 px / 12 mm wide<br>(small cut from 24 px)</figcaption></figure>
<figure>{svg(FAV, style="width:16px")}<figcaption>Single O: 16 px</figcaption></figure>
</div></section>

<section><h2>5. Colour</h2><p class="sub">Use one blue per background. On light backgrounds use Deep blue, which has enough contrast for small sizes. On navy or other dark backgrounds use Electric blue. CMYK and Pantone values are close matches; check them against a printed swatch book before the first print run.</p>
<div class="grid">{swatches}</div>
<p style="margin-top:16px">One-colour versions, in black, white or navy, are for single-colour printing, embossing, engraving and fax. Don't make two-colour versions in other colours.</p></section>

<section><h2>6. Typography</h2>
<ul><li><b>Logo:</b> Inter Display SemiBold, with custom Os. It is already outlined, so you never need to type the logo.</li>
<li><b>Headlines:</b> Inter Display, SemiBold or Bold. <b>Body:</b> Inter, Regular and Medium.</li>
<li><b>Licence:</b> SIL Open Font License, free for commercial use. Fallback: <code>system-ui, -apple-system, "Segoe UI", sans-serif</code>.</li></ul></section>

<section><h2>7. Don'ts</h2><div class="grid">{dont_html}</div>
<ul style="margin-top:16px"><li>Don't rebuild the Os from a stock power icon, or type the name in another font.</li>
<li>Don't swap the colours of the two words, or of the switches.</li>
<li>Don't separate the switch from its O, or animate the logo other than with the supplied switch-on animation.</li></ul></section>

<section><h2>8. Files</h2><table>{file_rows}</table>
<p style="margin-top:16px;color:var(--muted)">The trademark has not been searched yet. Run a professional trademark search before registering or printing at scale.</p></section>
</main></body></html>'''
open(os.path.join(ROOT, "guidelines", "more-power-guidelines.html"), "w").write(html); print("ok")
