from typing import Dict, Any
from src.schemas import PredictionResponse

class Evaluator:
    def compare(self, primary: PredictionResponse, shadow: PredictionResponse) -> Dict[str, Any]:
        """
        Compares two model responses and returns metrics.
        """
        # 1. Check for output mismatch
        # If outputs are numbers, use a small tolerance, otherwise strict equality
        is_match = False
        try:
            if isinstance(primary.output, (int, float)) and isinstance(shadow.output, (int, float)):
                # Allow 0.1% difference for floating point variance
                is_match = abs(primary.output - shadow.output) <= 0.001 * abs(primary.output)
            else:
                is_match = primary.output == shadow.output
        except Exception:
            is_match = False # Fallback if comparison fails

        # 2. Calculate Latency Impact
        # Positive value means Shadow is slower
        latency_delta = shadow.latency_ms - primary.latency_ms

        return {
            "request_id": primary.request_id,
            "match": is_match,
            "primary_out": primary.output,
            "shadow_out": shadow.output,
            "latency_delta_ms": round(latency_delta, 2),
            "primary_latency": primary.latency_ms,
            "shadow_latency": shadow.latency_ms,
            "error_primary": primary.error,
            "error_shadow": shadow.error
        }