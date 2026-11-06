// Wraps the built dark page as an Artifact body: no document skeleton, theme follows the viewer.
import { readFileSync, writeFileSync } from "node:fs";
const html = readFileSync(new URL("./landlord-lease.html", import.meta.url), "utf8");
const style = html.match(/<style>([\s\S]*?)<\/style>/)[1];
const main = html.match(/<main class="iso-page">([\s\S]*?)<\/main>/)[1];
let script = html.match(/<script type="module">([\s\S]*)<\/script>/)[1];
script = script.replace(/^try\{const b=document\.body;[\s\S]*?\}catch\(e\)\{\}/, "");
const themeJs = `
const shell = document.getElementById("shell");
const media = matchMedia("(prefers-color-scheme: dark)");
const pick = () => { const forced = document.documentElement.dataset.theme; shell.dataset.theme = forced === "light" || forced === "dark" ? forced : (media.matches ? "dark" : "light"); };
pick(); media.addEventListener("change", pick);
new MutationObserver(pick).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
`;
const page = `<title>Landlord Battery Lease</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* One framed figure, centred in a single column. */
:root{--page:#f2f2ef;--ink:#57575a}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--page:#0b0b0b;--ink:#a3a3a3;color-scheme:dark}}
:root[data-theme="dark"]{--page:#0b0b0b;--ink:#a3a3a3;color-scheme:dark}
body{background:var(--page);color:var(--ink);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0}
${style.replace(/html\{color-scheme:dark\}/, "").replace(/body\[data-theme="light"\]\{color-scheme:light\}/, "").replace(/body\{margin:0;background:var\(--anatomy-page\);/, "#shell{background:var(--anatomy-page);")}
#shell{display:flow-root}
.iso-page{width:min(720px,100%);margin:48px auto 72px}
</style>
<div id="shell" class="iso" data-theme="dark"><main class="iso-page">${main}</main></div>
<script type="module">${themeJs}${script}</script>
`;
writeFileSync(new URL("./landlord-lease.artifact.html", import.meta.url), page);
console.log("wrote landlord-lease.artifact.html", page.length);
