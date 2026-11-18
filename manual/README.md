# Find wordlist terms in a document

Start with [Excel](EXCEL.md) for a single document or [PowerShell](POWERSHELL.md) for files and repeatable reports. Both workflows produce mentions to review, with citations.

## Files

| File | Purpose |
| --- | --- |
| [EXCEL.md](EXCEL.md) | Import the wordlist, use FIND/SEARCH, and display matching rows |
| [POWERSHELL.md](POWERSHELL.md) | Build a local wordlist and scan documents |
| [Build-WordList.ps1](Build-WordList.ps1) | Combine local repository exports while preserving provenance |
| [Find-WordList.ps1](Find-WordList.ps1) | Find literal terms and save an Excel-readable CSV report |
| [CITATIONS.md](CITATIONS.md) | Check sources, completeness, and known coverage limits |
| [examples/terms.tsv](examples/terms.tsv) | Small synthetic test list, not moderation vocabulary |
| [examples/document.txt](examples/document.txt) | Sample document with known matches |

Download the repository ZIP while signed into GitHub and extract it, or clone it using your usual authenticated Git setup. These scripts read local files; they do not upload documents or need GitHub tokens. Keep this folder inside the extracted repository.

The source wordlist is [masterlist.tsv](../lists/masterlist.tsv). It includes every text-compatible canonical term and explicit alias in this repository, including disabled contextual/research terms. [Canadian entity names](../lists/canada_lte_excel.tsv) are available separately and can be included with `-IncludeRegistry`. Inclusion in a file and enabling it for a search are separate choices.

Use your policy to select terms. A match records text, not intent or a reason to automatically ban someone. Short terms and numbers can have unrelated meanings. See [coverage and citations](CITATIONS.md) before interpreting results.

## Supported document input

- PowerShell reads UTF-8 `.txt`, `.md`, `.csv`, `.tsv`, and `.log` files. CSV/TSV files are scanned as text lines, including headers and delimiters.
- For Word, save a copy as plain text with UTF-8 encoding. For PDF, export to text using your PDF application; scanned PDFs need OCR. Check the extracted text against the original. Do not rename a binary file to `.txt`.
- The scripts do not extract DOCX/PDF contents, search images, or provide OCR. PowerShell line numbers refer to the exported text, not Word/PDF page numbers.
- Excel formulas search text already imported into cells. A filename in a cell does not load that document. For long documents, use the PowerShell report or split text into paragraphs/lines in separate cells.

## Quick example

Run from the repository root in PowerShell:

```powershell
.\manual\Find-WordList.ps1 -WordListPath .\manual\examples\terms.tsv -DocumentPath .\manual\examples\document.txt -OutputPath .\example-matches.csv
```

Expected: three report rows: `alpha` on lines 1 and 3, and literal `a*b` on line 2. The disabled `18` is not searched. Add `-WholeWord` to remove the `alpha` match inside `alphabet` on line 3. Use a new output filename for each run, or explicitly add `-Force` to replace an old report.

For extraction-based document review, see [evidence triage](EVIDENCE_TRIAGE.md). Keep case data outside the repository.
