import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

# Point the app at the throwaway test database before anything imports app.config.
# docker/initdb/01-test-db.sql creates it on first `docker compose up`.
# Set TEST_DATABASE_URL if your Postgres is not on localhost:5432.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+psycopg://showup:showup@localhost:5432/showup_test"
)
os.environ.setdefault("JWT_SECRET", "test-only-secret")

from alembic.config import Config  # noqa: E402

from alembic import command  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402

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
