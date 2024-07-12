from app.core.handle_exception import exception_handler
from fastapi import APIRouter, status, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from app.api import UPDATE_OR_DELETE_USER_ENDPOINT, UPDATE_OR_DELETE_USER_ENDPOINT_V2
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG, USER_MANAGEMENT_TAG_V2, firestore_client
from app.schemas.users import DeleteUserResponse
from sqlalchemy.orm import Session
from app.db.connector import db_connector
from app.crud.users import UserCRUD
from app.core.logger import logger
from openapi.custom_api_spec import delete_user_responses, delete_user_v2_responses
from app.core.config import USER_COLLECTION_NAME
from typing import Dict, Any

router = APIRouter()

@router.delete(
    UPDATE_OR_DELETE_USER_ENDPOINT.format("{user_id}"),
    tags=[USER_MANAGEMENT_TAG],
    description="Delete user",
    status_code=status.HTTP_200_OK,
    response_model=DeleteUserResponse,
    responses={**delete_user_responses},
)
@exception_handler
def delete_user(
    user_id: int,
    db_session: Session = Depends(db_connector.get_db_session),
    secret_key: str = Header(),
):
    """
    Endpoint to delete the user

    :param user_id: ID of the user
    :param db_session: Session object
    :param secret_key: Secret key in the header
    """
    user_crud = UserCRUD(db_session)
    deleted_user_response = user_crud.delete_user(user_id)

    if deleted_user_response.get("status") == "user_not_exist":
        logger.exception("User with user id %s does not exist" % (user_id))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    
    return deleted_user_response.get("user")

@router.delete(
    UPDATE_OR_DELETE_USER_ENDPOINT_V2.format("{user_id}"),
    tags=[USER_MANAGEMENT_TAG_V2],
    description="Delete user V2",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    responses={**delete_user_v2_responses},
)
@exception_handler
def delete_user_v2(
    user_id: str,
    secret_key: str = Header(),
):
    """
    V2 Endpoint to delete the user

    :param user_id: ID of the user
    :param secret_key: Secret key in the header
    """
    user_doc = firestore_client.collection(USER_COLLECTION_NAME).document(user_id)
    
    user = user_doc.get()
    if not user.exists:
        logger.exception("User with user id %s does not exist" % (user_id))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    
    user_doc.delete()
    user = user.to_dict()
    user["id"] = user_doc.id
    
    return JSONResponse(user)