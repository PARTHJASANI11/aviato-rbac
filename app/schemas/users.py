from pydantic import BaseModel
from typing import List
from enum import Enum

class UserDetails(BaseModel):
    """
    Users fields
    """

    id: int
    email: str
    first_name: str
    last_name: str
    created_at: str
    updated_at: str

class GetUserResponse(BaseModel):
    """
    Get users response 
    """
    users: List[UserDetails]
    total_users: int
    page_size: int
    page_number: int

class UserSortField(str, Enum):
    """
    Sorting fields for get users 
    """
    EMAIL = "email"
    CREATED_AT = "created_at"