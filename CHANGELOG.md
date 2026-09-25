# Changelog

All notable changes to this project are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project uses [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-09-25

First public release.

### Added
- `CLAUDE.md` template: the main Claude Code session acts as the
  Orchestrator — it delegates, runs the hiring flow, the QA gate, the inboxes,
  journals, the Daily Seven and the session rituals, and follows the claim
  rule.
- Starter agents in `.claude/agents/`: hr, researcher, qa, knowledge-manager,
  engineer. Matching profiles and roster in `Team/`.
- SOPs in `Team/SOPs/`: session start, session close, hiring, QA gate, Daily
  Seven.
- `Owner Inbox/`, `Team Inbox/` and `Team/Journals/` folders.
- `AGENTS.md` and `GEMINI.md` pointer files so other coding agents find
  `CLAUDE.md`; `AGENTS.md` also carries a summary of the core rules.
- SQLite starter schema (`db/schema.sql`), `scripts/init_db.py` to create the
  database and `scripts/db.py` to run SQL on any system, including Windows.
  Standard library only.
- Seven database guards (G1–G7): Owner list capped at 7, unique live ranks,
  priced admission past rank 7 on the Team list, reasons required to roll or
  drop, finish in rank order, no QA self-review, and valid carry-overs. Each
  guard has a test that must make it fire.
- README for non-technical users: opening a terminal, requirements and
  install, Remote Control, using other AI tools (Gemini, Antigravity, Codex,
  Ollama), customising and hiring, daily workflow, FAQ, disclaimer and
  trademarks.
- Apache-2.0 `LICENSE`, `NOTICE`, `CONTRIBUTING.md` (DCO sign-off),
  `SECURITY.md`.
