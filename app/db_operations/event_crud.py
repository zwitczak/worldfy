import datetime
from .db_set import SQLiteDatabase
from sqlalchemy import update
from sqlalchemy.orm import Session, joinedload
from ..models.event import EventPost, EventGet, EventType, EventBase
from ..models.user import UserBase
from ..models.localization import AddressBase, Place
from ..db_model.db_models import EventDB, PlaceDB, AddressDB, PhotoEventBridgeDB, PhotoDB, EventTypeBridgeDB, EventTypeDB, OrganizerDB
from enum import Enum


class EventCRUD:
    def __init__(self, session: Session) -> None:
        self._session = session

    def insert_event(self, event: EventPost):
        """
        Używając ORM, obiekt Session() jest odpowiedzialny za konstruowanie instrukcji INSERT w ramach danej tranzakcji.
        The way we instruct the Session to do so is by adding object entries to it; 
        the Session then makes sure these new entries will be emitted to the database when they are needed, 
        using a process known as a flush. The overall process used by the Session to persist objects i s known as the unit of work pattern.
        """
        try:
            # create base event object
            print('Adding new event', event.name)
            db_event = EventDB(name=event.name,
                            date_start=event.date_start,
                            date_end = event.date_end,
                            is_public =event.is_public,
                            description = event.description,
                            is_outdoor = event.is_outdoor,
                            participants_limit = event.participants_limit,
                            age_limit = event.age_limit
                            )
        

            if event.place.id is not None:
                print('Place already exists')
                db_event.place_id = event.place.id
            else:
                # Place does not exist
                print('Creating new place...')
                print("place:", event.place.name)
                place = PlaceDB(name = event.place.name,
                      link = event.place.link,
                      photo = event.place.photo ,
                      private = event.place.private)
      
                db_event.place = place

                stmt = self._session.query(AddressDB).where(AddressDB.country == event.address.country)\
                                .where(AddressDB.city == event.address.city)\
                                .where(AddressDB.street == event.address.street)\
                                .where(AddressDB.postal_code == event.address.postal_code)\
                                .where(AddressDB.street_number == event.address.street_number)\
                                .first()
                
                if stmt and (stmt.local_number is None and event.address.local_number is None):
                    # address already exists
                    print('Address is already in database...')
                    print('Id:',stmt.id)
                    db_event.place.address_id = stmt.id
                else:
                    print('Adding new address')
                    address = AddressDB(country = event.address.country,
                            city = event.address.city,
                            street = event.address.street,
                            postal_code = event.address.postal_code,
                            street_number = event.address.street_number,
                            local_number= event.address.local_number,
                            latitude = event.address.latitude,
                            longitude = event.address.longitude
                            )
                    db_event.place.address = address
            
            # add photos
            for photo in event.photos:
                photo_event_db = PhotoEventBridgeDB(type=photo.type)
                photo_event_db.photo = PhotoDB(link =photo.photo_link , description = photo.photo_description, datetime_posted = datetime.datetime.now())
                db_event.photos.append(photo_event_db)

            self._session.add(db_event)
            self._session.flush()


            #TODO: add icon
            organizers = []
            for org in event.organizers:
                organizers.append(OrganizerDB(event_id=db_event.id, user_id=org.id))

            self._session.add_all(organizers)
            types = []
            for ty in event.types:
                types.append(EventTypeBridgeDB(event_id=db_event.id, type_id=ty.id))

            self._session.add_all(types)

            self._session.commit()
            return {"result":f"Event {db_event} inserted to database successfully"}
        except Exception as e:
            print(e)
            return {"exception": str(e)}

    def get_base_event(self, event_id):
        try:
            db_event = self._session.query(EventDB).where(EventDB.id == event_id).options(joinedload(EventDB.place))\
                                    .options(joinedload(EventDB.photos))\
                                    .options(joinedload(EventDB.organizers))\
                                    .options(joinedload(EventDB.types)).first()
        
            # prepare place object
            place_obj = db_event.place.as_dict()
            place_obj.pop("address_id")


            result = EventGet(id=db_event.id,
                            name=db_event.name,
                            date_start=db_event.date_start,
                            date_end=db_event.date_end,
                            is_public=db_event.is_public,
                            description=db_event.description,
                            is_outdoor=db_event.is_outdoor,
                            participants_limit=db_event.participants_limit,
                            age_limit=db_event.age_limit,
                            organizers=[UserBase.model_validate(o.as_dict()) for o in db_event.organizers],
                            place=Place.model_validate(place_obj),
                            photos=db_event.photos,
                            address=AddressBase.model_validate(db_event.place.address.as_dict()),
                            types=[EventType.model_validate(et.as_dict()) for et in db_event.types]
                            )
        except Exception as e:
            # handle exceptions
            result = str(e)

        return result
    
    def get_event_types(self):
        try:
            event_types = self._session.query(EventTypeDB)
        
            # prepare place object
            result = [EventType.model_validate(et.as_dict()) for et in event_types]
            
        except Exception as e:
            result = e

        return result

    def update_event_base(self, event_id, event_modify: EventBase):
        try:
            stmt = update(EventDB).where(EventDB.id == event_id).values(event_modify.model_dump())
            
            # session.query(stmt)
            self._session.execute(stmt)
            self._session.commit()
            
            return {"status":"success"}
            
        except Exception as e:
            self._session.rollback()
            raise 

    def change_event_localization(self, event_id: int, event_place: Place, event_address: AddressBase):
        try:
            db_event = self._session.query(EventDB).where(EventDB.id == event_id).options(joinedload(EventDB.place)).first()
            # old_place= db_event.place

            if event_address is None:
            # change place only
                print('Change place only')
                if event_place.private is True:
                    # update params only name
                    print('private place')
                    stmt = update(PlaceDB).where(PlaceDB.id == event_place.id).values({'name': event_place.name})
                    self._session.execute(stmt)
                    result = {'status':'changed private place name'}
                
                else:
                    print('public place')
                    # update event.place_id, entry in place table already has information about address,
                    # so we need to update 

                    stmt = update(EventDB).where(EventDB.id == event_id).values({'place_id': event_place.id})
                    self._session.execute(stmt)
                    result = {'status':'changed place for another public place present in database'}

            else:
                if event_place.id is None:
                    # add new place
                    new_place = PlaceDB(name = event_place.name, private=event_place.private)

                    address_stmt = self._session.query(AddressDB).where(AddressDB.country == event_address.country)\
                                    .where(AddressDB.city == event_address.city)\
                                    .where(AddressDB.street == event_address.street)\
                                    .where(AddressDB.postal_code == event_address.postal_code)\
                                    .where(AddressDB.street_number == event_address.street_number)\
                                    .where(AddressDB.local_number == event_address.local_number).first()
                    
                    if address_stmt:
                        # address already exists in db
                        print('Address already exists in db...')
                        print('address id:', address_stmt.id)
                        new_place.address_id = address_stmt.id
                        result = {'status':'created new place with the existing address'}

                    else: 
                        # new address
                        new_address = AddressDB(country = event_address.country,
                                city = event_address.city,
                                street = event_address.street,
                                postal_code = event_address.postal_code,
                                street_number = event_address.street_number,
                                local_number= event_address.local_number,
                                latitude = event_address.latitude,
                                longitude = event_address.longitude
                                )
                        new_place.address = new_address
                        result = {'status': 'created new place with a new address'}


                    self._session.add(new_place)
                    self._session.flush()
                    stmt = update(EventDB).where(EventDB.id == event_id).values({'place_id': new_place.id})
                    self._session.execute(stmt)

                    
                else:
                    # place already exists
                    if event_place.private is True:
                        # modify existing private place

                        address_stmt = self._session.query(AddressDB).where(AddressDB.country == event_address.country)\
                                        .where(AddressDB.city == event_address.city)\
                                        .where(AddressDB.street == event_address.street)\
                                        .where(AddressDB.postal_code == event_address.postal_code)\
                                        .where(AddressDB.street_number == event_address.street_number)\
                                        .where(AddressDB.local_number == event_address.local_number).first()
                        
                        if address_stmt:
                            # address already exists in db
                            print('Address already exists in db...')
                            print('address id:', address_stmt.id)
                            stmt = update(PlaceDB).where(PlaceDB.id == event_place.id).values({'name': event_place.name, 'address_id': address_stmt.id})
                            self._session.execute(stmt)
                            result = {'status': 'modify place params and change address for another existing one'}
                            
                
                        else: 
                            # new address
                            new_address = AddressDB(country = event_address.country,
                                    city = event_address.city,
                                    street = event_address.street,
                                    postal_code = event_address.postal_code,
                                    street_number = event_address.street_number,
                                    local_number= event_address.local_number,
                                    latitude = event_address.latitude,
                                    longitude = event_address.longitude
                                    )
                            self._session.add(new_address)
                            self._session.flush()
                            stmt = update(PlaceDB).where(PlaceDB.id == event_place.id).values({'name': event_place.name, 'address_id': new_address.id})
                            self._session.execute(stmt)
                            result = {'status': 'modify place params and add new address'}

                    
            self._session.commit()
            return result
        except Exception as e:
            print(e)   

            
            
