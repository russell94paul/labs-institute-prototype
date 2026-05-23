# NeuroSpect — Start All Services
# Usage: .\start.ps1 [all|api|app|marketing|orchestrator]

param(
    [string]$Service = "all"
)

$RepoRoot = $PSScriptRoot

function Start-Api {
    Write-Host "[neurospect] Starting API (FastAPI) on :8000..." -ForegroundColor Cyan
    $env:PYTHONDONTWRITEBYTECODE = "1"
    Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c cd /d $RepoRoot\api && poetry run uvicorn app.main:app --reload --port 8000" -PassThru
}

function Start-App {
    Write-Host "[neurospect] Starting App (React) on :5173..." -ForegroundColor Cyan
    Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c cd /d $RepoRoot\app && npm run dev" -PassThru
}

function Start-Marketing {
    Write-Host "[neurospect] Starting Marketing site on :3000..." -ForegroundColor Cyan
    Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c cd /d $RepoRoot\neurospect-ui && python -m http.server 3000" -PassThru
}

function Start-Orchestrator {
    Write-Host "[neurospect] Starting Orchestrator on :8766..." -ForegroundColor Cyan
    Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList "/c cd /d $RepoRoot && python platform\orchestrator\server.py" -PassThru
}

Write-Host ""
Write-Host "  _   _                      ____                  _   " -ForegroundColor DarkCyan
Write-Host " | \ | | ___ _   _ _ __ ___ / ___| _ __   ___  ___| |_ " -ForegroundColor DarkCyan
Write-Host " |  \| |/ _ \ | | | '__/ _ \\___ \| '_ \ / _ \/ __| __|" -ForegroundColor Cyan
Write-Host " | |\  |  __/ |_| | | | (_) |___) | |_) |  __/ (__| |_ " -ForegroundColor Cyan
Write-Host " |_| \_|\___|\__,_|_|  \___/|____/| .__/ \___|\___|\__|" -ForegroundColor DarkCyan
Write-Host "                                   |_|                  " -ForegroundColor DarkCyan
Write-Host ""

switch ($Service) {
    "api"          { Start-Api }
    "app"          { Start-App }
    "marketing"    { Start-Marketing }
    "orchestrator" { Start-Orchestrator }
    "all" {
        $procs = @()
        $procs += Start-Orchestrator
        Start-Sleep -Seconds 1
        $procs += Start-Api
        Start-Sleep -Seconds 1
        $procs += Start-App
        Start-Sleep -Seconds 1
        $procs += Start-Marketing

        Write-Host ""
        Write-Host "[neurospect] All services starting..." -ForegroundColor Green
        Write-Host ""
        Write-Host "  API          http://localhost:8000" -ForegroundColor White
        Write-Host "  App          http://localhost:5173" -ForegroundColor White
        Write-Host "  Marketing    http://localhost:3000" -ForegroundColor White
        Write-Host "  Orchestrator http://localhost:8766" -ForegroundColor White
        Write-Host ""
        Write-Host "  Press Ctrl+C to stop all services" -ForegroundColor DarkGray
        Write-Host ""

        try {
            while ($true) { Start-Sleep -Seconds 60 }
        } finally {
            Write-Host "[neurospect] Stopping services..." -ForegroundColor Yellow
            $procs | Where-Object { $_ -and -not $_.HasExited } | ForEach-Object {
                Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
            }
        }
    }
    default {
        Write-Host "Usage: .\start.ps1 [all|api|app|marketing|orchestrator]" -ForegroundColor Yellow
    }
}
