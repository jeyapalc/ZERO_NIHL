[CmdletBinding()]
param(
    [string[]]$RepositoryPaths = @((Split-Path -Parent $PSScriptRoot)),
    [string]$OutputPath = (Join-Path (Get-Location) 'wordlist.tsv'),
    [switch]$IncludeRegistry,
    [switch]$Force
)
$ErrorActionPreference = 'Stop'
if (-not $RepositoryPaths.Count) { throw 'Provide at least one local repository path.' }
$destination = [IO.Path]::GetFullPath($OutputPath)
if ((Test-Path -LiteralPath $destination) -and -not $Force) { throw 'Output exists. Choose another filename or use -Force.' }
$rows = [Collections.Generic.List[object]]::new()
foreach ($repository in $RepositoryPaths) {
    $root = (Resolve-Path -LiteralPath $repository).Path
    $files = @('lists/masterlist.tsv')
    if ($IncludeRegistry) { $files += 'lists/canada_lte_excel.tsv' }
    foreach ($relative in $files) {
        $source = Join-Path $root $relative
        if ([IO.Path]::GetFullPath($source) -eq $destination) { throw 'Output cannot overwrite an input list.' }
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing canonical list: $source" }
        foreach ($row in (Import-Csv -LiteralPath $source -Delimiter "`t" -Encoding UTF8)) {
            if ([string]::IsNullOrWhiteSpace($row.term)) { throw "Empty term in $source" }
            $urls = if ($row.source_urls) { $row.source_urls } else { $row.source_url }
            if ([string]::IsNullOrWhiteSpace($urls)) { throw "Missing citation in $source" }
            $rows.Add([pscustomobject][ordered]@{
                term=$row.term; enabled=$row.enabled; tier=$row.tier
                category=$row.category; entry_id=$row.entry_id; language=$row.language
                context_note=$row.context_note; source_urls=$urls
                source_repository=(Split-Path -Leaf $root); source_file=$relative
                canada_basis=$row.canada_basis; evidence_basis=$row.evidence_basis
                official_aliases_raw=$row.official_aliases_raw
            })
        }
    }
}
if (-not $rows.Count) { throw 'No terms found; no output was written.' }
$lines = @($rows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation)
[IO.File]::WriteAllLines($destination, [string[]]$lines, [Text.UTF8Encoding]::new($true))
Write-Host "Wrote $($rows.Count) cited term/source rows to $destination"
