from fastapi import APIRouter, status, Depends, HTTPException
from app.api import CREATE_USER_ENDPOINT
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG
from app.schemas.users import CreateUserRequest, CreateUserResponse
from sqlalchemy.orm import Session
from app.db.connector import db_connector
from app.crud.users import UserCRUD
from app.core.logger import logger
from openapi.custom_api_spec import create_user_responses
from app.api.endpoints.user_management.helper import user_management_helper

router = APIRouter()

@router.post(
    CREATE_USER_ENDPOINT,
    tags=[USER_MANAGEMENT_TAG],
    description="Create a new user",
    status_code=status.HTTP_200_OK,
    response_model=CreateUserResponse,
    responses={**create_user_responses},
)
def create_user(
    user_payload: CreateUserRequest,
    db_session: Session = Depends(db_connector.get_db_session)
):
    """ 
    Endpoint to create a user

    :param user_payload: Request body to create user
    :param db_session: Session object
    """
    user_management_helper.verify_create_user_payload(user_payload)
    user_crud = UserCRUD(db_session)
    create_user_response = user_crud.create_user(user_payload)

    if create_user_response.get("status") == "already_exist":
        logger.exception(create_user_response.get("user")) 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=create_user_response.get("user"))

    return create_user_response.get("user")