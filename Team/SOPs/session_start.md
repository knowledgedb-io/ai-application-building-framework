# SOP — Session start

Run at the start of every working session. Owner: the Orchestrator.

1. **Catch up.** Read the most recent entry in `Team/Journals/` for each team
   member who will work today. Note open questions.
2. **Read back the lists.** Show today's Owner list and Team list, chosen at
   last night's close. Do not re-decide them — just read them back.
   ```bash
   python3 scripts/db.py "SELECT list_kind, rank, title, status FROM daily_seven
     WHERE plan_date = date('now','localtime') ORDER BY list_kind, rank"
   ```
   If last night's close was missed, propose lists now and mark them
   provisional.
3. **Check the inboxes.** New files in `Team Inbox/` go to the Knowledge
   Manager. Anything urgent is an emergency: it *displaces* an item on the list
   (with a reason) rather than being added on top.
4. **Check reminders that are due.**
   ```bash
   python3 scripts/db.py "SELECT id, title, due_at FROM reminders
     WHERE status='pending' AND due_at <= datetime('now') ORDER BY due_at"
   ```
5. **Start work** at Owner item #1 and Team item #1.
6. Write one `activity_log` row: `action='session_start'`.
