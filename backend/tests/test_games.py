from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Game, GameStatus, User
from app.seed import GAMES, SIGNUPS, USERS, seed

UPCOMING = [g for g in GAMES if g[4] > 0 and g[9] != GameStatus.CANCELLED]
UPCOMING_BASKETBALL = [g for g in UPCOMING if g[1] == "basketball"]
NOT_CANCELLED = [g for g in GAMES if g[9] != GameStatus.CANCELLED]


def test_seed_creates_rows_and_is_rerunnable(db: Session) -> None:
    first = seed(db)
    second = seed(db)

    assert first == second == {"users": len(USERS), "games": len(GAMES), "signups": len(SIGNUPS)}
    assert db.scalar(select(func.count()).select_from(User)) == len(USERS)
    assert db.scalar(select(func.count()).select_from(Game)) == len(GAMES)


def test_list_games_returns_upcoming_sorted_by_start(client: TestClient, db: Session) -> None:
    seed(db)

    response = client.get("/games")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == len(UPCOMING)
    starts = [g["starts_at"] for g in body]
    assert starts == sorted(starts)
    assert all(g["status"] != "cancelled" for g in body)


def test_list_games_filters_by_sport_case_insensitively(client: TestClient, db: Session) -> None:
    seed(db)

    response = client.get("/games", params={"sport": "Basketball"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == len(UPCOMING_BASKETBALL)
    assert {g["sport"] for g in body} == {"basketball"}


def test_list_games_unknown_sport_is_empty(client: TestClient, db: Session) -> None:
    seed(db)

    assert client.get("/games", params={"sport": "curling"}).json() == []


def test_list_games_can_include_past(client: TestClient, db: Session) -> None:
    seed(db)

    response = client.get("/games", params={"include_past": "true"})

    assert len(response.json()) == len(NOT_CANCELLED)


def test_game_shape(client: TestClient, db: Session) -> None:
    seed(db)

    game = client.get("/games").json()[0]

    assert set(game) == {
        "id",
        "host_id",
        "sport",
        "venue",
        "address",
        "starts_at",
        "spots",
        "cost",
        "min_reputation",
        "status",
    }
    assert isinstance(game["cost"], int | float)
