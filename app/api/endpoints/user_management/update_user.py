from fastapi import APIRouter, status, Depends, HTTPException, Header
from app.api import UPDATE_OR_DELETE_USER_ENDPOINT
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG
from app.schemas.users import UpdateUserRequest, DeleteUserResponse
from sqlalchemy.orm import Session
from app.db.connector import db_connector
from app.crud.users import UserCRUD
from app.core.logger import logger
from openapi.custom_api_spec import update_user_responses

router = APIRouter()

@router.put(
    UPDATE_OR_DELETE_USER_ENDPOINT.format("{user_id}"),
    tags=[USER_MANAGEMENT_TAG],
    description="Update user details",
    status_code=status.HTTP_200_OK,
    response_model=DeleteUserResponse,
    responses={**update_user_responses},
)
def update_user(
    user_id: int,
    update_user_payload: UpdateUserRequest,
    db_session: Session = Depends(db_connector.get_db_session),
    secret_key: str = Header(),
):
    """
    Endpoint to update the user details

    :param user_id: ID of the user
    :param update_user_payload: Request body to update the user details
    :param db_session: Session object 
    :param secret_key: Secret key in the header
    """
    user_crud = UserCRUD(db_session)
    updated_user_response = user_crud.update_user(user_id, update_user_payload.email, update_user_payload.password)

    if updated_user_response.get("status") == "user_not_exist":
        logger.exception("User with user id %s does not exist" % (user_id))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    
    return updated_user_response.get("user")