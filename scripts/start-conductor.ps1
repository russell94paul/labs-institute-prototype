<#
.SYNOPSIS
    Start the local Conductor server for viewing the dashboard.
.DESCRIPTION
    Runs engine/server.py on http://127.0.0.1:8888.
    If already running, prints the URL and exits.
#>

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$serverScript = Join-Path $repoRoot 'engine' 'server.py'

if (-not (Test-Path $serverScript)) {
    Write-Host "[conductor] ERROR: engine/server.py not found at $serverScript" -ForegroundColor Red
    Write-Host "[conductor] Run this script from the conductor repo root." -ForegroundColor Red
    exit 1
}

$url = 'http://127.0.0.1:8888'

try {
    $response = Invoke-WebRequest -Uri $url -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "[conductor] Server is already running." -ForegroundColor Green
        Write-Host "[conductor] Dashboard: $url" -ForegroundColor Cyan
        exit 0
    }
} catch {
    # Not running — proceed to start
}

Write-Host "[conductor] Starting Conductor server..." -ForegroundColor Yellow

$pythonCmd = $null
try {
    $null = Get-Command python -ErrorAction Stop
    $pythonCmd = 'python'
} catch {
    try {
        $null = Get-Command py -ErrorAction Stop
        $pythonCmd = 'py'
    } catch {
        Write-Host "[conductor] ERROR: Neither 'python' nor 'py' found in PATH." -ForegroundColor Red
        exit 1
    }
}

Write-Host "[conductor] Using: $pythonCmd" -ForegroundColor DarkGray
Write-Host "[conductor] Dashboard will be at: $url" -ForegroundColor Cyan
Write-Host "[conductor] Press Ctrl+C to stop the server." -ForegroundColor DarkGray
Write-Host "[conductor] This window must stay open while the server is running." -ForegroundColor DarkGray
Write-Host ""

if ($pythonCmd -eq 'py') {
    & py -3 $serverScript
} else {
    & python $serverScript
}
