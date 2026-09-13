# Design notes — how this documentation is built

The documentation for this repository is not a fresh design. It is the world of the **showcase film** (`v6`, 2:21), applied to the repository's own text. That film is the authoritative reference for every token below; where this document and your instinct disagree, the film wins.

The film's cold→warm arc is the system, not decoration: the docs open on the cold slate ground that holds the closed paragraph, and they finish on the warm paper that holds the paragraph after the loop.

---

## 1. Palette

Taken verbatim from the film's composition source (`DESIGN.md`, `compositions/s1..s10.html`).

| Token | Hex | Role in the film | Role here |
|---|---|---|---|
| `--slate` | `#16181d` | cold open surface | the documentation's ground |
| `--slate-2` | `#1d2026` | raised slate plates | every plate, card, icon body |
| `--cold-line` | `#3a4150` | hairlines, diagram rails | plate borders, wires, rules |
| `--row-rule` | `#2a2f3a` | table row rules | hairline between table rows |
| `--cold-text` | `#aab3c5` | secondary slate text | supporting prose |
| `--muted` | `#8f99ab` | tertiary text | captions, labels |
| `--dim` | `#7d8798` | eyebrows, kickers | letterspaced eyebrow labels |
| `--faint` | `#5f6a7d` | footnotes | provenance lines |
| `--head` | `#e9edf4` | the name, large | headline text |
| `--body` | `#c9d0dc` | the paragraph on slate | body text, figure text |
| `--jargon` | `#5b8dd6` | ungrounded terms on slate | insertions, the trace, not-yet-grounded signal |
| `--ember` | `#d96c3f` | the editor's warmth | the editor, edits, the turn |
| `--ember-warm` | `#b4551f` | ember on paper | ember inside the warm world |
| `--verdict` | `#2e9e6b` | evaluator PASS | the evaluator, PASS |
| `--seal` | `#1f8a5b` | the PASS seal rule | the seal |
| `--fail` | `#c4453a` | FAIL, struck terms | deletions, FAIL |
| `--fail-light` | `#e0685d` | failing feature scores | failing scores |
| `--gold` | `#e8b84b` | Agent Plugins standard accents | the standard, phase 2, Needs Revision |
| `--paper` | `#f4efe4` | warm paper | the finale ground |
| `--ink` | `#23201a` | ink on warm paper | text on paper |
| `--warm-label` | `#6b6353` | warm eyebrow | warm-world eyebrow |

**Color law, inherited:** the slate world carries blue-grays, jargon blue, and fail red. The warm world carries paper, ink, ember, and verdict green. Jargon blue never appears on warm paper; ember never appears on cold slate except at the transition beat. When a figure crosses worlds, it crosses on purpose.

---

## 2. Grounds are not flat

Two textures, both reproduced from the film rather than approximated.

### Ink grain — every dark section

A single `feTurbulence` noise field, the film's exact recipe:

```svg
<filter id="grain">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/>
  <feColorMatrix type="saturate" values="0"/>
</filter>
```

It is tiled at **240 × 240** (the film's own tile), the noise rect drawn at `opacity="0.5"` inside the tile, and the tiled field laid over the ground at a **layer opacity of `0.06` on slate** and **`0.075` on paper**. Below about 0.04 the grain is invisible once an image is scaled down; above about 0.12 it stops being texture and becomes visible dirt.

### Vignette — every section

The film's own overlay, unchanged:

```svg
<radialGradient id="vig" cx="50%" cy="50%" r="75%">
  <stop offset="58%"  stop-color="#000" stop-opacity="0"/>
  <stop offset="100%" stop-color="#000" stop-opacity="0.38"/>
</radialGradient>
```

Nothing darkens until 58% of the radius, then falls to 38% black at the edge. The same overlay is what makes the warm finale read as *lit paper* rather than beige: measured off the finished film, the paper's centre is `#f2eee3` and its corners are `#9c9990` — which is `#f4efe4` under exactly this vignette. Reproducing the film's finale meant reproducing its vignette, not picking a "parchment" colour.

### The finale section (warm world)

`docs/media/finale-plate.svg` is the film's light scene rebuilt in SVG: paper ground, grain at 0.075, vignette at 0.38, ink serif text, ember italic for the bridged clause, and the PASS seal as a 4 px rule rotated −2°, exactly as the closing card draws it.

### Section bands

`docs/media/band-slate.svg` and `docs/media/band-parchment.svg` are full-width 96 px grounds carrying the same grain and vignette with a hairline and a single centre node. They are used **between movements** of the document — the slate band between cold sections, the parchment band before the finale block — so that section boundaries are spatial events rather than empty gaps. Each band belongs to the world it separates: slate-on-slate, paper-on-dark.

---

## 3. Typography

The film's stack, and only that stack:

| Face | Role |
|---|---|
| **Source Serif 4** | the prose itself, both worlds — and the display lines |
| **Inter** | the analytical voice: UI labels, eyebrows, diagram labels, tables, scores |

Courier Prime was in an earlier cut and was dropped before the film shipped; no monospace register appears in these docs for display purposes.

All text inside the SVG plates and icons is **converted to outlines** (`fontTools` `SVGPathPen`), so no asset depends on a font being installed where it is read. Inside GitHub-rendered markdown, body text uses GitHub's own stack — the plates carry the design, the prose carries the content.

---

## 4. Revision marks

The repository's subject is tracked corrections, so its documents show them.

- **Deletion** — text dimmed to `#7d8798` with a 2 px strike in fail red `#c4453a`, drawn at 30% of the type size above the baseline (the film's ratio).
- **Insertion** — jargon blue `#5b8dd6`, italic for bridged prose, with a 1 px underline at 55% opacity.
- Both appear together in `docs/media/diff-plate.svg`, which is the real test paragraph with real marks on it.

Where the same marks must live in markdown rather than in a plate, the fallback is `<del>` and `<ins>` — GitHub renders both natively (strike and underline, uncolored). The colour lives in the plate; the semantics live in the markup.

---

## 5. Structure rules the documentation holds to

1. **The running hierarchy is icon-marked.** Every section carries its number and its structural mark, so a reader landing mid-page knows where they are within five seconds.
2. **The verdict legend is near the top**, before any argument: PASS, FAIL, Needs Revision, with the icon and the meaning.
3. **No prose block runs past six lines** without a structural break — a table, a callout, a plate, a diagram, or an icon-led list.
4. **Specific shapes are mandatory, not optional:** the Editor↔Evaluator loop is a **cycle diagram** (`loop-cycle.svg`), the five schemata are a **table**, the issue ledger is an **actual table**, and the diff example carries **real strike and insert rendering**.
5. **Nothing is described that is not shipped.** Every texture, gradient, filter, and mark named above exists as a file in `docs/media/` or `docs/icons/`.
6. **Static assets only.** No runtime dependency, no build step, no script — SVG, CSS-as-SVG-attributes, and WebP.

---

## 6. The figures, and where they come from

| File | Shows | Extracted from the film at |
|---|---|---|
| `hero-poster.webp` | title, subtitle, the two agent cards, the standard chip | the title scene, 0:45 |
| `exhibit-diff.webp` | the cold paragraph, ungrounded terms lit | the exhibit scene, 0:21 |
| `diff-marks.webp` | struck words in the compression pass beside the weld | phase 2 + 3, 1:14 |
| `issue-ledger.webp` | feature scores, target vs found, FAIL | the evaluator's ledger, 1:48 |
| `loop.webp` | the editor↔evaluator cycle and the five-cycle counter | the loop scene, 2:00 |
| `parchment-finale.webp` | the transformed paragraph on warm paper | the turn, 2:07 |
| `pass-verdict.webp` | PASS seal, warm-ink title, standard chip | the closing card, 2:17 |
| `cold-to-warm.webp` | 7.4 s of the film's defining motion: slate → paper | the turn, 2:02.9 |

## 7. Where the film is hosted, and why it is two places

The MP4 is not committed to the repository — it is an output of the design system, not source, and a 125 MB file is not recoverable once it is in git history. `.gitignore` keeps it out of the index.

It is published twice, because GitHub serves the two routes differently:

| Route | How GitHub serves it | What a click does |
|---|---|---|
| **Release asset** (`v6-showcase`) | `Content-Type: application/octet-stream`, `Content-Disposition: attachment` | **downloads.** This is the archival copy of the master (119 MiB). |
| **User attachment** (issue #12) | `Content-Type: video/mp4`, `Accept-Ranges: bytes`, 206 partial content | **streams and plays.** This is what the README player uses. |

GitHub's README sanitizer strips `<video>` when its source is repository-relative or third-party — but **keeps it when the source is a GitHub user-attachment**. That single fact decides the architecture: the README embeds a real player, streaming the attachment, and points anyone who wants a local copy at the release.

The uploaded file is a **web encode**, not the master, because the attachment CDN caps video at 100 MB:

| | |
|---|---|
| Encoding | H.264 High, 1920×1080, CRF 17, preset slow, `-g 60`, `+faststart`, audio **passed through unre-encoded** |
| Size | 80.0 MiB (master: 119.4 MiB) |
| Fidelity | mean SSIM **0.99596** against the master, min 0.98915, over all 4,250 frames |

The audio is a stream copy, so the approved mix is bit-for-bit the same in both files. GitHub adds `muted` to embedded players, which is why the README says so plainly rather than pretending the film starts with sound.