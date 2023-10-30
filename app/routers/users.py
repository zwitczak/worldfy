from fastapi import APIRouter, Path, Query, HTTPException
from app.logic.event_manager import EventManager, addEvent, getBaseEvent, getEventTypes
from ..models.user import UserBase

router = APIRouter(prefix="/user")



@router.get("/")
async def get_users(event_id: int):
    """
    Return basic intormations about event based on event_id.
    """
    pass






