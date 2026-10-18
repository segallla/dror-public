#!/usr/bin/env bash
# Rebuilds every MORE POWER file from the Inter Display font.
# Needs: python3, pip install fonttools skia-pathops uharfbuzz cairosvg, and Inter Display installed
# (the scripts read it from /usr/share/fonts/opentype/inter/; change FONT_DIR in source/make8.py if needed).
set -euo pipefail
cd "$(dirname "$0")"
SKILL=../../.claude/skills/logo-design/scripts
python3 source/build_logos.py logo
python3 source/favicon.py logo
for f in more-power-wordmark more-power-mark more-power-shared-o; do
  python3 "$SKILL/export_variants.py" "logo/$f.svg" --out-dir variants --title "MORE POWER" --only black white mono --mono "#0B1E3A"
done
python3 "$SKILL/export_variants.py" logo/more-power-mark.svg --out-dir web --name more-power --title "MORE POWER" \
  --favicon-source logo/more-power-mark-small.svg --icon-bg "#FFFFFF" --icon-fg keep --icon-scale 0.78 --only square app-icon --web-icons
tmp=$(mktemp -d)
python3 "$SKILL/export_variants.py" logo/more-power-mark.svg --out-dir "$tmp" --name more-power --title "MORE POWER" \
  --favicon-source logo/more-power-favicon-source.svg --only favicon --web-icons
cp "$tmp"/favicon.ico "$tmp"/favicon.svg "$tmp"/favicon-16.png "$tmp"/favicon-32.png "$tmp"/favicon-48.png "$tmp"/more-power-favicon.svg web/
python3 source/animation.py animation
python3 source/guidelines.py .
echo "done"
