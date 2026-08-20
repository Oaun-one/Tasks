# Composite photo-edit request rights audit — INT-09 rev 4

Audited as of **2026-03-31**. Every licence and consent currency test below is
made against that date; a record whose validity ends on 2026-03-31 is still
current, one that ended before it is not.

62 of the 70 rows in the log are audited, across 12 accounts. 38 carry at least
one finding and 24 are clean; 51 findings are raised in total.

## Requests taken out of the audit

REQ-13, REQ-16, REQ-26, REQ-31, REQ-38, REQ-47, REQ-58, REQ-70 are logged `withdrawn` — pulled by the client before production. INT-09 §1
takes them out of the audit entirely: they get no verdict, they are absent from
`composite_request_audit.csv`, and they count towards nothing — not the request
totals, not their accounts' counts, and not the batch-wide share §8 is measured
against. That is why ACC-04 shows 2 audited requests and ACC-07 and ACC-08 show 3,
where the log lists 4 apiece.

## Findings by code

### UNLICENSED_CHARACTER_USE — 12 request(s)

- REQ-05 composites Rook and Raven for social_public and the character occupies 28.7% of the canvas against the 20% prominence cap on LIC-109 (the row cites LIC-103; LIC-109 supersedes it and governs).
- REQ-09 composites Ember Knight for print_for_sale and the character occupies 41.5% of the canvas against the 40% prominence cap on LIC-104.
- REQ-10 composites Ember Knight for social_public and LIC-104 covers print_for_sale only, not social_public.
- REQ-17 composites Nimbus the Cat for print_for_sale and LIC-102 covers social_public only, not print_for_sale.
- REQ-21 composites Captain Marlow for client_internal and LIC-101 covers social_public and print_for_sale only, not client_internal. `client_internal` is distribution, so the personal-use allowance does not reach it.
- REQ-27 composites Nimbus the Cat for social_public and the character occupies 25.1% of the canvas against the 25% prominence cap on LIC-102.
- REQ-30 composites Ember Knight for print_for_sale and the character occupies 42.0% of the canvas against the 40% prominence cap on LIC-104.
- REQ-34 composites Verdant Automata for print_for_sale and LIC-113 covers social_public only, not print_for_sale (the row cites LIC-111; LIC-113 supersedes it and governs).
- REQ-35 composites Verdant Automata for social_public and the character occupies 22.1% of the canvas against the 22% prominence cap on LIC-113 (the row cites LIC-112; LIC-113 supersedes it and governs).
- REQ-49 composites Captain Marlow for social_public and the character occupies 30.1% of the canvas against the 30% prominence cap on LIC-101.
- REQ-54 composites Verdant Automata for social_public and the character occupies 30.0% of the canvas against the 22% prominence cap on LIC-113 (the row cites LIC-112; LIC-113 supersedes it and governs).
- REQ-57 composites Pockets the Fox for social_public and the character occupies 35.1% of the canvas against the 35% prominence cap on LIC-117.

### THIRD_PARTY_BACKGROUND_UNLICENSED — 9 request(s)

- REQ-04 is logged `third_party_unlicensed`, which is unlicensed on its own record.
- REQ-05 claims a licensed third-party background but LIC-106 (Aurora Ridge Panorama) lapsed on 2026-02-28.
- REQ-10 claims a licensed third-party background but LIC-108 covers print_for_sale only, not social_public.
- REQ-23 is logged `third_party_unlicensed`, which is unlicensed on its own record. The stray licence id LIC-107 on the row is an intake leftover and does not clear it.
- REQ-28 claims a licensed third-party background but LIC-110 covers print_for_sale only, not personal_only (the row cites LIC-105; LIC-110 supersedes it and governs).
- REQ-36 claims a licensed third-party background but LIC-116 covers client_internal only, not print_for_sale (the row cites LIC-114; LIC-116 supersedes it and governs).
- REQ-51 claims a licensed third-party background but LIC-116 covers client_internal only, not social_public (the row cites LIC-115; LIC-116 supersedes it and governs).
- REQ-60 claims a licensed third-party background but LIC-116 covers client_internal only, not print_for_sale (the row cites LIC-114; LIC-116 supersedes it and governs).
- REQ-69 claims a licensed third-party background but LIC-116 covers client_internal only, not print_for_sale (the row cites LIC-115; LIC-116 supersedes it and governs).

### MISSING_MINOR_CONSENT — 5 request(s)

- REQ-05 carries a minor's likeness and the consent on file is `basic`, which does not reach social_public.
- REQ-14 carries a minor's likeness and the consent on file is `basic`, which does not reach print_for_sale.
- REQ-32 carries a minor's likeness and no guardian consent record is on file.
- REQ-42 carries a minor's likeness and the consent on file is `basic`, which does not reach social_public.
- REQ-53 carries a minor's likeness and the publicity consent expired on 2026-03-30, before the audit date.

### COMMERCIAL_DISTRIBUTION_FLAG — 18 request(s)

- REQ-02 goes to social_public and ACC-01 holds no standing coverage.
- REQ-14 goes to print_for_sale and ACC-04's master agreement has lapsed, so the social_public it lists clears nothing.
- REQ-20 goes to social_public and ACC-05's agreement covers print_for_sale only.
- REQ-23 goes to print_for_sale and ACC-06 holds no standing coverage.
- REQ-27 goes to social_public and ACC-07 holds no standing coverage.
- REQ-30 goes to print_for_sale and ACC-08's master agreement has lapsed, so the social_public and print_for_sale it lists clears nothing.
- REQ-40 goes to social_public and ACC-10 holds no standing coverage.
- REQ-42 goes to social_public and ACC-10 holds no standing coverage.
- REQ-43 goes to print_for_sale and ACC-11's master agreement has lapsed, so the print_for_sale it lists clears nothing.
- REQ-44 goes to social_public and ACC-11's master agreement has lapsed, so the print_for_sale it lists clears nothing.
- REQ-45 goes to print_for_sale and ACC-11's master agreement has lapsed, so the print_for_sale it lists clears nothing.
- REQ-50 goes to print_for_sale and ACC-12's agreement covers social_public only.
- REQ-53 goes to social_public and ACC-01 holds no standing coverage.
- REQ-62 goes to social_public and ACC-06 holds no standing coverage.
- REQ-65 goes to social_public and ACC-07 holds no standing coverage.
- REQ-66 goes to print_for_sale and ACC-08's master agreement has lapsed, so the social_public and print_for_sale it lists clears nothing.
- REQ-68 goes to social_public and ACC-04's master agreement has lapsed, so the social_public it lists clears nothing.
- REQ-69 goes to print_for_sale and ACC-12's agreement covers social_public only.

### ALTERATION_DISCLOSURE_MISSING — 7 request(s)

- REQ-06 substantively alters a person's appearance for social_public with no disclosure on file.
- REQ-07 substantively alters a person's appearance for client_internal with no disclosure on file.
- REQ-10 substantively alters a person's appearance for social_public with no disclosure on file.
- REQ-30 substantively alters a person's appearance for print_for_sale with no disclosure on file.
- REQ-46 substantively alters a person's appearance for client_internal with no disclosure on file.
- REQ-50 substantively alters a person's appearance for print_for_sale with no disclosure on file.
- REQ-61 substantively alters a person's appearance for client_internal with no disclosure on file.

## What the policy clears

**The personal-use allowance (§3).** REQ-01, REQ-22, REQ-32, REQ-39, REQ-41 composite a licensed persona and are
logged `personal_only`, so §3 clears them on the allowance alone, whatever the
register says. The allowance releases §3 and nothing else: REQ-32 still carries
`MISSING_MINOR_CONSENT`, and REQ-04, REQ-19 and REQ-28 are still
`THIRD_PARTY_BACKGROUND_UNLICENSED` on personal-only requests.

**Supersession cuts both ways (§2).** Two register rows replace earlier ones, and
the replacement's terms govern every request citing either id.

- **LIC-109 supersedes LIC-103** (Rook and Raven) and runs to 2027-03-31. LIC-103
  itself ended 2026-03-30, one day before the audit date, but its own dates no
  longer decide anything — so REQ-05, which cites LIC-103 at `social_public`,
  raises **no** character finding. Reading LIC-103 on its face wrongly adds one.
- **LIC-110 supersedes LIC-105** (Old Quarry Skyline) and runs to 2027-12-31, but
  it narrows the scope from `all` to `print_for_sale` alone. REQ-18 cites LIC-105
  at `print_for_sale` and is still covered; REQ-28 cites the same licence at
  `personal_only` and is **not**, so it carries
  `THIRD_PARTY_BACKGROUND_UNLICENSED`. A renewal is not automatically the more
  generous of the two.

**Licences that do reach their request.** LIC-102 expires on 2026-03-31 — the
audit date itself — so it is still current, and REQ-02 and REQ-27 raise no
character finding; both are flagged only for routing. REQ-09 runs Ember Knight
under LIC-104, which names `print_for_sale`, so it is clean where REQ-10 — the
same property at `social_public` — is not.

**Requests that look loaded and are clean.** REQ-06 carries a licensed persona, a
public channel and a substantive alteration, and clears all three: LIC-101 names
`social_public`, ACC-02's active agreement covers that channel, and the
disclosure is on file. REQ-11's `publicity` consent expires on 2026-03-31 and is
therefore current. REQ-12 and REQ-07 are `client_internal`, which is neither
public nor paid and never routes; REQ-07's substantive alteration owes no
disclosure at that distribution. REQ-24 alters substantively for `personal_only`
and owes none either.

**The one licence that simply lapsed.** LIC-106 (Aurora Ridge Panorama) ended
2026-02-28 and nothing supersedes it, so it clears nothing: REQ-05 and REQ-19 are
both `THIRD_PARTY_BACKGROUND_UNLICENSED` on its account.

## Accounts whose master agreement has lapsed

- **ACC-04 (Birchwood School Yearbook)** — a `studio_partner` account listing `social_public`, but the agreement has lapsed. A
  lapsed agreement covers nothing, so its public and paid requests route like
  any uncovered account's: REQ-14, REQ-68.
- **ACC-08 (Ridgeway Sports Club)** — a `press_agency` account listing `social_public;print_for_sale`, but the agreement has lapsed. A
  lapsed agreement covers nothing, so its public and paid requests route like
  any uncovered account's: REQ-30, REQ-66.
- **ACC-11 (Kestrel Sports Media)** — a `press_agency` account listing `print_for_sale`, but the agreement has lapsed. A
  lapsed agreement covers nothing, so its public and paid requests route like
  any uncovered account's: REQ-43, REQ-44, REQ-45.

Account type does not clear a channel by itself: ACC-08 is a `press_agency` and
routes exactly as consumer account ACC-07 does.

## Escalation (§8)

The threshold is not given anywhere: it is the batch-wide flagged share, which
only exists once the audit is finished. Across the 62 audited requests, 38 carry
at least one finding — a batch share of **38/62 = 0.6129**. An account escalates
when its own flagged share is strictly greater than that, or when any single one
of its requests carries three or more findings.

- **ACC-01 — none.** Flagged share 3/6 = 0.5000, not above the batch 0.6129, and its deepest request carries 2 finding(s): neither limb of §8 is met.
- **ACC-02 — ESCALATION_REQUIRED.** flagged share 4/6 = 0.6667, above the batch 0.6129; REQ with 3 findings meets the second limb too.
- **ACC-03 — ESCALATION_REQUIRED.** flagged share 3/6 = 0.5000 is *not* above the batch 0.6129, but one request carries 3 findings.
- **ACC-04 — none.** Flagged share 2/4 = 0.5000, not above the batch 0.6129, and its deepest request carries 2 finding(s): neither limb of §8 is met.
- **ACC-05 — ESCALATION_REQUIRED.** flagged share 4/6 = 0.6667, above the batch 0.6129.
- **ACC-06 — none.** Flagged share 3/6 = 0.5000, not above the batch 0.6129, and its deepest request carries 2 finding(s): neither limb of §8 is met.
- **ACC-07 — none.** Flagged share 3/5 = 0.6000, not above the batch 0.6129, and its deepest request carries 2 finding(s): neither limb of §8 is met.
- **ACC-08 — ESCALATION_REQUIRED.** flagged share 3/5 = 0.6000 is *not* above the batch 0.6129, but one request carries 3 findings.
- **ACC-09 — none.** Flagged share 3/5 = 0.6000, not above the batch 0.6129, and its deepest request carries 1 finding(s): neither limb of §8 is met.
- **ACC-10 — none.** Flagged share 2/4 = 0.5000, not above the batch 0.6129, and its deepest request carries 2 finding(s): neither limb of §8 is met.
- **ACC-11 — ESCALATION_REQUIRED.** flagged share 4/4 = 1.0000, above the batch 0.6129.
- **ACC-12 — ESCALATION_REQUIRED.** flagged share 4/5 = 0.8000, above the batch 0.6129.

Escalation is a property of the account. It is not a finding against any request,
and it is counted from this audit rather than taken from elsewhere.
