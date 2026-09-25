# Contributing

Thanks for helping! This project aims to stay **small and approachable**, so
the bar for adding things is "would a first-time user be better off with this?"

## Good contributions

- Clearer wording in the README, `CLAUDE.md` or the SOPs.
- Fixes to `scripts/init_db.py` or `db/schema.sql`.
- New starter agents that many users would want (open an issue first).
- Translations of the README.

## Ground rules

1. **Keep it generic.** No personal names, emails, company details or real
   data in examples — use placeholders like `<OWNER_NAME>`.
2. **No secrets.** See `SECURITY.md`.
3. **Every guard ships with a test that makes it fire.** If you add a database
   constraint, trigger or check, add a test in `tests/` that proves it refuses
   bad input *and* accepts good input.
4. **Standard library only** for Python scripts, so installs stay simple.
5. **Don't claim what you didn't test.** In PR descriptions, say how you
   checked your change.

## Workflow

1. Fork the repository and create a branch. Fork a **clean copy** of this
   project — never push your own working team folder (with your inboxes,
   journals and business details) to a fork, because forks of public
   repositories are public.
2. Make your change.
3. Run the tests:
   ```bash
   python3 -m unittest discover -s tests -v
   ```
4. Update `CHANGELOG.md` under an *Unreleased* heading.
5. Commit with a sign-off: `git commit -s`. This adds a `Signed-off-by:` line
   certifying the [Developer Certificate of Origin](https://developercertificate.org):
   that you wrote the change or otherwise have the right to submit it under
   this project's licence.
6. Open a pull request describing what changed and how you tested it.

**AI-assisted contributions are welcome**, but you are responsible for them:
only submit AI-generated content that you have reviewed and have the right to
contribute under the Apache License 2.0, and sign it off as above.

By contributing you agree that your contributions are licensed under the
Apache License 2.0.
