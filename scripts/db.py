#!/usr/bin/env python3
"""Run one SQL statement against the team database and print the result.

Works everywhere Python does, including Windows (which has no sqlite3
command-line tool by default). Standard library only.

Usage:
    python3 scripts/db.py "SELECT list_kind, rank, title, status FROM daily_seven"
    python3 scripts/db.py "UPDATE daily_seven SET status='done' WHERE id=3"
    python3 scripts/db.py --db other.db "SELECT COUNT(*) FROM reminders"

On Windows PowerShell, use `python` instead of `python3` if needed, and put the
SQL in double quotes with single quotes inside, as above.

Foreign keys are switched on, so the same rules apply as in init_db.py.
Writes are committed only if the statement succeeds; a refused write (for
example an 8th item on the Owner list) prints the reason and changes nothing.
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / ".claude" / "team.db"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sql", help="one SQL statement, in quotes")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="database file (default: .claude/team.db)")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"db: no database at {args.db.name} — run: python3 scripts/init_db.py", file=sys.stderr)
        return 2

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        with conn:
            cur = conn.execute(args.sql)
            rows = cur.fetchall()
            headers = [d[0] for d in cur.description] if cur.description else []
            changed = cur.rowcount
    except sqlite3.Error as exc:
        print(f"db: REFUSED: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()

    if headers:
        print(" | ".join(headers))
        for row in rows:
            print(" | ".join("" if v is None else str(v) for v in row))
        print(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")
    else:
        print(f"db: OK ({changed} row{'s' if changed != 1 else ''} changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
