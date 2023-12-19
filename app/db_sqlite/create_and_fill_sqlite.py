from typing import List, Optional
import datetime
from sqlalchemy import ForeignKey, Integer, String, Float, Boolean, Date,DateTime, Text, BIGINT, VARCHAR, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.ext.associationproxy import association_proxy
import os     

pth = "//home//worldfy//app//db_sqlite//test3.db"

if os.path.exists(pth):
    os.rmdir(pth)
# A mapped class typically refers to a single particular database table, 
# the name of which is indicated by using the __tablename__ class-level attribute.
engine = create_engine(f"sqlite:///{pth}", 
                       future=True, 
                    #    echo=True,
                       connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AddressDB(Base):
    __tablename__ = "ADDRESS"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String(30), nullable=False)
    city: Mapped[str] = mapped_column(String(30), nullable=False)
    street: Mapped[str] = mapped_column(String(60), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(6), nullable=False)
    street_number: Mapped[str] = mapped_column(String(5), nullable=False)
    local_number: Mapped[Optional[int]] = mapped_column(String(30), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # relationships
    places: Mapped[List["PlaceDB"]] = relationship(back_populates="address")
    organization: Mapped["OrganizationDB"] = relationship(back_populates="address")


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""Address(id={self.id!r}, country={self.country!r}, city={self.city!r}, 
                   street={self.street!r}, postal_code={self.postal_code!r}, street_number={self.street_number!r}, 
                   loacal_number={self.local_number!r}, latitude={self.latitude!r}, longitude={self.longitude!r})"""


class PlaceDB(Base):
    __tablename__ = "PLACE"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100),nullable=True)
    link: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    address_id = mapped_column(ForeignKey("ADDRESS.id"), nullable=False)
    photo: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    private:  Mapped[bool] = mapped_column(Boolean, nullable=True)

    # relationships
    events: Mapped["EventDB"] = relationship(back_populates="place")
    address: Mapped["AddressDB"] = relationship(back_populates="places")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""Place(id={self.id!r}, name={self.name!r}, link={self.link!r}, 
                   address_id={self.address_id!r}, photo={self.photo!r}, private={self.private!r})"""


class EventDB(Base):
    __tablename__ = "EVENT"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    date_start: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    date_end: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    is_public: Mapped[bool] =  mapped_column(Boolean, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_outdoor: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    participants_limit: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    age_limit: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    place_id = mapped_column(ForeignKey("PLACE.id"), nullable=False) 
    accepted: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # relationships
    place: Mapped["PlaceDB"] = relationship(back_populates="events")
    types: Mapped[List["EventTypeDB"]] = relationship("EventTypeDB", secondary="EVENT_TYPE_BR", back_populates="events")
    photos =  relationship("PhotoEventBridgeDB" , back_populates="event")
    organizers: Mapped[List["UserDB"]] = relationship("UserDB", secondary="ORGANIZER", back_populates="organized_events")
    media = relationship("MediaDB", secondary ="MEDIA_EVENT_BR", back_populates="events_media")
    interested_users = relationship("ParticipantDB", back_populates="events")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""Event(id={self.id!r}, name={self.name!r}, date_start={self.date_start!r}, 
                   date_end={self.date_end!r}, is_public={self.is_public!r}, description={self.description!r},
                   is_outdoor={self.is_outdoor!r}, participants_limit={self.participants_limit!r}, age_limit={self.age_limit!r}, place_id={self.place_id!r})"""

    
class PhotoEventBridgeDB(Base):
    __tablename__ = "PHOTO_EVENT_BR"
    
    # https://www.gormanalysis.com/blog/many-to-many-relationships-in-fastapi/ 

    # attributes
    photo_id: Mapped[int] = mapped_column(ForeignKey("PHOTO.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("EVENT.id"), primary_key=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)

    # relationships
    event = relationship("EventDB", back_populates="photos")
    photo = relationship("PhotoDB", back_populates="event_obj")

    # proxies
    photo_link = association_proxy(target_collection='photo', attr='link')
    photo_description = association_proxy(target_collection='photo', attr='description')
    photo_datetime_posted = association_proxy(target_collection='photo', attr='datetime_posted')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""PhotoEventBridge(photo_id={self.photo_id!r}, event_id={self.event_id!r}, type={self.type!r})"""

class PhotoUserBridgeDB(Base):
    __tablename__ = "PHOTO_USER_BR"

    # attributes
    photo_id: Mapped[int] = mapped_column(ForeignKey("PHOTO.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("USER.id"), primary_key=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)

    # relationships
    user = relationship("UserDB", back_populates="photos")
    photo = relationship("PhotoDB", back_populates="user_obj")

    # proxies
    photo_link = association_proxy(target_collection='photo', attr='link')
    photo_description = association_proxy(target_collection='photo', attr='description')
    photo_datetime_posted = association_proxy(target_collection='photo', attr='datetime_posted')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""PhotoUserBridge(photo_id={self.photo_id!r}, event_id={self.event_id!r}, type={self.type!r})"""


class PhotoDB(Base):
    __tablename__ = "PHOTO"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    datetime_posted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    # relationships
    event_obj = relationship("PhotoEventBridgeDB", back_populates="photo")
    user_obj = relationship("PhotoUserBridgeDB", back_populates="photo")
    # comment_obj = relationship("PhotoCommentBridgeDB", back_populates="photo")
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""Photo(id={self.id!r}, link={self.link!r}, description={self.description!r}, datetime_posted={self.datetime_posted!r})"""



class EventTypeDB(Base):
    __tablename__ = "EVENT_TYPE"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # relationships
    events: Mapped[List["EventDB"]] = relationship("EventDB", secondary="EVENT_TYPE_BR", back_populates="types")

    def __repr__(self) -> str:
        return f"""EventType(id={self.id!r}, name={self.name!r}, description={self.description!r})"""
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

class EventTypeBridgeDB(Base):
    __tablename__ = "EVENT_TYPE_BR"
    
    type_id = mapped_column(ForeignKey("EVENT_TYPE.id"), primary_key=True)
    event_id = mapped_column(ForeignKey("EVENT.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"""EventTypeBridge(type_id={self.type_id!r}, event_id={self.event_id!r})"""

class OrganizerDB(Base):
    __tablename__ = "ORGANIZER"

    event_id: Mapped[int] = mapped_column(ForeignKey("EVENT.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("USER.id"), primary_key=True)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""Organizer(user_id={self.user_id!r}, event_id={self.event_id!r})"""

class UserDB(Base):
    
    __tablename__ = "USER"

    # https://docs.sqlalchemy.org/en/20/orm/inheritance.html

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    registration_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str]


    # relationships
    organized_events: Mapped[Optional[List["EventDB"]]]= relationship("EventDB", secondary="ORGANIZER",back_populates="organizers")
    # saved_events: Mapped[Optional[List["EventDB"]]]= relationship("EventDB", secondary="PARTICIPANT",back_populates="participants")
    photos =  relationship("PhotoUserBridgeDB" , back_populates="user")
    media = relationship("MediaDB", secondary="MEDIA_USER_BR",back_populates="users_media")

    __mapper_args__ = {
        "polymorphic_identity": "USER",
        "polymorphic_on": "type",
    }

    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""User(id={self.id!r}, name={self.name!r})"""

class PrivateUserDB(UserDB):
    
    __tablename__ = "PRIVATE_USER"

    id: Mapped[int] = mapped_column(ForeignKey("USER.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    nickname: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    birthday: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    visible: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "PRIVATE_USER"
    }

    # relationships 
    # TODO partitipated_events
    # relationships
    saved_events = relationship("ParticipantDB", back_populates="users")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""User(id={self.id!r}, name={self.name!r})"""

class OrganizationDB(UserDB):
    
    __tablename__ = "ORGANIZATION"

    id: Mapped[int] = mapped_column(ForeignKey("USER.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    organization_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    size: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ADDRESS.id"), nullable=True)

    # relationships
    address: Mapped[AddressDB] = relationship(back_populates='organization')

    __mapper_args__ = {
        "polymorphic_identity": "ORGANIZATION"
    }


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""User(id={self.id!r}, name={self.name!r})"""



class MediaUserBridgeDB(Base):
    __tablename__ = "MEDIA_USER_BR"
    
    # attributes
    user_id: Mapped[int] = mapped_column(ForeignKey("USER.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("MEDIA.id"), primary_key=True)


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""MediaUserBridge(user_id={self.user_id!r}, media_id={self.media_id!r})"""

class MediaEventBridgeDB(Base):
    __tablename__ = "MEDIA_EVENT_BR"
    
    # attributes
    event_id: Mapped[int] = mapped_column(ForeignKey("EVENT.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("MEDIA.id"), primary_key=True)


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""MediaEventBridge(event_id={self.event_id!r}, media_id={self.media_id!r})"""

class MediaDB(Base):
    __tablename__ = "MEDIA"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(String, nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("MEDIA_TYPES.id"), nullable=False)

    # relationships
    media_type = relationship("MediaTypesDB", back_populates="media_instances")
    # user
    users_media = relationship("UserDB", secondary="MEDIA_USER_BR", back_populates="media")
    # event
    events_media = relationship("EventDB", secondary="MEDIA_EVENT_BR", back_populates="media")


    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""Media(id={self.id!r}, link={self.link!r}, type_id={self.type_id!r})"""

class MediaTypesDB(Base):
    __tablename__ = "MEDIA_TYPES"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    icon: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # relationships
    media_instances = relationship("MediaDB", back_populates="media_type")
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""MediaType(id={self.id!r}, name={self.name!r}, icon={self.icon!r})"""

class ParticipantDB(Base):
    __tablename__ = "PARTICIPANT"
    user_id: Mapped[int] = mapped_column(ForeignKey("PRIVATE_USER.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("EVENT.id"), primary_key=True)
    # interested, goes, invited, maybe
    role: Mapped[str] = mapped_column(String, nullable=False)
    visibile: Mapped[bool] = mapped_column(Boolean, nullable=False)


    # relationships
    events = relationship("EventDB", back_populates="interested_users")
    users = relationship("PrivateUserDB", back_populates="saved_events")
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""Participant(user_id={self.user_id!r}, event_id={self.event_id!r}, role={self.role!r}, visibility={self.visibility!r})"""
    
Base.metadata.create_all(engine)


with Session(engine) as session:
    user1 = OrganizationDB(name='Evento',
                            email = 'eventeen@gmail.com',
                            password = 'OnO3424',
                            description= 'eventorganization',
                            registration_date = datetime.date.today(),
                            phone_number = '+48 045 231 098',
                            organization_type = 'events',
                            size = None)
    user2 = PrivateUserDB(name='Ala',
                          email="alakot@wp.pl",
                          password='wfecav',
                          description='girl from the hoods',
                          registration_date = datetime.date.today(),
                          surname='Kot',
                          nickname='alako',
                          gender='Female',
                          birthday=datetime.datetime(2001,5, 12),
                          visible=True
                          )
    user3 = OrganizationDB(
        name = 'Going',
        email = 'going@app.com',
        password = '12345',
        description= 'Nice app with tickets',
        registration_date = datetime.date.today(),
        phone_number = '+48 000 000 000',
        organization_type = 'entertainment',
        size = "500+"
    )
    user4 = OrganizationDB(name='DKS',
                            email = 'DKS@gmail.com',
                            password = '123sdcsvsd45',
                            description= 'more culture',
                            registration_date = datetime.date.today(),
                            phone_number = '+48 045 000 000',
                            organization_type = 'culture',
                            size = None)

    user5 = OrganizationDB(name='Jasna',
                            email = 'ciemna@gmail.com',
                            password = '123sdvssdcsvsd45',
                            description= 'techno industry engine',
                            registration_date = datetime.date.today(),
                            phone_number = '+48 045 666 000',
                            organization_type = 'club',
                            size = None)

    user6 = PrivateUserDB(name='Marek',
                          email="mareby@wp.pl",
                          password='wfecav',
                          description='boy from the hoods',
                          registration_date = datetime.date.today(),
                          surname='Bytur',
                          nickname='mareczek',
                          gender='Male',
                          birthday=datetime.datetime(1998,5, 22),
                          visible=False
                          )

    event1 = EventDB(name = 'Concert Beyonce',
                     date_start = datetime.datetime(2023, 10,28,19,30,00),
                     date_end = datetime.datetime(2023, 10,28,22,30,00),
                     is_public = True,
                     description = 'worldwide start',
                     is_outdoor = False,
                     participants_limit = 12000,
                     age_limit = "16+",
                     accepted=True
                     )
    
    event2 = EventDB(name = 'Helloween party',
                     date_start = datetime.datetime(2023, 10,30,19,30,00),
                     date_end = datetime.datetime(2023, 10,31,4,30,00),
                     is_public = False,
                     description = 'dress up a bit lol',
                     is_outdoor = False,
                     participants_limit = 50,
                     age_limit = "18+",
                     accepted=True
                     )
    
    address1 = AddressDB(country = "Poland",
                         city= "Warsaw",
                         street= "al. Księcia Józefa Poniatowskiego",
                         postal_code="03-901",
                         street_number= "1",
                         local_number=None,
                         latitude=52.238499486188445, 
                         longitude=21.044629426098936)
    
    address2 = AddressDB(country = "Poland",
                         city= "Warsaw",
                         street= "wl.Włodarzewska",
                         postal_code="02-384",
                         street_number= "57G",
                         local_number=14,
                         latitude=52.199827327627524, 
                         longitude=20.95785815187432)
    
    place1 =  PlaceDB(name='PGE Narodowy',private=False)
    place2 =  PlaceDB(private=True)

    place1.address = address1
    event1.place = place1

    place2.address = address2
    event2.place = place2

    type1 = EventTypeDB(name = 'concert')
    type2 = EventTypeDB(name = 'music')
    type3 = EventTypeDB(name = 'worldwide star')
    type4 = EventTypeDB(name = 'house party')
    type5 = EventTypeDB(name = 'helloween')
    type6 = EventTypeDB(name = 'new years eve')
    type7 = EventTypeDB(name = 'sport')
    type8 = EventTypeDB(name = 'art')
    type9 = EventTypeDB(name = 'party')

    photo1 = PhotoDB(link = 'https://bi.im-g.pl/im/51/82/16/z23604049ICR,Beyonce-i-Jay-Z.jpg',  
                    datetime_posted=datetime.datetime.now())
    
    mediatype1 = MediaTypesDB(name= "Instagram", icon="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
    mediatype2 = MediaTypesDB(name= "Facebook", icon="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/2021_Facebook_icon.svg/2048px-2021_Facebook_icon.svg.png")
    mediatype3 = MediaTypesDB(name= "X", icon="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/x-social-media-logo-icon.png")

    media1 = MediaDB(link='grat page lol')
    media2 = MediaDB(link='best best twitter lol')
    media3 = MediaDB(link='facebook')


    media1.media_type = mediatype1
    media2.media_type = mediatype2
    media3.media_type = mediatype3

    event2.media = [media1]
    user3.media = [media2, media3]

    event1.types = [type1, type2, type3]
    event2.types = [type4, type5]
    event1.organizers = [user1]
    event2.organizers = [user2]


    session.add_all([address1, address2, event1, event2, place1, place2, type1, type2, type3, type4, type5, photo1, user1, user2])
    session.add_all([type6, type7, type8, type9, user3, user4, user5, user6])
    # after commit objects receive id number
    session.commit()
    
    
    photoevent = PhotoEventBridgeDB(photo_id =photo1.id, event_id = event1.id, type='main')

    participant1 = ParticipantDB(user_id=user2.id, event_id=event1.id, role='interested', visibile = True)
    participant2 = ParticipantDB(user_id=user6.id, event_id=event1.id, role='going',  visibile = True)
    participant3 = ParticipantDB(user_id=user6.id, event_id=event2.id, role='interested', visibile = True)
    participant4 = ParticipantDB(user_id=user2.id, event_id=event2.id, role='going', visibile = False)



    session.add_all([photoevent, participant1, participant2, participant3, participant4])
    session.commit()
