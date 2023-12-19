from abc import ABC, abstractmethod
from typing import Any, List
from ..models.event import EventPost
from ..models.user import Organization, PrivateUser, ParticipantType
from ..db_operations.user_crud import UserCRUD,SQLiteDatabase
from ..validators.validators import ValidatorLogic, Status, Response
from ..validators.exceptions import InvalidParticipantRole
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
        try:
            events = UserCRUD(SQLiteDatabase.create_session()).get_users_organized_events(self._user_id)
            return events
        except Exception as ex:
            return Response(status=Status.FAILED, message=ex, exception=type(ex).__name__)
    
    
class getUsersByName(Strategy):
    def __init__(self, name: str, organizations: bool, pv_users: bool) -> None:
        super().__init__()
        self._name= name
        self._organizations = organizations
        self._pv_users = pv_users

    def execute(self):
        try:
            message = {}

            if self._organizations:
                organizations_result = UserCRUD(SQLiteDatabase.create_session()).get_organizations_by_name(self._name)
                if organizations_result.status == Status.SUCCEEDED:
                    message['organizations'] = organizations_result.message
                else:
                    return organizations_result
            if self._pv_users:

                pv_users_result = UserCRUD(SQLiteDatabase.create_session()).get_pv_users_by_name(self._name)
                if pv_users_result.status ==  Status.SUCCEEDED:
                    message['private_users'] = pv_users_result.message
                else: 
                    return pv_users_result
            return Response(status=Status.SUCCEEDED, message=message)

        except Exception as ex:
            return Response(status=Status.FAILED, message=ex, exception=type(ex).__name__ )

    
   
class saveEvent(Strategy):
    def __init__(self, user_id: int, event_id: bool, role: str, visible: bool):
        super().__init__()
        self._user_id= user_id
        self._event_id = event_id
        self._role = role
        self._visible = visible

    def execute(self):
        try:
            ValidatorLogic.is_participant_type(self._role)
            save_result = UserCRUD(SQLiteDatabase.create_session()).save_event(user_id=self._user_id, event_id=self._event_id, role=self._role, visible=self._visible)
            return save_result
        except Exception as ex:
            return Response(status=Status.FAILED, message=ex, exception=type(ex).__name__ )
        

        


    


