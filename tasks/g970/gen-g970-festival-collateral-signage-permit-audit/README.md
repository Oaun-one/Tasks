# gen-g970-festival-collateral-signage-permit-audit

Native Harbor (schema 1.3) non-connector task. Offline: a writable `/app`, four read-only
files under `/app/input`, no network dependency at grade time.

**Oracle 1.000 · GLM-5.2 pass@5 = 4/5 · stability 5/5 · 148 deterministic verifiers, no judge.**
The single failure is model-owned and is a reasoning error — see "Difficulty" below.

## What the task asks

A festival safety office wants the collateral and signage pass finished before the
walk-round. The agent audits 66 logged items against HLF-7, the venue zones, and the permit
register, and writes four deliverables to `/app`:

| file | contents |
| --- | --- |
| `collateral_audit.csv` | one row per in-scope item, `item_id` and `finding` |
| `zone_summary.csv` | one row per zone: items, pulled, standing area, allowance, §5 verdict |
| `collateral_memo.md` | safety-office memo, including the three §8 counterfactuals |
| `results.json` | eleven derived figures |

## Changes from the mined baseline

The baseline is in `../ORIGINAL_BACKUP/`. `task.toml` is unchanged. Everything graded is
generated from `tools/g970_build.py` (data model + adjudicator) via `tools/g970_emit.py`, so
the fixtures, the gold answer and `tests/verifier.json` cannot drift apart.

### 1. The prompt stopped being a recipe

The mined prompt listed the three finding codes, listed all five `results.json` keys, told
the agent to apply the rules "only to items classified as installed signage", and pointed
straight at the single trap: *"the item that looks like a permit-number finding and is not"*.
That measures instruction-following.

`instruction.md` is now a colleague's request — the backlog, the four filenames, the column
layouts, and "the eleven figures named in HLF-7 §7". Every definition moved into the standard
as numbered sections, so the model has to read HLF-7 and work out what applies.

### 2. Scale and structure

7 items and 2 files became **66 items (60 in scope), 8 zones, 14 permits, 4 files**. Each
zone carries its own egress minimum, per-item size cap and total allowance, so no limit can
be read off the item row.

### 3. The rules that carry the difficulty

- **§1 scope by nature, not by string.** Installed signage is `installed_signage` *and*
  `temporary_banner`. Matching the literal type string costs 40 verifiers.
- **§2 the governing permit row.** Two three-hop supersession chains, each narrowing:
  PMT-1004 → 1005 → **1006** ends covering one zone and one item type; PMT-1007 → **1008**
  ends expired. Reading the cited row instead of the governing one costs 17.
- **§3/§4 per-zone limits**, inclusive, with items sitting exactly on both.
- **§5 zone allowance reads the item audit.** An item failing §2 is *pulled* and its area
  does not stand against the allowance. Counting every item instead costs 29.
- **§6 heightened inspection** — a feedback rule. The trigger is the §5 breach count, and
  firing it tightens §4 **in the breaching zones only**. It fires at exactly 3 of 3 and moves
  5 verdicts and 4 figures. Missing it costs 9; applying it to every zone costs 15.
  It terminates: §5 counts standing area, which depends on §2 alone, so §4 can never move the
  trigger — and the standard says so.
- **§8 three standing counterfactuals**, each a fresh application of a rule under a stated
  change, none answerable from the audit already produced.

### 4. Grading

15 verifiers became **148**, and the shape changed more than the count:

- **exact-set per item** — every required code present *and* every other code absent. The
  mined set checked 5 of 7 items, presence-only, so an answer flagging the two unchecked
  items still scored 1.0.
- **`audit_excludes_*`** for every out-of-scope item, and a backreference check that no
  `item_id` appears twice.
- **per-zone rollup** rows, and **eleven derived figures** recomputed from the batch.
- **one memo check per flagged item**, each requiring the item beside the record that decides
  it — the permit number (cited or governing), the clearance and zone minimum, or the size
  and zone cap.
- **one memo check per counterfactual entity** under §8.

Assertions accept a correct answer in any reasonable shape: codes in any order and joined
with any separator, extra or reordered columns, quoted fields, `none` in any case or as a
synonym, numbers at any sensible precision, and memo prose or tables. Proximity checks match
with the explanation on either side of the identifier and are case-insensitive, so a memo
grouped by reason is accepted as readily as one grouped by item.

`tools/g970_negative_check.py` runs seven misreadings of HLF-7 through the real grader. Every
one loses verifiers; none scores 1.0:

| misreading | verifiers lost |
| --- | --- |
| one flat clearance and cap for all zones | 51 |
| scope read off the literal type string | 40 |
| zone allowance counts every item, not standing | 29 |
| validity dates read as exclusive | 25 |
| ignores the `supersedes` chain | 17 |
| §6 tightens every zone, not just breaching | 15 |
| misses §6 heightened inspection | 9 |

## Difficulty and the honest pass rate

**pass@5 = 4/5** on the shipped package (`evaluations/glm-5.2/`, Trials 5 / Exceptions 0, one
task checksum across all five).

The failing run scored **119 of 148**. Its error is a single misreading of §2: it followed the
supersession chains correctly but did not test `covers_item_types` against the item's recorded
type, so every `temporary_banner` standing under a permit that covers `installed_signage`
only was cleared instead of flagged — COL-06, COL-12, COL-17, COL-46, COL-60 to COL-64. That
one rule cascaded into five zone rollups, seven derived figures and four memo entries.

**This failure is reproducible.** It appeared in the same form in three earlier batteries on
earlier builds of this package, always on the same rule. It fires at roughly one run in five.

Two batteries were run against this exact package and are both reported: the first returned
5/5, the second 4/5. That spread is the ~20% per-run failure rate, not a change in the task.
The 4/5 battery is the one shipped in `evaluations/`; the 5/5 result is recorded here so the
distribution is visible rather than implied.

No verifier in this set grades a fact HLF-7 does not ask for, and none rejects a defensible
correct answer that could be constructed against it.

## Package layout

```
instruction.md                        the prompt as issued
task.toml                             schema_version 1.3, offline, no MCP servers
environment/Dockerfile                python:3.12-slim-bookworm, digest-pinned
environment/input/                    collateral log, venue zones, permit register, HLF-7
tests/verifier.json                   the 148 scored verifiers
tests/rl_world_verifiers/             vendored verifier engine
tests/test.sh, tests/test_outputs.py  Harbor entrypoint; reward 1 only if every check passes
solution/solve.sh                     Oracle entrypoint
solution/files/                       gold deliverables
solution/golden_trajectory.json       promoted from a reward-1.0 GLM-5.2 run (18 steps)
evaluations/                          oracle, glm-5.2/r1–r5, stability/repeat-01–05
```
