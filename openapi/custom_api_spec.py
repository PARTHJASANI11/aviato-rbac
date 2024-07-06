from app.api.endpoints.user_management import USER_MANAGEMENT_TAG

from openapi import (
    error_response_500,
    error_response_400,
    error_response_409,
    error_response_401,
)
from fastapi import status

# Polaris Auth RBAC
get_users_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_401_UNAUTHORIZED: error_response_401,
    status.HTTP_400_BAD_REQUEST: error_response_400
}

create_user_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_response_500,
    status.HTTP_409_CONFLICT: error_response_409
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

tags_metadata = [
    {
        "name": USER_MANAGEMENT_TAG,
        "description": "User Management Endpoints",
    },
]
