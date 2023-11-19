from fastapi import APIRouter, Path, Query, HTTPException
from app.logic.place_manager import PlaceManager, getPlacesByName, getAddressByPlaceId
from ..models.localization import Place

router = APIRouter(prefix="/places")



@router.get("/name")
async def get_places_by_name(place_name: str):
    """
    Return list of places with name containing given string
    """
    places = PlaceManager(getPlacesByName(place_name)).execute_operation()

    if not isinstance(places, list):
        raise HTTPException(status_code=500, detail='Databse exception')



@router.get("/{place_id}/address")
async def get_address_by_place_id(place_id: int):
    """
    Return address based on the place id.
    """
    address = PlaceManager(getAddressByPlaceId(place_id)).execute_operation()

    if isinstance(address, dict):
        raise HTTPException(status_code=500, detail='Database exception')
    elif address is None:
        raise HTTPException(status_code=404, detil='Address not found')


    return {"address": address}
