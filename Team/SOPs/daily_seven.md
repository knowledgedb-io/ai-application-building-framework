# SOP — The Daily Seven

The Daily Seven is how the day is worked. It is based on the Ivy Lee method:
decide the night before, then do the most important thing first.

## Two lists

| List | Who does it | Size | Ranked? |
|---|---|---|---|
| **Owner list** | Only what the Owner personally must do: decisions, approvals, calls, signatures | **At most 7** live items | Yes, 1–7 |
| **Team list** | What the AI team executes | No fixed cap; ranks 8+ need a written reason | Yes |

Anything else lives in `reminders` (the candidate pool). **The pool is not a
worklist.** Items move from the pool to a list only when someone ranks them.

## The ritual

**Evening (session close)**
1. Mark each of today's items `done`, `rolled` or `dropped`. Rolled and
   dropped need a reason of at least 12 characters.
2. The Orchestrator proposes tomorrow's Owner list; the Owner approves it.
3. The Orchestrator chooses tomorrow's Team list.
4. Rank by true importance. A due date is an input, not the answer.

**Morning (session start)**
1. Read the lists back. No re-deciding.
2. Start at #1 on each list.

**During the day**
- Finish #1 before starting #2. The database refuses completing a higher
  number while a lower one is still open, unless the lower one has a written
  `blocked_reason`.
- **Emergencies displace, they don't append.** Put the urgent item in a slot
  and mark the displaced item `dropped` with a reason.

## Health checks

- An item rolled **five days running** must be split or dropped.
- At close, compare items **admitted** to the team list versus items
  **finished**. If admissions keep exceeding finishes, the list is turning back
  into a backlog.

## Useful queries

Run any of these with `python3 scripts/db.py "<SQL>"` (works on Windows too),
or with the `sqlite3` tool if you have it.

```sql
-- Today's lists
SELECT list_kind, rank, title, status FROM daily_seven
 WHERE plan_date = date('now','localtime') ORDER BY list_kind, rank;

-- Add an Owner item
INSERT INTO daily_seven (plan_date, list_kind, rank, title)
VALUES (date('now','localtime','+1 day'), 'owner', 1, 'Approve the Q3 price list');

-- Roll an item: close today's row with a reason ...
UPDATE daily_seven SET status='rolled', exit_reason='Waiting on supplier reply'
 WHERE id = 42;
-- ... then create tomorrow's copy pointing back at it
INSERT INTO daily_seven (plan_date, list_kind, rank, title, carried_from, carry_count)
SELECT date(plan_date, '+1 day'), list_kind, rank, title, id, carry_count + 1
  FROM daily_seven WHERE id = 42;
```

`carried_from` must point to a rolled item on the same list from an earlier
day (guard G7). If tomorrow already has an item at that rank, put a free rank
in the INSERT instead. A rolled-over team item may keep a rank of 8 or more without a
new admission reason, because it was already admitted.

The rules the database enforces are listed in `db/schema.sql` and each one is
proved by a test in `tests/test_schema_guards.py`. G5 and G7 are triggers:
they stop mistakes, but anyone with access to the file can remove a trigger,
so they are not a security boundary.
