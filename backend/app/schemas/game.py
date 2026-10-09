from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import GameStatus


class GameOut(BaseModel):
    """A game as the app sees it in lists and detail screens."""

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
