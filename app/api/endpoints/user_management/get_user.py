from fastapi import APIRouter, status, Request, Query, Depends, HTTPException
from typing import Optional
from app.api import GET_USERS_ENDPOINT
from app.api.endpoints.user_management import USER_MANAGEMENT_TAG
from app.schemas.users import GetUserResponse, UserSortField
from app.schemas import SortEnum
from sqlalchemy.orm import Session
from app.db.connector import db_connector
from app.crud.users import UserCRUD

router = APIRouter()

@router.get(
    GET_USERS_ENDPOINT,
    tags=[USER_MANAGEMENT_TAG],
    description="Get users details",
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponse,
)
def get_users(
    request: Request,
    page_size: int = Query(default=10, ge=10, le=500, description="Page size"),
    page_number: int = Query(default=1, ge=1, description="Page number"),
    sort_by: Optional[UserSortField] = Query(
        UserSortField.CREATED_AT, description="Field of sorting"
    ),
    sort_order: Optional[SortEnum] = Query(
        "desc", description="Order of sorting"
    ),
    db_session: Session = Depends(db_connector.get_db_session)
):
    """
    Endpoint to get paginated and sorted user details

    :param request: Request object 
    :param page_size: Page size
    :param page_number: Page number
    :param sort_by: Field of sorting
    :param sort_order: Order of sorting
    :param db_session: Session object
    """
    user_crud = UserCRUD(db_session)
    users = user_crud.get_user_details(page_size, page_number, sort_order, sort_by.value)

    if users.get("status") == "invalid_page":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid Page Navigation")
    
    return users["users"]