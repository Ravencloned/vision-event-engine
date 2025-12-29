from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel


class VisionEvent(BaseModel):
    timestamp: datetime
    event_type: str
    confidence: float
    metadata: Dict[str, Any]
