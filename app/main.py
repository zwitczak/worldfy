import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from fastapi import FastAPI
from app.routers import events, users


app = FastAPI()
app.include_router(events.router, tags=['events'])
app.include_router(users.router, tags=['users'])

@app.get('/')
async def hello_test():
    return {'hello':'jeszcze tylko 63279219312 godzin pracy'}