from pydantic import BaseModel, constr, field_validator, validate_email
from typing import List, Optional
from enum import Enum
import re
from datetime import date

class UserDetails(BaseModel):
    """
    Users fields
    """

    id: int
    email: Optional[str]
    company_name: Optional[str]
    mobile_number: Optional[str]
    date_of_birth: Optional[str]
    hash_tag: Optional[List[str]]
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

class CreateUserRequest(BaseModel):
    """
    Request body schema for create user endpoint 
    """
    email: Optional[constr(strip_whitespace=True)] = None
    password: Optional[constr(min_length=6, max_length=10)] = None
    company_name: Optional[constr(strip_whitespace=True)] = None
    mobile_number: Optional[constr(min_length=1, max_length=10, strip_whitespace=True)] = None
    date_of_birth: Optional[date] = None
    hash_tag: Optional[List] = None
    first_name: constr(strip_whitespace=True)
    last_name: constr(strip_whitespace=True)

    @field_validator("email", mode="before")
    def validate_email_address(cls, email):
        try:
            validate_email(email)
            return email
        except Exception:
            raise
    
    @field_validator("password", mode="before")
    def validate_password(cls, password):
        password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$"
        if bool(re.match(password_pattern, password)) and ' ' not in password:
            return password
        else:
            raise ValueError(
                "Password's length should be between 6 to 10 characters"
                " without any whitespace. It should also contains at least"
                "  one small & capital letter, number."    
            )
    
    @field_validator("mobile_number", mode="before")
    def validate_mobile_number(cls, mobile_number):
        if len(mobile_number.strip()) != 10:
            raise ValueError("Mobile number should have 10 digits")
        
        return mobile_number
        
class CreateUserResponse(BaseModel):
    """
    Response of create user endpoint 
    """
    id: int
    email: Optional[str]
    company_name: Optional[str]
    mobile_number: Optional[str]
    date_of_birth: Optional[str]
    hash_tag: Optional[List[str]]
    first_name: str
    last_name: str


class UpdateUserRequest(BaseModel):
    """
    Request body schema for update user endpoint 
    """

    email: constr(strip_whitespace=True)
    password: constr(min_length=6, max_length=10)

    @field_validator("email", mode="before")
    def validate_email_address(cls, email):
        try:
            validate_email(email)
            return email
        except Exception:
            raise

    @field_validator("password", mode="before")
    def validate_password(cls, password):
        password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$"
        if bool(re.match(password_pattern, password)) and ' ' not in password:
            return password
        else:
            raise ValueError(
                "Password's length should be between 6 to 10 characters"
                " without any whitespace. It should also contains at least"
                "  one small & capital letter, number."    
            )
        
class DeleteUserResponse(BaseModel):
    """
    Response of delete user endpoint 
    """
    id: int
    email: str