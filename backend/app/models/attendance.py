from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.user import User


class Attendance(Base):
    """The host's record of whether a signed-up player showed up. Written after the game."""

    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("game_id", "user_id", name="uq_attendance_game_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    showed_up: Mapped[bool]
    marked_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    marked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    game: Mapped[Game] = relationship(back_populates="attendance")
    user: Mapped[User] = relationship(foreign_keys=[user_id])
