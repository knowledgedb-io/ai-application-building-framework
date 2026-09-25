# SOP — Hiring a new team member

Use when a task needs expertise nobody on the team has.

## Steps

1. **Orchestrator** names the gap in one sentence: "We need someone who can
   ___ because ___."
2. **Researcher** writes a skills brief (responsibilities, skills and tools,
   common beginner mistakes, limits, suggested name and description) and saves
   it to `Team Inbox/`.
3. **HR** creates:
   - `Team/<Name>.md` — the profile (template below)
   - `.claude/agents/<name>.md` — the agent definition (template below)
   - a row in `Team/roster.md`, the roster table in `CLAUDE.md`, and the
     `team_members` table
4. **QA** reviews the new profile and agent file.
5. **Orchestrator** delegates the original task to the new member.

## Profile template — `Team/<Name>.md`

```markdown
# <Name>

**Role:** <one line>
**Agent file:** `.claude/agents/<name>.md`

## Persona
<two or three sentences on how they think and communicate>

## Responsibilities
- ...

## Does not do
- ...

## Hands off to
- <other member> for <kind of work>
```

## Agent template — `.claude/agents/<name>.md`

```markdown
---
name: <name>
description: <When should the Orchestrator call this member? Be specific.>
---

# <Name>

You are <Name>, the <role> for the Owner's AI team.

## How you work
1. ...

## Rules
- Report "ready for QA" when done; never claim a QA verdict yourself.
- Never claim a guarantee you did not test.
```

Tip: restart Claude Code after adding an agent file so it is picked up.
