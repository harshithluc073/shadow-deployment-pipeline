import typer
import asyncio
import uvicorn
from fastapi import FastAPI
from src.schemas import PredictionRequest
from src.mock_models import ProductionModel, ShadowModel
from src.engine import ShadowEngine
from src.evaluator import Evaluator
from src.reporter import Reporter
from src.data_adapters import SyntheticGenerator

# --- Configuration ---
app = FastAPI(title="Shadow Deployment Pipeline")
cli = typer.Typer()

# Initialize Singletons
prod_model = ProductionModel()
shadow_model = ShadowModel()
engine = ShadowEngine(prod_model, shadow_model)
evaluator = Evaluator()
reporter = Reporter()

# --- API Endpoints ---
@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Real-time shadow testing endpoint.
    """
    results = await engine.run_shadow_test(request.data, request.request_id)
    comparison = evaluator.compare(results["primary"], results["shadow"])
    return comparison

# --- CLI Commands ---
@cli.command()
def run_simulation(count: int = 100):
    """
    Generates synthetic traffic and runs the shadow test suite locally.
    """
    print(f"🚀 Starting Shadow Simulation with {count} requests...")
    
    # 1. Generate Data
    gen = SyntheticGenerator(template={"value": 50, "metadata": "test"})
    data = gen.generate(count)
    
    # 2. Run Engine (Async loop in sync CLI)
    async def _run_loop():
        results_list = []
        inputs_list = []
        
        for i, item in enumerate(data):
            req_id = f"req_{i}"
            res = await engine.run_shadow_test(item, req_id)
            comparison = evaluator.compare(res["primary"], res["shadow"])
            results_list.append(comparison)
            inputs_list.append({"request_id": req_id, "data": item})
            
            # Simple progress bar
            if i % 10 == 0:
                print(".", end="", flush=True)
        
        print("\n✅ Simulation Complete.")
        
        # 3. Report
        reporter.generate_html_report(results_list)
        reporter.save_regressions(results_list, inputs_list)

    asyncio.run(_run_loop())

@cli.command()
def start_server():
    """Starts the API server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    cli()