from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    timestamp: datetime
    device_id: str
    count: int