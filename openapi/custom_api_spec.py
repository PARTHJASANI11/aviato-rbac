from app.api.endpoints.user_management import USER_MANAGEMENT_TAG, USER_MANAGEMENT_TAG_V2, USER_DETAILS
from app.api.endpoints.send_email import SEND_EMAIL_TAG
from typing import Dict, Any

from openapi import (
    error_response_500,
    error_response_400,
    error_response_409,
    error_response_401,
)
from fastapi import status

get_users_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400
}

get_users_v2_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400,
    status.HTTP_200_OK: {
        "model": Dict[str, Any],
        "content": {
            "application/json": {
                "example": {
                    "users": USER_DETAILS,
                    "total_users": 20,
                    "page_size": 10,
                    "page_number": 1,
                }
            },
        },
    },
}

create_user_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_409_CONFLICT: error_response_409,
    status.HTTP_400_BAD_REQUEST: error_response_400
}

create_user_v2_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_400_BAD_REQUEST: error_response_400,
    status.HTTP_200_OK: {
        "model": Dict[str, Any],
        "content": {
            "application/json": {
                "example": USER_DETAILS
            },
        },
    },
}

update_user_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400
}

update_user_v2_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400,
    status.HTTP_200_OK: {
        "model": Dict[str, Any],
        "content": {
            "application/json": {
                "example": USER_DETAILS
            },
        },
    },
}

delete_user_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400
}

delete_user_v2_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400,
    status.HTTP_200_OK: {
        "model": Dict[str, Any],
        "content": {
            "application/json": {
                "example": USER_DETAILS
            },
        },
    },
}

send_invitation_email_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
}

tags_metadata = [
    {
        "name": USER_MANAGEMENT_TAG,
        "description": "User Management Endpoints",
    },
    {
        "name": SEND_EMAIL_TAG,
        "description": "Email Sending Endpoints",
    },
    {
        "name": USER_MANAGEMENT_TAG_V2,
        "description": "User Management V2 Endpoints",
    },
]
