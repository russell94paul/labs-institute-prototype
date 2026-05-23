#!/bin/bash
# NeuroSpect — Start All Services
# Usage: ./start.sh [all|api|app|marketing|orchestrator]

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SERVICE="${1:-all}"
PIDS=()

cleanup() {
    echo -e "\n[neurospect] Stopping services..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null
    done
    exit 0
}
trap cleanup SIGINT SIGTERM

start_api() {
    echo -e "\033[36m[neurospect] Starting API (FastAPI) on :8000...\033[0m"
    cd "$REPO_ROOT/api" && poetry run uvicorn app.main:app --reload --port 8000 &
    PIDS+=($!)
}

start_app() {
    echo -e "\033[36m[neurospect] Starting App (React) on :5173...\033[0m"
    cd "$REPO_ROOT/app" && npm run dev &
    PIDS+=($!)
}

start_marketing() {
    echo -e "\033[36m[neurospect] Starting Marketing site on :3000...\033[0m"
    cd "$REPO_ROOT/neurospect-ui" && python -m http.server 3000 &
    PIDS+=($!)
}

start_orchestrator() {
    echo -e "\033[36m[neurospect] Starting Orchestrator on :8766...\033[0m"
    cd "$REPO_ROOT" && python platform/orchestrator/server.py &
    PIDS+=($!)
}

echo ""
echo -e "\033[36m  NeuroSpect Platform\033[0m"
echo ""

case "$SERVICE" in
    api)          start_api ;;
    app)          start_app ;;
    marketing)    start_marketing ;;
    orchestrator) start_orchestrator ;;
    all)
        start_orchestrator; sleep 1
        start_api; sleep 1
        start_app; sleep 1
        start_marketing
        echo ""
        echo -e "\033[32m[neurospect] All services starting...\033[0m"
        echo ""
        echo "  API          http://localhost:8000"
        echo "  App          http://localhost:5173"
        echo "  Marketing    http://localhost:3000"
        echo "  Orchestrator http://localhost:8766"
        echo ""
        echo -e "\033[90m  Press Ctrl+C to stop all services\033[0m"
        echo ""
        wait
        ;;
    *)
        echo "Usage: ./start.sh [all|api|app|marketing|orchestrator]"
        ;;
esac
