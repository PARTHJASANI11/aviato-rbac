from app.models.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Date, ARRAY


class Users(Base):
    """
    DB model for users table
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=True)
    password = Column(String(250), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    company_name = Column(String(50), unique=True, nullable=True)
    mobile_number = Column(String(10), unique=True, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    hash_tag = Column(ARRAY(String(100)), nullable=True)
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
