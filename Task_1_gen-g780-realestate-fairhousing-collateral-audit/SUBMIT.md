# FINAL — NONC-B1-1001608 / gen-g780-realestate-fairhousing-collateral-audit

Delivery Gate **90/100**, 0 blocking, all 10 client delivery requirements PASS.
Internal Gate 41/100 (advisory only — does not decide shipping).
Pass rate **5/5** → status **too easy**, row kept per Vahid.

---

## 1. Upload to Drive

**A. Task folder** (task location) — upload the FOLDER, flat, no zip:

    gen-g780-realestate-fairhousing-collateral-audit/
      README.md  instruction.md  task.toml
      environment/  (Dockerfile, input/)
      solution/     (solve.sh, golden_trajectory.json, files/)
      tests/        (verifier.json, test.sh, test_outputs.py, rl_world_verifiers/)
      evaluations/  (oracle, glm-5.2/r1..r5, stability/repeat-01..05)

**B. QC reports** (separate QC location) — both are from the final package (`f0d4d1`):

    gen-g780_FINAL-f0d4d1-delivery-c5cb5215.zip     <- Delivery Gate, 90/100  (in Downloads)
    gen-g780_FINAL-f0d4d1-internal-94131f55.zip     <- Internal Gate, advisory

Do NOT upload the older reports (`95e02f`, `1bb422`) — they were run against superseded
packages.

---

## 2. Tracker row

| Column | Value |
|---|---|
| Batch | b_batch_1 |
| Task ID | NONC-B1-1001608 |
| Dataset Task Name | gen-g780-realestate-fairhousing-collateral-audit |
| Task Link | (leave — the original Drive link) |
| Modified Task Link | Drive link to the folder from 1A |
| QC Report Link | Drive link to the Delivery Gate report from 1B |
| Golden Trajectory Zip File | in the package at `solution/golden_trajectory.json` |
| Trainer | muhammad.04@turing.com |
| Status | too easy (row kept) |
| Date Started | 8/18/2026 |
| Date submitted | (today) |
| Proof that this task has passed review using the QC Tool | Delivery Gate report link |
| Pass Rate (pass@5) | 5/5 |
| Trainer AHT (hrs) | (your actual hours) |
| Trainer Notes | paste the block below |

### Trainer Notes — paste this

Marked too easy. GLM-5.2 passes 5/5 (rewards 1,1,1,1,1; 0 exceptions). Delivery Gate 90/100,
0 blocking, all 10 client delivery requirements pass; the 10-point gap is E3, which requires a
run that failed for a real reason and cannot be awarded while every run passes. Internal Gate
41/100 is advisory and its blocking items are a truncated model stage plus a coverage flag on
an environment statement — both dispositioned.

The mined baseline was not an audit: the fixture CSV carried four boolean columns mapping 1:1
onto the four output labels with no section text, and 4 of 5 baseline runs echoed the input
header with a `finding` column appended. Rebuilt with approval to edit fixtures: 30 sections of
real marketing copy with a `role` column, RE-FH-9 extended with §5 amendments (§5a adds marital
status and source of income, 9 -> 11 required classes; §5b brings agent_bio into §4 scope),
verifiers 14 -> 46 all deterministic, Oracle 1.0, five stability repeats identical. task.toml,
the three deliverable filenames, the five results.json keys, the four finding labels and the
RE-FH-9 identifier are unchanged, and the input directory holds the same two files.

Eight batteries across successive versions. One produced a genuine model failure (clean stop,
42/46 verifiers, one agent_bio row with a stale notice marked clean, all three derived counts
one low); raising that row family from one member to five did not reproduce it, so it is
variance rather than a gap. Estimated per-run pass probability ~0.9.

Also fixed a real grading defect in the original: it scored 14/14 on a deliverable that failed
the SEC-04 trap, dropped 3 of 7 rows, and shipped a results.json contradicting its own CSV.
`mandated_trap_clean` was `^SEC-04\s*,.*none`, unanchored, so a rationale column containing
"none" satisfied it.

---

## 3. Channel post

**g780 — marking too easy. Delivery Gate 90/100, 0 blocking, all 10 delivery requirements pass.**

Rebuilt it first: the shipped fixture was the answer key (four boolean columns mapping 1:1 onto
the four labels, no section text), so with Vahid's OK I replaced it with 30 sections of real copy
and extended RE-FH-9 with §5 amendments that change the required class list and the §4 scope.
Verifiers 14 -> 46 all deterministic, Oracle 1.0, stability 5x identical. Still 5/5 — trajectories
show GLM reads the amendments, derives the eleven-class list and flags the stale disclosure block
correctly. Not a loose-verifier problem; it just solves it. The 10-point gap is E3, which needs a
failing run.

Four things worth the channel:

1. **The original grader passed a wrong answer** — 14/14 on a deliverable that failed the trap and
   shipped a results.json contradicting its own CSV. `mandated_trap_clean` was `^SEC-04\s*,.*none`,
   unanchored, so a rationale column containing "none" satisfied it. If these came from a
   generator, sibling shannon-200 tasks likely share the pattern — worth a sweep.
2. **`Compress-Archive` produces zips the QC platform cannot read.** PowerShell omits directory
   entries, bundle detection fails, and it reports a misleading "upload contains N JSON files".
   Zip via Explorer right-click or anything that writes directory entries.
3. **Do not rename `tests/verifier.json` to `manifest.json`** on non-connector tasks. The platform
   detects the layout from that filename; renaming makes it parse the file as a standalone
   task-harness config and report Verifiers (0). The onboarding doc's packaging step does not work
   as written here.
4. **Appendix A.3's PowerShell battery command is broken on PS 5.1** — strips the inner quotes from
   `--ak "opencode_config={...}"`, harbor parses it as a string and dies with `AttributeError`,
   reporting 0 trials / 5 exceptions which reads like a 0/5 pass rate. Run batteries from Git Bash.
   Also set `max_tokens: 96000` — one run truncated at the reasoning ceiling with zero output and
   scored 0.0.

---

## 4. Last thing

Claim one **peer review** on someone else's task. It is the only hard payment condition in the
playbook: "A completed task without a matching completed peer review is an incomplete task and is
not eligible for payment."
