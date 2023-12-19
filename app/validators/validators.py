# from __future__ import annotations

import re
from enum import Enum
from app.models.user import ParticipantType
from app.db_model.db_models import UserDB
from app.db_model.db_models import EventDB, ParticipantDB
from  app.validators.exceptions import EventDoNotExist, InvalidUserType, UserDoestNotExist, InvalidParticipantRole

class Status(Enum):
    SUCCEEDED = 1
    FAILED = 0

class Response:
    def __init__(self, status:Status, message: str, exception: str | None = None ):
        self.status = status
        self.message = message
        self.exception = exception

class ValidatorLogic:
    def is_participant_type(participant_type: str):
        try:
            participant_type = participant_type.upper()
            ParticipantType(participant_type)
        except:
            raise InvalidParticipantRole(f"Provided role [{participant_type}] is not valid.")
        

class ValidatorDB:
    def is_user_private(session, user_id):
        user = session.query(UserDB).where(UserDB.id == user_id).first()
        if user is None:
            raise UserDoestNotExist(f"User with given ID [{user_id}] does not exist.")
        if user.type != 'PRIVATE_USER':
            raise InvalidUserType("User is not of private user type.")
        
    def event_exists(session, event_id):
        event_count = session.query(EventDB).where(EventDB.id == event_id).count()

        if event_count != 1:
            raise EventDoNotExist(f"Event with given ID [{event_id}] does not exist.")
        
    def participant_exists(session, user_id, event_id):
        existing_role = session.query(ParticipantDB).where(ParticipantDB.user_id == user_id).where(ParticipantDB.event_id == event_id).count()
        if existing_role == 1:
            return True
        else: 
            return False
        
    def user_exists(session, user_id):
        existing_user = session.query(UserDB).where(UserDB.id == user_id).count()
        if existing_user != 1:
            raise UserDoestNotExist(f"User with given ID [{user_id}] does not exist.")
