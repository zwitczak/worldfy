from sqlalchemy.orm import Session
from .db_set import SQLiteDatabase
from ..models.localization import AddressBase, Place
from ..db_model.db_models import PlaceDB, AddressDB
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload

class LocalizationCRUD:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_places_by_name(self, place_name):
        try:
            filt = f"%{place_name}%"
            stmt = select(PlaceDB).filter(PlaceDB.name.ilike(filt))
            stmt = select(PlaceDB.id, PlaceDB.name).filter(PlaceDB.name.ilike(filt)).where(PlaceDB.private == False).limit(5)
            places_db = self._session.execute(stmt)
            result = []
            for pl in places_db:
                print('process places:',pl)
                place = Place(id=pl.id, name=pl.name, private=False)
                print(place)
                result.append(place)
            
        except Exception as e:

            print('Error occured:', e)
            result = {'status': e}

        return result

    def get_address_by_place(self, place_id: int):
        try:
            address = self._session.query(AddressDB).where(PlaceDB.id == place_id).where(PlaceDB.address_id == AddressDB.id).first()

            if address:
                result = AddressBase(country=address.country,
                                    city=address.city,
                                    street=address.street,
                                    street_number=address.street_number,
                                    postal_code=address.postal_code,
                                    local_number=address.local_number
                                    )
            else:
                result = None
            return result

        except Exception as e:
            print(e)
            return {'exception': str(e)}
