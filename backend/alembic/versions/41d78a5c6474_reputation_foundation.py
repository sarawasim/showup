"""reputation foundation

Revision ID: 41d78a5c6474
Revises: b8547a9d4de2
Create Date: 2026-10-08

Autogenerate found the new columns. The constraint and default changes below were added by
hand, because autogenerate does not detect check constraints or server default changes.
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "41d78a5c6474"
down_revision: str | Sequence[str] | None = "b8547a9d4de2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Players: everyone now starts at 100 (existing rows keep their value).
    op.alter_column("users", "reputation", server_default="100")

    # Attendance: a player may dispute a mark once.
    op.add_column("attendance", sa.Column("disputed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("attendance", sa.Column("dispute_note", sa.String(length=300), nullable=True))

    # Games: duration, one-step fallback minimum, updated_at.
    op.add_column(
        "games",
        sa.Column("duration_minutes", sa.Integer(), server_default="90", nullable=False),
    )
    op.add_column("games", sa.Column("fallback_min_reputation", sa.Integer(), nullable=True))
    op.add_column("games", sa.Column("fallback_hours_before_start", sa.Integer(), nullable=True))
    op.add_column(
        "games",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # Ranges for the new columns. min_reputation keeps its existing 0 to 100 constraint.
    op.create_check_constraint(
        "ck_games_fallback_min_reputation_range",
        "games",
        "fallback_min_reputation IS NULL OR fallback_min_reputation BETWEEN 0 AND 100",
    )
    op.create_check_constraint(
        "ck_games_fallback_hours_range",
        "games",
        "fallback_hours_before_start IS NULL OR fallback_hours_before_start BETWEEN 1 AND 168",
    )
    op.create_check_constraint(
        "ck_games_duration_range", "games", "duration_minutes BETWEEN 15 AND 480"
    )


def downgrade() -> None:
    op.drop_constraint("ck_games_duration_range", "games", type_="check")
    op.drop_constraint("ck_games_fallback_hours_range", "games", type_="check")
    op.drop_constraint("ck_games_fallback_min_reputation_range", "games", type_="check")
    op.drop_column("games", "updated_at")
    op.drop_column("games", "fallback_hours_before_start")
    op.drop_column("games", "fallback_min_reputation")
    op.drop_column("games", "duration_minutes")
    op.drop_column("attendance", "dispute_note")
    op.drop_column("attendance", "disputed_at")
    op.alter_column("users", "reputation", server_default="50")
