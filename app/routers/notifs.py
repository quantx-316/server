from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status, BackgroundTasks
from fastapi.security.utils import get_authorization_scheme_param
import asyncio
import app.models.users as users_models  
from app.utils.security import JWTBearer
from app.db import get_db

from app.utils.notifs import TargetedPublisher

publisher = TargetedPublisher() 

bearer = JWTBearer() 

router = APIRouter(
    prefix="/ws",
)

@router.websocket("/")
async def subscribe(websocket: WebSocket):
    await websocket.accept()
    auth = False 
    user_id = None 
    try:
        while True:            
            try: 
                if not auth: 
                    header = await asyncio.wait_for(websocket.receive_json(), timeout=5) # "{Authorization: Bearer ...}"
                    print(header)
                    if not 'Authorization' in header:
                        print("NO AUTHORIZATION")
                        raise Exception("Auth not given in info")
                    scheme, param = get_authorization_scheme_param(header.get('Authorization'))
                    if not scheme == "Bearer":
                        print("NO BEARER")
                        raise Exception("Improper auth scheme")
                    user = users_models.Users.get_auth_user(get_db(), param)
                    publisher.subscribe(user.id, websocket)
                    user_id = user.id 
                    auth = True 
            except Exception as e:
                print(e)
                print(str(e))
                await websocket.close()
    except WebSocketDisconnect: 
        if user_id is not None:
            publisher.unsubscribe(user_id, websocket)

# async def send_notification(user_ids: List[int], msg: str):
#     await publisher.push(user_ids, msg)
