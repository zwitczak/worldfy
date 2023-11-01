from sqlalchemy.orm import Session
from .db_set import SQLiteDatabase
from ..models.event import EventPost, EventGet, EventType
from ..models.user import UserBase
from ..models.localization import AddressBase, Place
from ..db_model.db_models import EventDB, PlaceDB, AddressDB, PhotoEventBridgeDB,\
                                 PhotoDB, EventTypeBridgeDB, EventTypeDB, OrganizerDB
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

class UserCRUD:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_users_organized_events(self, user_id):
        try:
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
            print(result)
        except Exception as e:
            # handle exceptions
            result = str(e)

        return result