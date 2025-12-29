from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel


class VisionEvent(BaseModel):
    timestamp: datetime
    event_type: str
    value: float
    confidence: float
    metadata: Dict[str, Any]
