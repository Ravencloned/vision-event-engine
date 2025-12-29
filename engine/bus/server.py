from fastapi import FastAPI, WebSocket
from engine.bus.websocket_bus import WebSocketEventBus

app = FastAPI()
event_bus = WebSocketEventBus()


@app.websocket("/ws/events")
async def event_stream(websocket: WebSocket):
    await event_bus.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        event_bus.disconnect(websocket)
