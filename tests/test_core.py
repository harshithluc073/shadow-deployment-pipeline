import pytest
from src.schemas import PredictionRequest
from src.mock_models import ProductionModel, ShadowModel
from src.engine import ShadowEngine
from src.evaluator import Evaluator

@pytest.mark.asyncio
async def test_shadow_engine_logic():
    # Setup
    prod = ProductionModel()
    shadow = ShadowModel()
    engine = ShadowEngine(prod, shadow)
    
    # Test Data
    req_id = "test_123"
    data = {"value": 10}
    
    # Action
    results = await engine.run_shadow_test(data, req_id)
    
    # Assertions
    assert "primary" in results
    assert "shadow" in results
    assert results["primary"].output == 20  # 10 * 2
    assert results["shadow"].output == 20   # 10 * 2

def test_evaluator_mismatch():
    evaluator = Evaluator()
    # Mocking responses directly
    from src.schemas import PredictionResponse
    
    r1 = PredictionResponse(request_id="1", model_name="A", output=100, latency_ms=10)
    r2 = PredictionResponse(request_id="1", model_name="B", output=101, latency_ms=12) # Mismatch
    
    result = evaluator.compare(r1, r2)
    assert result["match"] is False
    assert result["latency_delta_ms"] == 2.0