from abc import ABC, abstractmethod
from typing import Optional
from engine.core.event import VisionEvent


class BaseDetector(ABC):
    @abstractmethod
    def detect(self, frame) -> Optional[VisionEvent]:
        pass
