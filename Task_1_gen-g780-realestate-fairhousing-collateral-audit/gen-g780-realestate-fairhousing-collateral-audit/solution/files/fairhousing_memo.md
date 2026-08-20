# Seller's-book fair-housing audit - 30 sections

8 sections are clean. 22 carry at least one finding.

## The required class list

Everything below turns on which classes the disclosure is required to name. RE-FH-9 s2 lists
nine. RE-FH-9 s5a adds **marital status** and **source of income**, so for a book
entering print this quarter the required list is eleven. s5a says plainly that our
standing disclosure paragraph predates it, and that the audit runs against the amended list
rather than against whatever the book happens to carry.

That single point decides most of this audit, because several sections carry the old
nine-class notice and read as compliant until you measure them against eleven.

## Personal-narrative solicitation (s1) - SEC-02, SEC-07, SEC-08, SEC-17, SEC-24, SEC-27, SEC-29

Each of these invites the buyer to submit a personal narrative tied to their identity. All
are `PROHIBITED_PERSONAL_NARRATIVE`.

The s3 exemption never reaches these. It exempts from s2 and nothing else, so a section can
carry a perfectly compliant notice and still be flagged here.

## Protected-class language (s2) - SEC-03, SEC-04, SEC-07, SEC-09, SEC-11, SEC-12, SEC-14, SEC-15, SEC-16, SEC-17, SEC-19, SEC-22, SEC-23, SEC-25

Two different routes into this finding.

Some sections name protected classes, or proxies for them, in their own marketing prose -
describing the street by the households on it, or naming churches and parish schools. That
text is never covered by s3.

The rest carry an abridged notice. An abridged notice earns no exemption at all, so the
classes it does name fall under s2 in the ordinary way. This is where the stale nine-class
notices land, including the brokerage's own disclosure_block sections - being the disclosure
does not help if the disclosure is out of date.

Every section listed above is `PROTECTED_CLASS_LANGUAGE`.

## Missing disclaimer (s4) - SEC-05, SEC-07, SEC-09, SEC-11, SEC-12, SEC-14, SEC-15, SEC-16, SEC-21, SEC-23, SEC-30

s5b extends s4 responsibility from closing_page to agent_bio as well, so the
responsible set is both roles. A responsible section carrying no notice, or an abridged one,
is `DISCLAIMER_MISSING`. Sections carrying all eleven classes are clear.

## The sections that are clean, and why

SEC-10 and SEC-13 both carry the full eleven-class notice. SEC-10 is a closing_page and
SEC-13 an agent_bio, so both are responsible under s4 and both satisfy it; because the notice
is complete, s3 exempts that text from s2. They contain eleven protected-class terms each and
are correctly clean.

The remaining clean sections are plain listing copy in roles s4 does not reach.
