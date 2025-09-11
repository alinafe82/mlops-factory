## Quickstart (copy into README)

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
make install

# Optional: bring up MLflow
make compose-mlflow
# open http://localhost:5000

# Train & log a model (sklearn)
MODEL_NAME=factory-model MODEL_STAGE=Staging make train

# Run API locally
make run

# Health
curl -s localhost:8000/healthz

# Inference
curl -s -X POST localhost:8000/infer -H "Content-Type: application/json"   -d '{"temperature":60,"vibration":0.3,"pressure":30,"rpm":1500}'

# Metrics
curl -s localhost:8000/metrics | head

# Docker
make docker-build
make docker-run
```
