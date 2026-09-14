# Subagent Dispatch — Test Scenarios

**Skill under test:** `skills/editorial-recension/SKILL.md` (Steps 5–7), `agents/editor.md`, `agents/evaluator.md` (loaded via Claude Code's default `agents/` discovery), `.claude-plugin/marketplace.json` (Claude install route), root `plugin.json` (Agent Plugins 1.0.0)
**What this file is:** Manually verifiable acceptance criteria for subagent registration and the isolated dispatch flow. Not an automated test runner — these are reference scenarios for manual verification during development and review.

---

## Section 1: Manifest Registration

**Test 1.1 — Agents load, not just validate**
- **Setup:** the repo tree with `.claude-plugin/plugin.json` carrying NO `agents` field (default `agents/` discovery).
- **Run:** `claude plugin validate .`; then inventory the loader: `claude --plugin-dir <repo> plugin details editorial-recension` (inline) or install and `claude plugin details editorial-recension`.
- **Expected:** validate exits 0 AND the loader reports `Agents (2)` — `evaluator, editor`.
- **Why this is asserted twice:** on Claude Code 2.1.207 an `agents` field in the manifest (array or string form) SUPPRESSES the default `agents/` scan — the loader reports Agents (0) while `validate` still passes. Validation cannot see load behaviour; only the inventory proves registration. Directory-string and glob forms additionally fail validation.

**Test 1.2 — Portable manifest untouched**
- **Setup:** root `plugin.json` (Agent Plugins 1.0.0).
- **Expected:** no `agents` field; the Agent Plugins 1.0.0 schema deliberately excludes subagents in v1; unknown top-level fields are non-fatal but must not be shipped here. Schema-check the root manifest against `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`.

**Test 1.3 — Package contents**
- **Setup:** committed tree.
- **Run:** `git archive HEAD | tar -t`.
- **Expected:** `agents/editor.md` and `agents/evaluator.md` present in the distributable tree.

**Test 1.4 — Claude marketplace install route**
- **Setup:** `.claude-plugin/marketplace.json` present with an `owner` object and `plugins[0].source` as the string `"./"`.
- **Run:** in a clean `CLAUDE_CONFIG_DIR`: `claude plugin marketplace add <repo>`, then `claude plugin install editorial-recension@editorial-recension`, then `claude plugin details editorial-recension`.
- **Expected:** add succeeds — a missing `owner` fails the marketplace schema; `.claude-plugin/marketplace.json` is the only location Claude Code reads (`.agents/plugins/` is the Codex adapter, invisible here). Install succeeds — an object-form `source` passes marketplace-add but fails install ("source type your Claude Code version does not support"). Inventory after install: `Agents (2)  evaluator, editor`.

## Section 2: Editor Dispatch Isolation

**Test 2.1 — Payload boundaries**
- **Run:** complete the intake (Q1–Q3 valid), confirm the Step 4 block, dispatch the editor subagent.
- **Expected dispatch payload:** TARGET READER / KNOWS / DOESN'T KNOW template; PURPOSE / READER SHOULD template; source text; `PRECEDING CONTEXT` field verbatim; schemata file paths.
- **Expected absence:** no intake conversation, no user's original messages, no evaluator content in the editor's context.

**Test 2.2 — Editor return shape**
- **Run:** complete one editor dispatch and inspect its return.
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
- **Run:** continue any session until the evaluator returns PASS.
- **Expected:** termination condition confirmed; final edited text presented with the Output Format summary.

**Test 4.3 — Cycle caps**
- **Setup:** a text whose reported failures will not be fixed across cycles (e.g., instruct the editor to ignore one failure report).
- **Run:** observe the cycle counter and user prompts through cycles 3 and 5.
- **Expected:** maximum 5 editor↔evaluator cycles; non-decreasing failures surfaced to the user after cycle 3.

## Section 4b: Fallback Paths

**Test 4b.1 — Single-shot subagent hosts**
- **Setup:** a host that can spawn subagents but not continue them across messages — or simulate one by running two independent evaluator dispatches manually.
- **Run:** execute the evaluator round as two dispatches per the Step 6 single-shot rule.
- **Expected:** Message 1 and Message 2 run as two separate single-shot dispatches; the first dispatch's scores are passed into the second; no scoring context contains the trace; the second dispatch emits the unified report.

**Test 4b.2 — Hosts without subagents at all**
- **Run:** invoke the skill on a host with no subagent capability and follow it through dispatch to output.
- **Expected:** both roles adopted sequentially in one conversation per the agent files; the output summary states plainly that the independence guarantee is procedural (evaluator's score-before-trace discipline), not mechanical.

## Section 5: Documentation Sync

**Test 5.1 — README accuracy**
- **Run:** read README.md against the implemented flow.
- **Expected:** README describes subagent dispatch where the host supports it, sequential adoption otherwise, and the two-message evaluator round; no residual claim that agent files are read as prompt text by an adopted role.

**Test 5.2 — Version coherence**
- **Run:** print the version fields from `.claude-plugin/plugin.json`, root `plugin.json`, and `.github/plugin/marketplace.json`; compare.
- **Expected:** all report the same version.