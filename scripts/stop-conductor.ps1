<#
.SYNOPSIS
    Stop a local Conductor server using port 8888.
.DESCRIPTION
    Finds the process listening on port 8888 and asks for confirmation before stopping it.
#>

$port = 8888

$connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue

if (-not $connections) {
    Write-Host "[conductor] No process found listening on port $port." -ForegroundColor Yellow
    exit 0
}

foreach ($conn in $connections) {
    $pid = $conn.OwningProcess
    $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
    $procName = if ($proc) { $proc.ProcessName } else { '(unknown)' }

    Write-Host "[conductor] Found process on port ${port}:" -ForegroundColor Cyan
    Write-Host "  PID:  $pid" -ForegroundColor White
    Write-Host "  Name: $procName" -ForegroundColor White

    $confirm = Read-Host "Kill this process? (y/N)"
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        try {
            Stop-Process -Id $pid -Force -Confirm:$false
            Write-Host "[conductor] Process $pid stopped." -ForegroundColor Green
        } catch {
            Write-Host "[conductor] Failed to stop process $pid`: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "[conductor] Skipped." -ForegroundColor DarkGray
    }
}
