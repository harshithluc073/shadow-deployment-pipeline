# Shadow Deployment Pipeline 🕵️‍♂️

**Production-grade tooling for rigorous shadow testing of Machine Learning models.**

This project implements an asynchronous middleware that duplicates traffic from a "Primary" model to a "Shadow" model. It evaluates performance differences, detects concept drift, and captures diverging inputs into a regression test suite.

## 🚀 Features
- **Async Traffic Forking**: Non-blocking I/O using Python `asyncio`.
- **Pluggable Architecture**: Interface-based design allows hot-swapping of models (Local vs API).
- **Automated Reporting**: Generates HTML analysis and JSON regression suites.
- **Drift Detection**: Monitors latency spikes and output mismatches.
- **Docker Ready**: Fully containerized for cloud deployment.

## 🛠️ Installation

### Option A: Local Python
```bash
# Clone and Install
git clone https://github.com/harshithluc073/shadow-deployment-pipeline.git
cd shadow-deployment-pipeline
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```
## 🌍 Real-World Use Cases

This pipeline is designed to be industry-agnostic. Here is how it solves problems in different sectors:

### 1. 🏦 FinTech: Risk Model Migration
*   **Scenario**: Moving from Logistic Regression to a Deep Neural Network for loan approvals.
*   **Risk**: The new model might accidentally approve high-risk applicants that the old model correctly rejected.
*   **Solution**: The pipeline captures applicants where `Old Model = Reject` and `New Model = Approve`. These specific inputs are saved to `regression_suite.json` for manual auditing before the new model goes live.

### 2. 🤖 LLM Ops: Cost Reduction
*   **Scenario**: Replacing GPT-4 (Expensive) with Llama-3 (Self-Hosted/Free).
*   **Risk**: The cheaper model might lose context or "hallucinate" incorrect facts.
*   **Solution**: The `Evaluator` compares the semantic similarity of answers. If the cheaper model's answer drifts too far from GPT-4's baseline, it is flagged, allowing the team to retrain the Llama model on those specific edge cases.

### 3. 🛒 E-Commerce: Search Latency
*   **Scenario**: Upgrading from keyword search to Vector Search (Embeddings).
*   **Risk**: Vector search is computationally heavy and might slow down the website.
*   **Solution**: The pipeline measures `latency_delta`. If specific complex queries cause the new system to spike >200ms compared to the old one, the deployment is halted for optimization.