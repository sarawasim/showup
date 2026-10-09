from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.deps import DbDep
from app.models import Game, GameStatus, Signup, SignupStatus
from app.schemas.game import GameDetailOut, GameOut, PlayerOut

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


@router.get("/{game_id}", response_model=GameDetailOut)
def get_game(game_id: int, db: DbDep) -> GameDetailOut:
    """One game with its host name and the players who have joined, oldest signup first."""
    stmt = (
        select(Game)
        .where(Game.id == game_id)
        .options(selectinload(Game.host), selectinload(Game.signups).selectinload(Signup.user))
    )
    game = db.scalar(stmt)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Game not found")

    joined = sorted(
        (s for s in game.signups if s.status == SignupStatus.JOINED),
        key=lambda s: (s.created_at, s.id),
    )
    players = [PlayerOut.model_validate(s.user) for s in joined]
    return GameDetailOut(
        **GameOut.model_validate(game).model_dump(),
        host_name=game.host.name,
        players=players,
        spots_left=max(game.spots - len(players), 0),
    )
