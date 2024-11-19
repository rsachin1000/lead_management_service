from typing import Generator
from sqlalchemy.orm import Session
from src.database.connection import DBConfig, DatabaseConnection
from src.database.session import DatabaseSession
from src.database.data_models import Base, Lead, Salesperson

class Database:
    _instance = None
    _session = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def init_app(self, config: DBConfig):
        """Initialize database with configuration"""
        # Initialize connection
        db_connection = DatabaseConnection.get_instance()
        db_connection.initialize(config)
        
        # Create session
        self._session = DatabaseSession(db_connection)
        
        # Create tables
        Base.metadata.create_all(bind=db_connection.engine)
    
    @property
    def session(self) -> DatabaseSession:
        if self._session is None:
            raise RuntimeError("Database not initialized. Call init_app first.")
        return self._session


# Create a singleton instance
db = Database.get_instance()


# Dependency for FastAPI
def get_db() -> Session:
    """
    Database dependency to be used in FastAPI endpoints.
    """
    return db.session.get_db()


__all__ = ['db', 'get_db', 'DatabaseConfig', 'DatabaseType']
