[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$WordListPath,
    [Parameter(Mandatory=$true)][AllowEmptyCollection()][string[]]$DocumentPath,
    [string]$OutputPath = (Join-Path (Get-Location) 'matches.csv'),
    [switch]$AllTerms,
    [switch]$WholeWord,
    [switch]$CaseSensitive,
    [switch]$Force
)
$ErrorActionPreference = 'Stop'
if (-not $DocumentPath.Count) { throw 'No documents supplied.' }
$wordFile = (Resolve-Path -LiteralPath $WordListPath).Path
$destination = [IO.Path]::GetFullPath($OutputPath)
if ($destination -eq $wordFile) { throw 'Output cannot overwrite the wordlist.' }
if ((Test-Path -LiteralPath $destination) -and -not $Force) { throw 'Output exists. Choose another filename or use -Force.' }
$documents = foreach ($path in $DocumentPath) {
    $resolved = (Resolve-Path -LiteralPath $path).Path
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) { throw "Not a document file: $resolved" }
    if ([IO.Path]::GetExtension($resolved) -notin @('.txt','.md','.csv','.tsv','.log')) {
        throw 'Export Word/PDF or other formats to UTF-8 plain text before scanning.'
    }
    if ($destination -eq $resolved) { throw 'Output cannot overwrite an input document.' }
    $resolved
}
$terms = @(Import-Csv -LiteralPath $wordFile -Delimiter "`t" -Encoding UTF8 | Where-Object {
    -not [string]::IsNullOrWhiteSpace($_.term) -and ($AllTerms -or $_.enabled -eq 'TRUE')
})
if (-not $terms.Count) { throw 'No enabled terms. Select rows in the list or explicitly use -AllTerms.' }
foreach ($term in $terms) {
    if (-not $term.entry_id -or -not $term.source_urls) { throw 'Every term needs entry_id and source_urls.' }
}
$comparison = if ($CaseSensitive) { [StringComparison]::Ordinal } else { [StringComparison]::OrdinalIgnoreCase }
$options = [Text.RegularExpressions.RegexOptions]::CultureInvariant
if (-not $CaseSensitive) { $options = $options -bor [Text.RegularExpressions.RegexOptions]::IgnoreCase }
$searches = foreach ($term in $terms) {
    $regex = $null
    if ($WholeWord) {
        $regex = [regex]::new('(?<![\p{L}\p{N}_])' + [regex]::Escape($term.term) + '(?![\p{L}\p{N}_])', $options)
    }
    [pscustomobject]@{ Row=$term; Regex=$regex }
}
function Protect-SpreadsheetText([string]$Value) {
    if ($Value -match '^[\s]*[=+@-]' -or $Value -match '^[\t\r\n]') { return "'$Value" }
    return $Value
}
$results = [Collections.Generic.List[object]]::new()
foreach ($document in $documents) {
    $lineNumber = 0
    foreach ($line in [IO.File]::ReadLines($document, [Text.UTF8Encoding]::new($false,$true))) {
        $lineNumber++
        foreach ($search in $searches) {
            $term = $search.Row
            $position = -1
            if ($WholeWord) {
                $hit = $search.Regex.Match($line)
                if ($hit.Success) { $position = $hit.Index }
            } else { $position = $line.IndexOf($term.term, $comparison) }
            if ($position -lt 0) { continue }
            $record = [ordered]@{
                document_path=$document; line_number=$lineNumber; column=($position+1)
                term=$term.term; entry_id=$term.entry_id; source_urls=$term.source_urls
                source_repository=$term.source_repository; source_file=$term.source_file
                language=$term.language; tier=$term.tier; context_note=$term.context_note
                match_mode=$(if ($WholeWord) { 'whole_word' } else { 'substring' })
                case_sensitive=[bool]$CaseSensitive; text=$line
            }
            foreach ($key in @($record.Keys)) {
                if ($record[$key] -is [string]) { $record[$key] = Protect-SpreadsheetText $record[$key] }
            }
            $results.Add([pscustomobject]$record)
        }
    }
}
if ($results.Count) { $csv = @($results | ConvertTo-Csv -NoTypeInformation) }
else { $csv = @('"document_path","line_number","column","term","entry_id","source_urls","source_repository","source_file","language","tier","context_note","match_mode","case_sensitive","text"') }
[IO.File]::WriteAllLines($destination, [string[]]$csv, [Text.UTF8Encoding]::new($true))
Write-Host "Searched $($terms.Count) term/source rows in $(@($documents).Count) documents; wrote $($results.Count) matching rows to $destination"
