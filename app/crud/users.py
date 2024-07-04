from app.crud import BaseCRUD
from sqlalchemy.orm import Session
from app.models.users import Users
from math import ceil
from app.schemas.users import UserSortField
from app.schemas import SORT_TYPE

class UserCRUD(BaseCRUD):
    """
    Class to define CRUD methods for user management 
    """
    def __init__(self, session: Session):
        """
        :param session: Database session 
        """
        super().__init__(session)
        self.users = Users
        self.sort_field_mapping = {
            UserSortField.EMAIL.value : self.users.email,
            UserSortField.CREATED_AT.value: self.users.created_at
        }

    def get_user_details(self, page_size, page_number, sort_order, sort_by):
        """
        Method to get paginated and sorted data from database

        :param page_size: Page size
        :param page_number: Page number
        :param sort_order: Order of sorting
        :param sort_by: Field of sorting
        :return dict: Paginated and sorted data from database
        """
        user_query = self.db_session.query(self.users)

        total_users = user_query.count()

        if total_users >= 0 and page_number > ceil(total_users / page_size):
            return {"status": "invalid_page", "users": []}
        
        users = (
            user_query.order_by(SORT_TYPE[sort_order](self.sort_field_mapping.get(sort_by)))
            .offset((page_number - 1) * page_size)
            .limit(page_size)
            .with_entities(
                self.users.id, 
                self.users.email, 
                self.users.first_name, 
                self.users.last_name, 
                self.users.created_at, 
                self.users.updated_at
            )
            .all()
        )
        users_response = {}
        users_response["page_size"] = page_size
        users_response["page_number"] = page_number
        users_response["total_users"] = total_users
        users_response["users"] = list(users)

        return {"status": "success", "users": users_response}