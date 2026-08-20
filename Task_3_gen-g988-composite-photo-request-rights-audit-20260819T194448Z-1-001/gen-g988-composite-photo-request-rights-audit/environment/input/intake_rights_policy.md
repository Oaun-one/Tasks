# INT-09 — composite photo-edit request intake rights policy

Shop policy, revision 4. Supersedes INT-08. Binding for every request logged in
`composite_request_log.csv`.

## §1 Scope, audit date and how findings are reported

Every **audited** request in the log is checked against §3 to §7. Every client account
with audited requests is checked against §8.

**Withdrawn requests are not audited.** A request whose `intake_status` is `withdrawn`
was pulled by the client before it reached production. It has no finding and no verdict:
it does not appear in the audit at all, and it counts towards nothing — not the request
totals, not its own account's counts, and not the batch-wide share §8 is measured
against. Every figure in this audit is over audited requests only. The withdrawn rows are
left in the log so that the batch can be reconciled against intake, not so that they can
be assessed.

A request carries one finding code for each rule it breaches. A request may breach
several rules at once and every breach is reported; a request that breaches none is
reported as clean.

**This audit is run as of 2026-03-31.** Every currency test in this policy is made
against that date and against nothing else. A licence or consent record whose validity
ends **on** 2026-03-31 is still current on the audit date; one that ended before it is
not.

Two of the rules below take their answer from a record held outside the request log —
the licence register for §3 and §4, the account's master agreement for §6. A request
reaches its account through `account_id`, and the account's agreement is in
`client_accounts.csv`. A request reaches a licence through the licence id on its own
row, and the licence is in `licensed_property_register.csv`.

## §2 When a licence covers a request

`licensed_property_register.csv` is the shop's register of the rights it holds. A
licence **covers** a request only when all four of these hold:

1. the licence id on the request's row appears in the register;
2. the licence's `license_type` matches the use being tested — `character` for §3,
   `background` for §4;
3. the licence's `covers_distribution` lists the request's own `intended_distribution`,
   or is the single value `all`. `covers_distribution` is a `;`-joined list and it is
   exhaustive: a distribution it does not name is a distribution the licence does not
   reach;
4. the licence's `valid_until` is on or after the audit date.

A licence that fails any one of the four does not cover the request, and the use it was
meant to clear is unlicensed. A request whose licence id is `none` has no licence.

**Superseded licences.** A register row may name, in `supersedes`, the id of an earlier
licence it replaces; a row that replaces nothing carries `none`. Where a licence has been
superseded, the superseding row's terms — its `covers_distribution` and its `valid_until`
— are the terms that govern, and they govern every request citing **either** id. The
superseded row is kept in the register for the audit trail; its own dates and scope no
longer decide anything.

A renewal can widen a licence and it can narrow one. Do not assume a superseding row is
the more generous of the two: read its terms and apply them.

## §3 Licensed-character use — `UNLICENSED_CHARACTER_USE`

§3 applies to a request that composites a copyrighted or trademarked fictional persona
into a customer photo — that is, a request whose `character_property` is not `none`. A
request with no character property cannot breach §3 whatever else is on its row.

Such a request is `UNLICENSED_CHARACTER_USE` unless it is cleared by **either** of:

- **the licence.** A `character` licence covering the request in the sense of §2.
- **the personal-use allowance.** The composite is for the customer's strictly personal,
  non-commercial use with no distribution of any kind — that is, the request's
  `intended_distribution` is `personal_only`. Flagging a personal, non-distributed
  request for licensed-character use is the commonest false positive on this audit.

The two clear independently: a personal-only request needs no licence, and a request
with a covering licence needs no allowance.

**The scope of the allowance.** The personal-use allowance releases a request from §3
and from nothing else. It is not a general pardon: a personal-only request is still
audited against §4, §5, §6 and §7 exactly as any other request is.

`client_internal` is **not** personal use. A composite circulated inside a client's
organisation is distributed, and the allowance does not reach it. Such a request is
cleared under §3 only by a licence that names `client_internal`.

## §4 Third-party backgrounds — `THIRD_PARTY_BACKGROUND_UNLICENSED`

Each request records where its background came from, in `background_source`:

| `background_source` | §4 verdict |
| --- | --- |
| `customer_original` | never a finding — the customer shot it |
| `third_party_unlicensed` | always `THIRD_PARTY_BACKGROUND_UNLICENSED` |
| `third_party_licensed` | a finding unless a `background` licence covers the request in the sense of §2 |

A request logged as `third_party_unlicensed` is unlicensed on its own record. Some such
rows carry a licence id anyway, left over from intake; that id does not clear the row and
is not to be looked up.

## §5 Minor consent — `MISSING_MINOR_CONSENT`

§5 applies to a request whose `subject_is_minor` is `True`, and to no other request.

Such a request needs a parent or guardian consent record that is present, current and
wide enough for what the composite is for. All three:

1. **present** — `minor_consent_type` is not `none`;
2. **current** — `minor_consent_valid_until` is on or after the audit date;
3. **wide enough** — a `basic` consent covers `personal_only` and `client_internal` use
   only. A `publicity` consent covers every distribution. A minor's likeness going to
   `social_public` or `print_for_sale` on a `basic` consent is not consented to.

A request failing any one of the three is `MISSING_MINOR_CONSENT`. It is one finding
however many of the three it fails.

## §6 Commercial distribution routing — `COMMERCIAL_DISTRIBUTION_FLAG`

Public or paid distribution means `social_public` or `print_for_sale`. `personal_only`
and `client_internal` are neither public nor paid, and never route.

A request for public or paid distribution is `COMMERCIAL_DISTRIBUTION_FLAG` — routed to
the separate rights-clearance workflow — unless the account it belongs to has already
cleared that channel under its master agreement. An account clears a channel when **both**:

- the account's `agreement_status` is `active`; and
- the account's `master_agreement_covers` names that distribution. It is a `;`-joined
  list, or `none` for an account with no standing coverage.

**A lapsed agreement covers nothing.** `master_agreement_covers` is still recorded for a
lapsed account, because the agreement is expected back; until it is active again the
channels it names are not cleared and its requests route like any other.

`account_type` is recorded for reporting and for who handles the account. It does not by
itself clear any distribution: a `press_agency` with a lapsed agreement routes exactly as
a `consumer` does. Take the answer from `master_agreement_covers` and `agreement_status`,
never from the type.

§6 turns on distribution and on the agreement only. A licensed character, a third-party
background or a minor on the request changes nothing about it.

## §7 Alteration disclosure — `ALTERATION_DISCLOSURE_MISSING`

A composite that substantively alters how a real person looks must carry a disclosure
label when it goes out publicly or for sale.

§7 applies to a request whose `alteration_level` is `substantive` **and** whose
`intended_distribution` is `social_public` or `print_for_sale`. Such a request is
`ALTERATION_DISCLOSURE_MISSING` unless `alteration_disclosure_on_file` is `True`.

`cosmetic` and `none` alterations never owe a disclosure, at any distribution. A
`substantive` alteration going to `personal_only` or `client_internal` never owes one
either.

§7 reads the request's `intended_distribution` as logged. Whether §6 cleared that
distribution under a master agreement is irrelevant: a pre-cleared channel is still
public or paid distribution, and the disclosure is still owed.

## §8 Account escalation — `ESCALATION_REQUIRED`

An account goes to the rights manager rather than staying with the intake desk when
**either**:

- the share of its audited requests carrying at least one finding is **strictly greater
  than** the same share taken across the whole audited batch; or
- **any single one** of its audited requests carries **three or more** findings.

The batch-wide share is not a number given to you anywhere. Work it out from the audit
you have just produced — audited requests carrying at least one finding, divided by
audited requests — and compare each account's own share against it. An account whose
share equals the batch share does not escalate on the first limb.

§8 is a property of the account, not of any request in it. `ESCALATION_REQUIRED` is never
a finding against a request, and an account that is not escalated is reported as `none`.

## Finding names

Request-level: `UNLICENSED_CHARACTER_USE`, `THIRD_PARTY_BACKGROUND_UNLICENSED`,
`MISSING_MINOR_CONSENT`, `COMMERCIAL_DISTRIBUTION_FLAG`, `ALTERATION_DISCLOSURE_MISSING`,
`none`.

Account-level: `ESCALATION_REQUIRED`, `none`.
