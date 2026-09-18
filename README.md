# Editorial Recension SKILL.md

[![Standard Readme](https://img.shields.io/badge/standard--readme-fde047.svg)](https://github.com/RichardLitt/standard-readme)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## At a Glance

An agent plugin built for editing prose down to the knowledge level of the reader by deploying two agents that work in sequentially, the Editor and the Evaluator, on a loop of your text until the Evaluator confirms all tests pass (or until each has taken 5 turns, whichever comes first).

***Important Caveat:*** _this was built as a Claude Code plugin and includes the deployment of isolated subagents; however, if your agent does not have subagent deployment as a capability (or does not ingest subagent files from Agent Plugins 1.0.0 standard repos natively) then this plugin will not work as intended. After install, be sure to verify that the subagent files were received and deployable. If they weren't, ask your agent to build the subagents based on the SKILL.md which contains all of the relevant information your subagent needs to function._

---

## Install

The repository root *is* the plugin — `plugin.json` plus `skills/`, `agents/` and `schemata/`. Every client gets a small manifest that points at that root, so no plugin content is duplicated anywhere.

| Client | Install | Manifest it reads |
|---|---|---|
| **Claude Code** | `/plugin marketplace add AlastairZeved/Editorial-Recension` then `/plugin install editorial-recension@editorial-recension` | `.claude-plugin/marketplace.json` |
| **Codex CLI** | `codex plugin marketplace add AlastairZeved/Editorial-Recension`, then install Editorial Recension from the Plugins Directory | `.agents/plugins/marketplace.json` |
| **GitHub Copilot CLI** | `copilot plugin marketplace add AlastairZeved/Editorial-Recension` then `copilot plugin install editorial-recension@editorial-recension` | `.github/plugin/marketplace.json` |
| **VS Code** | Command Palette → *Chat: Install Plugin From Source* → the repository URL, or register the repository in `chat.plugins.marketplaces` and install from `@agentPlugins` in the Extensions view | `.claude-plugin/marketplace.json` |
| **Cursor** | Clone, then *Customize* in the sidebar → Editorial Recension → *Install*. For development, symlink the clone into `~/.cursor/plugins/local/`. Cursor loads Agent Plugins packages unchanged, so no Cursor manifest ships here | root `plugin.json` |
| **Google Antigravity** | Open the repository as a workspace — Antigravity scans `.agents/plugins/` — or copy `.agents/plugins/editorial-recension/` into `~/.gemini/config/plugins/` | `.agents/plugins/editorial-recension/plugin.json` |
| **Hermes Agent** | `hermes plugins install AlastairZeved/Editorial-Recension --enable` (repeat with `hermes --profile <name> … --enable` per profile) | root `plugin.json` |
| **Anything else** | Clone the repository into the agent's skill/plugin directory; anything that reads `SKILL.md` picks up `skills/editorial-recension/SKILL.md` | root `plugin.json` |

Each route was checked against that vendor's own documentation on 2026-09-14 (the verification table lives in issue #17). The Antigravity workspace manifest is a marker file plus a symlink to `skills/`, so skill content stays single-sourced — clones on Windows need `git config core.symlinks true`. Hermes Agent was additionally checked on 2026-09-18, against its docs and a live end-to-end run: the CLI ingests root `plugin.json` as a portable Agent Plugins package and registers the skill as `agent-plugin-editorial-recension-0d1aeec2:editorial-recension`; it does not ingest `agents/` natively, so the skill dispatches the editor and evaluator itself as isolated subagents using the agent files as their definitions (the fallback path described in the caveat above).

### Keeping the manifests in sync

`plugin.json` at the repository root is the single source of truth for name, version, description, author, repository and license. Every client manifest is generated from it:

```sh
python3 scripts/sync_manifests.py --write   # rewrite the client manifests from plugin.json
python3 scripts/sync_manifests.py           # drift check + structural validation, no writes
```

Bump the version in `plugin.json` only. CI runs the same script on every push and pull request — tree surface, drift and per-harness fields — re-runs `--write` and fails if that changes anything, tracked or untracked, and runs `claude plugin validate . --strict`.

---

## How to Use

Invoke the skill and a 3 question intake begins: who the target reader is, what the reader should be able to do or understand after reading, and what text is being edited. If the answers you provide are too vague, the agent will not accept it and try to help refine the scope. 

After answering the intake questions, two agents will be deployed sequentially: The Editor and the Evaluator. 

The **Editor** loops five questions and runs them in phases over your text, editing the text as it runs. Once complete, it passes over the edits to the evaluator agent.

The **Evaluator** scores the edits themselves *before* it reads the editor's explanation of what it did, then confirms or rejects the editor's claim that the editing is complete. 

<img src="docs/media/agent-cards.svg" alt="Two slate plates side by side, matching the film's title cards: EDITOR in ember, rewrites the text through five schemata, in phases; EVALUATOR in verdict green, scores the result against measurable features, blind. Beneath them the line: they loop until the evaluator confirms the termination condition." width="100%">

One after the other they loop until all tests pass (or until five turns are spent) and the edited text is presented to the user. 

***If each agent takes three turns and there is no reduction in test failures, the agent will alert the user and ask before continuing.***

***If each agent takes five turns and the text still fails, the best output and the fail points are presented.***


## When to Use

- Editing prose, essays, guides, documentation, or any writing with a reasoning chain
- Writing that bridges domains (explaining one field's concepts using another field's language)
- Any time writing must be followable by someone without the author's domain expertise
- When you need a text to "tighten up" or need a little help to "make this land"

## When Not to Use

- Code comments, commit messages, quick responses
- Writing where the audience shares the author's domain expertise and jargon is appropriate
- First drafts that haven't been written yet (this is an editing loop, not a generation tool)

