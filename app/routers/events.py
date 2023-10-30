from fastapi import APIRouter, Path, Query, HTTPException
from app.logic.event_manager import EventManager, addEvent, getBaseEvent, getEventTypes
from ..models.event import EventPost, EventGet

router = APIRouter(prefix="/event")



@router.get("/")
async def get_base_event(event_id: int):
    """
    Return basic intormations about event based on event_id.
    """
    base_event = EventManager(getBaseEvent(event_id)).execute_operation()

    return {"base": base_event}



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
    
    return {"message": "Event created successfully"}


@router.get('/types')
async def get_event_types():
    """ Returns the list of possible events type. """
    context = EventManager(getEventTypes()).execute_operation()

    if "exception" in list(context.keys()):
        raise HTTPException(status_code=501, detail=context)
    
    return context





