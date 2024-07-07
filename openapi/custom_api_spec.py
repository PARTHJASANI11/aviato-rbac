from app.api.endpoints.user_management import USER_MANAGEMENT_TAG
from app.api.endpoints.send_email import SEND_EMAIL_TAG

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

create_user_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_409_CONFLICT: error_response_409,
    status.HTTP_400_BAD_REQUEST: error_response_400
}

update_user_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400
}

delete_user_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400
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
]
