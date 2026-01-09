# .\run_sql.ps1 -User postgres -Database IT_JOB_LOCAL

param(
    [string[]]$Path = @(
        ".\insert_many_repo_meta.sql",
        ".\insert_many_repo_languages.sql",
        ".\insert_many_repo_commits.sql",
        ".\insert_many_repo_topics.sql",
        ".\insert_many_job.sql",
        ".\insert_many_tech_meta.sql",
        ".\insert_many_github_tech_bridge.sql",
        ".\insert_many_job_tech_bridge",
        ".\insert_many_stackoverflow_posts",
        ".\insert_many_stackoverflow_tech_bridge"
    ),

    [Parameter(Mandatory = $true)]
    [string]$User,

    [Parameter(Mandatory = $true)]
    [string]$Database,

    [string]$DbHost = "localhost",
    [string]$Port = "5432"
)

$files = @()

foreach ($p in $Path) {

    if (-not (Test-Path $p)) {
        Write-Host "Path not found: $p" -ForegroundColor Red
        exit 1
    }

    $item = Get-Item $p

    if ($item.PSIsContainer) {
        $files += Get-ChildItem $item.FullName -Filter *.sql | Sort-Object Name
    }
    elseif ($p.EndsWith(".sql")) {
        $files += $item
    }
    else {
        Write-Host "Invalid path (must be .sql or directory): $p" -ForegroundColor Red
        exit 1
    }
}

if ($files.Count -eq 0) {
    Write-Host "No .sql files found" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($files.Count) SQL file(s)" -ForegroundColor Green
Write-Host "psql will ask for password ONCE" -ForegroundColor Cyan

$cmd = @()
$cmd += "SET client_encoding = 'UTF8';"

foreach ($file in $files) {
    $fullPath = $file.FullName -replace '\\','/'
    Write-Host "Queue: $fullPath" -ForegroundColor Yellow
    $cmd += "\i '$fullPath'"
}

$cmd | psql `
    -U $User `
    -h $DbHost `
    -p $Port `
    -d $Database `
    -v ON_ERROR_STOP=1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR while executing SQL files" -ForegroundColor Red
    exit 1
}

Write-Host "All SQL files executed successfully" -ForegroundColor Green
