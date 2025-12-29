from typing import Set
from fastapi import WebSocket
from engine.core.event import VisionEvent


class WebSocketEventBus:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def publish(self, event: VisionEvent):
        dead_connections = []

        for ws in self.connections:
            try:
                await ws.send_json(event.dict())
            except Exception:
                dead_connections.append(ws)

        for ws in dead_connections:
            self.disconnect(ws)
