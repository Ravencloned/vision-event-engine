import cv2
import asyncio
import threading
import uvicorn
from datetime import datetime

from engine.input.video_source import VideoSource
from engine.bus.server import app as fastapi_app, event_bus
from engine.storage.sqlite_store import SQLiteEventStore
from engine.detectors.yolo_detector import YOLODetector
from engine.detectors.hand_detector import HandDetector
from engine.processing.entity_memory import EntityMemory
from engine.core.event import VisionEvent


def start_api():
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=8000,
        log_level="warning"
    )


async def main():
    video = VideoSource()
    yolo = YOLODetector()
    hand_detector = HandDetector()

    memory = EntityMemory()
    storage = SQLiteEventStore()

    while True:
        frame, fps = video.read()
        if frame is None:
            break

        detections = []

        # YOLO: people + cell phone ONLY
        yolo_event = yolo.detect(frame)
        if yolo_event:
            for d in yolo_event.metadata["objects"]:
                if d["label"] in {"person", "cell phone"}:
                    detections.append(d)

        # Hands (independent)
        detections.extend(hand_detector.detect(frame))

        # Structural reasoning
        events = memory.update(detections)

        for ev_type, entity_id, det in events:
            event = VisionEvent(
                timestamp=datetime.utcnow(),
                event_type=ev_type,
                confidence=1.0,
                metadata={
                    "entity_id": entity_id,
                    "label": det["label"]
                }
            )
            await event_bus.publish(event)
            storage.save(event)

        # Visualization
        for d in detections:
            x1, y1, x2, y2 = d["bbox"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                d["label"],
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )

        cv2.imshow("Vision Event Engine", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    threading.Thread(target=start_api, daemon=True).start()
    asyncio.run(main())
