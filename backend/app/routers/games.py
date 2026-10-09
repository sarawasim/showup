from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.deps import DbDep
from app.models import Game, GameStatus
from app.schemas.game import GameOut

router = APIRouter(prefix="/games", tags=["games"])


@router.get("", response_model=list[GameOut])
def list_games(
    db: DbDep,
    sport: str | None = Query(None, description="Only this sport, case-insensitive"),
    include_past: bool = Query(False, description="Also return games that already started"),
) -> list[Game]:
    """Upcoming games, soonest first. Cancelled games are never listed."""
    stmt = select(Game).where(Game.status != GameStatus.CANCELLED).order_by(Game.starts_at)
    if sport:
        stmt = stmt.where(func.lower(Game.sport) == sport.lower())
    if not include_past:
        stmt = stmt.where(Game.starts_at >= func.now())
    return list(db.scalars(stmt).all())
