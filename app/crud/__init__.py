from sqlalchemy.orm import Session


class BaseCRUD:
    """
    Base class for CRUD operations 
    """
    def __init__(self, session: Session):
        """
        :param session: Database session 
        """
        self.db_session = session
