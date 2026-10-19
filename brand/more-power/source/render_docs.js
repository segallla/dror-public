// Renders docs/more-power-guidelines.pdf and the presentation slide PNGs with Playwright (Chromium).
// Usage: node source/render_docs.js <path-to-playwright-module> [chromium-executable]
const path = require('path');
const { chromium } = require(process.argv[2]);
const root = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch(process.argv[3] ? { executablePath: process.argv[3] } : {});
  const p = await b.newPage({ viewport: { width: 1200, height: 900 }, colorScheme: 'light' });
  await p.goto('file://' + path.join(root, 'guidelines/more-power-guidelines.html'));
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: path.join(root, 'docs/more-power-guidelines.pdf'), format: 'A4', printBackground: true,
                margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' } });
  const s = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await s.goto('file://' + path.join(root, 'presentation/more-power-presentation.html'));
  let i = 0;
  for (const e of await s.$$('.slide')) { i++; await e.screenshot({ path: path.join(root, `presentation/slides/slide-${String(i).padStart(2, '0')}.png`) }); }
  await b.close();
})();
