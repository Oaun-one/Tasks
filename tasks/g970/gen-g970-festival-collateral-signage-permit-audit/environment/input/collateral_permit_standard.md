# Heritage Landing Festival — collateral and signage permit standard (HLF-7)

Revision 7. Binding for every item recorded in `collateral_log.csv`. Where an item's own
record and this standard disagree, this standard decides.

**This review is made as of 2026-08-20.** Every currency test below is made
against that date and nothing else. A permit whose validity ends **on**
2026-08-20 is still current; one that ended before it is not.

## §1 Scope — what counts as installed signage

§2 to §4 apply to **installed signage**: collateral that is physically mounted or displayed
at the venue. Of the types the log records, that is `installed_signage` and
`temporary_banner` — a temporary banner is hung at the venue and is installed signage for
every purpose in this standard.

A `standalone_graphic` (artwork produced for downstream or personal use and never installed)
and a `vehicle_wrap` (applied to a vehicle, not to the venue) are **not** installed signage.
They are outside §2 to §4 whatever their own permit, clearance or size values say, and they
do not sit against a zone's allowance under §5. Reading the scope off a single literal type
string is the commonest error in this review.

An item carries one finding code for each rule it breaches. Its `finding` entry holds every
code it breaches, joined with `|`, in any order; an item that breaches none is `none`.

The audit carries **one row per in-scope item**. An item §1 holds out of scope is not audited
and does not appear in it — it is accounted for in the memo and in the figures instead.

## §2 Permit — `PERMIT_NUMBER_MISSING`

An installed-signage item must be covered by a festival permit that actually reaches it. A
permit reaches an item only when the **governing** row of `permit_register.csv` satisfies all
of:

- it covers the item's zone (`covers_zones`, a `;`-joined list, or `all`);
- it covers the item's recorded type (`covers_item_types`, likewise);
- its `valid_until` is on or after the review date.

The governing row is not always the row the item names. Where a permit has been re-issued,
the register records the replacement with `supersedes` pointing at the row it replaces, and
it is the **last** row in that chain whose terms apply. A chain may run more than one step,
and a re-issue may be narrower than what it replaced — in zones, in item types, or in date.

An item with no permit number, an unknown one, or one whose governing row fails any of the
three tests is `PERMIT_NUMBER_MISSING`.

## §3 Egress markers — `EGRESS_MARKER_OBSTRUCTED`

Every zone sets its own minimum clearance from a designated safety egress marker, because the
zones differ in crowd flow. An item whose `egress_clearance_ft` is below its own zone's
`min_egress_clearance_ft` is `EGRESS_MARKER_OBSTRUCTED`. Clearance exactly equal to the
minimum meets it.

## §4 Size — `OVERSIZE_COLLATERAL`

Every zone sets its own per-item size cap. An item whose `size_sqft` exceeds its own zone's
`max_item_sqft` is `OVERSIZE_COLLATERAL`. A size exactly equal to the cap is within it.

§6 can tighten this cap. Where it does, §4 is applied against the tightened figure.

## §5 Zone allowance — `ZONE_ALLOWANCE_BREACH`

Each zone also carries a total allowance for the signage standing in it.

An item that fails §2 has no permit reaching it and comes down: it is **pulled**, and its
area does not sit against the allowance. What counts is the area of the items still standing
— the in-scope items in that zone whose permits do reach them.

A zone whose standing area exceeds its `aggregate_allowance_sqft` is `ZONE_ALLOWANCE_BREACH`. A zone
exactly on its allowance is within it. §5 is a property of the zone, not of any item in it,
and is never a finding against an item.

| zone | name | min clearance | per-item cap | zone allowance |
| --- | --- | --- | --- | --- |
| `ZN-01` | Main Gate Approach | 6.0 ft | 12.0 sq ft | 60.0 sq ft |
| `ZN-02` | Riverside Promenade | 4.0 ft | 16.0 sq ft | 80.0 sq ft |
| `ZN-03` | Craft Market Row | 4.0 ft | 8.0 sq ft | 40.0 sq ft |
| `ZN-04` | Main Stage Apron | 8.0 ft | 10.0 sq ft | 50.0 sq ft |
| `ZN-05` | Heritage Courtyard | 5.0 ft | 6.0 sq ft | 30.0 sq ft |
| `ZN-06` | Food Court | 6.0 ft | 14.0 sq ft | 70.0 sq ft |
| `ZN-07` | North Car Park | 3.0 ft | 20.0 sq ft | 90.0 sq ft |
| `ZN-08` | Volunteer Compound | 3.0 ft | 10.0 sq ft | 45.0 sq ft |

## §6 Heightened inspection

Where **3 or more** zones are in breach under §5, the festival is
placed under heightened inspection.

While heightened inspection is in force, the per-item size cap in §4 is reduced by
**1 sq ft — in the breaching zones only**. Every other zone keeps
the cap in the table above, and §2, §3 and §5 are unchanged.

The trigger reads the §5 breach count and nothing else. §5 counts standing area, and standing
depends on §2 alone, so §4 can never move the trigger: it is settled once the zone allowances
are, and it does not move again.

## §7 What the review reports

A completed review closes with four records: the per-item verdicts, the per-zone rollup, a
memo to the safety office, and the batch figures.

**The figures.** Eleven, every one taken over the review as HLF-7 settles it:

| key | counts |
| --- | --- |
| `collateral_count` | in-scope items audited |
| `zone_count` | venue zones |
| `permit_missing_count` | in-scope items carrying `PERMIT_NUMBER_MISSING` |
| `egress_obstructed_count` | in-scope items carrying `EGRESS_MARKER_OBSTRUCTED` |
| `oversize_count` | in-scope items carrying `OVERSIZE_COLLATERAL` |
| `compliant_count` | in-scope items carrying no finding |
| `flagged_count` | in-scope items carrying at least one finding |
| `finding_total` | findings raised across the batch |
| `out_of_scope_count` | logged items §1 holds outside §2 to §4 |
| `pulled_item_count` | items pulled under §5 |
| `zones_over_allowance` | zones in breach under §5 |

**The rollup.** One row per zone, carrying how many in-scope items it holds, how many were
pulled under §5, the standing area, the zone's allowance, and its §5 verdict.

**The memo.** The safety office reads the memo, not the tables. It records the date the
review is made as of; the logged items §1 holds out of scope, and why; every item carrying a
finding, with the code and the record that decides it — the permit, the zone minimum, or the
zone cap, named; any item whose numbers would read as a breach that the standard clears, and
what clears it; the zones over their allowance, with the standing area and the allowance they
passed; and whether heightened inspection is in force, with the count that put it there and
what it changed.

## Finding names

Item level: `PERMIT_NUMBER_MISSING`, `EGRESS_MARKER_OBSTRUCTED`, `OVERSIZE_COLLATERAL`, or `none`.
Zone level: `ZONE_ALLOWANCE_BREACH`, or `none`.
