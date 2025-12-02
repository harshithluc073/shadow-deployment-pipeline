from abc import ABC, abstractmethod
from src.schemas import PredictionRequest, PredictionResponse

class ModelInterface(ABC):
    """
    Abstract Base Class that all models must implement.
    This allows us to swap 'Production' and 'Shadow' models easily.
    """
    @abstractmethod
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        pass