from fastapi import APIRouter, status
from app.api import CREATE_USER_ENDPOINT
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG

router = APIRouter()

@router.post(
    CREATE_USER_ENDPOINT,
    tags=[USER_MANAGEMENT_TAG],
    description="Create a new user",
    status_code=status.HTTP_200_OK,
)
def create_user():
    pass