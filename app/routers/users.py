from fastapi import APIRouter, Path, Query, HTTPException
from app.logic.event_manager import EventManager, addEvent, getBaseEvent, getEventTypes
from app.logic.user_manager import UserManager, getEventsByUser

router = APIRouter(prefix="/user")



@router.get("/")
async def get_users(event_id: int):
    """
    Return basic intormations about event based on event_id.
    """
    raise HTTPException(status_code=501, detail='TO be done')
    pass


@router.get("/{user_id}/events")
async def get_users_events(user_id: int):
    """
    Return basic intormations about event based on event_id.
    """
    organized_events = UserManager(getEventsByUser(user_id)).execute_operation()

    return {"organized_Events": organized_events}







