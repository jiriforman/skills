# Gotchas — read this before writing any slide

Every item below cost a rebuild cycle. They are not hypothetical.

## Layout

**1. Flex containers shred inline text.** A `display:flex` block turns *each element child* into
its own flex item. `<div class="mb">text <b>bold</b> more text</div>` with `.mb{display:flex}`
renders the bold in a separate column. Fix: wrap the content in a single `<span>`, or don't make
the text block a flex container.

```html
<!-- BROKEN: <b> becomes a sibling flex item -->
<div class="mb">AI models operate as <b>probabilistic engines</b> that predict…</div>
<!-- FIXED -->
<div class="mb"><span>AI models operate as <b>probabilistic engines</b> that predict…</span></div>
```
`<br>`-separated text inside a flex item is usually fine (it stays one anonymous item); an
*element* child is not.

**2. `margin-top:auto` pins a block to the floor.** Often what you want is a deliberate lift —
`margin-top:44px` — so the block sits closer to the content above with whitespace below. Use
`margin-top:auto; margin-bottom:auto` to centre a block in leftover space.

**3. Fixed chrome vs. in-stage furniture can't be reliably separated.** The chrome is positioned
against the viewport; `.slide-no` and the logo are positioned inside the scaled stage. At some
scales they overlap. Keep the chrome band short and at the very top (`top:9px`, ~30px tall) and
it clears `.eyebrow` at every scale.

**4. Give `<video>` an explicit `aspect-ratio: 16/9`.** Before metadata loads the element has no
intrinsic size and collapses to 300×150, so `height:100%;width:auto` produces a wrong box on
first paint.

**5. Leave clearance for native video controls.** The control bar sits at the bottom of the
element; anything else fixed near the bottom of the viewport becomes unclickable. Bump
`padding-bottom` on that slide until they don't overlap.

## CSS animation

**6. `growW` / `growH` must animate `opacity` too.** `.anim { opacity:0 }` is the base state; a
keyframe set that only touches `transform` leaves opacity at 0 and the element never appears.
Symptom: an accent rule or bar chart is simply invisible.

## Build pipeline

**7. Assert every string replacement.** A `str.replace()` that matches nothing fails silently and
you ship a deck missing the change. Wrap each one:
```python
assert old in html, 'anchor missing: ' + old[:40]
html = html.replace(old, new, 1)
```

**8. Substitute longest tokens first.** `IMG_T81` is a prefix of `IMG_T810`, so replacing the
short one first leaves a stray `0` and the long token never resolves. Sort by length descending.

**9. No CDN inside the sandbox, and often none on the presenting machine either.** Chart.js and
friends will not load. Draw charts as **inline SVG** from the data. Compute the geometry in the
build step and emit `<rect>` / `<polyline>` / `<text>`.

**10. Avoid emoji on slides.** They render as empty boxes wherever no emoji font is installed
(common on Linux PDF-export boxes), and CETIN's guidance calls for line icons. Keep emoji in the
master `.md` if you like; strip them from the HTML.

## Assets

**11. Crop the CETIN logo to its alpha bounding box.** The canonical PNGs ship at ~5477×1653 with
huge transparent padding; embedded raw the visible mark renders tiny. See `scripts/prep_logo.py`.
If the deliverable must not carry "MEMBER OF PPF GROUP", crop above the claim — the script finds
the blank row band and splits there.

**12. Reference big video, embed everything else.** A 50 MB mp4 becomes ~70 MB of base64 and a
sluggish file. Keep it as a sibling file and say so in the handover; base64 the images so the
HTML stays portable.

**13. Flatten transparent PNGs onto white** if they might sit on a coloured surface (QR codes
especially — a transparent QR on a dark panel will not scan).

## Bundling multiple chapters into one file

**18. A `.divider{…}` rule must compound when scoped, not descend.** `divider` sits on the *same*
`<section class="slide divider">` element as `slide`, not on a child of it. Scope it as `.c8
.divider` (descendant) and it silently matches nothing once merged — the divider quietly loses its
CETIN-Blue background and white title in the bundled file while looking correct in every
standalone chapter file, which is exactly the case that hides it until someone opens the shared
file. `bundle_deck.py` detects every class sharing a slide's own `class="slide …"` attribute
(`cssmerge.slide_root_classes`) and compounds rules for any of them — not just `.slide` itself.
`scripts/selftest.py` has a fixture and an assertion for exactly this case; if you touch
`cssmerge.py`, rerun it.

**19. A blank YouTube iframe is worse than no video.** The moment the presenting room has no
network or the venue blocks video sites, a bare `<iframe src="youtube.com/...">` renders as a
blank white box mid-slide. Ship a local poster frame with a play badge instead, and only create the
iframe on click (`bundle_deck.py`'s `video_substitutions`, `.ytbox` in `bundle.css`). The slide
still shows something useful — a real frame plus a visible link — even offline.

**20. A non-greedy `.*?</div>` stops at the first NESTED close, not the wrapper's own close.**
Inserting "after the media wrapper" with `re.sub(r'<div class="videowrap[^>]*>.*?</div>', …)`
lands the insertion *inside* the wrapper the moment the wrapper contains another `<div>` (a poster
box, a caption), because the pattern is satisfied by the first `</div>` it meets. The inserted link
then lays out as a flex sibling of the video instead of sitting beneath it. Use a balanced-tag
scan (`after_div()` in `bundle_deck.py`) that counts open/close `<div>` tags to find the wrapper's
*matching* close.

## Reusing an existing PowerPoint

**14. Don't trust `python-pptx` group-child coordinates.** Children of a `GROUP` shape are in the
group's internal coordinate space, so a child can report a width larger than its parent. Either
resolve `chOff`/`chExt` yourself, or — far simpler — render the slide with LibreOffice and crop
the region you want. `scripts/crop_pptx.py` does the render-and-crop.

**15. Rebuild tables as HTML, crop only the artwork.** Table text belongs in real markup so it
stays editable, searchable and on-brand. Screenshots of diagrams and app-logo landscapes are
worth reusing 1:1.

## Verification

**16. `scrollHeight` checks alone are not enough.** Grid and absolute panels can visually cover
each other while every element reports no overflow. Take screenshots and look at them.

**17. Check the phone viewport.** The stage must stay exactly 16:9 (1.7778) at 390×844. If it
doesn't, something is reflowing that shouldn't be.

## Multi-file decks

**21. Every chapter's "Contents" button is a hardcoded `href="index.html"`.** Build a chapter
without also (re)building the index alongside it — a forgotten step, not a deliberate one — and
that button 404s or opens a stale page the moment someone clicks it, while every other check
(slide count, overflow, images) still passes, because none of them look at that one link. Use
`scripts/build_all.py` for every real build: it builds each chapter and the index together, so
there is no path through it that produces one without the other, and it derives each chapter's
slide list on the contents page straight from the HTML it just built rather than from a
hand-typed copy that can drift. `verify_deck.py` also clicks the Contents button for real and
checks it lands somewhere, as a backstop for anyone who still built a chapter on its own.

## Cross-browser

**22. `backdrop-filter` needs the `-webkit-` prefix for Safari.** Ship both declarations
side by side (unprefixed first, so a browser that supports both uses the standard one):
```css
.home-btn { -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px); }
```
Everything else in this skill (`transform`, `clip-path`, `aspect-ratio`, `mix-blend-mode`, and the
DOM APIs the engine uses) is broadly supported without a prefix. Automated verification here only
runs on Chromium — there's no Firefox or Safari engine installed in this environment — so
cross-browser correctness rests on sticking to this standard subset, not on an automated multi-
browser test run. Check manually on Safari before a high-stakes share if one is available.
