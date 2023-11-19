from fastapi import APIRouter, Path, Query, HTTPException
from app.logic.event_manager import EventManager, addEvent, getBaseEvent, getEventTypes
from app.logic.user_manager import UserManager, getEventsByUser, getUsersByName

router = APIRouter(prefix="/user")



@router.get("/")
async def get_users_by_name(name: str, organizations: bool, pv_users: bool):
    """
    Return basic list of users - contains only user name surname or 
    """
    try:
        users = UserManager(getUsersByName(name, organizations=organizations, pv_users=pv_users)).execute_operation()
        return users
    except Exception as e:
        print(e)
        raise HTTPException(404)
    


@router.get("/{user_id}/events")
async def get_users_events(user_id: int):
    """
    Return basic intormations about event based on event_id.
    """
    organized_events = UserManager(getEventsByUser(user_id)).execute_operation()

    return {"organized_Events": organized_events}







