from sqlalchemy.orm import Session
import bcrypt

class BaseCRUD:
    """
    Base class for CRUD operations 
    """
    def __init__(self, session: Session):
        """
        :param session: Database session 
        """
        self.db_session = session

    @staticmethod
    def generate_hash_for_password(password: str):
        """
        Method to generate hashed password

        :param password: Password
        :return str: hashed string 
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        return hashed_password