import datetime
from .db_set import SQLiteDatabase
from sqlalchemy import update, delete
from sqlalchemy.orm import Session, joinedload
from ..models.event import EventPost, EventGet, EventType, EventBase
from ..models.user import UserBase, Organization, PrivateUser
from ..models.media import Media, MediaGet
from ..models.localization import AddressBase, Place
from ..models.photo import Photo
from ..db_model.db_models import EventDB, PlaceDB, AddressDB, PhotoEventBridgeDB, PhotoDB, EventTypeBridgeDB, EventTypeDB, OrganizerDB, MediaEventBridgeDB, MediaDB
from enum import Enum
from typing import List


class EventCRUD:
    def __init__(self, session: Session) -> None:
        self._session = session


    def delete_event(self, event_id, event_modify: EventBase):
        try:
            self._session.delete(EventDB).where(EventDB.id == event_id)
            self._session.delete(OrganizerDB).where(OrganizerDB.event_id == event_id)
            # self._session.delete(ParticipantDB).where(ParticipantDB.event_id == event_id)

            
            # session.query(stmt)
            self._session.execute(stmt)
            self._session.commit()
            
            return {"status":"success"}
            
        except Exception as e:
            self._session.rollback()
            raise 

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
            if event.date_start > event.date_end:
                return {'status': 'failed','code':405, 'details':'date start after date end'}


            db_event = EventDB(name=event.name,
                            date_start=event.date_start,
                            date_end = event.date_end,
                            is_public =event.is_public,
                            description = event.description,
                            is_outdoor = event.is_outdoor,
                            participants_limit = event.participants_limit,
                            age_limit = event.age_limit,
                            accepted=event.accepted
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

            db_media = []
            for med in event.media:
                db_media.append(MediaDB(link=med.link, type_id=med.type_id))

            db_event.media = db_media 

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
            return {"status":"succeeded", "details":f"Event {db_event} inserted to database successfully"}
        except Exception as e:
            print(e)
            return {"status": "failed", "code": 500, "details":f"Exception: {str(e)}"}

    def get_base_event(self, event_id):
        try:
            db_event = self._session.query(EventDB).where(EventDB.id == event_id).options(joinedload(EventDB.place))\
                                    .options(joinedload(EventDB.photos))\
                                    .options(joinedload(EventDB.organizers))\
                                    .options(joinedload(EventDB.types))\
                                    .options(joinedload(EventDB.media)).first()
        
            # prepare place object
            if db_event is None:
                result = {"status":"failed", "code": 404, "details": f"Event with {event_id} id number does not exist"}
                return result
            print('------------------------',[o.email for o in db_event.organizers])

            organizers = []
            for organizer in db_event.organizers:
                print(organizer.type)
                if organizer.type.lower() == 'organization':
                    org = Organization(id = organizer.id, email=organizer.email, name=organizer.name)
                    organizers.append(org)
                   
                elif organizer.type.lower() == 'private_user':
                    usr = PrivateUser(id = organizer.id, email=organizer.email, name=organizer.name, surname=organizer.surname, nickname=organizer.surname, visible=organizer.visible)
                    organizers.append(usr)
                    
            
            place_obj = db_event.place.as_dict()
            place_obj.pop("address_id")
            photos = [Photo(id=pho.photo_id, 
                            photo_link=pho.photo_link, 
                            type=pho.type, 
                            photo_description=pho.photo_description,
                            datetime_posted=pho.photo_datetime_posted) for pho in db_event.photos]
            
            media = [MediaGet(id = med.id, link=med.link, type_name=med.media_type.name, media_icon=med.media_type.icon) for med in db_event.media]
            
            event = EventGet(id=db_event.id,
                            name=db_event.name,
                            date_start=db_event.date_start,
                            date_end=db_event.date_end,
                            is_public=db_event.is_public,
                            description=db_event.description,
                            is_outdoor=db_event.is_outdoor,
                            participants_limit=db_event.participants_limit,
                            age_limit=db_event.age_limit,
                            accepted=db_event.accepted,
                            organizers=organizers,
                            place=Place.model_validate(place_obj),
                            photos=photos,
                            address=AddressBase.model_validate(db_event.place.address.as_dict()),
                            types=[EventType.model_validate(et.as_dict()) for et in db_event.types],
                            media= media
                            )

            result = {"status": "succeeded", "object": event}
            return result
        except Exception as e:
            # handle exceptions
            result = {"status": "failed", "code": 500, "details": str(e)}
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
            if event_modify.date_start > event_modify.date_end:
                return {"status": "failed", "code": 405, "details": "Date start after date end"}
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
            # db_event = self._session.query(EventDB).where(EventDB.id == event_id).options(joinedload(EventDB.place)).first()
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
                            stmt = update(PlaceDB).where(PlaceDB.id == event_place.id)\
                                                  .values({'name': event_place.name, 'address_id': new_address.id})
                            self._session.execute(stmt)
                            result = {'status': 'modify place params and add new address'}

                    
            self._session.commit()
            return result
        except Exception as e:
            self._session.rollback()
            print(e)
            result = {'status':'failed'}
            return result

    def add_photo(self, event_id: int, photo: Photo):
        try:
            if photo.type == 'main':
                stmt = update(PhotoEventBridgeDB).where(PhotoEventBridgeDB.event_id == event_id).where(PhotoEventBridgeDB.type == 'main').values({"type":"side"})
                self._session.execute(stmt)
            
            photo_db = PhotoDB(
                description = photo.photo_description,
                link = photo.photo_link,
                datetime_posted = datetime.datetime.now()
            )

            self._session.add(photo_db)
            self._session.flush()

            photo_event_bridge = PhotoEventBridgeDB(event_id = event_id, photo_id = photo_db.id, type=photo.type)
            self._session.add(photo_event_bridge)
            self._session.commit()
            result = {'status':'succedded'}

        except Exception as e:
            print('Exception:', e)
            self._session.rollback()
            result = {'status':'failed'}
        return result


    def delete_photo(self, event_id: int, photo_id: int):
        try:
            stmt = delete(PhotoEventBridgeDB).where(PhotoEventBridgeDB.photo_id == photo_id)
            self._session.execute(stmt)
            self._session.commit()
            result = {'status':'succedded'}
        except Exception as e:
            print('Exception:', e)
            result = {'status':'failed'}

        return result

    def modify_photo(self, photo: Photo):
        try:
            stmt = update(PhotoDB).where(PhotoDB.id == photo.id).values({"description":photo.photo_description})
                
            self._session.execute(stmt)
            self._session.commit()
            result = {'status':'succedded'}

            
        except Exception as ex:
            print('Exception:', ex)
            result = {'status':'failed'}

        return result

    def add_organizer(self, event_id: int, user_id: int):
        try:
            organizer = OrganizerDB(user_id=user_id, 
                                    event_id=event_id)
            self._session.add(organizer)
            self._session.commit()
            result = {'status':'succedded'}
        except Exception as e:
            print('Exception:', e)
            result = {'status':'failed'}

        return result

    def delete_organizer(self, event_id: int, user_id: int):
        try:
            organizers = self._session.query(OrganizerDB.user_id).where(OrganizerDB.event_id == event_id).count()

            if int(organizers) == 1:
                result = {"status":"Operation forbidden", "reason": "One organizer left"}
                return result
            stmt = delete(OrganizerDB).where(OrganizerDB.event_id == event_id).where(OrganizerDB.user_id == user_id)
            self._session.execute(stmt)
            self._session.commit()
            result = {'status':f'succedded'}
        except Exception as e:
            print('Exception:', e)
            result = {'status':'failed'}

        return result


    def add_event_type(self, event_id: int, event_type_ids: List[int]):
        try:
            types = []
            existing_types = self._session.query(EventTypeBridgeDB.type_id).where(EventTypeBridgeDB.event_id == event_id).all()
            possible_types = self._session.query(EventTypeDB.id).all()
            existing_types = [i[0] for i in existing_types]
            possible_types = [i[0] for i in possible_types]
            passed = []
            inserted = []

            for type_id in event_type_ids:
                if type_id in existing_types:
                    passed.append(type_id)
                    continue
                if type_id in possible_types:
                    type_event = EventTypeBridgeDB(event_id=event_id, 
                                            type_id=type_id)
                    inserted.append(type_id)
                    types.append(type_event)
                else:
                    passed.append(type_id)
                    # result = {'status':'failed', 'details':'Passed event type id does not exist'}
            print(types)
            self._session.add_all(types)
            self._session.commit()
            result = {'status':'succedded','types_inserted':inserted, 'types_passed': passed}
        except Exception as e:
            print('Exception:', e)
            result = {'status':'failed', 'details':f'passed: {passed} '}

        return result

    def delete_event_type(self, event_id: int, type_id: int):
        try:

            existing_types = self._session.query(EventTypeBridgeDB.type_id).where(EventTypeBridgeDB.event_id == event_id).count()

            if int(existing_types) == 1:
                result = {"status":"Operation forbidden", "reason": "One event type left"}
                return result
            stmt = delete(EventTypeBridgeDB).where(EventTypeBridgeDB.event_id == event_id).where(EventTypeBridgeDB.type_id == type_id)
            self._session.execute(stmt)
            self._session.commit()
            result = {'status':f'succedded'}
        except Exception as e:
            print('Exception:', e)
            result = {'status':'failed'}

        return result
    


    def add_event_media(self, event_id: int, media: Media):
        try:
            exisiting = self._session.query(MediaDB).where(MediaEventBridgeDB.media_id == MediaDB.id).where(MediaEventBridgeDB.event_id == event_id).where(MediaDB.type_id == media.type_id).all()

            if len(exisiting) == 1:
                print('Replace current media entrance')
                print(exisiting[0].id)
                stmt = update(MediaDB).where(MediaDB.id == exisiting[0].id).values({"link": media.link})
                self._session.execute(stmt)
                self._session.commit()
                result = {'status':'succeeded', 'details':f'Updated: media id[{exisiting[0].id}] with new link'}

            else:
                print("Add new media entrance")
                db_media = MediaDB(link=media.link, type_id=media.type_id)
                self._session.add(db_media)
                self._session.flush()

                bridge = MediaEventBridgeDB(event_id= event_id, media_id = db_media.id)

                self._session.add(bridge)
                self._session.commit()
                result = {'status':'succeeded', 'details':f'Added: {db_media}'}

        except Exception as e:
            result = {'status':'failed', 'details':f'{e}'}

        return result

    def delete_event_media(self, event_id: int, media_id: int):
        try:

            existing_media = [int(m.media_id) for m in self._session.query(MediaEventBridgeDB.media_id).where(MediaEventBridgeDB.event_id == event_id).all()]

            if media_id not in existing_media:
                result = {'status':f'failed', 'status_code': 404, 'details':f'Media {media_id} does not exist'}
            else:
                stmt_bridge = delete(MediaEventBridgeDB).where(MediaEventBridgeDB.media_id == media_id).where(MediaEventBridgeDB.event_id == event_id)
                self._session.execute(stmt_bridge)
                stmt_media = delete(MediaDB).where(MediaDB.id == media_id)
                self._session.execute(stmt_media)
                self._session.commit()
                result = {'status':f'succedded', 'status_code': 200, 'details':f'Media {media_id} deleted'}

        except Exception as e:
            print('Exception:', e)
            result = {'status':'failed'}

        return result
    
    



            
            
