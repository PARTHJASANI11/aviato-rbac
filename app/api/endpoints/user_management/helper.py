from app.schemas.users import CreateUserRequest
from fastapi import status, HTTPException

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
            

user_management_helper = UserManagementHelper()