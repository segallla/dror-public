"""Switch-on animation: the switches drop into the Os, each ring answers with a small pulse."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make8 as k
OUT = sys.argv[1]; NAVY, LIGHT, BLUE, DEEP = k.NAVY, k.LIGHT, k.BLUE, "#0096DB"
OPEN = dict(gap_k=0.30, rise_k=0.0, bar_end=0.46, bar_k=0.88)
face = k.Face("InterDisplay-SemiBold.otf")

def svg_from(parts, vb, classes, cls):
    x, y, w, h = vb; body = []
    for (c, p), extra in zip(parts, classes):
        bb = k.bounds(p); cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        body.append(f'<path class="{extra}" style="transform-origin:{cx:.1f}px {cy:.1f}px" fill="{c}" d="{k.to_d(p)}"/>')
    return f'<svg class="{cls}" viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}" role="img" aria-label="MORE POWER">{"".join(body)}</svg>'

wm = k.wordmark(face, **OPEN); pad = 0.6 * wm["stem"]; top = wm["base"] - 1514 * wm["s"]
vb = (-pad, top - 0.9 * wm["stem"] - pad, wm["width"] + 2 * pad, wm["base"] + 24 * wm["s"] - top + 0.9 * wm["stem"] + 2 * pad)
CL = ["letters", "ring r1", "bar b1", "letters", "ring r2", "bar b2"]
light = svg_from(k.wordmark_parts(wm, accent=DEEP, power=DEEP), vb, CL, "lock")
dark = svg_from(k.wordmark_parts(wm, ink=LIGHT, reversed_=True, power=BLUE), vb, CL, "lock")
mk = k.mark(face, gap_k=0.25, rise_k=0.0, bar_end=0.46, bar_k=0.91)
x0, y0, x1, y1 = mk["bbox"]; p = 0.08 * (x1 - x0)
mvb = (x0 - p, y0 - p - 0.3 * (y1 - y0), x1 - x0 + 2 * p, y1 - y0 + 2 * p + 0.3 * (y1 - y0))
mark = svg_from(k.mark_parts(mk, accent=DEEP), mvb, ["ring r2", "bar b2", "ring r1", "bar b1"], "sym")

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MORE POWER switch-on</title>
<style>
:root{{--bg:#F4F5F7;--ink:#0B1E3A;--muted:#5b6b82}}
body{{margin:0;background:var(--bg);font:15px/1.5 Inter,system-ui,sans-serif;color:var(--ink)}}
main{{max-width:1000px;margin:0 auto;padding:32px 16px}}
h1{{font-size:22px;margin:0 0 4px}} p{{color:var(--muted);margin:0 0 20px}}
.card{{background:#fff;border-radius:16px;padding:48px 24px;margin:0 0 20px;display:flex;justify-content:center}}
.card.dark{{background:#0B1E3A}}
.lock{{width:min(820px,100%)}} .sym{{width:min(360px,80%)}}
button{{font:600 14px Inter,system-ui,sans-serif;border:0;border-radius:999px;padding:10px 18px;background:#0B1E3A;color:#fff;cursor:pointer}}
path{{transform-box:view-box}}
.play .letters{{animation:fade .5s ease-out both}}
.play .ring{{animation:fade .5s ease-out both, pulse .45s cubic-bezier(.3,1.6,.5,1) both}}
.play .r1{{animation-delay:0s,.95s}} .play .r2{{animation-delay:0s,1.35s}}
.play .bar{{animation:drop .5s cubic-bezier(.55,0,.25,1.25) both}}
.play .b1{{animation-delay:.5s}} .play .b2{{animation-delay:.9s}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes drop{{0%{{opacity:0;transform:translateY(-38%)}}60%{{opacity:1}}100%{{opacity:1;transform:none}}}}
@keyframes pulse{{0%{{transform:scale(1)}}40%{{transform:scale(1.045)}}100%{{transform:scale(1)}}}}
@media (prefers-reduced-motion:reduce){{.play *{{animation:none!important}}}}
</style></head><body><main>
<h1>MORE POWER · switch-on</h1>
<p>The switches drop into the Os, MORE first, then POWER; each ring answers with a small pulse. Total 1.8 s.</p>
<div class="card stage">{light}</div>
<div class="card dark stage">{dark}</div>
<div class="card stage">{mark}</div>
<button id="replay">Replay</button>
</main>
<script>
const stages=[...document.querySelectorAll('.stage')];
function play(){{stages.forEach(s=>{{s.classList.remove('play');void s.offsetWidth;s.classList.add('play')}})}}
document.getElementById('replay').addEventListener('click',play); play();
</script></body></html>'''
open(os.path.join(OUT, "more-power-switch-on.html"), "w").write(html); print("ok")
