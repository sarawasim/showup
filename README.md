# ShowUp

Drop-in sports games with a show-up reputation. Hosts post a game, players join, attendance builds trust.

COMP 7082 Software Engineering, BCIT, Fall 2026. Group 15.

## Layout

| Folder | What | Stack |
|---|---|---|
| `backend/` | REST API | Python 3.13, FastAPI, SQLAlchemy 2, Alembic, Postgres |
| `frontend/` | Mobile app | React Native (Expo) |
| `docs/` | ERD, decisions, meeting notes | Markdown |
| `docker/` | Local Postgres init scripts | SQL |

## Quick start (backend)

Needs [uv](https://docs.astral.sh/uv/) and Docker Desktop.

```bash
docker compose up -d db
cd backend
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

API docs: http://localhost:8000/docs. Health: http://localhost:8000/health.

Full backend guide: [backend/README.md](backend/README.md). Frontend: [frontend/README.md](frontend/README.md).

## Board

Trello: https://trello.com/b/0RpZh6q1/showup
