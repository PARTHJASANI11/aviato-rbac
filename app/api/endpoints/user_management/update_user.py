from fastapi import APIRouter, status
from app.api import UPDATE_OR_DELETE_USER_ENDPOINT
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG

router = APIRouter()

@router.put(
    UPDATE_OR_DELETE_USER_ENDPOINT,
    tags=[USER_MANAGEMENT_TAG],
    description="Update user details",
    status_code=status.HTTP_200_OK,
)
def update_user():
    pass