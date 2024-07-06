from app.crud import BaseCRUD
from sqlalchemy.orm import Session
from app.models.users import Users
from math import ceil
from app.schemas.users import UserSortField
from app.schemas import SORT_TYPE
from app.schemas.users import CreateUserRequest

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
                self.users.company_name,
                self.users.date_of_birth,
                self.users.mobile_number,
                self.users.hash_tag, 
                self.users.created_at, 
                self.users.updated_at
            )
            .all()
        )
        
        users_response = {}
        users_response["page_size"] = page_size
        users_response["page_number"] = page_number
        users_response["total_users"] = total_users
        users_response["users"] = [
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "company_name": user.company_name,
                "mobile_number": user.mobile_number,
                "hash_tag": user.hash_tag,
                "date_of_birth": str(user.date_of_birth),
                "created_at": str(user.created_at),
                "updated_at": str(user.updated_at)
            } 
            for user in users
        ]

        return {"status": "success", "users": users_response}
    
    def check_user_in_db(self, **kwargs):
        """ 
        Method to get user details by email

        :param email: Email ID
        """
        list_of_filters = []
        for filter in kwargs:
            filter_value = getattr(self.users, filter) == kwargs[filter]
            list_of_filters.append(filter_value)
        user = (
            self.db_session.query(self.users)
            .filter(*list_of_filters)
            .first()
        )
        return user
    
    
    def create_user(self, user_payload: CreateUserRequest):
        """
        Method to add user in the database

        :param user_payload: User details 
        :return dict: Inserted user details
        """
        email = user_payload.email
        password = user_payload.password
        first_name = user_payload.first_name.title()
        last_name = user_payload.last_name.title()
        company_name = user_payload.company_name
        date_of_birth = user_payload.date_of_birth
        mobile_number = user_payload.mobile_number
        hash_tag = set(user_payload.hash_tag) if user_payload.hash_tag else None

        if company_name:
            check_user_exist = self.check_user_in_db(company_name=company_name)
            if check_user_exist:
                return {"status": "already_exist", "user": "Company already exist"}
            password = self.generate_hash_for_password(password)
            
        if mobile_number:
            check_user_exist = self.check_user_in_db(mobile_number=mobile_number)
            if check_user_exist:
                return {"status": "already_exist", "user": "Mobile number already exist"}
            
        user = self.users(**{
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "company_name": company_name,
            "date_of_birth": date_of_birth,
            "mobile_number": mobile_number,
            "hash_tag": hash_tag,
        })
        
        self.db_session.add(user)
        self.db_session.commit()

        if company_name:
            inserted_user = self.check_user_in_db(company_name=company_name)
        else:
            inserted_user = self.check_user_in_db(mobile_number=mobile_number)
    
        return {
            "status": "added", 
            "user": {
                "id": inserted_user.id,
                "email": inserted_user.email,
                "first_name": inserted_user.first_name,
                "last_name": inserted_user.last_name,
                "company_name": inserted_user.company_name,
                "mobile_number": inserted_user.mobile_number,
                "date_of_birth": inserted_user.date_of_birth,
                "hash_tag": inserted_user.hash_tag
            }
        }

    def update_user(self, id, email, password):
        """
        Method to update the user details in the database

        :param id: ID of the user
        :param email: Email ID
        :param password: Password 
        :return dict: Updated user details
        """
        check_user_exist = self.check_user_in_db(id=id)

        if not check_user_exist:
            return {"status": "user_not_exist", "user": {}}
        
        hashed_password = self.generate_hash_for_password(password)

        check_user_exist.email = email
        check_user_exist.password = hashed_password

        self.db_session.commit()

        updated_user = self.check_user_in_db(email=email)

        return {
            "status": "updated", 
            "user": {
                "id": updated_user.id,
                "email": updated_user.email,
            }
        }
    
    def delete_user(self, id):
        """
        Method to delete user from the database

        :param id: ID of the user
        :return dict: Deleted user details 
        """
        check_user_exist = self.check_user_in_db(id=id)

        if not check_user_exist:
            return {"status": "user_not_exist", "user": {}}
        
        self.db_session.query(self.users).filter(self.users.id == id).delete()
        self.db_session.commit()
        
        return {
            "status": "deleted", 
            "user": {
                "id": check_user_exist.id,
                "email": check_user_exist.email
            }
        }