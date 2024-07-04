from app.models.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func


class Users(Base):
    """
    DB model for users table
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )
