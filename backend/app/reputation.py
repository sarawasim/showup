"""Reputation rules. Every number the team may want to tune lives here, nowhere else.

Reputation is a show-up rate with a cushion of CUSHION imaginary attended games, so a new
player starts at 100 and one slip on a first game lands at 75, not 0:

    reputation = round(100 * (shows + CUSHION) / (marked_games + CUSHION))

It is recomputed from the attendance table whenever a host marks a game, and stored on
users.reputation so listing games never has to count rows.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import Attendance, Game, GameStatus, User

START = 100
CUSHION = 3
# Below this many marked or hosted games the app shows "New" instead of the number.
NEW_PLAYER_GAMES = 3
# A host can mark, change or be disputed on attendance for this long after kickoff.
MARK_WINDOW_DAYS = 7
# The highest minimum a host may ask for. 100 would lock out anyone who ever slipped once.
MAX_MIN_REPUTATION = 95


def compute(shows: int, marked: int) -> int:
    return round(100 * (shows + CUSHION) / (marked + CUSHION))


def recompute(db: Session, user: User) -> int:
    """Recount the user's attendance rows and store the new reputation. Returns it."""
    shows, marked = _attendance_counts(db, [user.id]).get(user.id, (0, 0))
    user.reputation = compute(shows, marked)
    return user.reputation


def _attendance_counts(db: Session, user_ids: list[int]) -> dict[int, tuple[int, int]]:
    """user_id -> (games showed up to, games marked) for the given users."""
    if not user_ids:
        return {}
    stmt = (
        select(
            Attendance.user_id,
            func.count(case((Attendance.showed_up.is_(True), 1))),
            func.count(),
        )
        .where(Attendance.user_id.in_(user_ids))
        .group_by(Attendance.user_id)
    )
    return {uid: (int(shows), int(marked)) for uid, shows, marked in db.execute(stmt)}


def _hosted_counts(db: Session, user_ids: list[int]) -> dict[int, int]:
    """user_id -> games they hosted that were played."""
    if not user_ids:
        return {}
    stmt = (
        select(Game.host_id, func.count())
        .where(Game.host_id.in_(user_ids), Game.status == GameStatus.PLAYED)
        .group_by(Game.host_id)
    )
    return {uid: int(n) for uid, n in db.execute(stmt)}


def player_stats(db: Session, user_ids: list[int]) -> dict[int, dict[str, int | bool]]:
    """What the roster and profile show next to the reputation number."""
    attended = _attendance_counts(db, user_ids)
    hosted = _hosted_counts(db, user_ids)
    out: dict[int, dict[str, int | bool]] = {}
    for uid in user_ids:
        shows, marked = attended.get(uid, (0, 0))
        games_hosted = hosted.get(uid, 0)
        out[uid] = {
            "games_played": shows,
            "games_hosted": games_hosted,
            "is_new": marked + games_hosted < NEW_PLAYER_GAMES,
        }
    return out


def effective_min_reputation(game: Game, now: datetime | None = None) -> int:
    """The minimum that applies right now.

    A host may set a one-step fallback: within `fallback_hours_before_start` of kickoff the
    requirement drops to `fallback_min_reputation`. Evaluated on read, no timers.
    """
    if game.fallback_min_reputation is None or game.fallback_hours_before_start is None:
        return game.min_reputation
    now = now or datetime.now(UTC)
    if now >= game.starts_at - timedelta(hours=game.fallback_hours_before_start):
        return min(game.min_reputation, game.fallback_min_reputation)
    return game.min_reputation
