# Real-estate marketing collateral fair-housing standard (RE-FH-9)

Binding for `seller_book_sections.csv`. Every section carries a `role`, which some rules
below depend on. `finding` is one of `PROHIBITED_PERSONAL_NARRATIVE`,
`PROTECTED_CLASS_LANGUAGE`, `DISCLAIMER_MISSING`, or `none`. A section may carry more than
one finding, joined with `|`.

## 1. Personal-narrative solicitation

A section soliciting or presenting a buyer "love letter" or similar personal narrative tied
to buyer identity introduces fair-housing risk under RCW 49.60 and the federal Fair Housing
Act. Any such section is `PROHIBITED_PERSONAL_NARRATIVE`, whatever its role.

## 2. Protected-class language

A section naming protected-class-adjacent terms is `PROTECTED_CLASS_LANGUAGE`. The classes
this standard protects are: race, colour, religion, sex, familial status, national origin,
disability, sexual orientation and veteran status.

Proxies count. Naming houses of worship, parish or faith schools, or describing a street by
the kind of household that lives on it reaches familial status and religion just as the bare
terms do.

## 3. Mandated-disclosure exception

The fair-housing disclosure necessarily names protected classes in order to inform sellers
of the law. A section is exempt from §2 for disclosure text it carries **only if that notice
names every class the disclosure is required to name**. Check the required list against this
standard in full, amendments included.

The exemption is narrow, in two ways:

- An abridged notice — one naming some but not all of the required classes — earns no
  exemption at all, whatever the section's role and however official it looks.
- It exempts from §2 and nothing else. Every other rule continues to apply to the section on
  its own terms.

Protected-class terms a section uses in its own prose, outside the notice, are never covered.

## 4. Required disclaimer

Sections in a role responsible for carrying the disclosure must carry a compliant notice —
one naming every required class. A responsible section that carries no notice, or an
abridged one, is `DISCLAIMER_MISSING`. As drafted, the responsible role is `closing_page`;
the amendments below may extend that. Sections in other roles are not assessed here.

## 5. 2026 amendments

Following this year's amendments to RCW 49.60, the following changes apply to every seller's
book entering print from Q1 2026. Where they conflict with the sections above, these govern.

**5a. Two classes added to the required disclosure.** The disclosure carried in our collateral
must now name **marital status** and **source of income** in addition to the classes listed at
§2. A notice omitting either is abridged for the purposes of §3 and §4, whatever else it
contains.

Legal are aware that the standing disclosure paragraph in circulation predates this
amendment. Until the template is reissued, audit against the amended list rather than against
whatever the book happens to carry.

**5b. Agent biographies are now in scope for §4.** `agent_bio` sections have historically
escaped the disclaimer requirement. They no longer do; they carry the same responsibility as
`closing_page` sections.
