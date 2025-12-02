import asyncio
from typing import Any
from src.interfaces import ModelInterface
from src.schemas import PredictionRequest, PredictionResponse

class ProductionModel(ModelInterface):
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        # Simulate processing time
        await asyncio.sleep(0.05) 
        # Logic: Simple duplication
        input_val = request.data.get("value", 0)
        return PredictionResponse(
            request_id=request.request_id,
            model_name="production_v1",
            output=input_val * 2,
            latency_ms=50.0
        )

class ShadowModel(ModelInterface):
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        # Simulate slightly slower processing
        await asyncio.sleep(0.08)
        
        input_val = request.data.get("value", 0)
        # BUG SIMULATION: Shadow model fails if value > 80
        if input_val > 80:
            result = (input_val * 2) + 1 # Error!
        else:
            result = input_val * 2
            
        return PredictionResponse(
            request_id=request.request_id,
            model_name="shadow_v2-beta",
            output=result,
            latency_ms=80.0
        )