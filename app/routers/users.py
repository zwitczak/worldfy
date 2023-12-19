from fastapi import APIRouter, Path, Query, HTTPException
from app.logic.event_manager import EventManager, addEvent, getBaseEvent, getEventTypes
from app.logic.user_manager import UserManager, getEventsByUser, getUsersByName, saveEvent
from app.validators.validators import Status
from app.models.user import SignUpData
router = APIRouter(prefix="/user")


@router.post("/signup")
async def signup_user(user_data: SignUpData):
    print(user_data)
    if user_data:
        return {'status': Status.SUCCEEDED}
    else: 
        raise HTTPException(500, detail='error')

@router.get("/")
async def get_users_by_name(name: str, organizations: bool, pv_users: bool):
    """
    Return basic list of users - contains only user name surname or 
    """

    users_response = UserManager(getUsersByName(name, organizations=organizations, pv_users=pv_users)).execute_operation()

    if users_response.status == Status.SUCCEEDED:
        return users_response
    else:
        
        raise HTTPException(404, detail=str(users_response.message), headers=users_response.exception)
    


@router.get("/{user_id}/events")
async def get_users_events(user_id: int):
    """
    Return basic intormations about event based on event_id.
    """
    organized_events_response = UserManager(getEventsByUser(user_id)).execute_operation()
    if organized_events_response.status == Status.SUCCEEDED:
        return organized_events_response 
    else: 
        raise HTTPException(404, detail= str(organized_events_response.message), headers={'error':organized_events_response.exception})


@router.post("/{user_id}/save_events")
async def save_event(user_id: int, event_id:int, role:str, visible:bool):
    """
    Save event to user saved events group. User can have following roles as participant:
    * interested
    * going
    * maybe
    * invited (to be done)
    """
    save_status = UserManager(saveEvent(user_id=user_id, event_id=event_id, role=role, visible=visible)).execute_operation()

    if save_status.status == Status.SUCCEEDED:
        return save_status
    else:
        raise HTTPException(404, detail= str(save_status.message), headers={'error':save_status.exception})






