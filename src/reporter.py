import json
import os
from typing import List, Dict, Any
from jinja2 import Template

class Reporter:
    def __init__(self, output_dir: str = "artifacts"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_regressions(self, results: List[Dict[str, Any]], inputs: List[Dict[str, Any]]):
        """
        Saves inputs that caused mismatches into a JSON file.
        This becomes your new 'Regression Test Suite'.
        """
        # Create a lookup for inputs by request_id
        input_map = {item['request_id']: item['data'] for item in inputs if 'request_id' in item}
        
        failures = []
        for res in results:
            if not res['match']:
                failures.append({
                    "request_id": res['request_id'],
                    "input": input_map.get(res['request_id']),
                    "primary_out": res['primary_out'],
                    "shadow_out": res['shadow_out'],
                    "error": res.get('error_shadow') or res.get('error_primary')
                })

        path = os.path.join(self.output_dir, "regression_suite.json")
        with open(path, "w") as f:
            json.dump(failures, f, indent=2)
        print(f"Regression suite saved to {path} ({len(failures)} failures found)")

    def generate_html_report(self, results: List[Dict[str, Any]]):
        """Generates a visual HTML report."""
        
        # Calculate summary stats
        total = len(results)
        passed = sum(1 for r in results if r['match'])
        failed = total - passed
        avg_latency_delta = sum(r['latency_delta_ms'] for r in results) / total if total > 0 else 0

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Shadow Deployment Report</title>
            <style>
                body { font-family: sans-serif; padding: 20px; }
                .summary { display: flex; gap: 20px; margin-bottom: 20px; }
                .card { border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .fail { background-color: #ffdddd; color: red; }
                .pass { background-color: #ddffdd; color: green; }
            </style>
        </head>
        <body>
            <h1>Shadow Test Results</h1>
            <div class="summary">
                <div class="card"><strong>Total Requests:</strong> {{ total }}</div>
                <div class="card"><strong>Passed:</strong> {{ passed }}</div>
                <div class="card"><strong>Failed:</strong> {{ failed }}</div>
                <div class="card"><strong>Avg Latency Impact:</strong> {{ avg_delta | round(2) }} ms</div>
            </div>

            <h2>Detailed Logs</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Status</th>
                        <th>Primary Out</th>
                        <th>Shadow Out</th>
                        <th>Latency Delta</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in results %}
                    <tr class="{{ 'pass' if row.match else 'fail' }}">
                        <td>{{ row.request_id }}</td>
                        <td>{{ 'MATCH' if row.match else 'MISMATCH' }}</td>
                        <td>{{ row.primary_out }}</td>
                        <td>{{ row.shadow_out }}</td>
                        <td>{{ row.latency_delta_ms }} ms</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            results=results, 
            total=total, 
            passed=passed, 
            failed=failed, 
            avg_delta=avg_latency_delta
        )

        path = os.path.join(self.output_dir, "report.html")
        with open(path, "w") as f:
            f.write(html_content)
        print(f"HTML Report generated at {path}")