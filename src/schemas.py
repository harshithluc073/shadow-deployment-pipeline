from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    request_id: str = Field(..., description="Unique ID for the request")
    data: Dict[str, Any] = Field(..., description="Input features for the model")
    timestamp: datetime = Field(default_factory=datetime.now)

class PredictionResponse(BaseModel):
    request_id: str
    model_name: str
    output: Any
    latency_ms: float
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)