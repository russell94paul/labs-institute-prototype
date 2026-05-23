<#
.SYNOPSIS
    Check whether the local Conductor server is responding.
.DESCRIPTION
    Tests http://127.0.0.1:8888. Exits 0 if running, 1 if not.
#>

$url = 'http://127.0.0.1:8888'

try {
    $response = Invoke-WebRequest -Uri $url -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "[conductor] Server is running at $url" -ForegroundColor Green
        exit 0
    }
} catch {
    # Fall through
}

Write-Host "[conductor] Server is NOT running at $url" -ForegroundColor Red
exit 1
