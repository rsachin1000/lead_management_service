from sqlalchemy import create_engine
from urllib.parse import quote_plus


class DBConfig:
    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str,
            db_name: str
        ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

    def get_connection_string(self) -> str:
        password = quote_plus(self.password)
        return f'postgresql://{self.username}:{password}@{self.host}:{self.port}/{self.db_name}'


class DatabaseConnection:
    _instance = None
    _engine = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
    
    def initialize(self, config: DBConfig):
        self._engine = create_engine(
            config.get_connection_string(),
            pool_size=5,
            max_overflow=10,
            echo=True
        )

    @property
    def engine(self):
        if self._engine is None:
            raise Exception("Connection not initialized. Call initialize()")
        return self._engine
        


