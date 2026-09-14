# Manifest Sync — Test Scenarios

**Under test:** root `plugin.json` (single source of truth), `scripts/sync_manifests.py` (generator + guard), `.github/workflows/manifests.yml` (CI), `.agents/plugins/editorial-recension/` (Antigravity workspace manifest)
**What this file is:** Manually verifiable acceptance criteria for issue #17. The guard itself is automated (the same script runs in CI); the scenarios below record the verification runs, including the sabotage runs that prove the guard bites.

Conventions: commands run from the repository root. "exit 0" / "exit 1" are the expected shell exit codes.

---

## Section 1: Drift guard

**Test 1.1 — Repository is in sync**
- **Run:** `python3 scripts/sync_manifests.py`
- **Expected:** `manifest guard: OK (5 generated file(s) in sync with plugin.json <version>)`, exit 0.

**Test 1.2 — A hand-edited client manifest is caught (sabotage)**
- **Setup:** `--write` to a clean tree, then hand-edit `.claude-plugin/plugin.json` (e.g. set `version` to `9.9.9`).
- **Run:** `python3 scripts/sync_manifests.py --check`
- **Expected:** exit 1, naming the file and the reason. Recorded 2026-09-14:
  ```
  manifest guard: 1 problem(s)
    - .claude-plugin/plugin.json: drifted from plugin.json (run: python3 scripts/sync_manifests.py --write)
  ```
- **Why it is asserted on generated text, not on parsed JSON:** byte comparison keeps the tree stable, so the CI re-run of `--write` produces an empty `git diff` when the repository is in sync.

**Test 1.3 — One version bump propagates everywhere**
- **Run:** edit `version` in `plugin.json` only, then `python3 scripts/sync_manifests.py --write`.
- **Expected:** the new version lands in `.claude-plugin/plugin.json`, both marketplace entry versions, both `metadata.version` fields; the Codex marketplace entry is unchanged (that file carries no version — see Test 2.1).

## Section 2: Structural validation (per-harness required fields)

**Test 2.1 — Codex entry keeps its documented shape**
- **Setup:** the Codex repo marketplace at `.agents/plugins/marketplace.json`; per the OpenAI packaging docs every entry carries `source{source:"local", path:"./…"}`, `policy.installation`, `policy.authentication` and `category`.
- **Run:** remove `policy` from the entry, then `python3 scripts/sync_manifests.py --validate`.
- **Expected:** exit 1. Recorded 2026-09-14:
  ```
  manifest guard: 3 problem(s)
    - .agents/plugins/marketplace.json plugins[]: missing required field 'policy'
    - .agents/plugins/marketplace.json plugins[]: policy.installation must be one of AVAILABLE/INSTALLED_BY_DEFAULT/NOT_AVAILABLE
    - .agents/plugins/marketplace.json plugins[]: policy.authentication missing
  ```

**Test 2.2 — Antigravity marker stays minimal**
- **Setup:** `.agents/plugins/editorial-recension/plugin.json`; the Antigravity CLI schema sets `additionalProperties: false` with only `name` and `description`.
- **Run:** add any other key (e.g. `version`), then `--validate`.
- **Expected:** exit 1 listing the unsupported keys.

**Test 2.3 — No duplicated plugin content**
- **Run:** `--validate`.
- **Expected:** the Antigravity wrapper holds exactly `plugin.json` + the `skills` symlink, and the symlink resolves to `skills/<name>/SKILL.md`. Any copied `skills/` tree fails the check.

**Test 2.4 — Symlink replaced by a copy is caught (sabotage)**
- **Setup:** `--write` to a clean tree, then `rm .agents/plugins/editorial-recension/skills` and `cp -r skills .agents/plugins/editorial-recension/skills`.
- **Run:** `python3 scripts/sync_manifests.py --check`
- **Expected:** exit 1. Recorded 2026-09-14:
  ```
  manifest guard: 1 problem(s)
    - .agents/plugins/editorial-recension/skills: not a symlink to ../../../skills (run: python3 scripts/sync_manifests.py --write; on Windows, enable core.symlinks)
  ```

## Section 3: Install regression

**Test 3.1 — Claude Code marketplace add + install still succeed**
- **Setup:** clean config dir: `export CLAUDE_CONFIG_DIR=/tmp/claude-17` (empty).
- **Run:** `claude plugin marketplace add <clone>` → `claude plugin install editorial-recension@editorial-recension` → `claude plugin details editorial-recension`.
- **Expected:** both commands report success, and the inventory shows the new version with both agents. Recorded 2026-09-14 on Claude Code 2.1.207:
  ```
  ✔ Successfully added marketplace: editorial-recension (declared in user settings)
  ✔ Successfully installed plugin: editorial-recension@editorial-recension (scope: user)
  editorial-recension 0.3.0
  Component inventory
    Skills (1)  editorial-recension
    Agents (2)  evaluator, editor
  ```
- **Why the inventory matters:** `validate` cannot see load behaviour (see `tests/subagent-dispatch-tests.md`, Test 1.1).

**Test 3.2 — `claude plugin validate . --strict` passes**
- **Run:** `claude plugin validate . --strict` and `claude plugin validate .claude-plugin/plugin.json --strict`.
- **Expected:** exit 0 for both. Recorded 2026-09-14. On `main` before this change the same command exited 1 with `description: No marketplace description provided` — the marketplace `metadata.description` this change adds clears it, which is what lets CI keep `--strict`.

## Section 4: Exercised vs documented-only

Run 2026-09-14. Routes NOT exercised here, because the client is not installed on the authoring machine: Codex CLI, GitHub Copilot CLI, VS Code, Cursor, Google Antigravity, OpenClaw. Their rows are documentation-verified only (see the Phase 0 table on issue #17); re-verify with the client itself before calling a route exercised. Claude Code is exercised end to end (Section 3) plus CI-side validation.
