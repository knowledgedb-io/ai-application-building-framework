# SOP — Session close

Run when the Owner says "close the session", "end session", "log the session"
or similar. Owner: the Orchestrator.

1. **Update today's lists.** Every item ends the day as one of:
   - `done`
   - `rolled` — carried to tomorrow; needs a reason (at least 12 characters).
     Tomorrow's copy is a new row with `carried_from` set to this row's id
     (see `Team/SOPs/daily_seven.md`)
   - `dropped` — no longer worth doing; needs a reason
   Items that have rolled five days running must be split or dropped.
2. **Journals.** For every team member who worked today, append an entry to
   `Team/Journals/<Name>.md` and a row to `journal_entries`:
   - What we did
   - Decisions and why
   - What went well
   - What went badly
   - Open questions for next time
3. **Reminders.** Close any that were resolved; add new ones for anything the
   Owner still needs to do.
4. **Choose tomorrow's lists.** The Orchestrator proposes the Owner list (at
   most 7) and the Owner approves it. The Orchestrator chooses the Team list.
   Rank by importance, not by due date.
5. **Report** to the Owner in a few lines: what got done, what rolled, what
   tomorrow's #1 items are, and how many team items were admitted versus
   finished today (if the team list keeps growing, it is becoming a dumping
   ground).
6. **Save your work.**
   ```bash
   git add -A && git commit -m "Session close <YYYY-MM-DD>" && git push
   ```
   Push only to a **private** repository you created yourself — never to a fork
   of this project (forks of public repositories are public). Skip this step if
   you don't use git.
   The database is git-ignored; back it up separately if it matters to you.
7. Write one `activity_log` row: `action='session_close'`.
