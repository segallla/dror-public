"""Builds the usage guidelines (guidelines/more-power-guidelines.html) from the master SVG files."""
import os, re, sys
ROOT = sys.argv[1]
def raw(name): return open(os.path.join(ROOT, "logo", name)).read()
def vbw(name): return float(re.search(r'viewBox="([^"]+)"', raw(name)).group(1).split()[2])
def svg(name, style=""):
    s = re.sub(r'\swidth="[^"]+"\sheight="[^"]+"', "", raw(name), count=1)
    return s.replace("<svg ", f'<svg style="{style}" ', 1)
WM, WMR, ST, STR = "more-power-wordmark.svg", "more-power-wordmark-reversed.svg", "more-power-stacked.svg", "more-power-stacked-reversed.svg"
MK, MKR, MKS = "more-power-mark.svg", "more-power-mark-reversed.svg", "more-power-mark-small.svg"
SO, SOR, FAV = "more-power-shared-o.svg", "more-power-shared-o-reversed.svg", "more-power-favicon-source.svg"
O_DIAM = 1538 * 120 / 2048                     # outer diameter of the power O in the wordmark, in artwork units
X = {WM: 0.5 * O_DIAM / vbw(WM), ST: 0.5 * O_DIAM / vbw(ST), MK: 0.25 * 200 / vbw(MK)}   # mark: a quarter of a ring

COLOURS = [("Navy", "#0B1E3A", "11 30 58", "C100 M78 Y30 K55", "289 C"),
           ("Deep blue", "#0096DB", "0 150 219", "C85 M25 Y0 K0", "2925 C"),
           ("Electric blue", "#00B0FF", "0 176 255", "C70 M10 Y0 K0", "2995 C"),
           ("Off-white", "#F8FAFC", "248 250 252", "paper white / white ink", "—")]
swatches = "".join(f'<div class="sw"><div class="chip" style="background:{h}"></div><b>{n}</b><code>{h}</code>'
                   f'<span>RGB {r}</span><span>{c}</span><span>Pantone {p}</span></div>' for n, h, r, c, p in COLOURS)
def chip(h): return f'<i class="dot" style="background:{h}"></i>'
mapping = [("MORE", "Navy", "#0B1E3A", "Off-white", "#F8FAFC"),
           ("Switch in the O of MORE", "Deep blue", "#0096DB", "Electric blue", "#00B0FF"),
           ("POWER (and its ring)", "Deep blue", "#0096DB", "Electric blue", "#00B0FF"),
           ("Switch in the O of POWER", "Navy", "#0B1E3A", "Off-white", "#F8FAFC"),
           ("Mark: left ring · right ring · core", "Navy · Deep blue · Electric blue", None, "Off-white · Electric blue · Off-white", None)]
map_rows = "".join(f'<tr><td>{e}</td><td>{chip(lh) if lh else ""}{l}</td><td>{chip(dh) if dh else ""}{d}</td></tr>' for e, l, lh, d, dh in mapping)
hier = [("1", "Primary", WM, False, "Default everywhere: documents, website header, presentations, signage", "logo/more-power-wordmark.svg"),
        ("2", "Primary reversed", WMR, True, "The same on navy or other dark backgrounds", "logo/more-power-wordmark-reversed.svg"),
        ("3", "Stacked", ST, False, "Square and vertical formats; entrance and wayfinding signs", "logo/more-power-stacked.svg"),
        ("4", "Mark", MK, False, "App icon, avatar, patterns, merchandise — never with the name inside it", "logo/more-power-mark.svg"),
        ("5", "Expressive shared-O", SO, False, "Campaigns, covers, posters and animation only — not for signage or official documents", "logo/more-power-shared-o.svg"),
        ("6", "Single O", FAV, False, "Favicon and other uses from 16 to 23 px", "logo/more-power-favicon-source.svg")]
hier_html = "".join(f'<div class="tile{" dark" if dk else ""}"><span class="n">{n}</span>{svg(f, "max-height:96px")}<b>{t}</b><small>{u}</small><code>{p}</code></div>'
                    for n, t, f, dk, u, p in hier)
mins = [("Primary", "128 px", "30 mm"), ("Stacked", "96 px", "24 mm"), ("Expressive shared-O", "120 px", "30 mm"),
        ("Mark — standard (with core)", "48 px", "12 mm"), ("Mark — small cut (core left open)", "24–47 px", "use standard"),
        ("Single O", "16–23 px", "—")]
min_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in mins)
donts = [("transform:scaleX(1.35)", "Don't stretch or squash"), ("filter:hue-rotate(140deg)", "Don't recolour"),
         ("filter:drop-shadow(4px 6px 3px rgba(0,0,0,.45))", "Don't add shadows or effects"), ("transform:rotate(-12deg)", "Don't rotate"),
         ("opacity:.35", "Don't fade or tint"), ("", "Don't place on busy or low-contrast backgrounds")]
dont_html = "".join(f'<figure class="dont{" busy" if i == 5 else ""}"><div class="dbox">{svg(WM, st + ";width:72%")}</div><figcaption>{t}</figcaption></figure>'
                    for i, (st, t) in enumerate(donts))
files = [("logo/", "SVG masters: primary, reversed, stacked, mark (standard and small cut), expressive shared-O, single O"),
         ("variants/", "Black, white and one-colour navy SVGs"),
         ("png/", "High-resolution transparent PNGs for screens"),
         ("print/cmyk/", "CMYK vector PDFs (exact values above; not certified PDF/X-4, see note)"),
         ("print/spot/", "Pantone spot-colour vector PDFs (289 C, 2925 C, 2995 C)"),
         ("print/one-colour/", "Black and Pantone 289 C one-colour vector PDFs"),
         ("print/eps/", "CMYK EPS files for sign makers and older workflows"),
         ("print/production/", "Simplified one-colour artwork for embroidery, engraving, laser and vinyl cutting"),
         ("web/", "favicon.ico, favicon.svg, PNG icons, site.webmanifest and head snippet"),
         ("app-icons/", "iOS sizes, Android adaptive and legacy icons, Play Store icon, social avatars"),
         ("animation/", "Switch-on animation: plays once and holds"),
         ("presentation/", "Presentation board and mockups"),
         ("docs/", "This guide as PDF, release notes, font and licence information"),
         ("source/ · build.sh", "Scripts that rebuild every file from the font")]
file_rows = "".join(f"<tr><td><code>{a}</code></td><td>{b}</td></tr>" for a, b in files)
cs = lambda name, w: (f'<figure class="csf"><div class="cs" style="--w:{w}px;--x:calc(var(--w) * {X[name]:.4f})">'
                      f'<span class="x">X</span><span class="inner">{svg(name, "display:block;width:var(--w);max-width:100%")}</span></div></figure>')

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MORE POWER Guidelines</title>
<style>
:root{{--bg:#F4F5F7;--card:#fff;--ink:#0B1E3A;--muted:#5b6b82;--line:#dde2ea}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0a1424;--card:#111e33;--ink:#e8eef6;--muted:#9aaac0;--line:#24334d}}}}
:root[data-theme="dark"]{{--bg:#0a1424;--card:#111e33;--ink:#e8eef6;--muted:#9aaac0;--line:#24334d}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,sans-serif}}
main{{max-width:1080px;margin:0 auto;padding:40px 16px 80px}}
h1{{font:700 36px/1.15 "Inter Display",Inter,sans-serif;margin:0 0 6px}} h2{{font:700 22px/1.2 "Inter Display",Inter,sans-serif;margin:0 0 8px}}
h3{{font:600 15px Inter,sans-serif;margin:18px 0 6px}}
.lead{{color:var(--muted);margin:0 0 28px;max-width:720px}} p{{max-width:780px;margin:0 0 12px}}
section{{background:var(--card);border-radius:18px;padding:28px;margin:0 0 20px;break-inside:avoid}}
.sub{{color:var(--muted)}}
.principle{{font:600 22px/1.35 "Inter Display",Inter,sans-serif;margin:18px 0 6px}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}}
.tile{{position:relative;border:1px solid var(--line);border-radius:14px;padding:30px 18px 16px;display:flex;flex-direction:column;align-items:center;gap:8px;background:#fff;color:#0B1E3A;text-align:center}}
.tile.dark{{background:#0B1E3A;color:#e8eef6;border-color:#0B1E3A}} .tile svg{{width:90%;margin-bottom:6px}}
.tile small{{opacity:.75;font-size:13px}} .tile code{{font-size:11.5px;opacity:.6}} .tile .n{{position:absolute;left:12px;top:8px;font:700 13px Inter;opacity:.5}}
.hero{{background:#fff;border-radius:14px;padding:44px 24px;display:flex;justify-content:center;margin-top:16px}} .hero svg{{width:min(760px,100%)}}
.csrow{{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start}} .csf{{margin:0}}
.cs{{position:relative;display:inline-block;padding:var(--x);border:1.5px dashed #0096DB;background:repeating-linear-gradient(45deg,rgba(0,150,219,.08) 0 8px,transparent 8px 16px)}}
.cs .inner{{background:#fff;display:block}}
.cs .x{{position:absolute;left:0;top:50%;transform:translateY(-50%);width:var(--x);text-align:center;font:600 12px Inter;color:#0096DB}}
.sw{{border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:2px;font-size:14px}}
.chip{{height:76px;border-radius:10px;margin-bottom:10px;border:1px solid var(--line)}} .sw span{{color:var(--muted)}}
.dot{{display:inline-block;width:14px;height:14px;border-radius:4px;margin-right:8px;vertical-align:-2px;border:1px solid var(--line)}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin:6px 0 4px}} th{{text-align:left;font-weight:600;color:var(--muted);padding:8px 6px}}
td{{padding:8px 6px;border-top:1px solid var(--line);vertical-align:top}} td code{{font-size:13px}}
.rule{{border-left:3px solid #0096DB;padding:8px 14px;margin:14px 0 0;background:rgba(0,150,219,.06);border-radius:0 8px 8px 0}}
.dont{{margin:0}} .dbox{{background:#fff;border:1px solid var(--line);border-radius:14px;height:124px;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}}
.dbox::after{{content:"";position:absolute;inset:0;background:linear-gradient(to top right,transparent calc(50% - 1.5px),#e5484d calc(50% - 1.5px),#e5484d calc(50% + 1.5px),transparent calc(50% + 1.5px))}}
.busy .dbox{{background:repeating-linear-gradient(60deg,#7fb8d8 0 14px,#2a6f97 14px 28px)}} .dont figcaption{{font-size:14px;margin-top:8px}}
ul{{margin:0;padding-left:20px}} li{{margin:5px 0}}
.legal{{border:2px solid #e5484d;}} .legal h2{{color:#c4373c}}
@media (max-width:560px){{section{{padding:20px}} h1{{font-size:28px}}}}
@media print{{body{{background:#fff}} section{{border:1px solid #dde2ea}}}}
</style></head><body><main>
<h1>MORE POWER · Logo guidelines</h1>
<p class="lead">Version 1.0 · How to use the logo, its colours and its files. Keep this guide with the logo files.</p>

<section><h2>1. The idea</h2>
<p>Each O in the name becomes a power switch. MORE is navy with a blue switch; POWER is blue with a navy switch. Together they express two complementary forces, real assets and power capacity, working as one system. In the standalone mark, the two switches are coupled like circuits and meet in one shared core.</p>
<p class="principle">Two words. Two power switches. One connected system.</p>
<p class="sub">MORE represents the assets and the platform. POWER represents the capacity they unlock. The reciprocal colours connect the two, and the coupled mark expresses cooperation, transfer and shared momentum.</p>
<div class="hero">{svg(WM)}</div></section>

<section><h2>2. Logo hierarchy</h2><p class="sub">Use the highest version in this list that fits the format. For entrance and distance signage use the primary or stacked logo, never the expressive shared-O lockup.</p>
<div class="grid">{hier_html}</div></section>

<section><h2>3. Colour</h2>
<div class="grid">{swatches}</div>
<p class="sub" style="margin-top:14px">CMYK and Pantone values are close matches. Check them against a printed swatch book before the first print run.</p>
<h3>Light and dark backgrounds</h3>
<table><tr><th>Element</th><th>Light background</th><th>Dark background</th></tr>{map_rows}</table>
<p class="rule"><b>Rule:</b> on dark backgrounds every navy element reverses to off-white. Every blue element becomes electric blue.</p>
<h3>Small sizes</h3>
<p>For small digital use on light backgrounds, prefer the navy one-colour version whenever maximum contrast is needed (below 128 px wide, or in text-heavy interfaces). Deep blue on white has a contrast ratio of about 3.3:1. It is meant for the standard-size wordmark and display use. Electric blue on navy (about 6.9:1) is strong at every size.</p>
<h3>One-colour versions</h3>
<p>Black, white and navy (Pantone 289 C) versions are for single-colour printing and for embossing, engraving, laser cutting, embroidery, vinyl cutting and other one-colour production methods. For embroidery and cutting use the simplified files in <code>print/production/</code>. Don't make two-colour versions in other colours.</p></section>

<section><h2>4. Clear space</h2>
<p>X equals one half of the outer diameter of the power-button O in the primary wordmark. Measure clear space from the outermost edge of the artwork, including the tip of each switch, not from the text baseline or an internal counter. The stacked logo uses the same X. For the mark, X is one quarter of a ring's outer diameter. Nothing, including text, other logos or the edge of the page, goes inside the clear space.</p>
<div class="csrow">{cs(WM, 520)}{cs(ST, 250)}{cs(MK, 210)}</div></section>

<section><h2>5. Minimum size</h2><p class="sub">All sizes are minimum <b>width</b>, not height. Below them, switch to the next version in the list.</p>
<table><tr><th>Version</th><th>Digital</th><th>Print</th></tr>{min_rows}</table></section>

<section><h2>6. Typography</h2>
<ul><li><b>Source of the wordmark:</b> Inter Display, version 4.000 (git a52131595), SemiBold, weight 600. Inter Display is the static display optical size of Inter.</li>
<li><b>Spacing:</b> tracking +35/1000 em, word space 0.24 em, the font's own OpenType kerning, and Os optically fitted by hand.</li>
<li><b>The Os</b> are custom geometry: power-button rings matched to the font's overshoot and stroke contrast. They are not glyphs from the font.</li>
<li><b>Production files</b> use outlined artwork and don't need the font. Never retype the logo.</li>
<li><b>Brand typefaces:</b> Inter Display (SemiBold or Bold) for headlines; Inter (Regular and Medium) for text. Licence: SIL Open Font License 1.1, free for commercial use. Fallback: <code>system-ui, -apple-system, "Segoe UI", sans-serif</code>.</li></ul></section>

<section><h2>7. Motion</h2>
<p>The supplied switch-on animation plays once and holds. Do not loop it by default. When the viewer has asked for reduced motion (<code>prefers-reduced-motion</code>), show the static logo instead. Don't animate the logo in any other way.</p></section>

<section><h2>8. Don'ts</h2><div class="grid">{dont_html}</div>
<ul style="margin-top:16px">
<li>Don't rebuild the Os from a stock power icon, or type the name in another font.</li>
<li>Don't swap the colours of the two words, or of the switches.</li>
<li>Don't separate a switch from its O.</li>
<li>Don't place the mark inside an unapproved circle, shield or badge.</li>
<li>Don't use the coupled mark as an O inside the wordmark.</li>
<li>Don't add "Fund" or any other descriptor directly to the artwork.</li>
<li>Don't use the expressive shared-O lockup below its minimum size, or for signage and official documents.</li>
<li>Don't put the name inside the app icon or avatar: they use the mark alone.</li></ul></section>

<section><h2>9. Files</h2><table>{file_rows}</table>
<p class="sub" style="margin-top:12px">Print note: the CMYK and spot PDFs carry exact colour values but no embedded output-intent profile, so they are not certified PDF/X-4. Ask the printer to convert them to PDF/X-4 for their press profile, or to export from the EPS files.</p></section>

<section class="legal"><h2>10. Trademark</h2>
<p><b>The trademark has not been searched yet.</b> Power-button symbols are a crowded category, so run a professional trademark search before registering the logo or printing it at scale. The search should cover:</p>
<ul><li>MORE POWER as a word mark;</li><li>the complete wordmark with its power-button Os;</li><li>the coupled two-O mark;</li>
<li>the energy, investment, real-estate and infrastructure classes.</li></ul></section>
</main></body></html>'''
os.makedirs(os.path.join(ROOT, "guidelines"), exist_ok=True)
open(os.path.join(ROOT, "guidelines", "more-power-guidelines.html"), "w").write(html); print("ok")
