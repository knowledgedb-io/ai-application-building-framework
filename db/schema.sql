-- AI Application building framework — starter team database (SQLite).
--
-- Created by: python3 scripts/init_db.py   (writes .claude/team.db)
-- Safe to re-run: every statement is CREATE ... IF NOT EXISTS.
--
-- Rules the database enforces (each one is proved by a test in
-- tests/test_schema_guards.py — a guard without a test that makes it fire is
-- not counted as a guard):
--   G1  Owner list: rank must be a whole number 1-7.
--   G2  No two live items on the same day and list share a rank
--       (with G1 this means at most 7 live Owner items per day).
--   G3  Team list: rank 8 or higher needs an admission_reason
--       (unless the item was rolled over from a previous day — see G7).
--   G4  Rolling or dropping an item needs a real exit_reason.
--   G5  Finish in order: an item cannot be marked done — by update, or by
--       inserting it already done — while a lower-ranked item on the same list
--       is still open, unless that item has a real blocked_reason.
--   G6  QA never reviews its own work (reviewer <> producer).
--   G7  carried_from must point to a ROLLED item on the SAME list from an
--       EARLIER day, so the G3 exemption cannot be claimed by pointing at
--       any row.
--
-- G5 and G7 are triggers. A trigger can be removed with DROP TRIGGER; the
-- CHECK constraints (G1, G3, G4, G6) and the unique index (G2) cannot be
-- bypassed that way.
--
-- "A real reason" = at least 12 characters once spaces, dots, dashes and
-- underscores are removed, so "n/a" or "............" is refused.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL DEFAULT (datetime('now')),
    description TEXT NOT NULL
);

-- Who is on the team. Mirrors Team/roster.md.
CREATE TABLE IF NOT EXISTS team_members (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    role         TEXT NOT NULL,
    agent_file   TEXT,                       -- .claude/agents/<name>.md
    profile_path TEXT,                       -- Team/<Name>.md
    is_active    INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    hired_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Units of work delegated by the Orchestrator.
CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY,
    title        TEXT NOT NULL,
    description  TEXT,
    assigned_to  INTEGER REFERENCES team_members(id),
    status       TEXT NOT NULL DEFAULT 'open'
                 CHECK (status IN ('open', 'in_review', 'done', 'cancelled')),
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT
);

-- The candidate pool: things to remember. Not a worklist until ranked.
CREATE TABLE IF NOT EXISTS reminders (
    id                    INTEGER PRIMARY KEY,
    title                 TEXT NOT NULL,
    details               TEXT,
    owner_action_required INTEGER NOT NULL DEFAULT 0
                          CHECK (owner_action_required IN (0, 1)),
    due_at                TEXT,
    status                TEXT NOT NULL DEFAULT 'pending'
                          CHECK (status IN ('pending', 'done', 'cancelled')),
    created_at            TEXT NOT NULL DEFAULT (datetime('now')),
    resolved_at           TEXT
);

-- Every meaningful action: who did what, to what, when, and why.
CREATE TABLE IF NOT EXISTS activity_log (
    id          INTEGER PRIMARY KEY,
    logged_at   TEXT NOT NULL DEFAULT (datetime('now')),
    actor       TEXT NOT NULL,
    action      TEXT NOT NULL,
    target_type TEXT,
    target_id   INTEGER,
    reason      TEXT
);

-- One journal entry per team member per day (mirrors Team/Journals/<Name>.md).
CREATE TABLE IF NOT EXISTS journal_entries (
    id             INTEGER PRIMARY KEY,
    entry_date     TEXT NOT NULL,
    team_member    TEXT NOT NULL,
    what_we_did    TEXT NOT NULL,
    decisions      TEXT,
    went_well      TEXT,
    went_badly     TEXT,
    open_questions TEXT,
    created_at     TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (entry_date, team_member)
);

-- QA verdicts. G6: a producer cannot review their own work.
CREATE TABLE IF NOT EXISTS qa_reviews (
    id          INTEGER PRIMARY KEY,
    deliverable TEXT NOT NULL,               -- path or short description
    producer    TEXT NOT NULL,
    reviewer    TEXT NOT NULL,
    verdict     TEXT NOT NULL
                CHECK (verdict IN ('PASS', 'PASS WITH OBSERVATIONS', 'NEEDS REWORK')),
    notes       TEXT,
    reviewed_at TEXT NOT NULL DEFAULT (datetime('now')),
    CONSTRAINT g6_no_self_review CHECK (lower(trim(reviewer)) <> lower(trim(producer)))
);

-- The Daily Seven.
CREATE TABLE IF NOT EXISTS daily_seven (
    id               INTEGER PRIMARY KEY,
    plan_date        TEXT NOT NULL CHECK (plan_date = date(plan_date)),
    list_kind        TEXT NOT NULL CHECK (list_kind IN ('owner', 'team')),
    rank             INTEGER NOT NULL,
    title            TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'open'
                     CHECK (status IN ('open', 'done', 'rolled', 'dropped')),
    admission_reason TEXT,                   -- required for team rank >= 8
    blocked_reason   TEXT,                   -- lets a later item finish first
    exit_reason      TEXT,                   -- required for rolled / dropped
    carried_from     INTEGER REFERENCES daily_seven(id),
    carry_count      INTEGER NOT NULL DEFAULT 0 CHECK (carry_count >= 0),
    reminder_id      INTEGER REFERENCES reminders(id),
    created_at       TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at       TEXT NOT NULL DEFAULT (datetime('now')),

    CONSTRAINT g1_rank_whole_number CHECK (typeof(rank) = 'integer' AND rank >= 1),
    CONSTRAINT g1_owner_rank_max_7  CHECK (list_kind <> 'owner' OR rank <= 7),
    CONSTRAINT g3_team_rank_8_needs_reason CHECK (
        list_kind <> 'team' OR rank <= 7 OR carried_from IS NOT NULL
        OR length(replace(replace(replace(replace(coalesce(admission_reason, ''),
               ' ', ''), '.', ''), '-', ''), '_', '')) >= 12),
    CONSTRAINT g4_exit_needs_reason CHECK (
        status NOT IN ('rolled', 'dropped')
        OR length(replace(replace(replace(replace(coalesce(exit_reason, ''),
               ' ', ''), '.', ''), '-', ''), '_', '')) >= 12)
);

-- G2: a rank is held by at most one live (open or done) item per day and list.
CREATE UNIQUE INDEX IF NOT EXISTS g2_unique_live_rank
    ON daily_seven (plan_date, list_kind, rank)
    WHERE status IN ('open', 'done');

-- G5: finish in rank order. Unqualified BEFORE UPDATE (no "OF status") so the
-- trigger runs on every update, whichever columns the statement names.
CREATE TRIGGER IF NOT EXISTS g5_finish_in_order
BEFORE UPDATE ON daily_seven
WHEN NEW.status = 'done' AND OLD.status <> 'done'
BEGIN
    SELECT RAISE(ABORT, 'G5: a lower-ranked item on this list is still open. Finish it first, or record a blocked_reason on it.')
    WHERE EXISTS (
        SELECT 1 FROM daily_seven d
         WHERE d.plan_date = NEW.plan_date
           AND d.list_kind = NEW.list_kind
           AND d.rank < NEW.rank
           AND d.status = 'open'
           AND length(replace(replace(replace(replace(coalesce(d.blocked_reason, ''),
                   ' ', ''), '.', ''), '-', ''), '_', '')) < 12
    );
END;

-- G5 for inserts: an item cannot be created already done out of order.
CREATE TRIGGER IF NOT EXISTS g5_finish_in_order_insert
BEFORE INSERT ON daily_seven
WHEN NEW.status = 'done'
BEGIN
    SELECT RAISE(ABORT, 'G5: a lower-ranked item on this list is still open. Finish it first, or record a blocked_reason on it.')
    WHERE EXISTS (
        SELECT 1 FROM daily_seven d
         WHERE d.plan_date = NEW.plan_date
           AND d.list_kind = NEW.list_kind
           AND d.rank < NEW.rank
           AND d.status = 'open'
           AND length(replace(replace(replace(replace(coalesce(d.blocked_reason, ''),
                   ' ', ''), '.', ''), '-', ''), '_', '')) < 12
    );
END;

-- G7: carried_from must be a rolled item on the same list from an earlier day.
CREATE TRIGGER IF NOT EXISTS g7_carried_from_valid_insert
BEFORE INSERT ON daily_seven
WHEN NEW.carried_from IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'G7: carried_from must point to a rolled item on the same list from an earlier day.')
    WHERE NOT EXISTS (
        SELECT 1 FROM daily_seven p
         WHERE p.id = NEW.carried_from
           AND p.status = 'rolled'
           AND p.list_kind = NEW.list_kind
           AND p.plan_date < NEW.plan_date
    );
END;

CREATE TRIGGER IF NOT EXISTS g7_carried_from_valid_update
BEFORE UPDATE ON daily_seven
WHEN NEW.carried_from IS NOT NULL
 AND (OLD.carried_from IS NOT NEW.carried_from
      OR OLD.plan_date IS NOT NEW.plan_date
      OR OLD.list_kind IS NOT NEW.list_kind)
BEGIN
    SELECT RAISE(ABORT, 'G7: carried_from must point to a rolled item on the same list from an earlier day.')
    WHERE NOT EXISTS (
        SELECT 1 FROM daily_seven p
         WHERE p.id = NEW.carried_from
           AND p.status = 'rolled'
           AND p.list_kind = NEW.list_kind
           AND p.plan_date < NEW.plan_date
    );
END;

CREATE TRIGGER IF NOT EXISTS daily_seven_touch
AFTER UPDATE ON daily_seven
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE daily_seven SET updated_at = datetime('now') WHERE id = NEW.id;
END;

INSERT OR IGNORE INTO schema_version (version, description)
VALUES (1, 'Starter schema: team, tasks, reminders, activity log, journals, QA reviews, Daily Seven (guards G1-G7)');
