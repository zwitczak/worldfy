import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from fastapi import FastAPI
from app.routers import events, users, places

description = """

### Events

* **Create event**
* **Get event info**
* **Get event filtered** (_not implemented_).
* **Get events types** 
* **Get events by localization** (_not implemented_).
* **Get events by name** (_not implemented_).
* **Edit event organizator info** (_not implemented_).
* **Edit event addres and place** (_not implemented_).
* **Edit event photos** (_not implemented_).
* **Edit event types** (_not implemented_).

### Users

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
* **Search user by name, return base** (_not implemented_).
* **Search user by name, return full** (_not implemented_).

### Places
* **Search place by name**.
* **Get place address by place id**.



"""

app = FastAPI(
    title="Worldfy",
    description=description,
    summary="Collecting, sharing and exploring events.",
    version="0.0.1"
)

app.include_router(events.router, tags=['events'])
app.include_router(users.router, tags=['users'])
app.include_router(places.router, tags=['places'])

@app.get('/')
async def hello_test():
    return {'hello':'jeszcze tylko 63279219312 godzin pracy'}