# Audit — 2026-11-03

## Corrections implemented

- Added Canadian primary-source coverage and separate EN/FR legal entity registry snapshots to every project.
- Reconciled all 89 English feed entries with the official English web-register anchors. Captured 89 French entries separately. These are 89 localized rows per language, not 178 distinct entities.
- Found that EN/FR feed IDs identify different organizations; language namespaces prevent erroneous joins.
- Preserved official alias text unsplit. Canonical names are exported; unreliable automatic alias splitting is avoided.
- Kept listed-entity status separate from research labels, speaker intent, membership, and category assignment. Full LTE coverage is a separate file, not injected into each project's ideology-specific filter.
- Removed named assessment-instrument references and obsolete initial dataset generators from current project files; retained general behavioral principles.
- Disabled broad research phrases in contextual reference matchers unless specifically opted into. Kept generic numbers, initials, and LTE names disabled by default in Excel imports.
- Added readable catalogs, one-term-per-row TSV with provenance, literal pipe lists, quoted OR lists, and Excel guidance.
- Added Canadian white-nationalist network references supported by dated Canadian research, and Canadian NVE safeguarding/chemical-security sources.

## Limits and remaining review

The source feeds report 2025-12-10 as their update date; the snapshot was fetched and checked against the English web register on 2026-11-03. The French feed is retained separately; it has not been reconciled against a French web-register snapshot. Do not assume legal status is timeless or identical across jurisdictions. Live changes require refresh and review.

This is a source/provenance and implementation audit, not independent subject-matter certification. Some existing sources are search-index excerpts, dated reports, or advocacy commentary; records disclose those limits. German translations need expert review; official Canadian entity names add French coverage but the entire behavioral vocabulary is not professionally translated into French. More Canadian regional slang and independently corroborated historic organizations remain gaps.

The matcher is literal retrieval. No statistical precision/recall study, deployment evaluation, clinical validation, or desktop Excel execution has been performed. Source citations support association, not every interpretation or inferred user intent. Original releases remain in Git history; current content removes the requested named references without rewriting published history.

## Suggested complementary collections

- **ZERO_CA_LTE**: maintain the shared bilingual Canadian entity registry as a standalone package, with reviewed updates and designation diffs.
- **ZERO_COERCE**: coercion, sextortion, doxing, swatting, and recruitment-to-harm vocabulary, with Canadian safeguarding sources.
- **ZERO_CONTEXT**: benign counterexamples, news/quotation/victim-disclosure fixtures, and identity/religion false-positive tests. A test corpus, not a blanket allowlist that could hide abuse.
- **ZERO_RMVE**: separately sourced religiously motivated violent-extremism collection if desired; protect ordinary religious practice and avoid conflating it with IMVE.

Recommended family name: **ZERO Moderation Review Lexicons**. They contain terms to inspect, not universally prohibited words.
