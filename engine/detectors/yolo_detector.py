from datetime import datetime
from ultralytics import YOLO

from engine.core.event import VisionEvent


class YOLODetector:
    def __init__(self):
        # Lightweight pretrained model (CPU friendly)
        self.model = YOLO("yolov8n.pt")

        # We do NOT restrict classes aggressively — this is a hypothesis generator
        self.allowed_classes = {
            "person",
            "cell phone",
            "backpack",
            "handbag",
            "laptop",
            "bottle",
            "cup",
            "chair"
        }

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]

        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]

            if label not in self.allowed_classes:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            detections.append({
                "label": label,
                "confidence": conf,
                "bbox": (x1, y1, x2, y2),
                "center": (
                    (x1 + x2) // 2,
                    (y1 + y2) // 2
                )
            })

        if not detections:
            return None

        # Perception event (used only as an intermediate container)
        return VisionEvent(
            timestamp=datetime.utcnow(),
            event_type="perception_update",
            confidence=1.0,
            metadata={
                "objects": detections
            }
        )
