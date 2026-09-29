#!/bin/bash

SESSION="dev_env"

echo "🚀 Starting development environment with tmux..."

# Kill any existing tmux session with the same name
tmux kill-session -t $SESSION 2>/dev/null

# Start new tmux session
tmux new-session -d -s $SESSION -n backend

# --- Backend Python Environment ---
tmux send-keys -t $SESSION:backend "
cd backend
python3 -m venv .env
source .env/bin/activate
echo '📦 Installing Python requirements (2 min max)...'
timeout 120s pip install -r requirements.txt || echo '⚠️ Pip install timed out or failed'
" C-m

# --- Frontend (npm run dev) ---
tmux new-window -t $SESSION -n frontend
tmux send-keys -t $SESSION:frontend "
cd frontend
source ../backend/.env/bin/activate
npm install
npm run dev
" C-m

# --- MailHog ---
tmux new-window -t $SESSION -n mailhog
tmux send-keys -t $SESSION:mailhog "
MailHog
" C-m

# --- Celery Worker ---
tmux new-window -t $SESSION -n celery_worker
tmux send-keys -t $SESSION:celery_worker "
cd backend
source .env/bin/activate
celery -A app.celery worker --loglevel=info
" C-m

# --- Celery Beat ---
tmux new-window -t $SESSION -n celery_beat
tmux send-keys -t $SESSION:celery_beat "
cd backend
source .env/bin/activate
celery -A app.celery beat --loglevel=info
" C-m

# --- Run app.py ---
tmux new-window -t $SESSION -n app
tmux send-keys -t $SESSION:app "
cd backend
source .env/bin/activate
python3 app.py
" C-m

# Attach to tmux session
tmux attach -t $SESSION