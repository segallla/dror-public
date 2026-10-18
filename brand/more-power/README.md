# MORE POWER — logo kit

Each O in the name is a power switch: MORE is navy with a blue switch, POWER is blue with a navy switch.
The mark puts the same two Os back to back, overlapping like a transformer.

Open `guidelines/more-power-guidelines.html` first: it covers versions, clear space, minimum sizes, colours,
typography and misuse.

| Folder | Contents |
|---|---|
| `logo/` | Master SVGs: wordmark, mark, mark small cut, shared-O lockup, favicon source (plus `-reversed` for dark backgrounds) |
| `variants/` | Black, white and one-colour navy versions |
| `png/` | High-resolution transparent PNGs |
| `web/` | `favicon.ico`, PNG icons, `site.webmanifest`, `head-snippet.html` |
| `animation/` | Switch-on animation (HTML, 1.8 s, respects reduced motion) |
| `presentation/` | Presentation board (`more-power-presentation.html`) and slide PNGs |
| `boards/` | Overview boards from the design rounds |
| `guidelines/` | One-page usage guidelines |
| `source/` | Scripts that rebuild every file from the font |

## Colours

| Name | HEX | Use |
|---|---|---|
| Navy | `#0B1E3A` | MORE, text, dark backgrounds |
| Deep blue | `#0096DB` | POWER and switches on light backgrounds |
| Electric blue | `#00B0FF` | POWER and switches on dark backgrounds |
| Off-white | `#F8FAFC` | Reversed artwork |

CMYK and Pantone matches are in the guidelines; confirm them on a printed swatch book before the first print run.

## Rebuilding

`./build.sh` regenerates every file. It needs Python 3 with `fonttools skia-pathops uharfbuzz cairosvg` and
Inter Display (SIL Open Font License) installed; the font path is `FONT_DIR` in `source/make8.py`.

The trademark has not been searched. Run a professional search before registering or printing at scale.
