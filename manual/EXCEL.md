# Excel: find matches and keep their citations

## 1. Import words as text

1. Open a blank workbook. Use **Data > From Text/CSV** and choose `lists/masterlist.tsv` in the repository (or a combined TSV built with the PowerShell instructions).
2. Choose UTF-8 and Tab as the delimiter. Select **Transform Data**, remove any automatic Changed Type step, and set all imported columns to **Text** before loading. This preserves numeric terms, IDs, and literal characters.
3. Load as a table and name it `Terms` using **Table Design > Table Name**. Keep `term`, `enabled`, `entry_id`, `language`, and `source_urls` visible. Keep the other context columns.
4. Set `enabled` to `TRUE` only for the rows you want to search. To deliberately search all supplied words, fill that column with `TRUE` in your workbook copy. Disabled words are still present in the list.

Use the canonical table rather than the Boolean OR, pipe-separated, or readable TXT files. Those are display/query formats, not one-word-per-row tables.

## 2. Search one document against every term

Create a worksheet named `Document`. Format cell A2 as Text, then paste a short document or paragraph into A2. On the `Terms` table add a `found` column and enter:

```excel
=IF(AND([@term]<>"",UPPER([@enabled]&"")="TRUE",ISNUMBER(FIND(LOWER([@term]),LOWER(Document!$A$2)))),"MATCH","")
```

Excel fills the formula down the table. Filter `found` to `MATCH`. Each matching row retains its ID, context, and citations. This is a literal substring search ignoring case: lowercasing both arguments makes FIND case-insensitive, while `*`, `?`, and `~` stay literal. For case-sensitive matching, use:

```excel
=IF(AND([@term]<>"",UPPER([@enabled]&"")="TRUE",ISNUMBER(FIND([@term],Document!$A$2))),"MATCH","")
```

Do not paste a long file into one cell: Excel limits cell text to 32,767 characters. Use the multi-row workflow below or PowerShell.

## 3. Flag many paragraphs or lines

On `Document`, put `document_id` in A1 and `text` in B1, then one paragraph or line per row. Put `review` in C1. In C2 enter and fill down:

```excel
=IF(SUMPRODUCT(--(Terms[term]<>""),--(UPPER(Terms[enabled]&"")="TRUE"),--ISNUMBER(FIND(LOWER(Terms[term]),LOWER(B2))))>0,"REVIEW","")
```

This reports whether any enabled term appears in each paragraph. For the exact matched terms and their citations across many lines, use the PowerShell CSV report. Keep the document ID alongside text when sorting/filtering.

## SEARCH alternative

SEARCH ignores case but treats `*` and `?` as wildcards. Escape them and `~` when using arbitrary wordlist terms:

```excel
=IF(AND([@term]<>"",UPPER([@enabled]&"")="TRUE",ISNUMBER(SEARCH(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE([@term],"~","~~"),"*","~*"),"?","~?"),Document!$A$2))),"MATCH","")
```

## Check your setup

Import `manual/examples/terms.tsv` as `Terms`, set Document!A2 to `ALPHA and a*b`, and confirm that `alpha` and `a*b` match. Set A2 to `alphabet`: the substring formula matches `alpha`. A2=`axb` must not match `a*b`. A2=`18` must not match while that term is disabled. Blank term rows must never match.

Formulas do not enforce whole-word boundaries, normalize Unicode variants, infer context, or search across cells. `18` can match `2018`; `alpha` can match `alphabet`. Use `-WholeWord` in PowerShell for boundaries. Translated Excel installations may use localized function names and semicolons instead of commas. These formulas are checked against Microsoft documentation; desktop Excel execution is not part of the automated tests.

## Microsoft references

- [FIND and SEARCH behavior](https://support.microsoft.com/en-us/excel/how-to-correct-a-value-error-in-find-findb-and-search-searchb-functions)
- [SEARCH syntax and wildcard escaping](https://support.microsoft.com/en-us/excel/functions/search-function)
- [Excel specifications and limits](https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3)
