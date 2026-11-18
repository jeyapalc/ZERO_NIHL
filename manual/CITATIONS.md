# Citation and coverage guide

## Trace a match to its evidence

1. Read `entry_id` and `source_urls` on the matched row. Combined lists also identify the source repository and file.
2. Find the same ID in [canonical vocabulary](../data/terms.json). Read its meaning, context, and source IDs. The matching schema depends on the repository.
3. Resolve those source IDs in [data/sources.json](../data/sources.json). Each source records its publisher, title, exact URL, research date, and evidence-access limits. A project translation or query phrase is not necessarily a quotation from that source.
4. Canadian registry rows link directly to their official record. Their snapshot date and raw alias text are in [lte_entities.json](../data/canada/lte_entities.json); see [Canadian coverage](../docs/CANADA.md) for reconciliation limits. Check the official page before relying on current legal status.

The wordlist builders preserve citations from the dataset. They do not independently certify every source or recheck live pages. Access restrictions, excerpt-only evidence, project translations, and dated research remain material limitations described in the source records and [audit](../docs/AUDIT.md).

## What completeness means

The automated coverage test checks every explicit text-compatible term/alias in the canonical vocabulary against `lists/masterlist.tsv`, including disabled terms, and checks its source URLs. It also checks every canonical English/French registry name against the separate registry TSV. Builds fail if rows or citation mappings are missing or unexpected.

This is completeness against the checked-in data, not an exhaustive dictionary of banned words. No additional policy ban-word list was supplied. Additions need explicit terms, context, and supporting sources before inclusion.

Known exclusions:

- ZERO_NAZ visual-only entries and structural patterns such as triple parentheses are not literal words. Its Python matcher handles the structural pattern; image/gesture recognition is outside this list.
- Canadian `official_aliases_raw` text is preserved as source metadata. It is not automatically split into individual searchable aliases because punctuation and conjunctions can be part of names. `-IncludeRegistry` searches canonical names, not every alias in the raw paragraph. Review and add individual aliases with their official citation when needed.
- Observation prompts in `data/indicators.json` describe questions for human review, not terms to search automatically.
- Unlisted spelling variants, obfuscations, translations, phrases broken across lines, and text missed during OCR are not guaranteed matches.

## Maintaining citations

Edit canonical JSON, retain stable IDs, cite the exact supporting page, describe whether wording is source-attested or project-authored, and record access limitations and the actual review date. Regenerate exports and run the coverage tests. Do not silently turn ordinary beliefs, identities, or ambiguous numbers into conclusive classifications.
