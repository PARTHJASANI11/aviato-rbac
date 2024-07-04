from typing import Any
from sqlalchemy.orm import as_declarative
from app.core.config import POSTGRES_SCHEMA

@as_declarative()
class Base:
    """
    Base class for SqlAlchemy models 
    """
    id = Any
    __name__ = str

    __table_args__ = {"extend_existing": True, "schema": POSTGRES_SCHEMA}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}