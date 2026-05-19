# conductor-serve

Start or verify the local Conductor UI server.

## When to use

When the user wants to view the Conductor dashboard, start the server, or check if it is running.

## Steps

1. Run `git status` — confirm the working tree state (do not modify files).
2. Run `powershell -File scripts/check-conductor.ps1` to check if the server is already running.
3. If the server is running, report the URL and stop:
   ```
   Conductor is running at http://127.0.0.1:8888
   ```
4. If the server is NOT running, start it:
   ```
   powershell -File scripts/start-conductor.ps1
   ```
   Note: This runs in the foreground. The terminal must stay open.
5. Report the local URL: `http://127.0.0.1:8888`

## Key URLs

- Dashboard: http://127.0.0.1:8888
- Build Studio: http://127.0.0.1:8888/#build-studio
- Bootstrap Console: http://127.0.0.1:8888/#bootstrap
- Sessions: http://127.0.0.1:8888/#sessions
- Pipelines: http://127.0.0.1:8888/#pipelines

## Constraints

- **Read-only.** Do not modify any repo files.
- Do not proceed into any build phase.
- Do not run tests unless asked.
- Do not touch secrets, .env files, or credentials.
- Do not install dependencies.
- Do not start the server if it is already running.
