import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

# Point the app at the throwaway test database before anything imports app.config.
# docker/initdb/01-test-db.sql creates it on first `docker compose up`.
# Set TEST_DATABASE_URL if your Postgres is not on localhost:5432.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+psycopg://showup:showup@localhost:5432/showup_test"
)
os.environ.setdefault("JWT_SECRET", "test-only-secret")

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c
