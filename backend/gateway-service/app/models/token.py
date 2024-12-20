from __future__ import annotations
from odmantic import Reference
from app.db.base_class import Base
from .user import User


class Token(Base):
    token: str
    authenticates_id: User = Reference()