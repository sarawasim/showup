from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import GameStatus
from app.seed import GAMES, seed

UPCOMING = [g for g in GAMES if g[4] > 0 and g[9] != GameStatus.CANCELLED]


def _upcoming_matching(text: str) -> list[tuple]:
    return [g for g in UPCOMING if text in g[2].lower() or text in g[3].lower()]


def test_location_matches_address_case_insensitively(client: TestClient, db: Session) -> None:
    seed(db)

    body = client.get("/games", params={"location": "BURNABY"}).json()

    assert len(body) == len(_upcoming_matching("burnaby"))
    assert all("burnaby" in g["address"].lower() for g in body)


def test_location_matches_venue_too(client: TestClient, db: Session) -> None:
    seed(db)

    body = client.get("/games", params={"location": "rec centre"}).json()

    assert [g["venue"] for g in body] == ["Bonsor Rec Centre"]


def test_location_combines_with_sport(client: TestClient, db: Session) -> None:
    seed(db)

    body = client.get("/games", params={"location": "vancouver", "sport": "soccer"}).json()

    assert [g["venue"] for g in body] == ["Trillium Park"]


def test_location_with_no_match_is_empty(client: TestClient, db: Session) -> None:
    seed(db)

    assert client.get("/games", params={"location": "kelowna"}).json() == []


def test_location_wildcards_are_literal(client: TestClient, db: Session) -> None:
    seed(db)

    assert client.get("/games", params={"location": "%%"}).json() == []
    assert client.get("/games", params={"location": "b_rnaby"}).json() == []


def test_location_too_short_is_422(client: TestClient, db: Session) -> None:
    seed(db)

    assert client.get("/games", params={"location": "b"}).status_code == 422
