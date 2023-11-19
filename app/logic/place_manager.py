from abc import ABC, abstractmethod
from typing import Any, List
from ..models.localization import Place, AddressBase
from ..db_operations.localization_crud import LocalizationCRUD, SQLiteDatabase
from .geocoding import Geocoder

class Strategy(ABC):
    @abstractmethod
    def execute(self):
        pass

class PlaceManager():
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



class getPlacesByName(Strategy):
    def __init__(self, place_name: str) -> None:
        super().__init__()
        self._place_name = place_name

    def execute(self):

        context = LocalizationCRUD(SQLiteDatabase.create_session()).get_places_by_name(self._place_name)

        return context

        


class getAddressByPlaceId(Strategy):
    def __init__(self, place_id: int) -> None:
        super().__init__()
        self._place_id = place_id

    def execute(self):
        # TODO: create abstraction class
        context = LocalizationCRUD(SQLiteDatabase.create_session()).get_address_by_place(self._place_id)
        # if context.get('exception',):

        #     pass
        
        return context