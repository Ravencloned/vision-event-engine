import cv2
import time
from engine.core.config import EngineConfig


class VideoSource:
    def __init__(self, source=EngineConfig.VIDEO_SOURCE):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError("Unable to open video source")

        self.prev_time = time.time()

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, 0.0

        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time

        return frame, fps

    def release(self):
        self.cap.release()
