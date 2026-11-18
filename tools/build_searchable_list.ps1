[CmdletBinding()]
param([string[]]$RepositoryPaths = @((Split-Path -Parent $PSScriptRoot)), [string]$OutputPath = (Join-Path (Get-Location) 'searchable_terms.tsv'), [switch]$IncludeRegistry, [switch]$Force)
& (Join-Path (Split-Path -Parent $PSScriptRoot) 'manual/Build-WordList.ps1') -RepositoryPaths $RepositoryPaths -OutputPath $OutputPath -IncludeRegistry:$IncludeRegistry -Force:$Force
