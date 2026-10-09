import os
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.orm import Session

# Point the app at the throwaway test database before anything imports app.config.
# docker/initdb/01-test-db.sql creates it on first `docker compose up`.
# Set TEST_DATABASE_URL if your Postgres is not on localhost:5432.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+psycopg://showup:showup@localhost:5432/showup_test"
)
os.environ.setdefault("JWT_SECRET", "test-only-secret-that-is-at-least-32-chars")

from alembic.config import Config  # noqa: E402

from alembic import command  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import User  # noqa: E402
from app.security import create_access_token  # noqa: E402

BACKEND_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def migrated_database() -> Iterator[None]:
    """Build the test schema from the real migrations, once per test run."""
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    yield


@pytest.fixture(autouse=True)
def clean_tables() -> Iterator[None]:
    """Every test starts with empty tables."""
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))


@pytest.fixture
def db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers(db: Session) -> Callable[[str], dict[str, str]]:
    """auth_headers("Maya") -> Authorization header for the seeded user with that name."""

    def _headers(name: str) -> dict[str, str]:
        user = db.scalar(select(User).where(User.name == name))
        assert user is not None, f"no seeded user named {name}"
        return {"Authorization": f"Bearer {create_access_token(user.id)}"}

    return _headers
