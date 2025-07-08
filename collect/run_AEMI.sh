cd /opt/APPS/AEMI/backend
./.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload &
cd /opt/APPS/AEIM/frontend
pnpm run dev -p 3000: &
