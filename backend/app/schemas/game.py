from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import GameStatus

# The sport picker on the Create Post screen. Lowercase, matched case-insensitively.
ALLOWED_SPORTS = (
    "basketball",
    "soccer",
    "volleyball",
    "badminton",
    "tennis",
    "pickleball",
    "ultimate",
    "hockey",
)


class GameOut(BaseModel):
    """A game as the app sees it in lists."""

    # Lets FastAPI build this straight from a Game ORM object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    host_id: int
    sport: str
    venue: str
    address: str
    starts_at: datetime
    spots: int
    # Sent as a number (5.0), not a string, so the app can show it without parsing.
    cost: float
    min_reputation: int
    status: GameStatus


class PlayerOut(BaseModel):
    """A player on a game's roster. Only what the Game Details screen shows."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    reputation: int


class GameDetailOut(GameOut):
    """A single game with its host and roster.

    `spots` is the number of player places the host offers, not counting the host.
    `spots_left` is `spots` minus the players who have joined.
    """

    host_name: str
    players: list[PlayerOut]
    spots_left: int


def _check_sport(value: str) -> str:
    sport = value.strip().lower()
    if sport not in ALLOWED_SPORTS:
        raise ValueError(f"sport must be one of: {', '.join(ALLOWED_SPORTS)}")
    return sport


def _check_future(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("starts_at must include a timezone, e.g. 2026-10-20T18:00:00-07:00")
    if value <= datetime.now(UTC):
        raise ValueError("starts_at must be in the future")
    return value


class GameCreate(BaseModel):
    """Body of POST /games. Validation mirrors the games table and the Create Post screen."""

    model_config = ConfigDict(extra="forbid")

    sport: str
    venue: str = Field(min_length=1, max_length=200)
    address: str = Field(min_length=1, max_length=300)
    starts_at: datetime
    spots: int = Field(ge=2, le=30)
    cost: Decimal = Field(default=Decimal(0), ge=0, max_digits=6, decimal_places=2)
    min_reputation: int = Field(default=0, ge=0, le=100)

    _sport = field_validator("sport")(_check_sport)
    _starts_at = field_validator("starts_at")(_check_future)


class GameUpdate(BaseModel):
    """Body of PATCH /games/{id}. Every field optional; only sent fields change."""

    model_config = ConfigDict(extra="forbid")

    sport: str | None = None
    venue: str | None = Field(default=None, min_length=1, max_length=200)
    address: str | None = Field(default=None, min_length=1, max_length=300)
    starts_at: datetime | None = None
    spots: int | None = Field(default=None, ge=2, le=30)
    cost: Decimal | None = Field(default=None, ge=0, max_digits=6, decimal_places=2)
    min_reputation: int | None = Field(default=None, ge=0, le=100)

    @field_validator("sport")
    @classmethod
    def _sport(cls, value: str | None) -> str | None:
        return None if value is None else _check_sport(value)

    @field_validator("starts_at")
    @classmethod
    def _starts_at(cls, value: datetime | None) -> datetime | None:
        return None if value is None else _check_future(value)
