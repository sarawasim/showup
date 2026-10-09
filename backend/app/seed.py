# ruff: noqa: E501  (the GAMES table below is wider than 100 columns on purpose)
"""Seed the database with demo users and games.

Run from backend/:  uv run python -m app.seed

Safe to run again: seed users are recognised by their email domain, and their games
and accounts are deleted and recreated each time. Real users are never touched.
"""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Game, GameStatus, User

SEED_DOMAIN = "seed.showup.local"

# Replaced by a real hash once the signup card lands. Seed users cannot log in until then.
PLACEHOLDER_HASH = "seed-user-no-login"

# (first name, reputation)
USERS: list[tuple[str, int]] = [
    ("Maya", 92),
    ("Jordan", 74),
    ("Sam", 50),
    ("Riley", 38),
    ("Alex", 61),
]

# fmt: off
# (host index into USERS, sport, venue, address, days from now, hour, spots, cost, min rep, status)
GAMES: list[tuple[int, str, str, str, int, int, int, str, int, GameStatus]] = [
    (0, "basketball", "BCIT Gym",               "3700 Willingdon Ave, Burnaby",         1, 18, 10, "5.00", 60, GameStatus.OPEN),
    (1, "basketball", "Bonsor Rec Centre",      "6550 Bonsor Ave, Burnaby",             3, 19,  8, "0",     0, GameStatus.OPEN),
    (2, "soccer",     "Central Park Turf",      "3883 Imperial St, Burnaby",            2, 17, 14, "3.00",  0, GameStatus.OPEN),
    (4, "soccer",     "Trillium Park",          "1 Trillium Ln, Vancouver",             5, 10, 12, "0",    50, GameStatus.OPEN),
    (3, "volleyball", "Kitsilano Beach Courts", "1499 Arbutus St, Vancouver",           4, 20, 12, "4.00",  0, GameStatus.OPEN),
    (0, "badminton",  "ClearOne Badminton",     "2368 No 5 Rd, Richmond",               6,  9,  4, "8.00", 70, GameStatus.OPEN),
    (4, "basketball", "Hillcrest Centre",       "4575 Clancy Loranger Way, Vancouver", -2, 18, 10, "0",     0, GameStatus.PLAYED),
    (1, "soccer",     "Burnaby Lake Fields",    "3677 Kensington Ave, Burnaby",         7, 11, 10, "0",     0, GameStatus.CANCELLED),
]
# fmt: on


def seed(db: Session) -> dict[str, int]:
    """Delete previous seed rows, insert fresh ones, commit. Returns row counts."""
    old_ids = db.scalars(select(User.id).where(User.email.like(f"%@{SEED_DOMAIN}"))).all()
    if old_ids:
        db.execute(delete(Game).where(Game.host_id.in_(old_ids)))
        db.execute(delete(User).where(User.id.in_(old_ids)))

    users = [
        User(
            email=f"{name.lower()}@{SEED_DOMAIN}",
            password_hash=PLACEHOLDER_HASH,
            name=name,
            reputation=reputation,
        )
        for name, reputation in USERS
    ]
    db.add_all(users)
    db.flush()  # assigns ids so games can point at their hosts

    now = datetime.now(UTC)
    games = [
        Game(
            host_id=users[host].id,
            sport=sport,
            venue=venue,
            address=address,
            starts_at=(now + timedelta(days=days)).replace(
                hour=hour, minute=0, second=0, microsecond=0
            ),
            spots=spots,
            cost=Decimal(cost),
            min_reputation=min_rep,
            status=status,
        )
        for host, sport, venue, address, days, hour, spots, cost, min_rep, status in GAMES
    ]
    db.add_all(games)
    db.commit()
    return {"users": len(users), "games": len(games)}


def main() -> None:
    with SessionLocal() as db:
        counts = seed(db)
    print(f"seeded {counts['users']} users and {counts['games']} games")


if __name__ == "__main__":
    main()
