from typing import List
from engine.core.event import VisionEvent


class VisionEventEngine:
    def __init__(self, detector, event_bus, storage):
        self.detector = detector
        self.event_bus = event_bus
        self.storage = storage

    async def handle_event(self, event: VisionEvent):
        await self.event_bus.publish(event)
        self.storage.save(event)

    async def run(self, frame):
        event = self.detector.detect(frame)
        if event:
            await self.handle_event(event)
