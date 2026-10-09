from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.user import User


class SignupStatus(enum.StrEnum):
    JOINED = "joined"
    WAITLIST = "waitlist"
    REMOVED = "removed"  # the host removed the player; keeps the history


class Signup(Base):
    """One player's place in one game. A user has at most one row per game."""

    __tablename__ = "signups"
    __table_args__ = (UniqueConstraint("game_id", "user_id", name="uq_signups_game_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[SignupStatus] = mapped_column(
        Enum(
            SignupStatus,
            native_enum=False,
            length=20,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=SignupStatus.JOINED,
        server_default=SignupStatus.JOINED.value,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    game: Mapped[Game] = relationship(back_populates="signups")
    user: Mapped[User] = relationship(back_populates="signups")
