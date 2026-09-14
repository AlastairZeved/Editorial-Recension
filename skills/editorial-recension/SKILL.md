---
name: editorial-recension
description: Use when editing prose, essays, guides, or any writing meant to carry a reader through a reasoning chain — especially cross-domain writing where the author has expertise the reader does not
---

# Editorial Recension

A two-agent editorial system. The editor agent edits through named schemata. The evaluator agent scores the output against measurable features. They loop until the evaluator confirms the termination condition.

## When to Use

- Editing prose, essays, guides, documentation, or any writing with a reasoning chain
- Writing that bridges domains (explaining one field's concepts using another field's language)
- Any time writing must be followable by someone without the author's domain expertise
- When the author says "edit this" or "tighten this up" or "make this land"

## When NOT to Use

- Code comments, commit messages, quick responses
- Writing where the audience shares the author's domain expertise and jargon is appropriate
- First drafts that haven't been written yet (this is an editing loop, not a generation tool)

## How to Execute This Skill

When invoked, follow this sequence exactly. Do not skip questions or pre-fill answers from surrounding context. The editor and evaluator agents inherit the audience definition established here — a vague target reader silently corrupts every downstream schema, so the validation below is load-bearing, not ceremony. Paths written `../../` are relative to this file; two levels up is the plugin root, where `agents/` and `schemata/` live.

Open with:

> I'll run the editorial recension. Before dispatching agents, I need three things they can't guess: who they're editing for, what the text needs to accomplish, and the text itself.

---

### Step 1: Ask Q1 — Target Reader

**Ask:**

> **Question 1: Target Reader**
>
> Describe your reader using three parts:
> - Their role or domain context
> - What they already know (vocabulary, concepts, frameworks they hold)
> - What they don't know (the specific gaps that need bridging)
>
> Be specific enough that an agent could decide sentence by sentence whether a term needs a bridge or not.

**Validate the answer.**

A Q1 answer is VALID if and only if it contains all three of the following:
1. A role or domain context (not just a trait like "smart" or "non-technical")
2. At least one explicit "knows" item — specific vocabulary, concept, or framework
3. At least one explicit "doesn't know" item — specific concepts or terminology that would stop them

A Q1 answer FAILS if any of the three components is missing or is so general it could describe almost anyone. "Non-technical," "general audience," and "someone curious about AI" always fail — they have no role, no knows, and no specific gaps.

**If the answer is invalid (first vague answer):**

Ask one targeted clarification question. Identify specifically what is missing. Include at least one concrete example of a valid answer. Do not restart the questionnaire. Do not ask multiple questions at once. For example:

- Missing role: name that role/domain is missing and give an example role
- Missing knows: name that known vocabulary is missing and give an example
- Missing doesn't-know: name that specific gaps are missing and give an example

Do not accept the second vague answer out of politeness.

**If the user gives a second consecutive vague answer to Q1:**

Restate the requirement as a direct checklist — do not ask another prose question:

> I need three specific things before I can continue — let me be direct about each one:
> - **Role or domain context:** What is this person's job or professional field? (e.g., healthcare legal counsel, VP of Finance at a SaaS company, high school science teacher)
> - **What they know:** What vocabulary, concepts, or frameworks are already in their model? (e.g., HIPAA policy, budget forecasting, AP-level biology)
> - **What they don't know:** What specific concepts need bridges? (e.g., software architecture, ML model training, genomic sequencing pipelines)
>
> All three must be present and specific. "Not technical" doesn't satisfy the third item — I need to know which technical concepts are the actual gaps.

**Once Q1 is valid:**

Reformat the answer into this template before holding it:

```
TARGET READER: [role/domain]
KNOWS: [list of specific vocabulary, concepts, or frameworks]
DOESN'T KNOW: [list of specific gaps]
```

Preserve the user's phrasing register — do not over-normalize. Then confirm: "Got it. Moving to question 2."

---

### Step 2: Ask Q2 — Purpose

**Ask:**

> **Question 2: Purpose**
>
> What should the reader be able to do, decide, or understand after reading? Give me a specific reader action or outcome — not a writing quality ("clear," "better flow"), but something the reader leaves with.

**Validate the answer.**

A Q2 answer is VALID if it contains:
1. A specific action verb attached to a specific object — "explain to their team," "decide whether to sign," "ask informed questions about X," "evaluate whether Y," "choose between X and Y"

A Q2 answer FAILS if it contains only:
- Writing-quality goals: "make it clear," "improve the flow," "make it better"
- Tautological goals: "help them understand this" (without specifying understand what, to what depth, or for what purpose)

**If the answer is invalid (first vague answer):**

Ask one targeted clarification question identifying what is missing, with at least one concrete example of a valid answer. For example, if the user says "make it clear": name that "clear" is a property of the writing, not a reader goal, and give an example like "understand X well enough to Y."

**If the user gives a second consecutive vague answer to Q2:**

Restate the requirement as a direct checklist:

> I need a reader goal I can measure. Let me be direct:
> - **Specific action verb:** What does the reader do after finishing? (e.g., explain, decide, evaluate, ask, choose)
> - **Specific object:** What are they doing that verb to? (e.g., "explain the mechanism to their team," "decide whether to sign the contract," "ask a vendor the right questions about FHIR compliance")
>
> Writing qualities like "clear" or "better flow" don't work here — the agents check those automatically. I need to know what the reader is supposed to leave with.

**Once Q2 is valid:**

Reformat into this template before holding it:

```
PURPOSE: [concrete outcome + measurable indicator]
READER SHOULD: [specific action verb + object]
```

Then confirm: "Got it. Moving to question 3."

---

### Step 3: Ask Q3 — Source Text

**Ask:**

> **Question 3: Source Text**
>
> Provide the text to be edited. You can:
> - Paste it directly (plain or backtick-enclosed)
> - Give me a file path (e.g., `/path/to/document.md`)
> - Point me to a specific message in this conversation (e.g., "the text I pasted four messages ago")
> - Give me a public URL
>
> If this text is part of a larger document, include the sentence or paragraph before it — agents use that for Flow Weld and Chain Repair.

**Validate the answer.**

A Q3 answer is VALID if the text is retrievable in the current session:
- Pasted directly (present in the message)
- File path that exists and is accessible
- Numbered message reference that resolves unambiguously in this conversation
- Public URL

A Q3 answer FAILS if:
- No text, path, URL, or reference is given ("the essay")
- The reference is temporal and external to this session ("what I wrote yesterday," "the thing from last week") — these have no path or paste and cannot be retrieved
- The message reference is too vague to resolve ("earlier," "the document") without a specific identifier

**If the answer is invalid:**

Ask one targeted clarification question. Identify specifically why the text is not retrievable. Include at least one example of how to submit it. Do not restart from Q1 or Q2.

If the user's second response still does not provide a retrievable reference, state directly what you need and why you cannot proceed without it. Do not escalate to a checklist — Q3 failures are retrieval failures, not vagueness failures. A checklist will not resolve a submission that contains no text. Wait for a valid submission before advancing.

**Preceding context handling:**

A Q3 submission may include preceding context, or it may not. The absence of preceding context does NOT invalidate the submission.

- If the user explicitly states there is no preceding context (e.g., "this is a section opener"), note it as absent and accept.
- If the user provides preceding context, note it and accept.
- If the submission is valid but preceding context status is unknown (the user pasted or referenced text without mentioning it), accept the submission as VALID and ask one supplemental question before dispatch — not a re-ask of Q3:

> One quick thing before I send this to the agents — is there a preceding paragraph or sentence you'd want them to factor in for flow? If so, paste it here or quote the last line. If this is a section opener or standalone piece, just say so.

If the user says there is no preceding context in response to the supplemental question, mark it as: `PRECEDING CONTEXT: None — Flow Weld operates at document boundaries only`

If the user provides preceding context in response to the supplemental question, append it to the Q3 template before dispatch.

Once the user responds to the supplemental question, replace the `PRECEDING CONTEXT` field in the Q3 template with the resolved value before proceeding to Step 4. The `Unknown` state must never appear in the Step 4 confirmation block.

**Once Q3 is valid:**

Confirm what was received:

```
SOURCE TEXT: [description — e.g., "pasted paragraph, ~4 sentences" or "file path to document.md, section starting at..."]
SOURCE TYPE: [Direct paste | File path | Message reference | URL]
PRECEDING CONTEXT: [quoted or described, OR "None — Flow Weld operates at document boundaries only", OR "Unknown — supplemental question asked"]
```

---

### Step 4: Pre-Dispatch Confirmation

Once all three questions are valid and formatted, present the full assembled context to the user before dispatching:

```
EDITORIAL CONTEXT — PLEASE CONFIRM

TARGET READER: [...]
KNOWS: [...]
DOESN'T KNOW: [...]

PURPOSE: [...]
READER SHOULD: [...]

SOURCE TEXT: [description]
SOURCE TYPE: [type]
PRECEDING CONTEXT: [status]
```

Then ask: "Does this look right? Say yes or tell me what to adjust and I'll dispatch the agents."

If the user requests an adjustment, update only the affected template field, re-present the full confirmation block with the correction in place, and ask for confirmation again. Do not dispatch until the user explicitly confirms the corrected block.

Do not dispatch agents until the user confirms this block is correct, or explicitly says to proceed.

---

### Step 5: Dispatch the Editor Subagent

**Only dispatch after user confirmation.** Spawn the editor as an isolated subagent defined by `../../agents/editor.md`. Isolation is the point: the subagent receives only the dispatch payload below — never the intake conversation, the user's original messages, or anything else from this session.

Send to the editor subagent:
- The full TARGET READER / KNOWS / DOESN'T KNOW template
- The full PURPOSE / READER SHOULD template
- The source text
- The `PRECEDING CONTEXT` field exactly as formatted in the Q3 template. Do not rephrase it.
- The schemata library (all files in `../../schemata/`) and the scale rules (`../../schemata/scale-rules.md`)

The editor subagent will:
1. Run Phase 1 schemata (Barrier Bridge + Chain Repair)
2. Run Phase 2 schema (Compression Pass)
3. Run Phase 3 schema (Flow Weld)
4. Run Phase 4 schema (Ripple Read)
5. Return: edited text + schema trace + termination assessment

Hold the editor's full return — edited text, schema trace, termination assessment. The schema trace is sent to the evaluator only in Message 2 of Step 6. It must never appear in the evaluator's scoring context.

---

### Step 6: Dispatch the Evaluator Subagent — Two-Message Round

Spawn the evaluator as a **separate** isolated subagent defined by `../../agents/evaluator.md`. Independence here is mechanical, not aspirational: the evaluator's scoring context must contain no trace of the editor's reasoning, drafts, or schema trace when it scores. Sending the whole editor return in one payload forfeits the independence this architecture exists for.

**Message 1 — blind scoring.** Send only:
- The full editorial context that was passed to the editor: TARGET READER / KNOWS / DOESN'T KNOW, PURPOSE / READER SHOULD, and the `PRECEDING CONTEXT` field verbatim
- The original source text
- The editor's output text

Do not send the schema trace, the editor's drafts, or the editor's reasoning in this message. Wait for the evaluator's complete Feature Scores report.

**Message 2 — trace verification.** To the same evaluator subagent, send:
- The editor's schema trace (held from Step 5)
- The instruction to verify the trace against its already-recorded scores without re-scoring

The evaluator's round output is the complete report — feature scores, trace discrepancies, failures, verdict (PASS/FAIL) — emitted as one document in Message 2.

**Hosts without multi-turn subagents:** run Message 1 and Message 2 as two separate single-shot evaluator dispatches, passing the first dispatch's scores into the second. The rule is unchanged: no scoring context contains the trace.

---

### Step 7: Loop or Terminate

**If evaluator returns FAIL:**
- Send the evaluator's failure report back to the editor subagent. On hosts that keep subagent instances alive, continue the same editor instance. On single-shot hosts, re-dispatch the editor seeded with its previous output, its schema trace, and the failure report.
- The editor re-enters its loop at the phase where failures were identified
- Return to Step 6 with the editor's revised output

**If evaluator returns PASS:**
- Confirm the termination condition is met
- Present the final edited text to the user with the summary below

The loop runs until the evaluator confirms the termination condition or five cycles complete. If failures are not decreasing after cycle 3, surface this to the user and let them decide whether to continue.

**Fallback for hosts that cannot spawn subagents:** adopt both roles sequentially in this conversation — the editor role first, then the evaluator role — following the same agent files as their definitions. State plainly in the output summary that the independence guarantee is then procedural (the evaluator's score-before-trace discipline) rather than mechanical.

## Loop Limits

- Maximum 5 editor↔evaluator cycles per editing session
- If not converged after 5 cycles, surface remaining failures to the user with the best output so far and let them decide how to proceed
- Each cycle should show convergence (fewer failures than the previous cycle). If failures are not decreasing, surface this to the user after cycle 3.

## Output Format

Present to the user:

**Edited Text** — the final version

**What Changed** — which schemata fired, major rewrites, barriers bridged, chains repaired

**Editorial Trace** — condensed: schema, location, finding, action taken

**Evaluator Verdict** — PASS with feature summary, or best-effort with remaining issues

## Schemata Reference

The five named editorial moves, in execution order:

| Phase | Schema | What It Does |
|-------|--------|-------------|
| 1 | Barrier Bridge | Detects and bridges tacit knowledge gaps |
| 1 | Chain Repair | Finds and rebuilds broken reasoning chains |
| 2 | Compression Pass | Evaluates word-level efficiency and rhythm |
| 3 | Flow Weld | Checks bidirectional flow at every edit point |
| 4 | Ripple Read | Full-document coherence scan + termination check |

See `../../schemata/scale-rules.md` for ordering constraints and authority boundaries.
