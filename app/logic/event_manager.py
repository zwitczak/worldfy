from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List
from ..models.event import EventPost, EventGet
from ..db_operations.event_crud import EventCRUD, SQLiteDatabase
from .geocoding import Geocoder


class EventManager():
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

class addEvent(Strategy):
    def __init__(self, event: EventPost) -> None:
        super().__init__()
        self._event = event

    def execute(self):
        if self._event.address.latitude is None:
            coordinates = Geocoder.get_lat_lon(self._event.address)
            if 'lat' in coordinates.keys():
                self._event.address.latitude = coordinates['lat']
                self._event.address.longitude = coordinates['lon']
        context = EventCRUD(SQLiteDatabase.create_session()).insert_event(self._event)
        print(context)
        return context

class getBaseEvent(Strategy):
    def __init__(self, event_id) -> None:
        super().__init__()
        self._event_id = event_id

    def execute(self):
        base_event = EventCRUD(SQLiteDatabase.create_session()).get_base_event(self._event_id)
        # print(base_event)
        return base_event
        


class deleteEvent(Strategy):
    def execute(self, event_id: int):
        pass

class editBaseEvent(Strategy):
    def execute(self, event):
        pass

class getEventTypes(Strategy):
    def execute(self):
        event_types = EventCRUD(SQLiteDatabase.create_session()).get_event_types()
        return {"event_types": event_types}

class editBaseEvent(Strategy):
    def __init__(self, event_id: int, event_base: EventBase) -> None:
        super().__init__()
        self._event_id= event_id
        self._event_base = event_base

    def execute(self):
        with SQLiteDatabase.create_session() as session:
            update_status = EventCRUD(session).update_event_base(self._event_id, self._event_base)
            return update_status

class editEventLocalization(Strategy):
    def __init__(self,  event_id: int, event_place, event_address):
        self._event_id= event_id
        self._event_place = event_place
        self._event_address = event_address

    def execute(self):
        with SQLiteDatabase.create_session() as session:
            if self._event_address is not None:
                if self._event_address.latitude is None:
                    coordinates = Geocoder.get_lat_lon(self._event_address)
                    if 'lat' in coordinates.keys():
                        self._event_address.latitude = coordinates['lat']
                        self._event_address.longitude = coordinates['lon']

            update_status = EventCRUD(session).change_event_localization(self._event_id, self._event_place, self._event_address)
            return update_status


class editEventPhotos(Strategy):
    def execute(self, event):
        pass

class editEventOrganizer(Strategy):
    def execute(self, event):
        pass

class editEventType(Strategy):
    def execute(self, event):
        pass

class editEventMedia(Strategy):
    def execute(self, event):
        pass

