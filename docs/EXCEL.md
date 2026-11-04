# Excel and readable exports

Use `lists/terms_readable.txt` or CATALOG.md to read the terms. `terms_or.txt` uses quoted Boolean OR separators; `terms_pipe.txt` uses literal pipes. These formats are not Excel formulas, executable regex, or universal search syntax. Adapt escaping to your destination tool. `canada_lte_en_or.txt` and `canada_lte_fr_or.txt` contain official names only; aliases remain unsplit in the registry TSV/JSON.

## Excel workflow

1. Import `lists/terms_excel.tsv` through **Data > From Text/CSV** with UTF-8 and Tab delimiters. Files include a UTF-8 BOM for compatibility. Keep IDs and terms as text, especially numeric codes.
2. Convert the import to an Excel Table named `Terms`. It includes `term`, `enabled`, `tier`, `category`, `entry_id`, `language`, `context_note`, and `source_urls`. For Canadian LTEs use `canada_lte_excel.tsv` as a separate table.
3. Review the vocabulary and set selected `enabled` cells to `TRUE`. Only distinctive ZERO_NAZ terms begin enabled. Contextual terms, generic numbers, short initials, research-only phrases, and all legal entity names begin disabled.
4. For dataset text in A2, place the formula below in the flag column and fill down. It returns REVIEW, never an automatic removal decision.

```excel
=IF(SUMPRODUCT(--(Terms[term]<>""),--(UPPER(Terms[enabled]&"")="TRUE"),--ISNUMBER(SEARCH(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Terms[term],"~","~~"),"*","~*"),"?","~?"),A2)))>0,"REVIEW","")
```

The formula is case-insensitive literal **substring** search and escapes Excel search wildcards. It has no word boundaries, Unicode normalization, intent detection, or context logic. Enabling 18 can match 2018; enabling SS can match ordinary words. Use the Python reference matcher when Unicode boundaries and normalization are needed. Excel function names and argument separators may vary by locale. The formula was reviewed but not executed in desktop Excel in this environment.

These are review vocabularies, not a validated list of universally bad words. Reporting, quotations, historical discussion, victim disclosure, religion, identity, politics, and ordinary numbers can all produce legitimate matches. Review tier and source must accompany every flag. Do not automatically exclude a victim or news item because it contains an entity name.
