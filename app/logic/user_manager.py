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
    
class getUsersByName(Strategy):
    def __init__(self, name: str, organizations: bool, pv_users: bool) -> None:
        super().__init__()
        self._name= name
        self._organizations = organizations
        self._pv_users = pv_users

    def execute(self):
        try:
            if self._organizations:
                print('Get organizations...')
                organizations_result = UserCRUD(SQLiteDatabase.create_session()).get_organizations_by_name(self._name)
                if organizations_result.get('status', None) == 'failed':
                    raise Exception(f"Operation failed due to exception:{organizations_result.get('details', 'exception')}")

            if self._pv_users:
                print('Get private users...')

                pv_users_result = UserCRUD(SQLiteDatabase.create_session()).get_pv_users_by_name(self._name)
                print(pv_users_result)
                if pv_users_result.get('status', None) == 'failed':
                    raise Exception(f"Operation failed due to exception:{pv_users_result.get('details', 'exception')}")

            result = {"organizations": organizations_result.get('organizations', None), "private users": pv_users_result.get('users', None)}
        except Exception as e:
            raise Exception(f"Operation failed due to exception:{pv_users_result.get('details', 'exception')}, \n{e}")

        return result
    


