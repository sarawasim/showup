# 0001: Backend stack

Date: 2026-10-01. Status: proposed, vote in Discord.

## Decision

Python 3.13 with FastAPI, Pydantic for validation, SQLAlchemy 2 with Alembic migrations, Postgres from day one, email and password auth with JWT, pytest, Docker image deployed to Render.

## Options compared

| | FastAPI | Flask |
|---|---|---|
| Validation | Built in through Pydantic; bad input returns 422 with the field named | Add Marshmallow or write it by hand |
| API docs | `/docs` generated from the code, the frontend can read the contract without asking | Add flask-smorest or write OpenAPI by hand |
| Auth helpers | `OAuth2PasswordBearer` dependency included | Add Flask-Login or Flask-JWT-Extended |
| Learning curve | Typed function signatures; routes stay plain `def` | Smallest core, more choices to make |
| Fit for a 3-week sprint | Less glue code to write and review | More glue code |

| | Postgres now | SQLite first |
|---|---|---|
| Migration later | None | A switch mid-term with type and constraint differences |
| Local setup | One `docker compose up -d db` | Nothing |
| Matches production | Yes | No |

## Consequences

- Everyone needs Docker Desktop for the local database.
- Google sign-in is out of sprint 1; the epic "Later" holds it.
- The frontend consumes `/openapi.json` instead of a hand-written API doc.
