from fastapi import APIRouter, status, Query, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from typing import Optional
from app.api import GET_USERS_ENDPOINT, GET_USERS_ENDPOINT_V2
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG, USER_MANAGEMENT_TAG_V2, firestore_client
from app.schemas.users import GetUserResponse, UserSortField, GetUserResponseV2
from app.schemas import SortEnum
from sqlalchemy.orm import Session
from app.db.connector import db_connector
from app.crud.users import UserCRUD
from app.core.handle_exception import exception_handler
from app.core.logger import logger
from openapi.custom_api_spec import get_users_responses, get_users_v2_responses
from app.core.config import USER_COLLECTION_NAME
from math import ceil

router = APIRouter()

@router.get(
    GET_USERS_ENDPOINT,
    tags=[USER_MANAGEMENT_TAG],
    description="Get users details",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponse,
    responses={**get_users_responses},
)
@exception_handler
def get_users(
    page_size: int = Query(default=10, ge=10, le=500, description="Page size"),
    page_number: int = Query(default=1, ge=1, description="Page number"),
    sort_by: Optional[UserSortField] = Query(
        UserSortField.CREATED_AT, description="Field of sorting"
    ),
    sort_order: Optional[SortEnum] = Query(
        "desc", description="Order of sorting"
    ),
    db_session: Session = Depends(db_connector.get_db_session),
    secret_key: str = Header(),
):
    """
    Endpoint to get paginated and sorted user details

    :param request: Request object 
    :param page_size: Page size
    :param page_number: Page number
    :param sort_by: Field of sorting
    :param sort_order: Order of sorting
    :param db_session: Session object
    :param secret_key: Secret key in the header
    """
    user_crud = UserCRUD(db_session)
    users = user_crud.get_user_details(page_size, page_number, sort_order, sort_by.value)

    if users.get("status") == "invalid_page":
        logger.exception("Invalid page navigation")
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid Page Navigation")
    
    return users["users"]


@router.get(
    GET_USERS_ENDPOINT_V2,
    tags=[USER_MANAGEMENT_TAG_V2],
    description="Get user details V2",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponseV2,
    responses={**get_users_v2_responses},
)
@exception_handler
def get_users_v2(
    page_size: int = Query(default=10, ge=10, le=500, description="Page size"),
    page_number: int = Query(default=1, ge=1, description="Page number"),
    secret_key: str = Header(),
):
    """ 
    V2 Endpoint to get paginated user details

    :param page_size: Page size
    :param page_number: Page number
    :param secret_key: Secret key in the header
    """

    user_doc = firestore_client.collection(USER_COLLECTION_NAME)

    total_users = len(list(user_doc.stream()))

    if total_users > 0 and page_number > ceil(total_users / page_size):
        logger.exception("Invalid page navigation")
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid Page Navigation")
    
    user_doc = user_doc.limit(page_size).offset((page_number - 1) * page_size).stream()
    
    user_list = []
    for user in user_doc:
        user_data = user.to_dict()
        user_data["id"] = user.id
        user_list.append(user_data)
    
    user_response = {
        "total_users": total_users,
        "page_size": page_size,
        "page_number": page_number,
        "users": user_list
    }
    return JSONResponse(user_response)