from app.schemas.users import CreateUserRequest, CreateUserRequestV2Enum
from fastapi import status, HTTPException
from typing import Dict
from pydantic import validate_email
import re

class UserManagementHelper:
    """
    User management API helper class 
    """
    @staticmethod
    def verify_create_user_payload(user_payload: CreateUserRequest):
        """
        Method to verify create user payload for various registration ways 
        """
        if user_payload.company_name is None and user_payload.mobile_number is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Company name or mobile number is required to register")
        elif user_payload.company_name is not None and (user_payload.email is None or user_payload.password is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email and password are required if you are registering with company name")
        elif (
            (user_payload.mobile_number is not None and user_payload.hash_tag is None) and 
            (user_payload.mobile_number is not None and user_payload.date_of_birth is None)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Hash tag or birth date is required if you are registering with company name")
            
    @staticmethod
    def verify_create_user_payload_v2(user_payload: Dict):
        """
        Method to verify user payload 
        """
        if user_payload == {}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="In order to register there should be some value in request body")
        if CreateUserRequestV2Enum.EMAIL.value in user_payload:
            try:
                validate_email(user_payload["email"].strip())
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Email ID is not valid")
        if CreateUserRequestV2Enum.PASSWORD.value in user_payload:
            password = user_payload["password"].strip()
            password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$"
            print(bool(re.match(password_pattern, password)))
            if not bool(re.match(password_pattern, password)) or ' ' in password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Password's length should be between 6 to 10 characters"
                    " without any whitespace. It should also contains at least"
                    "  one small & capital letter, number.")
        if CreateUserRequestV2Enum.MOBILE_NO.value in user_payload:
            if len(user_payload[CreateUserRequestV2Enum.MOBILE_NO.value].strip()) != 10:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Mobile number should have 10 digits")

user_management_helper = UserManagementHelper()