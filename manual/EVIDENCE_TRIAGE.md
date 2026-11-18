# Review document hits against their source artifacts

A wordlist hit is a retrieval result. It does not establish who performed an action, whether a purchase occurred, or why it occurred. Use the report to locate records for examination, then document observations separately from interpretations.

## Suggested review fields

| Field | Record |
| --- | --- |
| Evidence reference | Internal exhibit/artifact ID and location in the preserved source |
| Observed record | Exact query, page visit, cart, order confirmation, payment, or delivery artifact |
| Provenance | Source database/file/record; acquisition reference; tool and version |
| Time | Original value, timestamp meaning, timezone, conversion, known uncertainty |
| Attribution | Evidence linking the record to an account/device/person; shared access limitations |
| Corroboration | Independent records supporting the observation; distinguish duplicate parsing from separate evidence |
| Alternative explanation | Legitimate activity, research, quotation, shared-device use, cancellation, or contradictory evidence |
| Interpretation | Narrow statement of what the evidence supports and what it does not |
| Further review | Specific missing evidence or specialist examination needed |
| Reviewer | Analyst, date, and verification status |

## Synthetic example

**Observation:** an exported browser record contains a product page. An unrelated order email mentions the same ordinary product.

**Supported:** the extraction contains those records, subject to validation of their source and timestamps.

**Not established by those records alone:** who opened the page, whether the order was paid or delivered, possession of the item, intended use, or any connection to a device or offence. A cancelled order or documented legitimate use may contradict the initial hypothesis.

If physical-device interpretation is required, record the qualified examiner's conclusion and the exhibits supporting it. A keyword or combination of purchases must not be substituted for that examination. This manual does not map chemicals, components, acquisition queries, or purchases to explosive designs.

## Keep case data local

Use copies/exported text under your normal evidence-handling procedures. Preserve original artifacts and document any transformation. CSV line numbers identify the export, not necessarily the original application record. Keep real case documents, extraction archives, reports, screenshots, identifiers, and reviewer notes outside the repository. The bundled example files are synthetic.

Public references:

- [NIST SP 800-86: forensic process, correlation, documentation, and reporting](https://csrc.nist.gov/pubs/sp/800/86/final)
- [NIJ: Forensic Examination of Digital Evidence](https://nij.ojp.gov/library/publications/forensic-examination-digital-evidence-guide-law-enforcement)
- [Cellebrite: browser artifact examination](https://cellebrite.com/en/blog/how-to-discover-artifacts-in-ufed-physical-analyzer-part-3/)

These public references do not grant permission to redistribute vendor training materials, customer data, or case files. The scripts scan exported text; they are not validated parsers for proprietary forensic extraction formats.
