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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        fg_mask = self.bg_subtractor.apply(blurred)

        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        motion_pixels = cv2.countNonZero(thresh)

        if motion_pixels < EngineConfig.MOTION_THRESHOLD:
            return None

        confidence = min(1.0, motion_pixels / (EngineConfig.MOTION_THRESHOLD * 2))

        return VisionEvent(
            timestamp=datetime.utcnow(),
            event_type="motion_detected",
            value=float(motion_pixels),
            confidence=confidence,
            metadata={
                "threshold": EngineConfig.MOTION_THRESHOLD
            }
        )
