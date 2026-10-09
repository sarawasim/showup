"""Shared FastAPI dependencies. Import these in routers instead of repeating Depends(...)."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db

DbDep = Annotated[Session, Depends(get_db)]
