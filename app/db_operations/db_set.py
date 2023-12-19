import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

pth ="//home//worldfy//app//db_sqlite//test3.db"

class DataBase:
    def __init__(self, conn_str):
        self._conn_str = conn_str

class SQLite(DataBase):
    def __init__(self, echo):
        super().__init__(f"sqlite:///{pth}")
        self.engine = create_engine(url=self._conn_str,
                                    future=True,
                                    echo=echo,
                                    connect_args={"check_same_thread": False})
        
    def create_session(self):
        return Session(self.engine)

SQLiteDatabase = SQLite(echo=False)