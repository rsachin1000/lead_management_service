from typing import Generator
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from .connection import DatabaseConnection



class DatabaseSession:
    def __init__(self, db_connection: DatabaseConnection) -> None:
        self.SessionLocal = sessionmaker(bind=db_connection.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_db(self) -> Session:
        with self.get_session() as session:
            return session
