# Security

## Keep secrets out of the repository

- **Never commit** passwords, API keys, access tokens, private keys, bank
  details or personal ID numbers — not in code, not in markdown, not in the
  inboxes or journals.
- Keep secrets in environment variables, a `.env` file (git-ignored by this
  project), or your operating system's keychain.
- The team database `.claude/team.db` is **git-ignored** on purpose. It can
  hold your tasks, reminders and journals; it is not meant to be shared. Back
  it up separately if it matters to you.
- Before you push, run `git status` and read the list of files. If you see
  something you did not mean to share, stop.
- Push your working team folder only to a **private** repository you created
  yourself — never to a fork of this project (forks of public repositories are
  public).
- If a secret was committed, **rotate it** (issue a new one and cancel the old
  one). Deleting the file is not enough: it stays in git history.

## Your AI provider

Claude Code sends your conversations and the files it reads to the AI provider
you use. Don't ask it to read files you would not share with that provider.

## Supported versions

Only the latest release receives security fixes. There is no bug bounty.

## Reporting a vulnerability

Please report security issues privately rather than in a public issue. Use
GitHub's **"Report a vulnerability"** button on the repository's Security tab.
We aim to acknowledge reports within a few working days.
