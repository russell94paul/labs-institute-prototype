# Local Development — Starting Conductor

## Quick Start

```powershell
powershell -File scripts/start-conductor.ps1
```

Dashboard opens at: http://127.0.0.1:8888

## Scripts

### `scripts/start-conductor.ps1`

Starts the local Conductor server.

- Checks if `engine/server.py` exists
- Checks if the server is already running on port 8888
- If already running, prints the URL and exits
- If not running, starts `python engine/server.py`
- Falls back to `py -3 engine/server.py` if `python` is not in PATH

### `scripts/check-conductor.ps1`

Checks whether the server is responding.

- Tests http://127.0.0.1:8888
- Exits 0 if running, 1 if not
- Safe to call from scripts or CI

### `scripts/stop-conductor.ps1`

Stops a running server on port 8888.

- Finds the process using `Get-NetTCPConnection`
- Displays PID and process name
- Asks for confirmation before killing

## Claude Code Skill

Use `/conductor-serve` to start or check the server from within Claude Code.

## Dashboard Routes

| Route | URL |
|-------|-----|
| Build Studio | http://127.0.0.1:8888/#build-studio |
| Bootstrap Console | http://127.0.0.1:8888/#bootstrap |
| Sessions | http://127.0.0.1:8888/#sessions |
| Pipelines | http://127.0.0.1:8888/#pipelines |
| Phases | http://127.0.0.1:8888/#phases |
| Projects | http://127.0.0.1:8888/#projects |
| Conductor Console | http://127.0.0.1:8888/#conductor |

## Troubleshooting

### Port 8888 already in use

```powershell
# Find what is using the port
Get-NetTCPConnection -LocalPort 8888 -State Listen

# Or use the stop script
powershell -File scripts/stop-conductor.ps1
```

### Python not found

The start script tries `python` first, then `py -3`. If neither works:

```powershell
# Check Python installation
python --version
py -3 --version
```

### Server starts but dashboard is blank

The server serves static files from `dashboard/`. Make sure you run from the repo root:

```powershell
cd C:\Users\PaulRussell\repos\conductor
python engine/server.py
```

### Connection refused

The server binds to `127.0.0.1:8888`. If you need a different port:

```powershell
$env:CONDUCTOR_PORT = '9999'
python engine/server.py
```
