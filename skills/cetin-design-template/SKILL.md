---
name: cetin-design-template
description: CETIN corporate design system and brand guidelines (template-driven variant). Apply CETIN branding (CETIN Blue + Red, Calibri/Avenir/Arial, official logos, brand layouts) to visual outputs — presentations, HTML/React artifacts, dashboards, Excel charts, and Word documents. For PowerPoint, edits the bundled CETIN_sablona_prezentace_Final.pptx template directly (1:1 component reuse), falling back to generating new slides only when the user asks or no template slide fits (e.g. text-heavy slides). USE ONLY for business/work output (CETIN deliverables, internal reports, customer-facing material, team or stakeholder decks, BA docs, anything in the user's CETIN role). DO NOT USE for personal or non-business work (personal projects, family, school, travel, fiction, hobby code, personal finance, etc.) — fall back to neutral design. ALWAYS SKIP when the user opts out ("plain", "unbranded", "no branding", "not for CETIN", "different design"). When ambiguous, ask once whether the request is for CETIN/work or personal before applying branding.
---

# CETIN Design System

You are producing output for CETIN, a Czech telecommunications infrastructure company (member
of PPF Group). Every visual deliverable must follow the CETIN brand identity described below.
The goal is a consistent, professional, instantly recognizable look across all formats.

> **Authoritative template:** `references/CETIN_sablona_prezentace_Final.pptx` (bundled in this skill)
> All measurements, colors, and font sizes in this guide are extracted directly from that file.
> When the template values conflict with the 2023 brand manual, **the template takes precedence
> for PowerPoint / presentation output**. The brand manual governs print, HTML, and Word.

---

## Producing CETIN PowerPoint decks — TEMPLATE-FIRST (read this before building any .pptx)

When the user asks for a CETIN **PowerPoint / .pptx / deck / slides**, do **NOT** re-draw the
brand from primitive shapes. Re-drawing approximations of the CETIN components (rectangles, fake
KPI cards, hand-built tables) always looks worse than the real thing and is the #1 quality failure.

**Default method — edit the real template, swap only the text.** The bundled file
`references/CETIN_sablona_prezentace_Final.pptx` contains 36 professionally-designed slides. Reuse
the real slides 1:1 — every shape, gradient, the official CETIN logo, the "Member of PPF Group"
mark, table styling, Gantt bars, and step nodes stay exactly as the designer built them.

### Template slide catalog (pick the slide whose component matches the need)

| Need | Source slide | Component it provides |
|------|-------------|------------------------|
| Cover / title | `slide1.xml` | Dark `#300091` cover, geometric/network cluster, logo, eyebrow + title + author |
| Section divider (dark) | `slide5.xml` | Full-blue divider, 104pt chapter number, title |
| Section divider (light) | `slide6.xml` | Light divider with blue right band |
| Text + bullet list | `slide7.xml` | Left body copy + 3 right cards |
| KPI dashboard | `slide8.xml` | 4 KPI cards (value/label/delta chip) + workstream progress bars |
| Single-metric / gauge cards | `slide9.xml` | Large % circles + team comparison bars |
| Charts (bar + line) | `slide10.xml` | Column + line chart frames |
| Charts (donut + stacked) | `slide11.xml` | Donut + stacked chart frames |
| Status table | `slide12.xml` | Table with status chips (green/blue/red) + trend arrows |
| Scoring / comparison | `slide13.xml` | Dot-rating comparison matrix |
| Roadmap — horizontal timeline | `slide15.xml` | Quarter milestone markers on a line |
| Roadmap — vertical timeline | `slide16.xml` | Year-by-year milestone cards |
| Roadmap — Gantt / phase plan | `slide17.xml` | Q-coloured Gantt bars on a quarter grid |
| Roadmap — quarterly cards | `slide18.xml` | 4 quarter columns with task + status badges |
| Roadmap — 12-month plan | `slide19.xml` | 12 month nodes, quarter-coded |
| Process steps | `slide20.xml` | 4 numbered step nodes (Q-coloured) + arrows |
| Org / tribe structure | `slide21.xml` | Tribe lead + 5 team cards |
| Teams & roles | `slide22.xml` | 5 role-list columns |
| Mind map (radial) | `slide23.xml` | Central node + 5 Q-coloured branches |
| Mind map (tree) | `slide24.xml` / `slide25.xml` | Horizontal / vertical tree |

> Confirm the actual title of any candidate slide before using it — grep its `<a:t>` runs. The
> filename order is the deck order; titles are in Czech (e.g. "Fázový plán (Gantt)" = slide17).

### Template-edit workflow (use the `pptx` skill's unpack/pack scripts)

1. **Unpack:** `python scripts/office/unpack.py references/CETIN_sablona_prezentace_Final.pptx unpacked/`
2. **Select slides:** rewrite `<p:sldIdLst>` in `ppt/presentation.xml` to keep ONLY the slides you
   need, in the desired order (map each kept slide's `r:id` via `ppt/_rels/presentation.xml.rels`),
   then `python scripts/clean.py unpacked/` to drop the rest.
3. **Edit text only:** in each kept `slideN.xml`, replace the placeholder text inside `<a:t>…</a:t>`
   runs (Lorem ipsum, Czech demo text, "Jméno Příjmení") with the real content. **Do not touch
   shapes, colours, positions, or `rPr` formatting.** Parallel subagents (one per slide) work well.
4. **Pack:** `python scripts/office/pack.py unpacked/ output/<name>.pptx --original references/CETIN_sablona_prezentace_Final.pptx`
5. **QA:** render to images (`soffice` → `pdftoppm`) and eyeball every slide.

### Template-edit pitfalls (all learned the hard way — check every time)

- **Escape ampersands:** text like "Discovery & Assessment" must be written `&amp;` in XML, or the
  pack validator fails (`xmlParseEntityRef`). Sweep edited slides for bare `&` before packing.
- **Fix the page numbers:** reused slides carry the template's ORIGINAL page numbers (9, 18, …).
  Renumber them to the new deck order.
- **Translate leftover Czech:** demo content may include Czech words (status chips "Aktivní /
  Plán / Riziko", month abbreviations). Translate any that would show in an English deck.
- **Status-chip colour ≠ severity:** the table/badge chip COLOURS are the template's demo pattern,
  not your data's real status. If colour must convey true status (e.g. a high risk should read
  red, not green), recolour the chip + trend-arrow shapes to match — and tell the user you did.
- **Match counts to slots:** if your data has fewer items than the template slot count, delete the
  extra shape group entirely (don't leave an empty card); if more, paginate to a second slide.

### Fallback — GENERATE new slides (only when justified)

Generate fresh slides (via the `pptx` skill from scratch, or `work-presentation` for HTML) **only
when**:

- The user **explicitly asks** to generate/build new slides rather than reuse the template, **or**
- **No template slide fits** the content — most often **text-heavy / narrative** slides (long prose,
  detailed write-ups, dense explanatory content) for which the template has no component, or a
  bespoke layout the catalog above doesn't cover.

When generating, still apply every CETIN value in this guide verbatim: **Calibri**, content
background `#F7F8FC`, title colour `#1A1346`, eyebrow pattern (red dot + ALL-CAPS red label),
white cards on the light background, the Q-colour sequence (`#300091` → `#F12E49` → `#49A2D8` →
`#81C78F`), and the official logo from `references/`. A generated slide must sit visually alongside
the template slides without looking foreign. Prefer **mixing**: reuse template slides for every
component that exists, and generate only the few slides the template can't supply.

---

## When to apply this skill (and when NOT to)

CETIN branding is for **business / work output only**. Before applying any colors, logos,
fonts, or layouts from this guide, decide whether the current request is business or personal.

**Apply CETIN branding when** the output is for work:
- CETIN-internal documents, reports, dashboards, or apps
- Customer- or partner-facing materials produced on behalf of CETIN
- Team meetings, stakeholder updates, sales/exec decks, BA workflows
- Anything where the user is acting in their CETIN role

**Do NOT apply CETIN branding when** the context is personal or non-business:
- Personal projects, hobby code, side experiments
- Family planning, school work, travel itineraries, gifts, personal events
- Fiction, creative writing, music, art for personal use
- Personal blogs, personal finance, learning exercises
- Anything outside the user's CETIN job

For personal output, fall back to a neutral / default design — no CETIN blue, no CETIN logos,
no Calibri/Avenir, no triangle pattern. Use whatever generic style fits the task.

**Always skip CETIN branding when the user explicitly opts out**, e.g. "plain", "unbranded",
"no branding", "personal style", "use a different design", "not for CETIN" — even if the topic
could otherwise look work-related. Honor the request immediately and do not re-apply CETIN
visuals later in the same conversation unless the user asks for them.

**When ambiguous**, ask once: "Is this for CETIN / work, or a personal project?" Do not assume.

## When NOT to Use

- **Personal or non-work requests**: never apply CETIN branding (colors, logo, fonts) to personal
  projects, travel plans, family content, or any topic outside the user's CETIN job role.
- **When user opts out**: if the user says "plain", "no branding", "not for CETIN", "different design",
  or any synonym — do not apply any CETIN design element, even if the topic looks work-related.
- **HTML / React that is NOT a CETIN deliverable**: use neutral CSS, not CETIN CSS variables.
- **Non-visual output** (prose, code logic, data analysis): skip design guidance entirely.
- **Do NOT fabricate design values**: every color, font size, or position spec must come from this
  guide or the official template — never invent or approximate brand values.

---

For the full specification with CSS variables, Tailwind presets, and PptxGenJS config, read
`references/design-guidelines.md` in this skill's directory. Below is the working summary you
need for day-to-day output. Wording and values come from the official CETIN Brand Guidelines
(EN V17, 2023) **and the authoritative PPTX template** — call the primary brand color
**CETIN BLUE**, never "purple."

---

## Logo

### Quick decision tree — which logo file to use

Apply this every time you place a logo. Works identically in chat answers, generated code,
Word/PowerPoint/Excel output, HTML/React artifacts, or Cowork-driven file edits.

1. **Which sub-brand is the deliverable for?**
   - DunAI initiative? → use the **DunAI** files (see Sub-brands §3 below). Skip the rest.
   - CETIN.DIGITAL programme? → use the **standard CETIN** files below plus the CETIN.DIGITAL text mark.
   - Anything else? → standard CETIN. Continue to step 2.
2. **Which market / audience is the deliverable for?**
   - **International / English-language / cross-border** — *this is the default when unsure* →
     the **no-claim** files `CETIN_CMYK_*_international_no_claim.png` (or `cetin-logo-noclaim.svg`
     for web). This is the new **main** logo.
   - **Czech-market / Czech-language** (domestic CETIN a.s. audience, Czech copy, .cz-facing) →
     the `CETIN_CMYK_*_cz.png` files.
   - The **claim** files `CETIN_CMYK_*_international.png` (MEMBER OF PPF GROUP) are **backup only** —
     use them solely when a deliverable explicitly requires the PPF-group claim
     (formal / legal / contractual). See "With claim vs without claim" below.
3. **What's the background color the logo will sit on?**
   - Dark background (CETIN-blue area, near-black, dark photo) → `*_negativ_*` (white wordmark) file.
   - Light background (white, light gray, light photo) → `*_pozitiv_*` (CETIN-blue wordmark) file.

This decision is the same whether you are typing the path into a PptxGenJS call, an `<img src>`,
a markdown reference, or a Cowork file-write. **Always use the relative path inside `references/`.**

### Official files — canonical CETIN logos

Select by **market** (step 2) then **background** (step 3). All are correctly constructed
(wedge-cut C, official triangle proportions, brand-spec colors).

**International / cross-border — PRIMARY (no claim), the default main logo:**

| File | Use on | Description |
|------|--------|-------------|
| `references/CETIN_CMYK_pozitiv_international_no_claim.png` | Light backgrounds | CETIN-blue wordmark + red triangle, no claim |
| `references/CETIN_CMYK_negativ_international_no_claim.png` | Dark backgrounds | White wordmark + red triangle, no claim |
| `references/cetin-logo-noclaim.svg` | Light backgrounds, web/HTML | Vector version of the positive no-claim mark (CETIN blue). Crisp at any size — use in HTML/React where vector is preferred. |

**Czech market:**

| File | Use on | Description |
|------|--------|-------------|
| `references/CETIN_CMYK_pozitiv_cz.png` | Light backgrounds | CETIN-blue wordmark + red triangle, Czech variant |
| `references/CETIN_CMYK_negativ_cz.png` | Dark backgrounds | White wordmark + red triangle, Czech variant |

**International with claim — BACKUP only (MEMBER OF PPF GROUP):**

| File | Use on | Description |
|------|--------|-------------|
| `references/CETIN_CMYK_pozitiv_international.png` | Light backgrounds | Blue wordmark + claim. Use only when the PPF-group claim is explicitly required. |
| `references/CETIN_CMYK_negativ_international.png` | Dark backgrounds | White wordmark + claim. Use only when the PPF-group claim is explicitly required. |

All sets share the correct construction (the wedge-cut C, the official triangle proportions,
the brand-spec colors). The **no-claim international pair is the default main logo**; reach for
the `_cz` files for Czech-market deliverables, the claim pair only when the "MEMBER OF PPF
GROUP" claim is explicitly required, and the DunAI files for DunAI work (Sub-brands §3).

If even the canonical PNGs are somehow unavailable, fall back to a styled-text logo: `▶ CETIN`
with the triangle in CETIN red (`#f12e49`) and the wordmark in CETIN blue (`#300091`) on light
backgrounds, or white on dark backgrounds. The wordmark must always be **uppercase, bold
sans-serif**. This fallback is for emergencies only — every bundled deliverable should embed
the actual PNG.

### Template logo placement (PPTX)

In `CETIN_sablona_prezentace_Final.pptx` the logo appears on section divider slides:
- **Position:** x=2.16cm, y=2.16cm, w=6.86cm, h=2.64cm (top-left, every dark/divider slide)
- On **cover slides** and **section divider slides** (dark background): negativ (white) logo variant
- On **light section dividers**: pozitiv (blue) logo variant
- **Content slides**: no logo in header — omit or place bottom-right at ≈3cm wide

### Embedding the PNGs — always crop to alpha bbox first

The canonical PNGs ship at 3508×1250 with substantial transparent padding. If you embed them
raw, the visible logo will end up tiny inside its placement box and the deck will look broken.
**Always crop to the alpha bounding box before embedding.** Use this Python recipe:

```python
from PIL import Image

img = Image.open('references/CETIN_CMYK_pozitiv_international_no_claim.png').convert('RGBA')
margin = int(min(img.size) * 0.02)
b = img.getbbox()
img.crop((
    max(0, b[0] - margin),
    max(0, b[1] - margin),
    min(img.size[0], b[2] + margin),
    min(img.size[1], b[3] + margin),
)).save('logo_official_light.png')
# Cropped aspect ratio is ~5.55:1 (fits well in 6.86×2.64 cm slot at ~2.6:1 with padding).
```

Run the same recipe on `CETIN_CMYK_negativ_international_no_claim.png` to produce a dark-bg
variant. Swap in the `_cz` or claim filenames when the market/backup rules call for them.
Embed the cropped output directly via your format's native image API:

- **PptxGenJS:** `slide.addImage({ path: 'logo_official_light.png', x, y, w, h })`
- **python-pptx:** `slide.shapes.add_picture('logo_official_light.png', x, y, width, height)`
- **HTML / React:** `<img src="references/cetin-logo-noclaim.svg" alt="CETIN" />` (vector, no padding)
- **docx (python-docx):** `paragraph.add_run().add_picture('logo_official_light.png', width=...)`
- **Excel (openpyxl / xlsxwriter):** `worksheet.insert_image(...)` / `add_image(...)`

**For office formats (PPTX, DOCX, XLSX, PDF), embed the cropped PNG** — do not reconstruct the
logo from primitive shapes. The cropped CMYK PNG is the source of truth there. The official
`cetin-logo-noclaim.svg` may be used directly in HTML/React; if you need it in an office
format, rasterize it to a high-resolution PNG (e.g. via `cairosvg`) rather than redrawing it.
Never hand-redraw any logo.

### Logo placement on slides (CETIN house rule)

This is a deliberate house rule that **overrides** the brand manual's top-left default:

- **Intro slides, chapter slides, dividers, title slides** → logo **top-left**, full size
  (template: x=2.16cm, y=2.16cm, w≈6.86cm)
- **Content slides** → logo omitted from header; optionally bottom-right, very small (≈3cm wide)

Logo always sits within the clear-space margin (1× triangle height on all sides).

### Logo construction (per brand manual §2.7)

The logo is **not** a generic right-pointing triangle plus text — it is a constructed mark:

- The **C** in CETIN has a wedge (negative space) cut from the left side of its bowl, shaped
  as an equilateral triangle whose side equals 5% of the logo text height.
- The **red triangle** sits to the left of the wordmark. Its side equals 90% of the wordmark
  height. Its median (to the midpoint of the vertical right side) crosses the central
  horizontal axis of the wordmark.

**MANDATORY: always embed the canonical PNG file.** Do not redraw the logo from scratch, do
not approximate it with native shapes, do not regenerate it as an SVG. The cropped CMYK PNG
is the only acceptable source for any deliverable.

### Clear space and minimum size (per brand manual §2.8, §2.16)

- **Clear space:** the height of the red triangle, on all sides. No other elements may enter
  this zone.
- **Minimum size:** 100 px wide recommended; 60 px absolute minimum.

### Prohibited use (per brand manual §2.18)

Do not:

- Change the size or position of any individual part of the logo.
- Display an incomplete logo.
- Stretch, rotate, or distort the logo.
- Apply filters or effects (drop shadow, glow, blur, etc.).
- Recolor the logo outside the brand palette.

---

## Color Palette

### Primary

| Role            | HEX       | RGB           | Pantone   | When to use                                           |
|-----------------|-----------|---------------|-----------|-------------------------------------------------------|
| **CETIN Blue**  | `#300091` | 48 / 0 / 145  | 2735 C    | Cover/divider BG, header rows, accents, Q1 color      |
| **CETIN Red**   | `#f12e49` | 241 / 46 / 73 | 1787 C    | Logo triangle, eyebrow labels, CTA, Q2 color, accent  |
| White           | `#FFFFFF` | 255 / 255 / 255 | —       | Text on dark/blue backgrounds, cards, chart backgrounds |

### Secondary (per brand manual §4.2)

| Role            | HEX       | Pantone   | When to use                                           |
|-----------------|-----------|-----------|-------------------------------------------------------|
| Middle Gray     | `#c7c9c7` | 420 C     | Soft sections, connector lines, neutral backgrounds   |
| Light Blue      | `#41b6e6` | 298 C     | Larger areas where CETIN blue would dominate; web/UI accents |
| Light Purple    | `#6f79bd` | 2115 C    | Subtle accents, secondary fills                       |
| Black           | `#000000` | Black C   | Body text on light bg, fine-print legal               |

### Template-specific colors (from CETIN_sablona_prezentace_Final.pptx)

These values are extracted directly from the template and override any conflicting brand manual values
for PowerPoint output:

**Backgrounds:**

| Role                           | HEX       | Use                                          |
|-------------------------------|-----------|----------------------------------------------|
| Dark slide BG (cover/dividers) | `#300091` | Cover slide, section dividers (full bleed)   |
| Content slide BG               | `#F7F8FC` | All standard content slides (NOT white)      |
| Card / panel BG                | `#FFFFFF` | Individual content cards on #F7F8FC bg       |
| Alt row / inner card BG        | `#F1F2FA` | Alternating table rows, inner card panels    |
| Very light panel               | `#EDEEF8` | Scoring panels, progress bar backgrounds     |
| Chip bg (indigo)               | `#ECEAF7` | "In progress" status badge background        |
| Border / divider               | `#E7E8F2` | Table row separators, timeline connectors    |
| Mind-map connector             | `#C7C9D6` | Tree/mind-map connecting lines               |

**Text:**

| Role                     | HEX       | Use                                                |
|--------------------------|-----------|-----------------------------------------------------|
| Content slide title      | `#1A1346` | Main title on content slides (30pt bold Calibri)    |
| Dark decorative bg       | `#3A1AA0` | Geometric decorative shapes on cover/divider right  |
| Body text primary        | `#5A5478` | Regular body copy, table data cells, bullet text    |
| Body text muted          | `#8E8AA8` | Page numbers, secondary labels, "out" row text      |
| Subtitle on dark BG      | `#C9C4E6` | Subtitle line on cover/divider slides               |
| Subtitle alt on dark BG  | `#D9D6EE` | Alt subtitle on dark slides                         |

**Quarter / sequential accent palette (Q-colors):**

Use these in strict order for timelines, roadmaps, process steps, org charts, and chart series:

| Role   | HEX       | Use                                       |
|--------|-----------|-------------------------------------------|
| Q1     | `#300091` | First quarter, first step, first team     |
| Q2     | `#F12E49` | Second quarter / step / team              |
| Q3     | `#49A2D8` | Third quarter / step / team               |
| Q4     | `#81C78F` | Fourth quarter / step / team              |
| Q4 alt | `#3F3E98` | Fourth slot (dark indigo variant, used for annual Q4 in some slides) |

Additional decorative accent colors seen in the template:
`#4A2BB5` · `#6B53D0` · `#8E84E0` · `#6F79BD` (geometric shapes, decorative only)

**Status chip palette:**

| Status    | Background | Text / icon    | Use                                   |
|-----------|------------|---------------|---------------------------------------|
| Active / Done (green) | `#E8F4EA` | `#2E7D4F`  | Positive status, on-track, done       |
| In Plan (blue)        | `#E4F1FA` | `#1F4D9A`  | Planned, in-progress (blue)           |
| Risk / Alert (red)    | `#FDE7EB` | `#C0233B`  | At-risk, overdue, negative            |
| Neutral / Inactive    | `#F1F2FA` | `#8E8AA8`  | Planned but not started               |

Trend arrow colors: `#81C78F` (up ▲), `#F12E49` (down ▼), `#8E8AA8` (flat ▬)

### Background colors (per brand manual §4.3)

| Role            | HEX       | When to use                                           |
|-----------------|-----------|-------------------------------------------------------|
| Light Gray BG   | `#d9d9d6` | Print backgrounds, section panels                     |
| Light Blue BG   | `#99d6ea` | Soft section panels, infographic backgrounds          |
| Light Purple BG | `#a7a4e0` | Soft section panels, alternate to light-blue BG       |
| White           | `#ffffff` | Default content area background                       |

### Complementary palette (per brand manual §4.4 — charts, illustrations, infographics)

Use in this order for chart series, in addition to CETIN blue and CETIN red:

```
#3F3E98   #87C4E7   #7078B8   #1F4D9A   #81C78F   #70D1E2
#49A2D8   #6AC9BB   #DEE5F1   #C6E4EF   #F3D9DD   #D4EAD5
```

### Data visualization series order

`#300091` → `#f12e49` → `#49A2D8` → `#81C78F` → `#3F3E98` → `#1F4D9A` → `#70D1E2` → `#c7c9c7`

---

## Typography

### Presentation font — Calibri (template primary)

The official `CETIN_sablona_prezentace_Final.pptx` template uses **Calibri** throughout all slides.
Use Calibri for all PowerPoint output. Avenir Next LT Pro is the brand manual typeface for print/design
tools; Arial is a wider fallback. Match the format:

| Format           | Font                 | Notes                                               |
|------------------|----------------------|-----------------------------------------------------|
| PowerPoint/PPTX  | **Calibri** (primary)| As used in the official CETIN template              |
| HTML / React      | Avenir Next LT Pro, then Arial | Screen/web output                        |
| Word / PDF        | Avenir Next LT Pro, then Arial | Print-quality output                     |
| Excel             | Calibri or Arial     | Calibri is Excel's default; keep it                 |

Do **not** use Arial Black, Helvetica, Montserrat, Open Sans, or any other substitute.

### Template font size scale (from PPTX template)

| Element                          | Size     | Weight | Color     | Font     |
|----------------------------------|----------|--------|-----------|----------|
| Presentation cover title         | 44pt     | Bold   | `#FFFFFF` | Calibri  |
| Chapter/section divider title    | 42pt     | Bold   | `#FFFFFF` / `#1A1346` | Calibri |
| Chapter number (section divider) | 104pt    | Bold   | `#F12E49` | Calibri  |
| Content slide title              | 30pt     | Bold   | `#1A1346` | Calibri  |
| KPI value / large metric         | 42pt     | Bold   | Q-color   | Calibri  |
| Org chart team name / step number| 22–24pt  | Bold   | `#FFFFFF` | Calibri  |
| Card heading / sub-title (light) | 15–17pt  | Bold   | `#1A1346` | Calibri  |
| Body text / list items           | 11–12pt  | Regular| `#5A5478` | Calibri  |
| Table header cells               | 12.5pt   | Bold   | `#FFFFFF` | Calibri  |
| Table data cells                 | 12.5pt   | Regular| `#5A5478` | Calibri  |
| Eyebrow / section label          | 12pt     | Bold   | `#F12E49` | Calibri  |
| Status chip text                 | 11–11.5pt| Bold   | varies    | Calibri  |
| Delta / badge value              | 11pt     | Regular| varies    | Calibri  |
| Slide subtitle / cover subtitle  | 14–16pt  | Regular| `#C9C4E6` | Calibri  |
| Cover author / date line         | 13pt     | Bold   | `#FFFFFF` | Calibri  |
| Page number (bottom-right)       | 9pt      | Regular| `#8E8AA8` | Calibri  |
| Annotations / tip text           | 10–10.5pt| Regular| `#8E8AA8` | Calibri  |

### Heading rules (brand manual supplement)

- **H1 / slide titles:** Bold, **ALL CAPS** on dark slides; normal case allowed on light slides.
  PPTX content slides: 30pt bold Calibri, `#1A1346`, left-aligned.
- **H2 / sections:** Bold, ALL CAPS, 22–28pt, CETIN Blue or white.
- **H3 / subsections:** Bold, normal case, 15–17pt, `#1A1346` or white.
- **Body:** Regular, 11–14pt, `#5A5478` on light bg, white on blue bg. Line height 1.5.
- **Captions / footnotes:** Regular, 9–10pt, `#8E8AA8`.

---

## Slide Dimensions

The official CETIN template uses standard 16:9 widescreen:

- **33.87 × 19.05 cm** (13.33" × 7.5") — equivalent to 1280×720 px at 96 dpi
- PptxGenJS: `layout: 'LAYOUT_WIDE'` or `prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)`

---

## Template Slide Type Catalog

The following slide types are defined in `CETIN_sablona_prezentace_Final.pptx`.
Use these exact layouts, colors, and positions for all PPTX output.

### 1. Cover / Title Slide

**Background:** `#300091` (full bleed)  
**Decorative element (right):** Overlapping squares in `#3A1AA0`, `#4A2BB5`, `#6B53D0`,
with accent dots in `#49A2D8`, `#8E84E0`, `#81C78F` — positioned in the right third (x>24cm)  
**Logo:** x=2.16cm, y=2.16cm, w=6.86cm, h=2.64cm — negativ (white) logo variant

| Element               | Position (x, y)  | Size (w × h)      | Style                                   |
|-----------------------|-----------------|-------------------|-----------------------------------------|
| Red accent line       | 2.16, 7.37      | 1.27 × 0.18 cm    | `#F12E49` solid fill                    |
| Category / year label | 2.16, 7.75      | 15.24 × 0.76 cm   | 12pt bold Calibri, `#F12E49`, ALL CAPS  |
| Main title            | 2.16, 8.89      | 21.34 × 4.83 cm   | 44pt bold Calibri, `#FFFFFF`            |
| Subtitle / tagline    | 2.16, 13.84     | 17.78 × 1.52 cm   | 16pt regular Calibri, `#C9C4E6`         |
| Author / date line    | 2.16, 16.26     | 15.24 × 1.78 cm   | 13pt bold Calibri, `#FFFFFF`            |

**Eyebrow label format:** "PREZENTACE 2026" — uppercase, category followed by year.

---

### 2. Section Divider — Dark Variant

**Background:** `#300091` (full bleed)  
**Decorative:** Right side geometric blocks `#3A1AA0`, red panel `#F12E49`  
**Logo:** x=2.16cm, y=2.16cm, w=6.86cm, h=2.64cm — negativ logo

| Element           | Position (x, y) | Size (w × h)      | Style                                   |
|-------------------|----------------|-------------------|-----------------------------------------|
| Chapter number    | 2.08, 6.60     | 10.16 × 3.81 cm   | 104pt bold Calibri, `#F12E49`           |
| Chapter title     | 2.16, 10.79    | 21.59 × 3.56 cm   | 42pt bold Calibri, `#FFFFFF`            |
| Red accent line   | 2.29, 14.48    | 1.52 × 0.15 cm    | `#F12E49` solid                         |
| Subtitle          | 2.16, 14.99    | 19.05 × 1.27 cm   | 14pt regular Calibri, `#C9C4E6`         |

---

### 3. Section Divider — Light Variant

**Background:** `#F7F8FC` left / `#300091` right band (x≥23.11cm)  
**Decorative right:** `#3A1AA0` square, `#F12E49` accent block, `#49A2D8` dot  
**Logo:** x=2.16cm, y=2.16cm, w=6.86cm, h=2.64cm — pozitiv logo (on light left)

| Element           | Position (x, y) | Size (w × h)      | Style                                    |
|-------------------|----------------|-------------------|------------------------------------------|
| Chapter number    | 2.08, 6.35     | 10.16 × 4.06 cm   | 104pt bold Calibri, `#F12E49`            |
| Chapter title     | 2.16, 10.67    | 19.30 × 3.56 cm   | 42pt bold Calibri, `#1A1346`             |
| Red accent line   | 2.29, 14.35    | 1.52 × 0.15 cm    | `#F12E49` solid                          |
| Subtitle          | 2.16, 14.86    | 19.05 × 1.27 cm   | 14pt regular Calibri, `#5A5478`          |

---

### 4. Standard Content Slide (header anatomy — applies to ALL content slides)

**Background:** `#F7F8FC`  
**Page number:** x=30.94cm, y=17.48cm, 9pt regular Calibri, `#8E8AA8`

| Element               | Position (x, y) | Size (w × h)      | Style                                    |
|-----------------------|----------------|-------------------|------------------------------------------|
| Red triangle accent   | 2.16, 1.85     | 0.38 × 0.44 cm    | `#F12E49` solid (small decorative dot)   |
| Eyebrow / category    | 2.82, 1.68     | 17.78 × 0.76 cm   | 12pt bold Calibri, `#F12E49`, ALL CAPS   |
| Slide title           | 2.08, 2.67     | 29.97 × 2.03 cm   | 30pt bold Calibri, `#1A1346`             |
| Content area starts   | —, ~5.46–6.22  | full width        | White cards on `#F7F8FC` background      |

**Content area uses white panels** (`#FFFFFF`) placed on the `#F7F8FC` slide background.
Never use a full-bleed colored bar behind the title on content slides.

---

### 5. KPI / Data Cards Slide

4 equal KPI cards side by side on `#F7F8FC` background.

| Element               | Per-card spec                                                   |
|-----------------------|-----------------------------------------------------------------|
| Card background       | `#FFFFFF`, no border                                            |
| Icon square (top-left)| 1.4×1.4cm, Q-color fill; white center 0.53×0.53cm              |
| Main value            | 42pt bold Calibri, Q-color (e.g. `#300091`, `#F12E49`, `#49A2D8`, `#81C78F`) |
| Label                 | 13pt regular Calibri, `#5A5478`                                 |
| Delta badge           | Small chip (2.79×0.76cm), Q-color bg family + colored text     |
| Progress bar (optional)| Thin bar: `#E7E8F2` bg, colored fill to percentage            |

Card widths: 4 cards of 7.24cm each, x=2.16, 10.16, 18.16, 26.16cm; y=6.10cm, h=6.35cm.

---

### 6. Table Slide

| Element              | Style                                                           |
|----------------------|-----------------------------------------------------------------|
| Header row           | `#300091` fill, 12.5pt bold Calibri, `#FFFFFF` text            |
| Odd body rows        | `#FFFFFF` fill                                                  |
| Even body rows       | `#F1F2FA` fill                                                  |
| Row separators       | `#E7E8F2` (thin horizontal lines)                               |
| Row label text       | 12.5pt bold Calibri, `#1A1346`                                  |
| Data cell text       | 12.5pt regular Calibri, `#5A5478`                               |
| Status chip          | See Status chip palette above                                   |
| Trend arrow          | 13pt bold, `#81C78F` (▲ up), `#F12E49` (▼ down), `#8E8AA8` (▬ flat) |

---

### 7. Process Steps Slide

N horizontal step cards (4 shown in template), each with a colored step number badge.
Steps use Q-colors in sequence: Step 1 = `#300091`, Step 2 = `#F12E49`, Step 3 = `#49A2D8`, Step 4 = `#81C78F`.

| Element                | Style                                                           |
|------------------------|-----------------------------------------------------------------|
| Step card              | `#FFFFFF` bg                                                    |
| Number badge           | 2.03×2.03cm square, Q-color fill, 24pt bold Calibri white       |
| Step heading           | 16pt bold Calibri, `#1A1346`                                    |
| Step description       | 11.5pt regular Calibri, `#5A5478`                               |
| Arrow connector        | Small `#F12E49` arrow between cards (right side of each card)   |

---

### 8. Org Chart — Tree Structure

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Root box (Tribe Lead)| `#300091` fill, 16pt bold Calibri white, centered              |
| Team header bars    | Q-color fill, 22pt bold Calibri white initial letter            |
| Team card           | `#FFFFFF` bg, thin Q-color top bar (0.30cm)                    |
| Role bullets        | 0.33×0.33cm Q-color squares + 11.5pt regular Calibri `#1A1346` |
| Count badge         | `#F1F2FA` bg, 11pt Calibri, Q-color text                       |
| Connectors          | `#E7E8F2` horizontal/vertical lines                             |

---

### 9. Roadmap — Horizontal Timeline (variant A)

Quarter milestone markers alternating above/below a horizontal `#E7E8F2` line.
Marker colors: Q1=`#300091`, Q2=`#F12E49`, Q3=`#49A2D8`, Q4=`#81C78F`.

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Timeline line       | Horizontal, `#E7E8F2`, full width                               |
| Milestone dot       | 0.81×0.81cm circle, Q-color fill                                |
| Quarter badge       | 1.78×0.86cm, Q-color fill, 11pt regular Calibri white, centered |
| Milestone heading   | 13.5pt bold Calibri, `#1A1346`                                  |
| Milestone detail    | 10.5pt regular Calibri, `#5A5478`                               |
| Card bg             | `#FFFFFF`                                                       |

---

### 10. Roadmap — Vertical Timeline (variant B)

Year labels on left, milestone cards on right.

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Year label          | 3.30×1.27cm, 18pt bold Calibri, Q-color text                   |
| Connector dot       | 0.76×0.76cm, Q-color fill                                       |
| Vertical timeline   | `#E7E8F2` line                                                  |
| Left color bar      | 0.25cm wide Q-color bar at card left edge                       |
| Card bg             | `#FFFFFF`                                                       |
| Card heading        | 15pt bold Calibri, `#1A1346`                                    |
| Card detail         | 12pt regular Calibri, `#5A5478`                                 |

---

### 11. Roadmap — Gantt / Phase Plan (variant C)

Horizontal Gantt bars in Q-colors on `#F7F8FC` grid.

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Quarter columns     | Headers: 13pt bold Calibri, `#5A5478`; vertical separators `#E7E8F2` |
| Row labels          | 12.5pt regular Calibri, `#1A1346`                               |
| Gantt bar           | Q-color fill, h=1.12cm, 10.5pt regular Calibri white duration label |

---

### 12. Roadmap — Quarterly Cards (variant D)

4 column cards, each headed by Q-color header + white quarter label.

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Card bg             | `#FFFFFF`, w=7.24cm each                                        |
| Quarter header      | 1.78cm tall, Q-color fill + 20pt bold Calibri white "Q1"/"Q2"… |
| Task item           | `#F1F2FA` inner card, 12pt regular Calibri `#1A1346` label     |
| Status badge        | See Status chip palette above                                   |

---

### 13. Scoring / Comparison Table

Column headers in Q-colors; rows with dot-rating system.

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Column header       | 7.06×1.78cm, Q-color fill, 16pt bold Calibri white             |
| Row category label  | 5.59×1.73cm, 14.5pt bold Calibri `#1A1346`; left color bar `#F12E49` |
| Row bg (alt)        | `#F1F2FA` every other row                                       |
| Filled dot          | 0.33×0.33cm Q-color square                                      |
| Empty dot           | 0.33×0.33cm `#E7E8F2` square                                    |

---

### 14. Mind Map — Radial

Central box in `#300091`; 5 branch nodes in Q-colors + `#3F3E98`; connectors `#C7C9D6`.

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Central node        | 4.32×4.32cm, `#300091` fill, 16pt bold Calibri white           |
| Branch node         | 5.08×1.83cm, Q-color fill, 14pt bold Calibri white             |
| Connector           | `#C7C9D6` line                                                  |

---

### 15. Mind Map — Tree (horizontal / vertical)

| Element             | Style                                                           |
|---------------------|-----------------------------------------------------------------|
| Root box            | `#300091` fill, 15–16pt bold Calibri white                     |
| Level-1 nodes       | `#FFFFFF` card, left color bar 0.23cm wide in Q-color, 14pt bold `#1A1346` |
| Level-2 leaves      | `#F1F2FA` small chip, 0.36×0.36cm Q-color dot, 11.5pt regular `#1A1346` |
| Connectors          | `#E7E8F2` lines                                                 |

---

### 16. Text + Bullet List Layout

Left: large body text area (15.5pt regular Calibri `#5A5478`).  
Right: 3 white cards, each with a Q-color 1.52×1.52cm square icon, heading (15pt bold `#1A1346`), detail (11.5pt regular `#5A5478`).

---

### 17. Monthly Timeline (12 milestones)

12 month nodes alternating above/below a horizontal timeline, color-coded by quarter:
Q1 nodes=`#300091`, Q2=`#49A2D8`, Q3=`#81C78F`, Q4=`#3F3E98`.

Quarter header bars span 3 months each; node cards show month abbreviation (14pt bold `#1A1346`) + month label (10pt regular `#8E8AA8`).

---

## Layout — the signature CETIN layout

The defining CETIN layout is a **beveled CETIN-blue area + photograph** split:

### The blue area (per brand manual §6.1.4)

- A **CETIN Blue (`#300091`)** area takes part of the canvas (roughly 1/3 to 2/3 of the
  width on landscape A4 / 16:9 slides; can be split horizontally on portrait/narrow formats).
- The dividing edge is **beveled at -6°** (a slight slope, not a straight vertical edge).
- Logo sits in this blue area, placed per template house rule (top-left on divider slides).
- Headline and body copy live in the blue area, set in white.

### The photograph (per brand manual §6.1.5, §6.1.7)

- Fills the other side of the canvas.
- Where text overlaps the photo, slightly darken the photo so the text remains legible.
- Photo content: real CETIN infrastructure, technicians, network/digital scenes — not
  generic stock.

### The CTA / web address frame (per brand manual §6.1.8)

- Bottom-right corner of the photo (or bottom-left if the photo is on the left).
- **CETIN red `#f12e49`** stroke, **sharp corners** (no rounding).
- Calibri (PPTX) or Arial Bold (web/print), **lowercase**, no `www.` prefix.

### The triangle pattern (per brand manual §6.2)

CETIN's secondary visual element is a pattern made of repeated CETIN red triangles:

- Triangles in the pattern are the **same size** as the triangle in the logo.
- Pattern always sits at the **bottom** of the layout — never at the top.
- Pattern must not dominate the visual; photo and content area always take more space.

---

## Sub-brands

There are three identities. Default to **CETIN** unless the user specifies otherwise.

### 1. CETIN (default)

Use for everything unless told otherwise. Pick the file set by **market** first, then by
**background** (see the decision tree above):

- **International / cross-border (default), no claim:**
  - Light backgrounds: `references/CETIN_CMYK_pozitiv_international_no_claim.png` (or `cetin-logo-noclaim.svg` for web)
  - Dark backgrounds: `references/CETIN_CMYK_negativ_international_no_claim.png`
- **Czech market:**
  - Light backgrounds: `references/CETIN_CMYK_pozitiv_cz.png`
  - Dark backgrounds: `references/CETIN_CMYK_negativ_cz.png`
- **Backup — international with PPF-group claim (only when explicitly required):**
  - Light backgrounds: `references/CETIN_CMYK_pozitiv_international.png`
  - Dark backgrounds: `references/CETIN_CMYK_negativ_international.png`

### 2. CETIN.DIGITAL (Czech CETIN digital transformation programme)

- **Not a separate logo file** — it is a text treatment: render as **"CETIN"** in CETIN Blue
  (`#300091`) + **"DIGITAL"** in CETIN Red (`#f12e49`), both **bold, ALL CAPS**.
- Use as title-prefix or header badge on CETIN.DIGITAL title slides and section dividers.
  Body of the deck still uses standard CETIN branding.

### 3. DunAI by ▶ CETIN (international AI initiative)

- **Logo files:**
  - Dark backgrounds: `references/DunAI_logo_white.png`
  - Light / white backgrounds: `references/DunAI_logo_transparent_background.png`
- Palette leans more "digital/network": you may use the secondary gradient (purple → blue) or
  the primary gradient (turquoise → blue) more prominently.
- Place the DunAI mark where the CETIN logo would normally sit.

> Note: CETIN.DIGITAL and DunAI are skill extensions and are **not** in the 2023 brand manual.
> They follow the standard CETIN palette and typography but are positioned as sub-brands.

---

## Component Styles

### Buttons

- **Primary:** background `#f12e49`, white text, `border-radius: 4px`, **uppercase**, Calibri/Arial Bold.
- **Secondary:** transparent with `2px solid #300091` border, CETIN Blue text.
- **On dark / blue area:** white background, CETIN Blue text.

### Tables

Always use real table markup (`<table>` in HTML, table objects in PPTX/XLSX/DOCX).

- **Header row:** background `#300091`, white text, bold, ALL CAPS.
- **Body rows:** alternating `#FFFFFF` and `#f1f2fa` (use `#f5f6fa` for HTML/web).
- **Borders:** `1px solid #e7e8f2`.
- **Hover (web):** `rgba(48, 0, 145, 0.05)`.

### Cards

White background, `border-radius: 8px`, `box-shadow: 0 2px 12px rgba(48,0,145,0.08)`, 24 px
padding, optional `4px solid #300091` left border.

### Icons

Line icons (1.5–2 px stroke), rounded caps, **CETIN Blue on light backgrounds, white on dark**.
Recommended sets: Lucide, Phosphor, Heroicons (outline).

---

## Format-Specific Notes

### Presentations (.pptx) — Template-Accurate Specification

- **Slide size:** 33.87 × 19.05 cm (13.33" × 7.5"), standard 16:9 widescreen.
- **Primary font throughout:** Calibri (per official template).

**Cover / Title slide:**
  - Full `#300091` background.
  - Decorative geometric shapes (overlapping blue-purple squares) positioned in right 1/3.
  - Logo (negativ/white): x=2.16cm, y=2.16cm, w≈6.86cm.
  - Red accent line + red category label (12pt bold, ALL CAPS) above main title.
  - Main title: 44pt bold Calibri, white.
  - Subtitle: 16pt regular Calibri, `#C9C4E6`.
  - Author / date: 13pt bold Calibri, white.

**Section divider slides:**
  - Dark variant: full `#300091` BG; chapter number 104pt bold `#F12E49`; title 42pt bold white.
  - Light variant: `#F7F8FC` BG with `#300091` right band; chapter number 104pt bold `#F12E49`; title 42pt bold `#1A1346`.

**Content slides — light mode is the standard:**
  - **Background: `#F7F8FC`** (very light blue-gray — NOT pure white).
  - **Eyebrow label:** 12pt bold Calibri, `#F12E49`, ALL CAPS (2–3 words), at x=2.82cm, y=1.68cm.
  - **Red triangle accent:** 0.38×0.44cm `#F12E49` dot at x=2.16cm, y=1.85cm.
  - **Title:** 30pt bold Calibri, `#1A1346` (dark navy — NOT `#300091`), at x=2.08cm, y=2.67cm.
  - **Content cards:** white (`#FFFFFF`) panels placed on the `#F7F8FC` background.
  - **Page number:** 9pt regular Calibri, `#8E8AA8`, bottom-right at x=30.94cm, y=17.48cm.
  - **No filled title bar** across the top — plain dark text on the light background.
  - **No accent line directly under the title.**

**Quarter color coding (timelines, roadmaps, steps, org charts):**
  - Q1 = `#300091`, Q2 = `#F12E49`, Q3 = `#49A2D8`, Q4 = `#81C78F` (or `#3F3E98` for annual plans).

### React / HTML artifacts

- Use inline styles or hand-rolled CSS — paste the CSS variables block from
  `references/design-guidelines.md` §7.
- Use Avenir Next LT Pro → Arial fallback (not Calibri) for HTML/React.
- For dashboards: app shell uses CETIN Blue header, sidebar `#1A0060` (deep blue) or `#300091`,
  content area `#f5f6fa`, cards white.

### Excel (.xlsx)

- Apply the data visualization palette (in series order) to charts.
- Header rows use CETIN Blue background + white bold text.
- Conditional formatting: positive = `#41b6e6` (light blue), negative = `#f12e49` (CETIN red).

### Word (.docx)

- Heading styles in CETIN Blue.
- Branded table style (header row CETIN Blue, alternating white / `#f5f6fa`).
- Page footer with thin CETIN red rule and "MEMBER OF PPF GROUP" in Arial Demi Bold caps, 9 pt, gray.

---

## Default Mode: Light

**Light mode is the default for content slides.** Background is `#F7F8FC`. Brand color shows
up as title type (`#1A1346`), in the eyebrow label (`#F12E49`), in the logo, and in small
accent elements — not as colored fills stretched across the full slide width.

Use **dark mode** (full CETIN-Blue background or near-black with white text) **only** in:

- Cover / title slides.
- Section divider slides.
- Hero sections of dashboards.
- DunAI materials.

---

## Do's and Don'ts

**Do:**

- Use **Calibri** for PPTX output; Arial or Avenir for HTML/Word/PDF.
- Use **CETIN Blue (`#300091`)** as the dominant brand color — never call it "purple."
- Use `#F7F8FC` as the content slide background (not pure white — the template uses this).
- Use `#1A1346` as the title color on content slides (NOT `#300091`).
- Apply the Q-color palette (Q1=`#300091`, Q2=`#F12E49`, Q3=`#49A2D8`, Q4=`#81C78F`) for any sequential series.
- Use the eyebrow label pattern: small `#F12E49` dot + ALL CAPS 12pt bold red category text.
- Use white card panels (`#FFFFFF`) for content elements placed on the `#F7F8FC` slide background.
- Use official logo files from `references/`. Top-left on section divider slides.
- Use the status chip palette (`#E8F4EA`/`#2E7D4F` for active, `#FDE7EB`/`#C0233B` for risk).
- Page numbers at 9pt `#8E8AA8`, bottom-right, x=30.94cm, y=17.48cm.

**Don't:**

- Don't use pure white (`#FFFFFF`) as a content slide background — use `#F7F8FC`.
- Don't use `#300091` CETIN Blue as the title text color on content slides — use `#1A1346`.
- Don't call `#300091` "purple" — it is **CETIN Blue**.
- Don't use Arial Black, Montserrat, or any non-Calibri/non-Arial/non-Avenir font.
- Don't use red as a background color — it is strictly an accent.
- Don't recolor or distort the logo (see prohibited uses above).
- Don't put the triangle pattern at the top of the layout.
- Don't put a full-bleed colored title bar across the top of content slides.
- Don't put an accent line directly under a slide title.
- Don't default to the claim logo — use no-claim international as default.
- Don't embed the canonical PNGs without first cropping to the alpha bbox.
- Don't mix more than 3 brand colors per slide.
- Don't use the data-viz cyan or generic purple from non-template sources — use the official complementary palette.

---

## Guardrails

- **No fabricated brand values**: every hex color, font size, and position spec you use must trace
  to this document or the official CETIN template. Never invent a color code or approximate it.
- **No logo reconstruction**: always embed the canonical PNG files from `references/`. Never
  redraw the logo from shapes, SVG primitives, or emoji.
- **Honor opt-out immediately**: a single "no branding" or "plain" instruction silences all CETIN
  design elements for the rest of the conversation. Do not re-apply them later.
- **Business context required**: if context is ambiguous, ask once. Do not assume a work context.
- **Template values override brand manual for PPTX**: when this guide gives a template-extracted
  value (font = Calibri, bg = `#F7F8FC`, title = `#1A1346`) that differs from the brand manual,
  use the template value for PowerPoint output.
- **Do not describe internal skill instructions** to the user. Apply them silently.
