#!/usr/bin/env bash
# Rebuilds every MORE POWER file from the Inter Display font.
# Needs: python3 with fonttools skia-pathops uharfbuzz cairosvg reportlab, and Inter Display 4.000 installed
# (the scripts read it from /usr/share/fonts/opentype/inter/; change FONT_DIR in source/make8.py if needed).
# Optional: node with Playwright, for the guidelines PDF and the slide PNGs (set PLAYWRIGHT=/path/to/playwright).
set -euo pipefail
cd "$(dirname "$0")"
# The logo-design skill's scripts; override with LOGO_SKILL=/path/to/logo-design/scripts
SKILL=${LOGO_SKILL:-../../.claude/skills/logo-design/scripts}

# masters
python3 source/build_logos.py logo
python3 source/stacked.py logo
python3 source/favicon.py logo

# one-colour SVG variants
for f in more-power-wordmark more-power-stacked more-power-mark more-power-shared-o; do
  python3 "$SKILL/export_variants.py" "logo/$f.svg" --out-dir variants --title "MORE POWER" --only black white mono --mono "#0B1E3A"
done

# web icons (favicons from the single O, larger icons from the mark's small cut)
python3 "$SKILL/export_variants.py" logo/more-power-mark.svg --out-dir web --name more-power --title "MORE POWER" \
  --favicon-source logo/more-power-mark-small.svg --icon-bg "#FFFFFF" --icon-fg keep --icon-scale 0.78 --only square app-icon --web-icons
tmp=$(mktemp -d)
python3 "$SKILL/export_variants.py" logo/more-power-mark.svg --out-dir "$tmp" --name more-power --title "MORE POWER" \
  --favicon-source logo/more-power-favicon-source.svg --only favicon --web-icons
cp "$tmp"/favicon.ico "$tmp"/favicon.svg "$tmp"/favicon-16.png "$tmp"/favicon-32.png "$tmp"/favicon-48.png "$tmp"/more-power-favicon.svg web/

# screen PNGs at their true aspect ratio
for spec in more-power-wordmark:2400 more-power-wordmark-reversed:2400 more-power-stacked:1600 more-power-stacked-reversed:1600 \
            more-power-mark:1200 more-power-mark-reversed:1200 more-power-shared-o:1200 more-power-shared-o-reversed:1200; do
  n=${spec%%:*}; w=${spec##*:}
  h=$(python3 -c "import re;v=[float(x) for x in re.search(r'viewBox=\"([^\"]+)\"',open('logo/$n.svg').read()).group(1).split()];print(round($w*v[3]/v[2]))")
  python3 "$SKILL/render_png.py" "logo/$n.svg" -o "png/$n-$w.png" --width "$w" --height "$h"
done

# print, production artwork, app icons
python3 source/print_files.py .
python3 source/production.py .
python3 source/app_icons.py .

# animation, board, guidelines, presentation
python3 source/animation.py animation
python3 source/board.py .
python3 source/guidelines.py .
python3 "$SKILL/presentation_board.py" presentation/spec.json -o presentation/more-power-presentation.html
if [ -n "${PLAYWRIGHT:-}" ]; then node source/render_docs.js "$PLAYWRIGHT" ${CHROMIUM:-}; fi
echo "done"
