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