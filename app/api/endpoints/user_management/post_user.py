from app.core.handle_exception import exception_handler
from fastapi import APIRouter, status, Depends, HTTPException, Body
from app.api import CREATE_USER_ENDPOINT, CREATE_USER_ENDPOINT_V2
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG, firestore_client, USER_MANAGEMENT_TAG_V2, CREATE_USER_REQUEST_BODY_EXAMPLE
from app.schemas.users import CreateUserRequest, CreateUserResponse, CreateUserRequestV2Enum
from sqlalchemy.orm import Session
from app.db.connector import db_connector
from app.crud.users import UserCRUD
from app.crud import BaseCRUD
from app.core.logger import logger
from openapi.custom_api_spec import create_user_responses, create_user_v2_responses
from app.api.endpoints.user_management.helper import user_management_helper
from app.core.config import USER_COLLECTION_NAME
from typing import Dict, Any

router = APIRouter()

@router.post(
    CREATE_USER_ENDPOINT,
    tags=[USER_MANAGEMENT_TAG],
    description="Create a new user",
    status_code=status.HTTP_200_OK,
    response_model=CreateUserResponse,
    responses={**create_user_responses},
)
@exception_handler
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


@router.post(
    CREATE_USER_ENDPOINT_V2,
    tags=[USER_MANAGEMENT_TAG_V2],
    description="Create a new user V2",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    responses={**create_user_v2_responses},
)
@exception_handler
def create_user_v2(user_data: Dict[str, Any] = Body(example=CREATE_USER_REQUEST_BODY_EXAMPLE)):
    """ 
    V2 Endpoint to create a user

    :param user_data: Request body to create user
    """
    user_management_helper.verify_create_user_payload_v2(user_data)

    if CreateUserRequestV2Enum.PASSWORD.value in user_data:
        password = BaseCRUD.generate_hash_for_password(user_data[CreateUserRequestV2Enum.PASSWORD.value])
        user_data[CreateUserRequestV2Enum.PASSWORD.value] = password

    user_doc = firestore_client.collection(USER_COLLECTION_NAME).document()
    user_doc.set(user_data)
    user_data["id"] = user_doc.id
    return user_data