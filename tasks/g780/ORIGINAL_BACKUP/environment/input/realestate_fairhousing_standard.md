# Real-estate marketing collateral fair-housing standard (RE-FH-9)

Binding for `seller_book_sections.csv`. `finding` is one of
`PROHIBITED_PERSONAL_NARRATIVE`, `PROTECTED_CLASS_LANGUAGE`, `DISCLAIMER_MISSING`, or
`none`. A section may carry more than one finding, joined with `|`.

## 1. Personal-narrative solicitation

A section soliciting or presenting a buyer "love letter" or similar personal narrative
tied to buyer identity introduces fair-housing risk under RCW 49.60 and the federal Fair
Housing Act. Any such section is `PROHIBITED_PERSONAL_NARRATIVE`.

## 2. Protected-class language

A section naming protected-class-adjacent terms (family status, religion, national
origin, and similar) is `PROTECTED_CLASS_LANGUAGE`.

## 3. Mandated-disclosure exception

The brokerage's own mandated fair-housing disclosure paragraph necessarily names
protected classes in order to inform sellers of the law. A section marked as this
mandated disclosure is **exempt** from the protected-class-language rule (§2). Flagging
the mandated disclosure itself as a violation is the commonest false positive in this
audit.

## 4. Required disclaimer

Every seller's book must include the mandated fair-housing disclosure somewhere. A
section responsible for carrying it that omits it is `DISCLAIMER_MISSING`.
