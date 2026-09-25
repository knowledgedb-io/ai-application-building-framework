#!/usr/bin/env python3
"""scripts/db.py: reads print rows, and a refused write changes nothing."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from init_db import init_db  # noqa: E402


def run(db, sql):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "db.py"), "--db", str(db), sql],
                          capture_output=True, text=True)


class DbHelper(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "t.db"
        init_db(self.db).close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_select_prints_rows(self):
        r = run(self.db, "SELECT name FROM team_members WHERE name='QA'")
        self.assertEqual(r.returncode, 0)
        self.assertIn("QA", r.stdout)
        self.assertIn("(1 row)", r.stdout)

    def test_refused_write_exits_1_and_changes_nothing(self):
        r = run(self.db, "INSERT INTO daily_seven (plan_date, list_kind, rank, title) VALUES ('2030-01-15','owner',8,'x')")
        self.assertEqual(r.returncode, 1)
        self.assertIn("REFUSED", r.stderr)
        n = run(self.db, "SELECT COUNT(*) AS n FROM daily_seven")
        self.assertIn("\n0\n", n.stdout)

    def test_valid_write_is_committed(self):
        r = run(self.db, "INSERT INTO daily_seven (plan_date, list_kind, rank, title) VALUES ('2030-01-15','owner',7,'x')")
        self.assertEqual(r.returncode, 0)
        n = run(self.db, "SELECT COUNT(*) AS n FROM daily_seven")
        self.assertIn("\n1\n", n.stdout)

    def test_missing_database_is_reported(self):
        r = run(Path(self.tmp.name) / "nope.db", "SELECT 1")
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
