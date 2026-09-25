# AI Application building framework

A free, open-source starting point for running a small **team of AI agents**
inside [Claude Code](https://claude.com/product/claude-code). You get an
orchestrator that delegates, a hiring process for adding new specialists, a
quality-assurance gate, inboxes, journals, a simple daily planning method, and
a small SQLite database to keep track of it all.

It is plain text files and two small Python scripts (`scripts/init_db.py`
and `scripts/db.py`). No server, no account, no
lock-in. Change anything you like.

---

## Contents

- [What it is](#what-it-is)
- [Opening a terminal](#opening-a-terminal)
- [Requirements](#requirements)
- [Install](#install)
- [Starting Claude Code in the folder](#starting-claude-code-in-the-folder)
- [Remote Control mode](#remote-control-mode)
- [Connecting other AI brains](#connecting-other-ai-brains-google-gemini-openai-local-models)
- [Customising your team](#customising-your-team)
- [Hiring a new member](#hiring-a-new-member)
- [Daily workflow](#daily-workflow)
- [FAQ](#faq)
- [Disclaimer and trademarks](#disclaimer-and-trademarks)
- [Licence](#licence)
- [Free intro call](#free-intro-call)

---

## What it is

When you open Claude Code in this folder, it reads `CLAUDE.md` and behaves as
the **Orchestrator** of a team:

| Piece | What it does | Where it lives |
|---|---|---|
| Orchestrator | Plans and delegates; never does the work itself | `CLAUDE.md` (the main session) |
| Team members | Specialist sub-agents (HR, Researcher, QA, Knowledge Manager, Engineer) | `.claude/agents/`, `Team/` |
| Hiring flow | Researcher writes a brief, HR creates the new member | `Team/SOPs/hiring.md` |
| QA gate | Every deliverable is checked before it reaches you | `Team/SOPs/qa_gate.md` |
| Inboxes | `Team Inbox/` for your requests, `Owner Inbox/` for the team's replies | folders |
| Journals | What each member did, decided and learned | `Team/Journals/` |
| Daily Seven | Your top 7 and the team's ranked list, chosen the night before | `Team/SOPs/daily_seven.md` |
| Database | Tasks, reminders, QA reviews, journals, activity log | `db/schema.sql` → `.claude/team.db` |

The Orchestrator is the main Claude Code session you type into. It is defined
by `CLAUDE.md`, so it has no file in `.claude/agents/`; the files there are the
specialists it delegates to.

"Owner" throughout means **you** — the person the team works for.

## Opening a terminal

A terminal is a window where you type commands. Every command in this README
is typed into one, so start here. You only need a few commands.

**Not downloaded the framework yet?** Open the terminal now (step 1 below),
and come back to the `cd` step for your system once you have finished
[Install](#install).

### macOS

1. Press **Cmd + Space**, type **Terminal**, press **Enter**.
   (iTerm2 works the same way if you prefer it.)
2. Type `cd ` (with a space after it), then **drag the project folder from
   Finder into the Terminal window**. The folder's path appears. Press
   **Enter**.
3. Type `ls` and press Enter. You should see `README.md`, `CLAUDE.md` and the
   other files.

### Windows

1. Install **Windows Terminal** from the Microsoft Store if you don't have it.
2. Choose how to run commands:
   - **WSL (recommended for developer tools):** open PowerShell as
     Administrator, run `wsl --install`, restart, then choose **Ubuntu** from
     the Windows Terminal drop-down. Your Windows files are under
     `/mnt/c/Users/<YOUR_USER>/`.
   - **PowerShell:** open Windows Terminal; it starts in PowerShell. Use
     `python` instead of `python3` if `python3` is not found.
   Check the Claude Code setup guide for which of these your version supports.
3. Move into the project folder, for example:
   ```bash
   cd /mnt/c/Users/<YOUR_USER>/Documents/my-ai-team      # WSL
   ```
   ```powershell
   cd $HOME\Documents\my-ai-team                          # PowerShell
   ```
4. Type `ls` and press Enter to see the files.

### Linux

1. Open your terminal app (often **Ctrl + Alt + T**).
2. `cd ~/path/to/my-ai-team`
3. `ls` to see the files.

## Requirements

You need three things: **Python 3**, **Claude Code**, and (optionally) **git**.
Type each command below into your terminal.

### Python 3

Check whether you have it:

```bash
python3 --version
```

You need version 3.8 or newer. If the command is not found:

- **macOS:** download the installer from
  [python.org/downloads](https://www.python.org/downloads/) and run it.
- **Windows (PowerShell):** download Python from
  [python.org/downloads](https://www.python.org/downloads/) and follow the
  Windows instructions there. If the installer offers **"Add python.exe to
  PATH"**, tick it. Afterwards, close and reopen the terminal and use
  `python` instead of `python3` in every command in this README.
- **Windows (WSL) and Linux:** Python 3 is usually already installed. If not,
  use your system's package manager — for example `sudo apt install python3`
  on Ubuntu.

### Claude Code

Anthropic's command-line assistant. You need a Claude subscription or API
access. Install it with one of these commands (the official
[setup guide](https://code.claude.com/docs/en/setup) is the authority if they
change):

```bash
curl -fsSL https://claude.ai/install.sh | bash      # macOS, Linux, WSL
```

```powershell
irm https://claude.ai/install.ps1 | iex             # Windows PowerShell
```

Check it worked with `claude --version`. This native install updates itself;
you can also run `claude update`.

Or use a package manager — these do **not** update themselves, so update them
with the same tool:

| Install | Update |
|---|---|
| `brew install --cask claude-code` (macOS) | `brew upgrade claude-code` |
| `winget install Anthropic.ClaudeCode` (Windows) | `winget upgrade Anthropic.ClaudeCode` |

### git (optional, recommended)

Check with `git --version`. You need it only for Option B below and for saving
your work at session close.

### sqlite3 (not needed)

Everything in this framework uses `python3 scripts/db.py` to look inside the
database, which works on every system. Windows does not include the `sqlite3`
tool; if you want it anyway, get it from
[sqlite.org/download.html](https://sqlite.org/download.html).

## Install

**Option A — download a ZIP (no git needed)**

1. On the [project's GitHub page](https://github.com/knowledgedb-io/ai-application-building-framework),
   click **Code → Download ZIP**.
2. Unzip it somewhere easy to find, for example your Documents folder.
3. Open a terminal in that folder (see [Opening a terminal](#opening-a-terminal))
   and run:
   ```bash
   python3 scripts/init_db.py
   ```

**Option B — git clone**

```bash
git clone https://github.com/knowledgedb-io/ai-application-building-framework.git my-ai-team
cd my-ai-team
python3 scripts/init_db.py
```

You should see `init_db: OK` and a list of tables. That's it — the database
file `.claude/team.db` now exists. It is ignored by git, so it never gets
uploaded by accident.

To check everything works:

```bash
python3 -m unittest discover -s tests -v
```

To look inside the database:

```bash
python3 scripts/db.py "SELECT name, role FROM team_members"
```

**Keeping your team private.** Once you start using it, this folder holds
your business details, inboxes and journals. If you back it up with git, push
only to a **private** repository you created yourself — never to a fork of
this project, because forks of public repositories are public.

## Starting Claude Code in the folder

From a terminal inside the project folder, type:

```bash
claude
```

Claude Code starts and reads `CLAUDE.md`. Try:

> Read CLAUDE.md and the roster, then tell me who is on the team.

The first time, fill in the placeholders in `CLAUDE.md` (`<PROJECT_NAME>`,
`<OWNER_NAME>`, `<BUSINESS_DESCRIPTION>`) — or ask Claude to interview you and
fill them in.

## Remote Control mode

Remote Control lets you continue the Claude Code session running on your
computer from your phone, a tablet or another browser. Claude keeps running on
your computer the whole time — your files and commands stay there; the phone
or browser is a window into that session.

**Before you start, you need:**

- A **Claude Pro, Max, Team or Enterprise** plan, signed in inside Claude Code
  with `/login`. **API keys do not work** for Remote Control. On Team and
  Enterprise plans, an admin must first switch Remote Control on.
- Claude Code talking to Anthropic directly — not through a gateway or proxy.
  If you have set `ANTHROPIC_BASE_URL` to another host, unset it.
- The terminal left **open** and the computer left **awake and online**. If the
  computer sleeps or the network drops, Claude Code reconnects when it comes
  back.

**Steps:**

1. Install Claude Code (see [Requirements](#requirements)).
2. Open a terminal and `cd` into the framework folder.
3. Run `claude` once and accept the prompt asking whether you trust this
   folder. (Start from the project folder, not your home folder.)
4. Turn on Remote Control, either:
   - inside a running session, type `/remote-control` (short form `/rc`), or
   - start a new session with it on: `claude --remote-control "My Team"`

   The first time, confirm that you want to enable Remote Control.
5. Connect from your other device using any of:
   - the **session URL** printed in the terminal,
   - the **QR code**, scanned with the Claude mobile app (in a session, run
     `/remote-control` again to show it; with the `claude remote-control`
     server command, press the **space bar**),
   - the session list at [claude.ai/code](https://claude.ai/code) or in the
     Claude mobile app.

To disconnect, run `/remote-control` again and choose disconnect in the
status panel; your local session keeps running. The conversation is synced through
Anthropic so it can appear on your other devices.

Full details and troubleshooting:
[Remote Control documentation](https://code.claude.com/docs/en/remote-control).

## Connecting other AI brains (Google Gemini, OpenAI, local models)

This framework is built for **Claude Code** and works best there. But it is
all plain files — `CLAUDE.md`, agent files, markdown SOPs and a SQLite
database — so any coding agent that can read files and run Python can use
it. What differs between tools is **which instruction file they read at
startup** and **how well they hand work to sub-agents**.

> Checked against each vendor's own documentation in September 2026. These
> tools change quickly: if a command below fails, check the linked page first.

### Which file each tool reads

| Tool | Reads at startup | Sub-agents | MCP |
|---|---|---|---|
| Claude Code | `CLAUDE.md`, or `AGENTS.md` only if there is **no** `CLAUDE.md` (v2.1.277+) | Yes, `.claude/agents/*.md` | Yes |
| Antigravity CLI (`agy`, Google) | `GEMINI.md` and `AGENTS.md` | Yes (see Google's docs) | Yes, `.agents/mcp_config.json` |
| Gemini CLI (`gemini`, Google) | `GEMINI.md`, or any name set in `context.fileName` | Yes, `.gemini/agents/*.md` | Yes |
| OpenAI Codex CLI (`codex`) | `AGENTS.override.md` or `AGENTS.md`, or — only when there is no `AGENTS.md` — a name in `project_doc_fallback_filenames`; one file per folder | Yes, `.codex/agents/*.toml` | Yes |

**Gemini users, read this first:** on **18 June 2026** Google stopped serving
Gemini CLI to free, Google AI Pro and Google AI Ultra accounts that sign in
with Google. Its successor is **Antigravity CLI**, which has a $0 individual
plan. Gemini CLI still works with a **paid** Gemini API key or a Gemini Code
Assist Standard/Enterprise licence. Sources:
[Google deprecation notice](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals),
[Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli).

### One set of instructions, several entry files

`CLAUDE.md` stays the single source of truth. This repository already ships
two small pointer files so other tools find it — they point at `CLAUDE.md`
rather than copying it, because a copy drifts out of date:

- **`AGENTS.md`** (read by Codex, Antigravity and many others) carries a
  short summary of the core rules and tells the tool to read `CLAUDE.md` in
  full and follow it. It does not affect Claude Code: when both files exist,
  Claude Code reads only `CLAUDE.md`. The pointer is an instruction, not an
  import, so the other tool has to choose to follow it; the summary is there
  so the essentials apply even if it does not.
- **`GEMINI.md`** (Gemini CLI and Antigravity CLI) starts with `@./CLAUDE.md`,
  which Gemini CLI expands as an import, plus the same plain-language pointer.
  *Unverified:* whether Antigravity CLI expands `@` imports — the plain pointer
  is there in case it does not.

**Codex users.** Codex loads **one** instruction file per folder, and
because `AGENTS.md` exists it will not load `CLAUDE.md` by itself — it sees
the summary plus the pointer. If you want Codex to have the full rules in
every session without relying on it following the pointer, replace the
contents of `AGENTS.md` with a copy of `CLAUDE.md` (and remember to update
both when you change a rule). Codex stops adding instruction files once they
reach `project_doc_max_bytes` (**32 KiB** by default); the starter `CLAUDE.md`
is well under that, but if yours grows, raise the limit in
`~/.codex/config.toml`:

```toml
project_doc_max_bytes = 65536
```

**Sub-agents don't carry over automatically.** Gemini CLI agent files use the
same `name`/`description` front matter as Claude Code, but different tool
names: if you copy `.claude/agents/*.md` into `.gemini/agents/`, delete any
`tools:` line (*untested*). Codex needs one TOML file per agent, with `name`,
`description` and `developer_instructions`.

### Install and sign in

```bash
# Antigravity CLI (Google). Sign in with Google, or use an API key (see its docs)
curl -fsSL https://antigravity.google/cli/install.sh | bash && agy
# Gemini CLI: after June 2026, individuals need a paid key from https://aistudio.google.com/apikey
npm install -g @google/gemini-cli && export GEMINI_API_KEY="..." && gemini
# OpenAI Codex CLI: sign in with a ChatGPT plan, or an API key
npm install -g @openai/codex && codex
```

### Gemini as a second brain inside Claude Code

Keep Claude Code as the orchestrator and have it send Gemini a one-off
question from the terminal:

```bash
agy -p "Summarise the risks in Team/SOPs/session_close.md"      # Antigravity CLI
gemini -p "Summarise the risks in Team/SOPs/session_close.md"   # Gemini CLI (paid key)
```

Community MCP servers that wrap other models exist; check each one's licence
and code before use.

### Local models (Ollama)

- **Codex + Ollama** is the documented route: `codex --oss` (or
  `ollama launch codex`). Ollama recommends a context window of at least 64k
  tokens.
- **Claude Code + Ollama** (`ollama launch claude`) is documented by Ollama,
  **not by Anthropic** — see the next point.

### Can Claude Code itself run on Gemini or GPT?

**Not officially supported.** Anthropic's gateway documentation says it
["doesn't support routing Claude Code to non-Claude models through any gateway"](https://code.claude.com/docs/en/llm-gateway).
Proxies such as LiteLLM and Ollama can make it run, but expect some features
to break, and you are on your own when they do. Pointing `ANTHROPIC_BASE_URL`
at a non-Anthropic host also **turns off Remote Control**.

### What you give up outside Claude Code

The features this framework leans on are most complete in Claude Code: named
sub-agents with their own tools, hooks, auto memory, scheduled routines and
Remote Control (which needs a Claude subscription, not an API key). Other tools
can read the same folders and follow the same SOPs; how well they do it
varies, and we don't test the framework against them.

## Customising your team

- **Rename members.** Change the name in `Team/<Name>.md`, the `name:` line in
  `.claude/agents/<name>.md`, `Team/roster.md` and the roster table in
  `CLAUDE.md`. Keep all four in step.
- **Give them personalities.** Edit the *Persona* section of a profile and the
  opening lines of the agent file.
- **Tell the team about your business.** Fill in *About your business* at the
  bottom of `CLAUDE.md`. A few short paragraphs is enough.
- **Keep `CLAUDE.md` short.** Every rule in it is read every session. If a rule
  no longer matches how you work, delete it rather than adding an exception.

## Hiring a new member

Just ask in plain words:

> We need someone who can write product descriptions for our online shop.

The Orchestrator runs the hiring flow in `Team/SOPs/hiring.md`:

1. The **Researcher** writes a brief on what a skilled human in that role does.
2. **HR** creates `Team/<Name>.md` and `.claude/agents/<name>.md` and updates
   the rosters.
3. **QA** checks the new member's files.
4. The Orchestrator gives the new member the original task.

Restart Claude Code afterwards so it picks up the new agent file.

## Daily workflow

**Morning** — say *"start the session"*. The Orchestrator reads recent journals,
reads back today's lists and checks `Team Inbox/`.

**During the day** — ask for things in plain language, or drop files into
`Team Inbox/`. Finished work lands in `Owner Inbox/` after passing QA. Work the
lists top-down: #1 before #2.

**Evening** — say *"close the session"*. The Orchestrator:
1. marks each item done, rolled or dropped (with reasons),
2. writes the journals,
3. proposes tomorrow's Owner list for you to approve and sets the Team list,
4. commits your changes with git.

The **Daily Seven** in one line: *decide tonight, then tomorrow do the most
important thing first.* Your list never has more than seven items; the
database enforces that. Details: `Team/SOPs/daily_seven.md`.

## FAQ

**Do I need to know how to code?**
No. You talk to Claude Code in plain language. The terminal is only needed to
start it.

**Where does my data go?**
- **Your files and the database stay on your computer.** The framework itself
  runs nothing in the background and contacts no server.
- **Your prompts, and the files Claude reads to answer them, go to the AI
  model provider** you use (Anthropic for Claude), under that provider's terms.
- **Remote Control** syncs the conversation through Anthropic so it can appear
  on your other devices; the files and commands stay on your computer.
- **If you push the folder to a git host** (such as GitHub), it is stored
  there — and it is public if the repository is public.

**Where are my passwords stored?**
Not in this folder. Never put passwords, API keys or tokens in these files. See
`SECURITY.md`.

**Can I use it for a team of people, not just me?**
It is designed for one Owner. Several people can share it through git, but the
Daily Seven assumes one person approves the Owner list.

**The database refused my change. Why?**
Some rules are enforced by the database (for example: no 8th item on your
list, rolled items need a reason). The error message says which rule. The full
list is at the top of `db/schema.sql`.

**How do I reset everything?**
Delete `.claude/team.db` and run `python3 scripts/init_db.py` again. This
erases all tasks, reminders and journals in the database (the markdown files
are untouched).

## Disclaimer and trademarks

This framework is provided **"as is", without warranty of any kind**, and the
authors are not liable for any damage arising from its use — see sections 7
and 8 of the Apache License 2.0. Your AI team can make mistakes: **you are
responsible for checking its output** before you rely on it or send it to
anyone.

This is an **independent project**. It is not affiliated with, sponsored by or
endorsed by Anthropic, Google, OpenAI or Ollama. Claude, Claude Code, Gemini,
Antigravity, OpenAI, Codex, ChatGPT and Ollama are trademarks of their
respective owners and are used here only to describe compatibility.

## Licence

Apache License 2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). You may
use, change and share this freely, including commercially. If you
redistribute it (changed or not), section 4 of the licence asks you to:

- include a copy of the `LICENSE` file,
- keep the `NOTICE` file (and any copyright notices),
- mark any files you changed with a prominent notice saying so.

## Free intro call

Want help setting this up for your business? Book a free intro call via
[KnowledgeDB.io](https://knowledgedb.io) (contact form).

The call is offered by KnowledgeDB.io separately from this open-source
project. The licence creates no obligation to provide support. The call is
intended for businesses and professionals.
