import pandas as pd
import json
import random
from typing import List, Dict, Any

class LogLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Dict[str, Any]]:
        """Loads data from CSV or JSON file into a list of dictionaries."""
        if self.file_path.endswith('.csv'):
            df = pd.read_csv(self.file_path)
            # Convert NaN to None for JSON compatibility and return records
            return df.where(pd.notnull(df), None).to_dict(orient='records')
        elif self.file_path.endswith('.json'):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            raise ValueError("Unsupported file format. Use .csv or .json")

class SyntheticGenerator:
    def __init__(self, template: Dict[str, Any]):
        """
        template: A sample dictionary representing the input structure.
        """
        self.template = template

    def generate(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generates synthetic data by slightly modifying the template."""
        data = []
        for _ in range(count):
            item = {}
            for k, v in self.template.items():
                # Simple fuzzing logic based on type
                if isinstance(v, int):
                    item[k] = v + random.randint(-5, 5)
                elif isinstance(v, float):
                    item[k] = round(v * random.uniform(0.9, 1.1), 4)
                elif isinstance(v, str):
                    item[k] = f"{v}_{random.randint(100, 999)}"
                else:
                    item[k] = v
            data.append(item)
        return data