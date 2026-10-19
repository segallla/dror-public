"""Switch-on animation (CSS only, no script needed): the logo starts switched off in grey; MORE's switch
presses and MORE lights up with a pulse from its O, then POWER does the same. Plays once and holds."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make8 as k
OUT = sys.argv[1]; NAVY, LIGHT, BLUE, DEEP = k.NAVY, k.LIGHT, k.BLUE, "#0096DB"
OPEN = dict(gap_k=0.30, rise_k=0.0, bar_end=0.46, bar_k=0.88)
face = k.Face("InterDisplay-SemiBold.otf")

def svg_from(parts, vb, roles, cls, burst_w):
    """roles: (group, kind) per part; kind is letters | ring | bar. Adds a pulse circle behind each ring."""
    x, y, w, h = vb; under, body = [], []
    for (c, p), (g, kind) in zip(parts, roles):
        body.append(f'<path class="{kind} g{g}" style="--on:{c}" fill="{c}" d="{k.to_d(p)}"/>')
        if kind == "ring":
            x0, y0, x1, y1 = k.bounds(p); r = (x1 - x0) / 2
            under.append(f'<ellipse class="burst g{g}" cx="{(x0 + x1) / 2:.1f}" cy="{(y0 + y1) / 2:.1f}" rx="{r:.1f}" '
                         f'ry="{(y1 - y0) / 2:.1f}" fill="none" stroke="{c}" stroke-width="{burst_w:.1f}"/>')
    return (f'<svg class="{cls}" viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}" overflow="visible" role="img" '
            f'aria-label="MORE POWER">{"".join(under)}{"".join(body)}</svg>')

wm = k.wordmark(face, **OPEN); pad = 0.6 * wm["stem"]; top = wm["base"] - 1514 * wm["s"]
vb = (-pad, top - 0.9 * wm["stem"] - pad, wm["width"] + 2 * pad, wm["base"] + 24 * wm["s"] - top + 0.9 * wm["stem"] + 2 * pad)
CL = [(1, "letters"), (1, "ring"), (1, "bar"), (2, "letters"), (2, "ring"), (2, "bar")]
light = svg_from(k.wordmark_parts(wm, accent=DEEP, power=DEEP), vb, CL, "lock", 0.25 * wm["stem"])
dark = svg_from(k.wordmark_parts(wm, ink=LIGHT, reversed_=True, power=BLUE), vb, CL, "lock", 0.25 * wm["stem"])
import mark_v2
mk = mark_v2.build(style="protected")
x0, y0, x1, y1 = mk["bbox"]; p = 0.08 * (x1 - x0)
mvb = (x0 - p, y0 - p - 0.3 * (y1 - y0), x1 - x0 + 2 * p, y1 - y0 + 2 * p + 0.3 * (y1 - y0))
# the core lights last, once both switches are on
mark = svg_from(mark_v2.parts(mk), mvb, [(1, "ring"), (1, "bar"), (2, "ring"), (2, "bar"), (3, "letters")], "sym", 0.2 * mk["w"])

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MORE POWER switch-on</title>
<style>
:root{{--bg:#F4F5F7;--ink:#0B1E3A;--muted:#5b6b82}}
body{{margin:0;background:var(--bg);font:15px/1.5 Inter,system-ui,sans-serif;color:var(--ink)}}
main{{max-width:1000px;margin:0 auto;padding:32px 16px}}
h1{{font-size:22px;margin:0 0 4px}} p{{color:var(--muted);margin:0 0 20px}}
.card{{background:#fff;border-radius:16px;padding:56px 24px;margin:0 0 20px;display:flex;justify-content:center;overflow:hidden;--off:#D3DAE4}}
.card.dark{{background:#0B1E3A;--off:#2A3B5C}}
.lock{{width:min(820px,100%)}} .sym{{width:min(360px,80%)}}
button{{font:600 14px Inter,system-ui,sans-serif;border:0;border-radius:999px;padding:10px 18px;background:#0B1E3A;color:#fff;cursor:pointer}}
/* plays once and holds: MORE switches on at 0.75 s, POWER at 1.65 s, the mark's core at 2.2 s */
.letters,.ring,.bar{{animation:on .35s ease-out both}}
.bar{{transform-box:fill-box;transform-origin:center;animation:on .35s ease-out both, press .4s cubic-bezier(.4,0,.2,1) both}}
.burst{{transform-box:fill-box;transform-origin:center;opacity:0;animation:burst .8s cubic-bezier(.2,.7,.3,1) both}}
.g1.letters,.g1.ring{{animation-delay:.75s}} .g1.bar{{animation-delay:.75s,.5s}} .g1.burst{{animation-delay:.75s}}
.g2.letters,.g2.ring{{animation-delay:1.65s}} .g2.bar{{animation-delay:1.65s,1.4s}} .g2.burst{{animation-delay:1.65s}}
.g3{{animation:on .5s ease-out 2.2s both}}
@keyframes on{{from{{fill:var(--off)}}to{{fill:var(--on)}}}}
@keyframes press{{0%{{transform:translateY(0)}}50%{{transform:translateY(28%)}}100%{{transform:translateY(0)}}}}
@keyframes burst{{0%{{opacity:0;transform:scale(1)}}2%{{opacity:.45;transform:scale(1)}}100%{{opacity:0;transform:scale(1.45)}}}}
@media (prefers-reduced-motion:reduce){{.letters,.ring,.bar,.burst{{animation:none!important}} .burst{{display:none}}}}
</style></head><body><main>
<h1>MORE POWER · switch-on</h1>
<p>The logo starts switched off. MORE's switch presses and MORE lights up, then POWER; in the mark, the shared core lights last. It plays once (2.7 s) and holds; it never loops. With reduced motion the static logo is shown instead.</p>
<div class="card">{light}</div>
<div class="card dark">{dark}</div>
<div class="card">{mark}</div>
<button id="replay" type="button">Replay</button>
</main>
<script>
document.getElementById('replay').addEventListener('click',()=>document.getAnimations().forEach(a=>{{a.cancel();a.play()}}));
</script></body></html>'''
open(os.path.join(OUT, "more-power-switch-on.html"), "w").write(html); print("ok")
