from typing import List, Optional
import datetime
from sqlalchemy import ForeignKey, Integer, String, Float, Boolean, DateTime, Text, BIGINT, VARCHAR, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.ext.associationproxy import association_proxy
import os     

pth = "//home//worldfy//app//db_sqlite//test.db"

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

    # relationships
    place: Mapped["PlaceDB"] = relationship(back_populates="events")
    types: Mapped[List["EventTypeDB"]] = relationship("EventTypeDB", secondary="EVENT_TYPE_BR", back_populates="events")
    photos =  relationship("PhotoEventBridgeDB" , back_populates="event")
    organizers: Mapped[List["UserDB"]] = relationship("UserDB", secondary="ORGANIZER", back_populates="organized_events")
    
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


class PhotoDB(Base):
    __tablename__ = "PHOTO"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    datetime_posted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    # relationships
    event_obj = relationship("PhotoEventBridgeDB", back_populates="photo")
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""Photo(id={self.id!r}, link={self.link!r}, description={self.description!r}, datetime_posted={self.datetime_posted!r})"""



class EventTypeDB(Base):
    __tablename__ = "EVENT_TYPE"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=False)

    # relationships
    organized_events: Mapped[Optional[List["EventDB"]]]= relationship("EventDB", secondary="ORGANIZER",back_populates="organizers")
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f"""User(id={self.id!r}, name={self.name!r})"""

Base.metadata.create_all(engine)


with Session(engine) as session:
    user1 = UserDB(name='Evento')
    user2 = UserDB(name='Ala')
    user3 = UserDB(name='Going')
    user4 = UserDB(name='DKS')
    user5 = UserDB(name='Jasna')

    event1 = EventDB(name = 'Concert Beyonce',
                     date_start = datetime.datetime(2023, 10,28,19,30,00),
                     date_end = datetime.datetime(2023, 10,28,22,30,00),
                     is_public = True,
                     description = 'worldwide start',
                     is_outdoor = False,
                     participants_limit = 12000,
                     age_limit = "16+"
                     )
    
    event2 = EventDB(name = 'Helloween party',
                     date_start = datetime.datetime(2023, 10,30,19,30,00),
                     date_end = datetime.datetime(2023, 10,31,4,30,00),
                     is_public = False,
                     description = 'dress up a bit lol',
                     is_outdoor = False,
                     participants_limit = 50,
                     age_limit = "18+"
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
    
    event1.types = [type1, type2, type3]
    event2.types = [type4, type5]
    event1.organizers = [user1]
    event2.organizers = [user2]
    session.add_all([address1, address2, event1, event2, place1, place2, type1, type2, type3, type4, type5, photo1, user1, user2])
    session.add_all([type6, type7, type8, type9, user3, user4, user5])
    # after commit objects receive id number
    session.commit()
    
    
    photoevent = PhotoEventBridgeDB(photo_id =photo1.id, event_id = event1.id, type='main')

    session.add_all([photoevent])
    session.commit()
