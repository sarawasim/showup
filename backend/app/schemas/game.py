from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import GameStatus


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
