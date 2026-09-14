# Subagent Dispatch — Test Scenarios

**Skill under test:** `skills/editorial-recension/SKILL.md` (Steps 5–7), `agents/editor.md`, `agents/evaluator.md`, `.claude-plugin/plugin.json` (`agents` field)
**What this file is:** Manually verifiable acceptance criteria for subagent registration and the isolated dispatch flow. Not an automated test runner — these are reference scenarios for manual verification during development and review.

---

## Section 1: Manifest Registration

**Test 1.1 — Agents registered as individual file paths**
- **Setup:** `.claude-plugin/plugin.json` contains `"agents": ["./agents/editor.md", "./agents/evaluator.md"]`.
- **Expected:** `claude plugin validate .` exits 0.
- **Why:** The agents field is an array of file paths. A directory string fails validation (verified: `"agents": "./agents"` produces `agents: Invalid input`).

**Test 1.2 — Portable manifest untouched**
- **Setup:** root `plugin.json` (Agent Plugins 1.0.0).
- **Expected:** no `agents` field; the Agent Plugins 1.0.0 schema deliberately excludes subagents in v1; unknown top-level fields are non-fatal but must not be shipped here. Schema-check the root manifest against `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`.

**Test 1.3 — Package contents**
- **Setup:** `git archive HEAD | tar -t`.
- **Expected:** `agents/editor.md` and `agents/evaluator.md` present in the distributable tree.

## Section 2: Editor Dispatch Isolation

**Test 2.1 — Payload boundaries**
- **Run:** complete the intake (Q1–Q3 valid), confirm the Step 4 block, dispatch the editor subagent.
- **Expected dispatch payload:** TARGET READER / KNOWS / DOESN'T KNOW template; PURPOSE / READER SHOULD template; source text; `PRECEDING CONTEXT` field verbatim; schemata file paths.
- **Expected absence:** no intake conversation, no user's original messages, no evaluator content in the editor's context.

**Test 2.2 — Editor return shape**
- **Expected:** edited text + schema trace + termination assessment, all three present. The dispatcher holds the full return; the schema trace does not leave dispatcher custody until evaluator Message 2.

## Section 3: Evaluator Two-Message Round

**Test 3.1 — Message 1 is blind**
- **Run:** dispatch evaluator Message 1.
- **Expected payload:** editorial context + original source text + editor's output text. Nothing else.
- **Expected absence:** no schema trace, no editor drafts, no editor reasoning anywhere in the scoring context.
- **Expected return:** complete Feature Scores report.

**Test 3.2 — Message 2 verifies without re-scoring**
- **Run:** send the schema trace to the same evaluator with the verify-without-re-scoring instruction.
- **Expected return:** one unified document — feature scores (Step 1), trace discrepancies (Step 2), failures, verdict PASS/FAIL — matching the canonical shape of `tests/evaluator-test-output.md`.

**Test 3.3 — Trace-leak protocol violation**
- **Run:** deliberately include the trace in Message 1 on a test pass.
- **Expected:** the evaluator scores on legitimately provided content and records the protocol violation at the top of its report (per evaluator.md, "How You Work").

## Section 4: Loop Mechanics

**Test 4.1 — FAIL routes to editor**
- **Setup:** evaluator verdict FAIL with located failures.
- **Expected:** the failure report goes back to the editor subagent (same instance on multi-turn hosts; re-dispatch seeded with previous output + trace + failure report on single-shot hosts); the editor re-enters at the phase where failures were identified; the next evaluator round begins with Message 1 containing the revised output.

**Test 4.2 — PASS terminates**
- **Expected:** termination condition confirmed; final edited text presented with the Output Format summary.

**Test 4.3 — Cycle caps**
- **Expected:** maximum 5 editor↔evaluator cycles; non-decreasing failures surfaced to the user after cycle 3.

## Section 4b: Fallback Paths

**Test 4b.1 — Single-shot subagent hosts**
- **Expected:** evaluator Message 1 and Message 2 run as two separate single-shot dispatches; the first dispatch's scores are passed into the second; no scoring context contains the trace; the second dispatch emits the unified report.

**Test 4b.2 — Hosts without subagents at all**
- **Expected:** both roles adopted sequentially in one conversation per the agent files; the output summary states plainly that the independence guarantee is procedural (evaluator's score-before-trace discipline), not mechanical.

## Section 5: Documentation Sync

**Test 5.1 — README accuracy**
- **Expected:** README describes subagent dispatch where the host supports it, sequential adoption otherwise, and the two-message evaluator round; no residual claim that agent files are read as prompt text by an adopted role.

**Test 5.2 — Version coherence**
- **Expected:** `.claude-plugin/plugin.json`, root `plugin.json`, and `.github/plugin/marketplace.json` all report the same version.