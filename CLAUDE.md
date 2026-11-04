# CLAUDE.md

## Purpose
This repo is my English practice journal. I'm a native Traditional Chinese speaker (Taiwan) practicing English through conversations with Claude.

## Structure
```
english-log/
├── sessions/          # One file per practice session
├── vocabulary.md      # Accumulated words and phrases
├── mistakes.md        # Recurring mistakes, grouped by type
├── CLAUDE.md
└── README.md
```

## Session file format
Filename: `sessions/YYYY-MM-DD-topic.md` (kebab-case topic)

```markdown
# Topic

**Date:** YYYY-MM-DD

## Conversation
(dialogue)

## Corrections
| Original | Corrected | Note |
|----------|-----------|------|

## New vocabulary
- **word / phrase**: meaning (中文) — example sentence
```

## Workflow
When I paste a conversation or ask you to create a session:
1. Create the session file using the format above
2. Extract corrections and new vocabulary into the file
3. Append new vocabulary to `vocabulary.md` (skip duplicates, keep alphabetical)
4. Update `mistakes.md` if a mistake type recurs; group by category (tense, articles, prepositions, word choice, etc.)
5. Commit with message: `session: YYYY-MM-DD topic`

## Rules
- Keep my original sentences unchanged in the Conversation section
- Explanations in English, with short Chinese notes only when helpful
- Remove personal info (real names, company or project details) before committing
