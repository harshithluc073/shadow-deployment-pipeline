import asyncio
from typing import Dict, Any
from src.interfaces import ModelInterface
from src.schemas import PredictionRequest, PredictionResponse

class ShadowEngine:
    def __init__(self, primary_model: ModelInterface, shadow_model: ModelInterface):
        self.primary = primary_model
        self.shadow = shadow_model

    async def run_shadow_test(self, request_data: Dict[str, Any], req_id: str) -> Dict[str, PredictionResponse]:
        """
        Sends the request to both models in parallel.
        """
        # Create the standard request object
        request = PredictionRequest(request_id=req_id, data=request_data)

        # Launch both tasks simultaneously
        # return_exceptions=True ensures one failure doesn't crash the other
        results = await asyncio.gather(
            self.primary.predict(request),
            self.shadow.predict(request),
            return_exceptions=True
        )

        primary_res, shadow_res = results

        # Handle potential crashes in models gracefully
        if isinstance(primary_res, Exception):
            primary_res = PredictionResponse(
                request_id=req_id, model_name="primary", output=None, latency_ms=0.0, error=str(primary_res)
            )
        
        if isinstance(shadow_res, Exception):
            shadow_res = PredictionResponse(
                request_id=req_id, model_name="shadow", output=None, latency_ms=0.0, error=str(shadow_res)
            )

        return {
            "primary": primary_res,
            "shadow": shadow_res
        }