from abc import ABC, abstractmethod
from typing import Any, List
from ..models.event import EventPost
from ..db_operations.user_crud import UserCRUD,SQLiteDatabase
# from ..db_operations import SQLiteDatabase
class Strategy(ABC):
    @abstractmethod
    def execute(self):
        pass

class UserManager():
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute_operation(self):
        result = self._strategy.execute()
        return result

class Strategy(ABC):
    @abstractmethod
    def execute(self):
        pass

class getEventsByUser(Strategy):
    def __init__(self, user_id) -> None:
        super().__init__()
        self._user_id= user_id

    def execute(self):
        events = UserCRUD(SQLiteDatabase.create_session()).get_users_organized_events(self._user_id)
        return events
    


