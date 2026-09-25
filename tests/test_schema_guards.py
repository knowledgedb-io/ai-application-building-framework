#!/usr/bin/env python3
"""Every database guard ships with an input that MUST make it fire.

Run:  python3 -m unittest discover -s tests -v

Each test pairs a refusal (the guard fires) with a positive control (a valid
input is accepted), so a guard that refused everything would also fail.
Tests run against a throwaway database in a temp folder, never .claude/team.db.

What these tests do NOT cover: concurrent writers, someone dropping a trigger
(G5 and G7 are triggers), a carried-over item's source row being edited after
the carry, or edits made with tools other than SQLite. They prove the guards
fire on the inputs below, nothing more. test_g7_carry_from_missing_row is also
refused by the foreign key, so it does not isolate G7 on its own.
"""
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from init_db import init_db  # noqa: E402

DAY = "2030-01-15"
YESTERDAY = "2030-01-14"


class SchemaGuards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = init_db(Path(self.tmp.name) / "test.db")

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def add(self, list_kind, rank, title="item", plan_date=DAY, **extra):
        cols = ["plan_date", "list_kind", "rank", "title", *extra]
        vals = [plan_date, list_kind, rank, title, *extra.values()]
        sql = f"INSERT INTO daily_seven ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})"
        with self.db:
            return self.db.execute(sql, vals).lastrowid

    def refused(self, fn, *args, **kwargs):
        with self.assertRaises(sqlite3.IntegrityError):
            fn(*args, **kwargs)

    # G1 ---------------------------------------------------------------
    def test_g1_owner_rank_8_is_refused(self):
        self.refused(self.add, "owner", 8)

    def test_g1_owner_rank_7_is_accepted(self):
        self.assertIsNotNone(self.add("owner", 7))

    def test_g1_fractional_rank_is_refused(self):
        self.refused(self.add, "owner", 6.5)

    def test_g1_g2_an_eighth_live_owner_item_cannot_exist(self):
        for r in range(1, 8):
            self.add("owner", r)
        for r in range(1, 9):  # every possible rank, and one past the cap
            self.refused(self.add, "owner", r)
        live = self.db.execute(
            "SELECT COUNT(*) FROM daily_seven WHERE list_kind='owner' AND status='open'").fetchone()[0]
        self.assertEqual(live, 7)

    # G2 ---------------------------------------------------------------
    def test_g2_duplicate_live_rank_is_refused(self):
        self.add("team", 3)
        self.refused(self.add, "team", 3)

    def test_g2_dropped_item_frees_its_rank(self):
        rid = self.add("owner", 3)
        with self.db:
            self.db.execute("UPDATE daily_seven SET status='dropped', exit_reason='Displaced by urgent item' WHERE id=?", (rid,))
        self.assertIsNotNone(self.add("owner", 3))

    # G3 ---------------------------------------------------------------
    def test_g3_team_rank_8_without_reason_is_refused(self):
        self.refused(self.add, "team", 8)

    def test_g3_team_rank_8_with_junk_reason_is_refused(self):
        self.refused(self.add, "team", 8, admission_reason="............")

    def test_g3_team_rank_8_with_real_reason_is_accepted(self):
        self.assertIsNotNone(self.add("team", 8, admission_reason="Customer demo moved to Friday"))

    def test_g3_team_rank_7_needs_no_reason(self):
        self.assertIsNotNone(self.add("team", 7))

    # G4 ---------------------------------------------------------------
    def test_g4_roll_without_reason_is_refused(self):
        rid = self.add("team", 1)
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db:
                self.db.execute("UPDATE daily_seven SET status='rolled' WHERE id=?", (rid,))

    def test_g4_clearing_reason_after_drop_is_refused(self):
        rid = self.add("team", 1)
        with self.db:
            self.db.execute("UPDATE daily_seven SET status='dropped', exit_reason='No longer needed by client' WHERE id=?", (rid,))
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db:
                self.db.execute("UPDATE daily_seven SET exit_reason=NULL WHERE id=?", (rid,))

    def test_g4_roll_with_real_reason_is_accepted(self):
        rid = self.add("team", 1)
        with self.db:
            n = self.db.execute("UPDATE daily_seven SET status='rolled', exit_reason='Waiting on supplier reply' WHERE id=?", (rid,)).rowcount
        self.assertEqual(n, 1)

    # G5 ---------------------------------------------------------------
    def test_g5_finishing_out_of_order_is_refused(self):
        self.add("team", 1)
        second = self.add("team", 2)
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db:
                self.db.execute("UPDATE daily_seven SET status='done' WHERE id=?", (second,))

    def test_g5_blocked_first_item_can_be_skipped(self):
        first = self.add("team", 1)
        second = self.add("team", 2)
        with self.db:
            self.db.execute("UPDATE daily_seven SET blocked_reason='Waiting for API key from vendor' WHERE id=?", (first,))
            n = self.db.execute("UPDATE daily_seven SET status='done' WHERE id=?", (second,)).rowcount
        self.assertEqual(n, 1)

    def test_g5_inserting_done_out_of_order_is_refused(self):
        self.add("team", 1)
        self.refused(self.add, "team", 2, status="done")

    def test_g5_inserting_done_in_order_is_accepted(self):
        self.add("team", 1, status="done")
        self.assertIsNotNone(self.add("team", 2, status="done"))

    # G6 ---------------------------------------------------------------
    def test_g6_self_review_is_refused(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db:
                self.db.execute("INSERT INTO qa_reviews (deliverable, producer, reviewer, verdict) VALUES ('report.md', 'QA', 'qa ', 'PASS')")

    def test_g6_independent_review_is_accepted(self):
        with self.db:
            n = self.db.execute("INSERT INTO qa_reviews (deliverable, producer, reviewer, verdict) VALUES ('report.md', 'Engineer', 'QA', 'PASS')").rowcount
        self.assertEqual(n, 1)

    # G7 ---------------------------------------------------------------
    def rolled_yesterday(self, list_kind="team"):
        return self.add(list_kind, 1, plan_date=YESTERDAY, status="rolled",
                        exit_reason="Waiting on supplier reply")

    def test_g7_valid_carry_is_accepted_and_exempt_from_g3(self):
        src = self.rolled_yesterday()
        self.assertIsNotNone(self.add("team", 9, carried_from=src, carry_count=1))

    def test_g7_carry_from_same_day_is_refused(self):
        src = self.add("team", 1, status="rolled", exit_reason="Waiting on supplier reply")
        self.refused(self.add, "team", 9, carried_from=src)

    def test_g7_carry_from_unrolled_item_is_refused(self):
        src = self.add("team", 1, plan_date=YESTERDAY)
        self.refused(self.add, "team", 9, carried_from=src)

    def test_g7_carry_from_other_list_is_refused(self):
        src = self.rolled_yesterday("owner")
        self.refused(self.add, "team", 9, carried_from=src)

    def test_g7_carry_from_missing_row_is_refused(self):
        self.refused(self.add, "team", 9, carried_from=99999)

    def test_g7_update_to_invalid_carry_is_refused(self):
        rid = self.add("team", 2)
        other = self.add("team", 3)
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db:
                self.db.execute("UPDATE daily_seven SET carried_from=? WHERE id=?", (other, rid))

    # init -------------------------------------------------------------
    def test_init_is_idempotent(self):
        path = Path(self.tmp.name) / "again.db"
        init_db(path).close()
        conn = init_db(path)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM team_members").fetchone()[0], 6)
        conn.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
