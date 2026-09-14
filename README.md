# Editorial Recension SKILL.md

[![Standard Readme](https://img.shields.io/badge/standard--readme-fde047.svg)](https://github.com/RichardLitt/standard-readme)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## At a Glance

An agent skill built for editing prose down to the knowledge level of the reader by deploying two agents that work in sequentially, the Editor and the Evaluator, on a loop of your text until the Evaluator confirms all tests pass (or until each has taken 5 turns, whichever comes first).

_***Important Caveat:*** this was built as a Claude Code plugin with deployment of isolated agents; however, to make this accessible to a wider agentic market it has been packaged under the Agent Plugins 1.0.0 standard which does not currently accept subagents in its standard. The skill works fine on its own, but conversations where there is preceding context before the skill is invoked may have that context creep. Ask your agent to build the subagents according to the SKILL.md if your agent is capable of deploying them, otherwise your agent will adopt the two roles sequentially and attempt isolation of context. As soon as the Agent Plugins 1.0.0 standard is updated to include subagents, I'll update the repo to include them natively. _

***[Insert a video here]***

---

## How to Use

Invoke the skill and a 3 question intake begins: who the target reader is, what the reader should be able to do or understand after reading, and what text is being edited. If the answers you provide are too vague, the agent will not accept it and try to help refine the scope. 

After answering the intake questions, two agent roles will be adopted sequentially: The Editor and the Evaluator. 

The **Editor** loops five questions and runs them in phases over your text, editing the text as it runs. Once complete, it passes over the edits to the evaluator agent.

The **Evaluator** scores the edits themselves *before* it reads the editor's explanation of what it did, then confirms or rejects the editor's claim that the editing is complete. 

<img src="docs/media/agent-cards.svg" alt="Two slate plates side by side, matching the film's title cards: EDITOR in ember, rewrites the text through five schemata, in phases; EVALUATOR in verdict green, scores the result against measurable features, blind. Beneath them the line: they loop until the evaluator confirms the termination condition." width="100%">

One after the other they loop until all tests pass (or until five turns are spent) and the edited text is presented to the user. 

***If each persona/agent takes three turns and there is no reduction in test failures, the agent will alert the user and ask before continuing.***

***If each persona/agent takes five turns and the text still fails, the best output and the fail points are presented.***


## When to Use

- Editing prose, essays, guides, documentation, or any writing with a reasoning chain
- Writing that bridges domains (explaining one field's concepts using another field's language)
- Any time writing must be followable by someone without the author's domain expertise
- When you need a text to "tighten up" or need a little help to "make this land"

## When Not to Use

- Code comments, commit messages, quick responses
- Writing where the audience shares the author's domain expertise and jargon is appropriate
- First drafts that haven't been written yet (this is an editing loop, not a generation tool)

