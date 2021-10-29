from typing import List 
from fastapi import WebSocket

class Publisher:
    # publish/subscribe pattern
    # publishes to everyone  

    def __init__(self):
        self.subscribers = [] # List[WebSocket]
    
    async def push(self, msg: str):
        await self._notify(msg)

    async def _notify(self, msg: str):
        live_subs = [] 
        while len(self.subscribers) > 0:
            socket = self.subscribers.pop()
            await socket.send_text(msg)
            live_subs.append(socket)
        self.subscribers = live_subs 

    async def subscribe(self, websocket: WebSocket):
        await websocket.accept()
        self.subscribers.append(websocket)

    def unsubscribe(self, websocket: WebSocket):
        self.subscribers.remove(websocket)

class TargetedPublisher:
    # targeted publishing to specific users  

    def __init__(self):
        self.subscribers = {} # user id : WebSocket
    
    async def push(self, user_ids: List[int], msg: str):
        await self._notify(user_ids, msg)

    async def _notify(self, user_ids: List[int], msg: str):
        for user_id in user_ids:
            if user_id in self.subscribers:
                socket = self.subscribers[user_id]
                await socket.send_text(msg)
    
    async def subscribe(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.subscribers[user_id] = websocket 
    
    def unsubscribe(self, user_id: int):
        del self.subscribers[user_id]
