#!/usr/bin/env python3
"""Create (or update) the team database from db/schema.sql.

Usage:
    python3 scripts/init_db.py              # creates .claude/team.db
    python3 scripts/init_db.py --db other.db

Safe to run more than once: the schema only creates what is missing, and the
starter team members are inserted only if they are not already there.
Standard library only.
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "db" / "schema.sql"
DEFAULT_DB = ROOT / ".claude" / "team.db"

STARTER_TEAM = [
    # (name, role, agent_file, profile_path)
    ("Orchestrator", "Orchestrator & team lead", "CLAUDE.md", "Team/Orchestrator.md"),
    ("HR", "Hiring & team profiles", ".claude/agents/hr.md", "Team/HR.md"),
    ("Researcher", "Research & skills briefs", ".claude/agents/researcher.md", "Team/Researcher.md"),
    ("QA", "Quality assurance gate", ".claude/agents/qa.md", "Team/QA.md"),
    ("Knowledge Manager", "Files and indexes incoming material", ".claude/agents/knowledge-manager.md", "Team/Knowledge Manager.md"),
    ("Engineer", "Code, scripts, database", ".claude/agents/engineer.md", "Team/Engineer.md"),
]


def init_db(db_path: Path) -> sqlite3.Connection:
    """Apply the schema and seed the starter team. Returns an open connection."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    with conn:
        conn.executemany(
            "INSERT OR IGNORE INTO team_members (name, role, agent_file, profile_path) VALUES (?, ?, ?, ?)",
            STARTER_TEAM,
        )
        conn.execute(
            "INSERT INTO activity_log (actor, action, target_type, reason) VALUES (?, ?, ?, ?)",
            ("init_db", "schema_applied", "database", "scripts/init_db.py run"),
        )
    return conn


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="database file (default: .claude/team.db)")
    args = parser.parse_args()

    try:
        conn = init_db(args.db)
    except sqlite3.Error as exc:
        print(f"init_db: FAILED: {exc}", file=sys.stderr)
        return 1

    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    members = conn.execute("SELECT COUNT(*) FROM team_members").fetchone()[0]
    conn.close()
    try:
        shown = args.db.resolve().relative_to(ROOT)
    except ValueError:
        shown = args.db
    print(f"init_db: OK  db={shown}")
    print(f"init_db: tables={len(tables)} ({', '.join(tables)})")
    print(f"init_db: team_members={members}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
