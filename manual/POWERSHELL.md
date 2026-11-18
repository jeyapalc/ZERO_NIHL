# PowerShell: build a wordlist and find document matches

Use PowerShell 5.1 or 7. Run the commands from the extracted repository root. Quote paths containing spaces. Scripts never download repository contents or send document text anywhere.

## 1. Build a local wordlist

For this repository:

```powershell
.\manual\Build-WordList.ps1 -OutputPath .\wordlist.tsv
```

For all three repositories, extract/clone them into sibling folders and run:

```powershell
.\manual\Build-WordList.ps1 -RepositoryPaths '..\ZERO_NIHL','..\ZERO_FAITH','..\ZERO_NAZ' -OutputPath .\all-words.tsv
```

Add `-IncludeRegistry` to include English/French Canadian entity names. The shared registry is copied into each repository; combined results keep each repository's provenance, so the same name can appear more than once. Counts are word/source rows, not distinct organizations.

The builder reads only canonical `terms_excel.tsv` and, optionally, `canada_lte_excel.tsv`. It preserves all literal vocabulary rows, including disabled ones, without collapsing spelling or punctuation differences. Output includes term, enabled switch, tier, ID, language, context, citations, repository, and source file. If one repository is missing, the command fails rather than silently building a partial list.

## 2. Search a document

Search the enabled rows:

```powershell
.\manual\Find-WordList.ps1 -WordListPath .\wordlist.tsv -DocumentPath 'C:\Documents\target.txt' -OutputPath .\matches.csv
```

To deliberately search every nonempty row, including disabled contextual/research words:

```powershell
.\manual\Find-WordList.ps1 -WordListPath .\all-words.tsv -DocumentPath 'C:\Documents\target.txt' -AllTerms -WholeWord -OutputPath .\all-matches.csv
```

`-AllTerms` does not add words that are absent from the selected list. The default matching is case-insensitive literal substring matching. `-CaseSensitive` changes case handling; `-WholeWord` requires no adjacent Unicode letter, number, or underscore. Punctuation in terms is escaped, so `a*b` is literal. Matching preserves accents and does not normalize whitespace, spelling, or Unicode variants. Phrases cannot span lines. Whole-word matching also works with phrases, but extraction can split a phrase across lines and cause a miss.

For multiple files:

```powershell
$documents = @(Get-ChildItem -LiteralPath 'C:\Documents\review' -File -Filter '*.txt' | Select-Object -ExpandProperty FullName)
.\manual\Find-WordList.ps1 -WordListPath .\wordlist.tsv -DocumentPath $documents -AllTerms -OutputPath .\folder-matches.csv
```

An empty file list or a list with no enabled terms produces a clear error. Use a new output path or `-Force` to replace a previous result. The output path cannot be the wordlist or an input document.

## 3. Read the report

Import the CSV into Excel through **Data > From Text/CSV**, with UTF-8 and all columns as Text. Each row describes one term/source row found on one document line, including the first occurrence's 1-based column. Repeated occurrences of the same term on a line produce one row; separate provenance rows remain separate.

Columns include `document_path`, `line_number`, `column`, `term`, `entry_id`, `source_urls`, `source_repository`, `context_note`, `match_mode`, and `text`. Spreadsheet formula-looking text is prefixed with an apostrophe when exported. A report with no matches still contains column headers. Review each line in its original document and open its source citation.

## 4. Single-term quick check

```powershell
Select-String -LiteralPath 'C:\Documents\target.txt' -Pattern 'example term' -SimpleMatch -Encoding UTF8
```

Use `-SimpleMatch` for literal terms rather than interpreting them as regex. This quick command does not attach source citations; use the supplied script for cited reports. See [Microsoft Select-String documentation](https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/select-string).

If local script execution is blocked, follow your organization's PowerShell policy. For a downloaded script you have inspected and trust, Windows file Properties may offer **Unblock**. These instructions do not require changing machine-wide execution policy.

## Updating

Download/pull updated repositories, regenerate a fresh wordlist, and reapply your chosen enabled rows. Keep a copy of the wordlist with each result so you know which vocabulary was searched. Python maintainers regenerate canonical exports with `python tools/build.py` and run `python -m unittest discover -s tests -v`; ordinary users can use the checked-in TSV files without Python.
