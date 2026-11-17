[CmdletBinding()]
param(
    [string]$OutputPath = (Join-Path (Get-Location) 'searchable_terms.tsv')
)

$ErrorActionPreference = 'Stop'
$repositories = @(
    'jeyapalc/ZERO_NIHL',
    'jeyapalc/ZERO_FAITH',
    'jeyapalc/ZERO_NAZ'
)
$headers = @{ 'User-Agent' = 'ZERO-searchable-list-builder' }
$entries = [System.Collections.Generic.List[object]]::new()

function ConvertTo-MatchKey([string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
    $normalized = $Value.Trim().Normalize([Text.NormalizationForm]::FormD).ToLowerInvariant()
    $normalized = [regex]::Replace($normalized, '\p{Mn}', '')
    return ([regex]::Replace($normalized, '[^\p{L}\p{N}]+', ' ')).Trim()
}

function Add-ListTerm([string]$Term, [string]$Repository, [string]$File, [string]$ListType, [hashtable]$Fields) {
    $Term = $Term.Trim().Trim([char]0xFEFF)
    if ([string]::IsNullOrWhiteSpace($Term)) { return }

    $searchParts = [System.Collections.Generic.List[string]]::new()
    $searchParts.Add($Term)
    foreach ($value in $Fields.Values) {
        if ($null -ne $value -and -not [string]::IsNullOrWhiteSpace([string]$value)) {
            $searchParts.Add([string]$value)
        }
    }

    $record = [ordered]@{}
    foreach ($key in $Fields.Keys) { $record[$key] = $Fields[$key] }
    $record['source_repository'] = $Repository
    $record['source_file'] = $File
    $record['list_type'] = $ListType

    $script:entries.Add([pscustomobject]@{
        Term          = $Term
        MatchKey      = ConvertTo-MatchKey $Term
        ListType      = $ListType
        SourceRepository = $Repository
        SourceFile    = $File
        SearchText    = ($searchParts -join ' ')
        SourceRecord  = $record
    })
}

foreach ($repository in $repositories) {
    $contentsUrl = "https://api.github.com/repos/$repository/contents/lists?ref=main"
    $files = Invoke-RestMethod -Uri $contentsUrl -Headers $headers

    foreach ($file in $files | Where-Object { $_.type -eq 'file' -and $_.name -match '\.(txt|tsv|csv)$' }) {
        $response = Invoke-WebRequest -Uri $file.download_url -Headers $headers
        $text = ([string]$response.Content).TrimStart([char]0xFEFF)
        $listType = [IO.Path]::GetFileNameWithoutExtension($file.name)

        if ($file.name -match '\.(tsv|csv)$') {
            $delimiter = if ($file.name.EndsWith('.tsv')) { "`t" } else { ',' }
            $rows = @($text | ConvertFrom-Csv -Delimiter $delimiter)
            foreach ($row in $rows) {
                $fields = @{}
                foreach ($property in $row.PSObject.Properties) {
                    $fieldName = $property.Name.TrimStart([char]0xFEFF)
                    $fields[$fieldName] = [string]$property.Value
                }
                $termColumn = @($fields.Keys | Where-Object { $_ -ieq 'term' }) | Select-Object -First 1
                if ($termColumn) {
                    Add-ListTerm -Term $fields[$termColumn] -Repository $repository -File $file.path -ListType $listType -Fields $fields
                }
            }
            continue
        }

        # Query-format lists contain quoted terms separated by OR; pipe-format lists
        # contain terms separated by |. Readable lists prefix terms with metadata.
        if ($file.name -match 'terms_or\.txt$') {
            foreach ($match in [regex]::Matches($text, '"([^"]+)"')) {
                Add-ListTerm -Term $match.Groups[1].Value -Repository $repository -File $file.path -ListType $listType -Fields @{}
            }
        } elseif ($file.name -match 'terms_pipe\.txt$') {
            foreach ($part in ($text -split '\|')) {
                Add-ListTerm -Term $part -Repository $repository -File $file.path -ListType $listType -Fields @{}
            }
        } elseif ($file.name -match 'terms_readable\.txt$') {
            foreach ($line in ($text -split "`r?`n")) {
                if ($line -match '^\s*(.*?)\s+\[[^\]]+\]\s+—') {
                    Add-ListTerm -Term $Matches[1] -Repository $repository -File $file.path -ListType $listType -Fields @{}
                }
            }
        } else {
            foreach ($line in ($text -split "`r?`n")) {
                $candidate = $line.Trim()
                if ($candidate -and $candidate -notmatch '^\s*(#|//)' -and $candidate -notmatch '^REVIEW VOCABULARY') {
                    Add-ListTerm -Term $candidate -Repository $repository -File $file.path -ListType $listType -Fields @{}
                }
            }
        }
    }
}

# Collapse duplicate spellings across the three repositories and list formats,
# while retaining provenance and every source row's original metadata as JSON.
$merged = foreach ($group in ($entries | Group-Object -Property MatchKey | Sort-Object Name)) {
    $items = @($group.Group)
    $first = $items[0]
    $sourceRecords = @($items | ForEach-Object { $_.SourceRecord })
    $searchText = ($items | ForEach-Object { $_.SearchText } | Where-Object { $_ } | Select-Object -Unique) -join ' '

    [pscustomobject]@{
        term              = $first.Term
        match_key         = $first.MatchKey
        list_types        = (($items | ForEach-Object ListType | Sort-Object -Unique) -join '; ')
        source_repositories = (($items | ForEach-Object SourceRepository | Sort-Object -Unique) -join '; ')
        source_files      = (($items | ForEach-Object SourceFile | Sort-Object -Unique) -join '; ')
        search_text       = $searchText
        source_data_json  = ConvertTo-Json -InputObject $sourceRecords -Depth 10 -Compress
    }
}

$destination = [IO.Path]::GetFullPath($OutputPath)
$parent = Split-Path -Parent $destination
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}
$merged | Export-Csv -LiteralPath $destination -Delimiter "`t" -NoTypeInformation -Encoding UTF8
Write-Host "Wrote $(@($merged).Count) unique searchable terms to $destination"
