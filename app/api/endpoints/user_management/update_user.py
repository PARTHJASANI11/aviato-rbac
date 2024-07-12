from app.core.handle_exception import exception_handler
from fastapi import APIRouter, status, Depends, HTTPException, Header, Body
from fastapi.responses import JSONResponse
from app.api import UPDATE_OR_DELETE_USER_ENDPOINT, UPDATE_OR_DELETE_USER_ENDPOINT_V2
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG, USER_MANAGEMENT_TAG_V2, firestore_client, UPDATE_USER_REQUEST_BODY_EXAMPLE
from app.schemas.users import UpdateUserRequest, DeleteUserResponse, CreateUserRequestV2Enum
from sqlalchemy.orm import Session
from app.db.connector import db_connector
from app.crud.users import UserCRUD
from app.crud import BaseCRUD
from app.core.logger import logger
from openapi.custom_api_spec import update_user_responses, update_user_v2_responses
from typing import Dict, Any
from app.core.config import USER_COLLECTION_NAME
from app.api.endpoints.user_management.helper import user_management_helper

router = APIRouter()

@router.put(
    UPDATE_OR_DELETE_USER_ENDPOINT.format("{user_id}"),
    tags=[USER_MANAGEMENT_TAG],
    description="Update user details",
    status_code=status.HTTP_200_OK,
    response_model=DeleteUserResponse,
    responses={**update_user_responses},
)
@exception_handler
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

@router.put(
    UPDATE_OR_DELETE_USER_ENDPOINT_V2.format("{user_id}"),
    tags=[USER_MANAGEMENT_TAG_V2],
    description="Update user details V2",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    responses={**update_user_v2_responses},
)
@exception_handler
def update_user(
    user_id: str,
    update_user_data: Dict[str, Any] = Body(example=UPDATE_USER_REQUEST_BODY_EXAMPLE),
    secret_key: str = Header(),
):
    """
    V2 Endpoint to update the user details

    :param user_id: ID of the user
    :param update_user_data: Request body to update the user details
    :param secret_key: Secret key in the header
    """
    user_management_helper.verify_create_user_payload_v2(update_user_data)

    user_doc = firestore_client.collection(USER_COLLECTION_NAME).document(user_id)
    
    user = user_doc.get()
    if not user.exists:
        logger.exception("User with user id %s does not exist" % (user_id))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    
    if CreateUserRequestV2Enum.PASSWORD.value in update_user_data:
        password = BaseCRUD.generate_hash_for_password(update_user_data[CreateUserRequestV2Enum.PASSWORD.value])
        update_user_data[CreateUserRequestV2Enum.PASSWORD.value] = password
    
    user_doc.update(update_user_data)
    
    updated_user_doc = firestore_client.collection(USER_COLLECTION_NAME).document(user_id)
    updated_user = updated_user_doc.get()
    updated_user = updated_user.to_dict()
    updated_user["id"] = updated_user_doc.id
    
    return JSONResponse(updated_user)