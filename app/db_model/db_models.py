from typing import List, Optional
import datetime
from sqlalchemy import ForeignKey, Integer, String, Float, Boolean, DateTime, Text, BIGINT, VARCHAR, create_engine, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.associationproxy import association_proxy

# A mapped class typically refers to a single particular database table, 
# the name of which is indicated by using the __tablename__ class-level attribute.
# engine = create_engine("sqlite:///C:\\Users\\zuzan\\Desktop\\et\\sqlite\\test.db", 
#                        future=True, 
#                     #    echo=True,
#                        connect_args={"check_same_thread": False})

# Base = declarative_base()
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
        return f"""Participant(user_id={self.user_id!r}, event_id={self.event_id!r}, role={self.role!r}, visibility={self.visibile!r})"""