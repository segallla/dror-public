# MORE POWER — logo kit 1.0

Two words. Two power switches. One connected system.

Each O in the name becomes a power switch: MORE is navy with a blue switch, POWER is blue with a navy switch.
In the standalone mark the two switches are coupled like circuits and meet in one shared core.

Start with `docs/more-power-guidelines.pdf` (or `guidelines/more-power-guidelines.html`): logo hierarchy,
colour mapping for light and dark backgrounds, clear space, minimum sizes, typography, motion and misuse.

## Logo hierarchy

| # | Version | Use |
|---|---|---|
| 1 | Primary | Default everywhere |
| 2 | Primary reversed | Dark backgrounds |
| 3 | Stacked | Square and vertical formats, entrance signs |
| 4 | Mark | App icon, avatar, patterns — never with the name inside |
| 5 | Expressive shared-O | Campaigns, covers, posters, animation only |
| 6 | Single O | Favicon, 16–23 px |

## Folders

| Folder | Contents |
|---|---|
| `logo/` | SVG masters (plus `-reversed` for dark backgrounds) |
| `variants/` | Black, white and one-colour navy SVGs |
| `png/` | High-resolution transparent PNGs |
| `print/cmyk/` · `print/spot/` | CMYK and Pantone spot-colour vector PDFs |
| `print/one-colour/` · `print/eps/` | Black and Pantone 289 C PDFs; CMYK EPS |
| `print/production/` | Simplified one-colour artwork for embroidery, engraving and cutting |
| `web/` | Favicons, PNG icons, `site.webmanifest`, `head-snippet.html` |
| `app-icons/` | iOS, Android (adaptive and legacy), Play Store, social avatars |
| `animation/` | Switch-on animation: CSS only, plays once and holds, honours reduced motion |
| `presentation/` | Presentation board and slide PNGs |
| `boards/` | Overview boards from the design rounds |
| `guidelines/` · `docs/` | Guidelines (HTML and PDF), release notes, font and licence information |
| `source/` · `build.sh` | Scripts that rebuild every file from the font |

## Colours

| Name | HEX | CMYK | Pantone |
|---|---|---|---|
| Navy | `#0B1E3A` | C100 M78 Y30 K55 | 289 C |
| Deep blue | `#0096DB` | C85 M25 Y0 K0 | 2925 C |
| Electric blue | `#00B0FF` | C70 M10 Y0 K0 | 2995 C |
| Off-white | `#F8FAFC` | paper white / white ink | — |

On dark backgrounds every navy element reverses to off-white and every blue element becomes electric blue.
CMYK and Pantone values are close matches; confirm them on a printed swatch book before the first print run.
The print PDFs are not certified PDF/X-4; the printer should convert them for their press profile.

## Rebuilding

`./build.sh` regenerates every file. It uses the logo-design skill's scripts (`.claude/skills/logo-design`,
or set `LOGO_SKILL=/path/to/logo-design/scripts`), Python 3 with `fonttools skia-pathops uharfbuzz cairosvg
reportlab`, and Inter Display 4.000 (see `docs/font-and-licence.md`). Set `PLAYWRIGHT=/path/to/playwright` to
also render the guidelines PDF and slide PNGs.

**The trademark has not been searched.** Run a professional search before registering or printing at scale.
