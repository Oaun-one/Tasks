# Composite photo-edit request intake policy (INT-09)

Binding for every request logged in `composite_request_log.csv`.

## 1. Licensed-character use

A request that composites a copyrighted or trademarked fictional persona into a customer
photo is `UNLICENSED_CHARACTER_USE`, **unless** the composite is for the customer's
strictly personal, non-commercial use with no public or paid distribution** — in that case
it falls under the personal-use allowance and is not a defect. Flagging a personal,
non-distributed request for licensed-character use is the commonest false positive.

## 2. Third-party backgrounds

A request that composites in a background sourced from another party's copyrighted photo
(not the customer's own, and not a properly licensed stock image) without a license on
file is `THIRD_PARTY_BACKGROUND_UNLICENSED`.

## 3. Minor consent

Any request involving a minor's likeness requires a parent or guardian consent record on
file. Its absence is `MISSING_MINOR_CONSENT`.

## 4. Commercial distribution

Any request intended for public social posting or print-for-sale distribution is
`COMMERCIAL_DISTRIBUTION_FLAG` (routed to a separate rights-clearance workflow),
regardless of whether a licensed character is involved.

## Finding names

`UNLICENSED_CHARACTER_USE`, `THIRD_PARTY_BACKGROUND_UNLICENSED`, `MISSING_MINOR_CONSENT`,
`COMMERCIAL_DISTRIBUTION_FLAG`, `none`.
