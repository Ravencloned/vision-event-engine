import cv2
import numpy as np
from datetime import datetime

from engine.detectors.base import BaseDetector
from engine.core.event import VisionEvent
from engine.core.config import EngineConfig


class MotionDetector(BaseDetector):
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=True
        )

    def detect(self, frame):
        # Preprocessing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Background subtraction
        fg_mask = self.bg_subtractor.apply(blurred)

        # Thresholding + noise removal
        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        thresh = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)
        )

        # Find motion contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        boxes = []
        motion_pixels = 0.0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 600:  # ignore tiny noise
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            boxes.append((x, y, w, h))
            motion_pixels += area

        # Event threshold
        if motion_pixels < EngineConfig.MOTION_THRESHOLD:
            return None

        confidence = min(
            1.0, motion_pixels / (EngineConfig.MOTION_THRESHOLD * 2)
        )

        return VisionEvent(
            timestamp=datetime.utcnow(),
            event_type="motion_detected",
            value=float(motion_pixels),
            confidence=confidence,
            metadata={
                "boxes": boxes,
                "threshold": EngineConfig.MOTION_THRESHOLD
            }
        )
