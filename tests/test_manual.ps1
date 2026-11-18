$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$temporary = Join-Path ([IO.Path]::GetTempPath()) ('zero-manual-test-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($temporary) | Out-Null
$scan = Join-Path $root 'manual/Find-WordList.ps1'
$terms = Join-Path $root 'manual/examples/terms.tsv'
$document = Join-Path $root 'manual/examples/document.txt'
function Assert-True($Condition, [string]$Message) { if (-not $Condition) { throw $Message } }
$output = Join-Path $temporary 'matches.csv'
& $scan -WordListPath $terms -DocumentPath $document -OutputPath $output
$rows = @(Import-Csv -LiteralPath $output)
Assert-True ($rows.Count -eq 3) 'Expected three substring rows.'
Assert-True (@($rows | Where-Object term -eq 'a*b').Count -eq 1) 'Asterisk must match literally.'
Assert-True (@($rows | Where-Object source_urls -eq 'https://example.org/alpha').Count -eq 2) 'Citations were not preserved.'
& $scan -WordListPath $terms -DocumentPath $document -WholeWord -OutputPath (Join-Path $temporary 'whole.csv')
Assert-True (@(Import-Csv -LiteralPath (Join-Path $temporary 'whole.csv')).Count -eq 2) 'Whole-word boundary failed.'
& $scan -WordListPath $terms -DocumentPath $document -CaseSensitive -OutputPath (Join-Path $temporary 'case.csv')
Assert-True (@(Import-Csv -LiteralPath (Join-Path $temporary 'case.csv')).Count -eq 2) 'Case-sensitive matching failed.'
& $scan -WordListPath $terms -DocumentPath $document -AllTerms -OutputPath (Join-Path $temporary 'all.csv')
Assert-True (@(Import-Csv -LiteralPath (Join-Path $temporary 'all.csv')).Count -eq 4) 'AllTerms failed.'
$empty = Join-Path $temporary 'empty.txt'
[IO.File]::WriteAllText($empty, 'no matching text', [Text.UTF8Encoding]::new($false))
& $scan -WordListPath $terms -DocumentPath $empty -OutputPath (Join-Path $temporary 'none.csv')
Assert-True ((Get-Content -LiteralPath (Join-Path $temporary 'none.csv') -TotalCount 1) -match 'source_urls') 'No-match report lost headers.'
$blocked = $false
try { & $scan -WordListPath $terms -DocumentPath $document -OutputPath $output } catch { $blocked = $true }
Assert-True $blocked 'Existing report was overwritten without Force.'
$blocked = $false
try { & $scan -WordListPath $terms -DocumentPath $document -OutputPath $document -Force } catch { $blocked = $true }
Assert-True $blocked 'Input document overwrite was permitted.'
$badDocument = Join-Path $temporary 'file.pdf'
[IO.File]::WriteAllText($badDocument,'not a real pdf')
$blocked = $false
try { & $scan -WordListPath $terms -DocumentPath $badDocument -OutputPath (Join-Path $temporary 'bad.csv') } catch { $blocked = $true }
Assert-True $blocked 'PDF was incorrectly treated as text.'
$formula = Join-Path $temporary 'formula.txt'
[IO.File]::WriteAllText($formula,'=alpha', [Text.UTF8Encoding]::new($false))
& $scan -WordListPath $terms -DocumentPath $formula -OutputPath (Join-Path $temporary 'formula.csv')
Assert-True ((Import-Csv -LiteralPath (Join-Path $temporary 'formula.csv')).text -eq "'=alpha") 'Formula-like content was not protected.'
$unicodeTerms = Join-Path $temporary 'unicode.tsv'
$unicodeDocument = Join-Path $temporary 'unicode.txt'
$accent = [string][char]0xE9
$term = "Qu${accent}bec"
[IO.File]::WriteAllText($unicodeTerms, "term`tenabled`tentry_id`tsource_urls`n$term`tTRUE`tunicode`thttps://example.org/unicode`n", [Text.UTF8Encoding]::new($true))
[IO.File]::WriteAllText($unicodeDocument, $term.ToUpperInvariant(), [Text.UTF8Encoding]::new($false))
& $scan -WordListPath $unicodeTerms -DocumentPath $unicodeDocument -WholeWord -OutputPath (Join-Path $temporary 'unicode.csv')
Assert-True (@(Import-Csv -LiteralPath (Join-Path $temporary 'unicode.csv')).Count -eq 1) 'Unicode match failed.'
$combined = Join-Path $temporary 'combined.tsv'
& (Join-Path $root 'manual/Build-WordList.ps1') -RepositoryPaths $root -IncludeRegistry -OutputPath $combined
$expected = @(Import-Csv -LiteralPath (Join-Path $root 'lists/masterlist.tsv') -Delimiter "`t").Count + @(Import-Csv -LiteralPath (Join-Path $root 'lists/canada_lte_excel.tsv') -Delimiter "`t").Count
$actual = @(Import-Csv -LiteralPath $combined -Delimiter "`t")
Assert-True ($actual.Count -eq $expected) 'Combined list dropped rows.'
Assert-True (@($actual | Where-Object { -not $_.source_urls }).Count -eq 0) 'Combined list lost citations.'
Write-Host 'PowerShell manual tests passed.'
# Leave only synthetic temporary fixtures; no real document data is used.
