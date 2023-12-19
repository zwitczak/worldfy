import logging

from sqlalchemy.orm import Session
from .db_set import SQLiteDatabase
from ..models.event import EventPost, EventGet, EventType
from ..models.user import UserBase, Organization, PrivateUser
from ..models.localization import AddressBase, Place
from ..db_model.db_models import EventDB, OrganizerDB, PrivateUserDB, OrganizationDB, ParticipantDB, UserDB

from sqlalchemy import create_engine, or_, select, delete
from sqlalchemy.orm import Session, joinedload
from ..validators.validators import ValidatorDB, Response, Status

logging.basicConfig(level=logging.ERROR)
class UserCRUD:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_users_organized_events(self, user_id):
        try:

            ValidatorDB.user_exists(self._session, user_id)
            events_ids  = [el.id for el in self._session.query(EventDB.id)\
                            .where(OrganizerDB.user_id == user_id)\
                            .where(OrganizerDB.event_id == EventDB.id).all()]
            
            db_events = self._session.query(EventDB).filter(EventDB.id.in_(events_ids))\
                        .options(joinedload(EventDB.place))\
                        .options(joinedload(EventDB.photos))\
                        .options(joinedload(EventDB.organizers))\
                        .options(joinedload(EventDB.types)).all()

            result = [EventGet(id=db_event.id,
                            name=db_event.name,
                            date_start=db_event.date_start,
                            date_end=db_event.date_end,
                            is_public=db_event.is_public,
                            description=db_event.description,
                            is_outdoor=db_event.is_outdoor,
                            participants_limit=db_event.participants_limit,
                            age_limit=db_event.age_limit,
                            organizers=[UserBase.model_validate(o.as_dict()) for o in db_event.organizers],
                            place=Place(id=db_event.place.id,
                                        private= db_event.place.private
                                        ),
                            photos=db_event.photos,
                            address=AddressBase.model_validate(db_event.place.address.as_dict()),
                            types=[EventType.model_validate(et.as_dict()) for et in db_event.types]
                            ) for db_event in db_events]
            
            return Response(status=Status.SUCCEEDED, message=result)
        except Exception as ex:
            # handle exceptions
            return Response(status=Status.FAILED, message=ex, exception=type(ex).__name__)

    
    def get_organizations_by_name(self, name: str):
        try:
            name = name.lower()
            organizations = self._session.query(OrganizationDB).filter(OrganizationDB.name.contains(name)).limit(10)
           
            orgs = []
            for organization in organizations:
                org = Organization(id = organization.id, name=organization.name)
                orgs.append(org)
            
            return Response(status=Status.SUCCEEDED, message=orgs)
        except Exception as ex:
            return Response(status=Status.FAILED, message=ex, exception=type(ex).__name__)

            

    def get_pv_users_by_name(self, name: str):
        try:
            name = name.lower()
            # stmt = select(PrivateUserDB).where((PrivateUserDB.name + PrivateUserDB.surname + PrivateUserDB.nickname).contains(name)).limit(10)
            priv_users = self._session.query(PrivateUserDB).where(PrivateUserDB.visible == True).filter((PrivateUserDB.name + PrivateUserDB.surname + PrivateUserDB.nickname).contains(name)).limit(10)
            usrs = []
            for u in priv_users:
                # print(u.id, u.name, u.surname, u.nickname)
                usr = PrivateUser(id = u.id, name=u.name, surname = u.surname, nickname = u.nickname, visible=u.visible)
                print(usr)
                print("----")
                usrs.append(usr)

            return Response(status=Status.SUCCEEDED, message=usrs)
        except Exception as ex:
            return Response(status=Status.FAILED, message=ex, exception=type(ex).__name__)
    

    def save_event(self, user_id, event_id, role, visible):
        try:
            # check if event exists
            ValidatorDB.event_exists(self._session, event_id)
            
            # check user type
            ValidatorDB.is_user_private(self._session, user_id)

            # check if user is already some kind of participant
            participant_exists = ValidatorDB.participant_exists(self._session, user_id, event_id)

            if participant_exists:
                stmt = delete(ParticipantDB).where(ParticipantDB.user_id == user_id).where(ParticipantDB.event_id == event_id)
                self._session.execute(stmt)
                self._session.commit()
                details = {f"Status of participant ID[{user_id}] changed role to {role}"}
            else:
                details = {f"Status of participant ID[{user_id}] set as: {role}"}

            participant_entrance = ParticipantDB(user_id = user_id, 
                                                 event_id = event_id,
                                                 role = role,
                                                 visibile = visible)
            
            print(participant_entrance)
            self._session.add(participant_entrance)
            self._session.commit()

            return Response(status=Status.SUCCEEDED, message=details)

        except Exception as ex:
            logging.error(f"Exception: {type(ex).__name__}")
            return Response(status=Status.FAILED, message=ex, exception=type(ex).__name__)
