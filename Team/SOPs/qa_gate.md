# SOP — The QA gate

Every deliverable goes through QA before it reaches the Owner.

## Flow

1. Producer finishes and reports **"ready for QA"** to the Orchestrator, with
   the file paths and how to check the work (commands, tests).
2. Orchestrator sends the deliverable and the original request to **QA**.
3. QA reviews (see `.claude/agents/qa.md`) and returns one verdict:

| Verdict | Meaning | Next step |
|---|---|---|
| **PASS** | Correct, complete, honest, safe. | Deliver to the Owner. |
| **PASS WITH OBSERVATIONS** | Fine to ship; notes worth keeping. | Deliver; record the notes. |
| **NEEDS REWORK** | Something must change first. | Back to the producer; repeat. |

4. QA records a row in `qa_reviews` (deliverable, verdict, notes, reviewer).
5. Only the Orchestrator tells the Owner the verdict.

## Rules

- QA never reviews its own work.
- A producer never writes a QA verdict or a `qa_reviews` row for their own work.
- "It should work" is not evidence. QA checks by running, opening or testing.
- Any guard or check in the deliverable must come with a test input that makes
  it fire. Missing that test is a valid reason for NEEDS REWORK.
- Don't start rework while QA is still reviewing the same files — the thing
  under review would change underneath the reviewer.
