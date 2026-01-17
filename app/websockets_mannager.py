from fastapi import WebSocket
from typing import List
import json

class ConnectionMannager:
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New client connected. Total: {len(self.active_connections)}")
    
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(json.dumps(message))


mannager = ConnectionMannager()