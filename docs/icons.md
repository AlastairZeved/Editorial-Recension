# Icon inventory

One icon family for the whole package: **agents, schemata, verdicts, loop steps, and the structural marks** the documentation uses to build its running hierarchy.

Each icon is a standalone SVG file in this directory, embedded in the README with `<img>` (see [Why files, not inline SVG](#why-files-not-inline-svg)).

---

## The family rules

| Rule | Value |
|---|---|
| Canvas | 48 × 48 grid, `viewBox="0 0 48 48"` |
| Stroke width | `2.4` for marks, `1.6`–`2.0` for secondary rules, `1.4` for the plate hairline |
| Caps and joins | `round` on every stroke |
| Plate | `rect` at `3.2, 3.2, 41.6 × 41.6`, `rx="6"`, fill `#1d2026`, stroke `#3a4150` |
| Hue | one semantic hue per mark (table below); never decorative |
| Filled accents | at most one per mark, and only where it carries meaning (the inserted step, the weld point, the closed state) |

The plate is not a new invention: it is the video's own node treatment — raised slate `#1d2026`, hairline `#3a4150`, radius 6–8, the same plate that holds `EDITOR` and `EVALUATOR` in the title scene and the loop scene. Putting every mark inside that plate is what makes the family read as one system at any size, from 22 px in a README heading up to a full-width diagram.

---

## Agents

| Icon | File | Hue | Meaning |
|---|---|---|---|
| <img src="icon-editor.svg" width="24" height="24" alt=""> | `icon-editor.svg` | ember `#d96c3f` | **Editor** — the agent that rewrites text through the five schemata, in phases. Three rules of text, one of them still to be rewritten (gold). |
| <img src="icon-evaluator.svg" width="24" height="24" alt=""> | `icon-evaluator.svg` | verdict green `#2e9e6b` | **Evaluator** — the examiner that scores the text against measurable features *before* reading the editor's trace: a lens over the feature lines. |

## The five schemata

| Icon | File | Hue | Meaning |
|---|---|---|---|
| <img src="icon-barrier-bridge.svg" width="24" height="24" alt=""> | `icon-barrier-bridge.svg` | ember | **Barrier Bridge** — Phase 1. Two dots (the reader's knowledge, the author's assumption) joined by a bridge that carries grounding, not a definition. |
| <img src="icon-chain-repair.svg" width="24" height="24" alt=""> | `icon-chain-repair.svg` | ember, hollow gold node | **Chain Repair** — Phase 1. A chain of steps; the hollow middle node is the step that was asserted but never derived, now rebuilt. |
| <img src="icon-compression-pass.svg" width="24" height="24" alt=""> | `icon-compression-pass.svg` | gold `#e8b84b` | **Compression Pass** — Phase 2. Three rules shortening in turn: words removed until the next removal would change meaning or feeling. |
| <img src="icon-flow-weld.svg" width="24" height="24" alt=""> | `icon-flow-weld.svg` | ember, gold weld point | **Flow Weld** — Phase 3. Two segments re-joined at the edit point; the gold dot is the weld. |
| <img src="icon-ripple-read.svg" width="24" height="24" alt=""> | `icon-ripple-read.svg` | verdict green | **Ripple Read** — Phase 4. Arcs radiating from the document point it reads from: the whole, across five ledgers. |

## Verdicts

| Icon | File | Hue | Meaning |
|---|---|---|---|
| <img src="icon-pass.svg" width="24" height="24" alt=""> | `icon-pass.svg` | verdict green `#2e9e6b` | **PASS** — every feature meets its target, no trace discrepancies, termination condition confirmed on an independent clean read. |
| <img src="icon-fail.svg" width="24" height="24" alt=""> | `icon-fail.svg` | fail red `#c4453a` | **FAIL** — one or more features below target or a trace discrepancy found. Named, located, not softened; feedback returns to the phase that owns it. |
| <img src="icon-needs-revision.svg" width="24" height="24" alt=""> | `icon-needs-revision.svg` | gold | **Needs Revision** — the FAIL state as the editor actually receives it (located feedback, re-enter at the failing phase), and the best-effort output after five cycles, where the remaining failures are named and left open rather than papered over. |

## Loop steps

| Icon | File | Hue | Meaning |
|---|---|---|---|
| <img src="icon-intake.svg" width="24" height="24" alt=""> | `icon-intake.svg` | gold | **Intake** — the three-question questionnaire (target reader, purpose, source text) and the hard validation before anything is dispatched. |
| <img src="icon-dispatch.svg" width="24" height="24" alt=""> | `icon-dispatch.svg` | ember | **Dispatch** — the confirmed editorial context goes to the editor with the schemata library. |
| <img src="icon-verify.svg" width="24" height="24" alt=""> | `icon-verify.svg` | verdict green | **Verify** — the evaluator scores every feature independently, then compares its scoring to the trace. |
| <img src="icon-loop.svg" width="24" height="24" alt=""> | `icon-loop.svg` | ember | **Loop** — on FAIL the output returns to the editor; each cycle converges. |
| <img src="icon-terminate.svg" width="24" height="24" alt=""> | `icon-terminate.svg` | verdict green | **Terminate** — the termination condition confirmed; the closed inner square is the loop at rest. |

## Structural marks

Used for the running hierarchy and the design notes, not for agent behavior.

| Icon | File | Hue | Meaning |
|---|---|---|---|
| <img src="icon-ledger.svg" width="24" height="24" alt=""> | `icon-ledger.svg` | dim `#7d8798` | **Ledger** — the running record: Ripple Read's five ledgers (flow, coherence, rhythm, arc, audience) and the evaluator's feature ledger. |
| <img src="icon-standard.svg" width="24" height="24" alt=""> | `icon-standard.svg` | gold | **Standard** — the Agent Plugins 1.0.0 package and the gold chip the video uses for it. |
| <img src="icon-trace.svg" width="24" height="24" alt=""> | `icon-trace.svg` | jargon blue `#5b8dd6` | **Trace** — the editor's schema trace, and the cold, ungrounded signal generally: the blue the film uses for terms that are not yet grounded. |
| <img src="icon-grain.svg" width="24" height="24" alt=""> | `icon-grain.svg` | dim | **Grain** — the ink-grain ground texture, marked in the design notes. |

---

## Why files, not inline SVG

GitHub's README sanitizer strips `<style>`, `class`, `id`, inline `style` attributes, and `<video>`; inline SVG is unreliable for anything beyond trivial shapes. A file referenced with `<img src="…">` from the repository is served and rendered as a real image, so every mark above arrives intact, scales, and needs no runtime dependency.

The SVGs carry their text as outlines (Source Serif 4 and Inter, converted with `fontTools`), so no icon or plate depends on a font being installed on the reader's machine.

Zero emoji: this family is the only pictographic layer in the repository's documentation.