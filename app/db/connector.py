from app.core.config import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool


class DatabaseConnector:
    """
    Class to define database connection 
    """
    def __init__(self):
        self.client = None

    def create_database_connection(self) -> None:
        """
        Create a connection to the database
        """
        self.client = create_engine(DB_URI, poolclass=NullPool)

    def get_db_session(self) -> Session:
        """
        Create a new SQLAlchemy session
        """
        session = Session(bind=self.client)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def close_database_connection(self) -> None:
        """
        Close a connection to the database
        """
        self.client.dispose()


db_connector = DatabaseConnector()
