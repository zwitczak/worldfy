from fastapi import APIRouter, Path, Query, HTTPException
from app.logic.event_manager import EventManager, addEvent, getBaseEvent, getEventTypes,\
                                    editEventLocalization, editBaseEvent,addEventPhoto, \
                                    deleteEventPhoto, modifyEventPhoto, addEventOrganizer, deleteEventOrganizer,\
                                    addEventType, deleteEventType, addEventMedia, deleteEventMedia
from ..models.event import EventPost, EventGet, EventLocalization, EventBase
from ..models.photo import Photo
from ..models.media import Media
from typing import List

router = APIRouter(prefix="/event")



@router.get("/")
async def get_base_event(event_id: int):
    """
    Return basic intormations about event based on event_id.
    """
    context = EventManager(getBaseEvent(event_id)).execute_operation()

    if context.get("status", None) == "failed":
        raise HTTPException(status_code = context.get("code", 500), detail=context.get("details"))
    else:
        return {"base": context.get("object")}



@router.get("/filtered/")
async def get_filtered_events(event_id: int, filter):
    """
    Return list of events with basic intormations about event based on filters.
    """

    pass


@router.post("/create")
async def add_full_event(event: EventPost):
    """Receives event model from user"""
    context = EventManager(addEvent(event)).execute_operation()

    # if "exception" in list(context.keys()):
    #     raise HTTPException(status_code=501, detail=context)
    if context.get('status', None) == 'failed':
        raise HTTPException(status_code=context.get("code", 500), detail=context.get("details"))

    return {"message": "Event created successfully"}


@router.get('/types')
async def get_event_types():
    """ Returns the list of possible events type. """
    context = EventManager(getEventTypes()).execute_operation()

    if "exception" in list(context.keys()):
        raise HTTPException(status_code=501, detail=context)
    
    return context

@router.put('/{event_id}/edit/base')
async def modify_event_data(event_id: int, event_base: EventBase):
    """ Edit event data """
    context = EventManager(editBaseEvent(event_id=event_id, event_base=event_base)).execute_operation()

    if context.get('status', None) == 'failed':
        raise HTTPException(status_code = context.get("code", 405), detail=context.get("details", None))
    return context

@router.put('/{event_id}/edit/place')
async def modify_event_place(event_id: int, event_place: EventLocalization):
    """ Edit event data """
    context = EventManager(editEventLocalization(event_id=event_id,event_place=event_place.place, event_address=event_place.address)).execute_operation()

    if context.get('status', None) == 'failed':
        raise HTTPException(status_code = context.get("code", 405), detail=context.get("details", None))
    return context


@router.put('/photo')
async def modify_event_photo_description(photo: Photo):
    """ Edit event photo description """
    context = EventManager(modifyEventPhoto(photo=photo)).execute_operation()
    return context

@router.post('/{event_id}/photo')
async def add_event_photo(event_id: int, photo: Photo):
    """ Add new event photo  """
    context = EventManager(addEventPhoto(event_id=event_id, photo=photo)).execute_operation()
    return context

@router.delete('/{event_id}/photo')
async def delete_event_photo(event_id: int, photo_id: int):
    """ Delete event photo  """
    context = EventManager(deleteEventPhoto(event_id=event_id, photo_id=photo_id)).execute_operation()
    return context


@router.post('/{event_id}/organizer')
async def add_event_organizer(event_id: int, user_id: int):
    """ Add new event photo  """
    context = EventManager(addEventOrganizer(event_id=event_id, user_id=user_id)).execute_operation()
    return context



@router.delete('/{event_id}/organizer')
async def delete_event_organizer(event_id: int, user_id: int):
    """ Delete event photo  """
    context = EventManager(deleteEventOrganizer(event_id=event_id, user_id=user_id)).execute_operation()
    if context.get('reason', None) is not None:
        raise HTTPException(status_code=405, detail=context['reason'])
    return context

@router.post('/{event_id}/type')
async def add_event_types(event_id: int, event_type_ids: List[int]):
    """ Add new event types  """
    context = EventManager(addEventType(event_id=event_id, event_type_ids=event_type_ids)).execute_operation()
    return context



@router.delete('/{event_id}/type')
async def delete_event_type(event_id: int, event_type_id: int):
    """ Delete event type. If one left, return 405: Method not allowed  """
    context = EventManager(deleteEventType(event_id=event_id, event_type_id=event_type_id)).execute_operation()
    if context.get('reason', None) is not None:
        raise HTTPException(status_code=405, detail=context['reason'])
    return context

@router.post('/{event_id}/media')
async def add_event_media(event_id: int, media: Media):
    """ Add new event types  """
    context = EventManager(addEventMedia(event_id=event_id, media=media)).execute_operation()
    return context



@router.delete('/{event_id}/media')
async def delete_event_type(event_id: int, media_id: int):
    """ Delete event type. If one left, return 405: Method not allowed  """
    context = EventManager(deleteEventMedia(event_id=event_id, media_id=media_id)).execute_operation()
    if context.get('status', None) == 'failed':
        raise HTTPException(status_code=context.get('status_code', 404), detail=context.get('details', None))
    return context






