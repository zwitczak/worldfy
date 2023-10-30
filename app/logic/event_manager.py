from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List
from ..models.event import EventPost, EventGet
from ..db_operations.event_crud import EventCRUD, SQLiteDatabase


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
        print(self._event)
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
