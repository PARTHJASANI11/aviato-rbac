from fastapi import APIRouter, status
from app.api import UPDATE_OR_DELETE_USER_ENDPOINT
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG

router = APIRouter()

@router.delete(
    UPDATE_OR_DELETE_USER_ENDPOINT,
    tags=[USER_MANAGEMENT_TAG],
    description="Delete user",
    status_code=status.HTTP_200_OK,
)
def delete_user():
    pass