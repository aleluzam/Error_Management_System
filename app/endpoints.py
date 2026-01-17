from fastapi import APIRouter, Depends, status, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import asyncio


from database import get_db
from crud import get_all_incidents, post_new_incident, resolve_incident
from schemas import IncidentResponse, IncidentCreate, UserValidate, UserBase
from websockets_mannager import mannager
from security import register, login, validate_user


routes = APIRouter(prefix="/api/v1",tags=["incidents"])
routes_login = APIRouter(prefix="/api/v1",tags=["users"])



@routes.get("/incidents", response_model=list[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)) -> list[IncidentResponse]:
    return get_all_incidents(db=db)


@routes.post("/incidents", response_model=IncidentResponse)
async def create_new_incident(new_incident: IncidentCreate, db: Session = Depends(get_db)) -> IncidentResponse:
    return await post_new_incident(db=db, new_incident=new_incident)
      
    
@routes.patch("/incidents/{id}/resolve", status_code=status.HTTP_200_OK, response_model=dict)
async def change_incident_status(id: int, db: Session = Depends(get_db), user: UserValidate = Depends(validate_user))-> dict:
    return await resolve_incident(db=db,id=id)


@routes.websocket("/ws")
async def websocket_connection(websocket: WebSocket):
    await mannager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
    
    except WebSocketDisconnect:
        await mannager.disconnect(websocket)


@routes_login.post("/register")
def register_user(data: UserValidate, db: Session = Depends(get_db)):
        return register(data, db)


@routes_login.post("/login")
def login_user(data: UserValidate, db: Session = Depends(get_db)):
        return login(data, db)