# Editorial Recension SKILL.md

[![Standard Readme](https://img.shields.io/badge/standard--readme-fde047.svg)](https://github.com/RichardLitt/standard-readme)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## At a Glance

An agent skill built for editing prose down to the knowledge level of the reader by deploying two independent subagents that work in tandem, the Editor and the Evaluator, on a loop of your text until the Evaluator confirms all tests pass (or until each subagent has taken 5 turns, whichever comes first).

<p align="center">
<video src="https://github.com/user-attachments/assets/5faf8217-02eb-473a-bcc3-64ab35563ca7" controls preload="metadata"></video>
</p>

---

<p><img src="docs/icons/icon-intake.svg" width="18" height="18" alt=""> <sub>00 &middot; START HERE</sub></p>

## How to Use

Invoke the skill and a 3 question intake begins: who the target reader is, what the reader should be able to do or understand after reading, and what text is being edited. If the answers you provide are too vague, the agent will not accept it and try to help refine the scope. 

After answering the intake questions, two agents will be deployed sequentially: The Editor and the Evaluator. 

The **Editor** agent loops five questions and runs them in phases over your text, editing the text as it runs. Once complete, it passes over the edits to the evaluator agent.

The **Evaluator** scores the edits themselves *before* it reads the editor's explanation of what it did, then confirms or rejects the editor's claim that the editing is complete. 

Together, they loop until all tests pass, or until five turns are spent, and the edited text is presented to the user. 

If each agent takes three turns and there is no reduction in test failures, the agent will alert the user and ask before continuing.

If each agent takes five turns and the text still fails, the best output and the fail points are presented.


## When to Use

Editorial Recension is a two-agent editorial system packaged as a skill. Its purpose is narrow and specific: edit prose until a reader who lacks the author's domain expertise can follow the reasoning chain — not until it "reads well" to someone who already understands the underlying concepts of a topic.

<img src="docs/media/agent-cards.svg" alt="Two slate plates side by side, matching the film's title cards: EDITOR in ember, rewrites the text through five schemata, in phases; EVALUATOR in verdict green, scores the result against measurable features, blind. Beneath them the line: they loop until the evaluator confirms the termination condition." width="100%">

## How it Works


## When to Use

- Editing prose, essays, guides, documentation, or any writing with a reasoning chain
- Writing that bridges domains (explaining one field's concepts using another field's language)
- Any time writing must be followable by someone without the author's domain expertise
- When you need a text to "tighten up" or need a little help to "make this land"

## When Not to Use

- Code comments, commit messages, quick responses
- Writing where the audience shares the author's domain expertise and jargon is appropriate
- First drafts that haven't been written yet (this is an editing loop, not a generation tool)

