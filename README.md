# MLOps Factory

A public-safe example of the shape of an ML platform service: a training CLI, MLflow model registry integration, a FastAPI inference API with Prometheus metrics, and Kubernetes manifests for review.

Everything runs locally. The Kubernetes manifests are reviewable examples, not pointers to a live cluster. There is no deployed production behind this repo.

## Service shape

```
+------------------+           +-------------------+
|  Data Sources    |  ----->   |  Pipeline (CLI)   |  -- register --> [ MLflow Registry ]
+------------------+           +-------------------+
                                          |
                                          v
                          +--------------------+
                          |  Docker Image      |  (FastAPI + Model + /metrics)
                          +--------------------+
                                          |
                                          v
                         +-----------------------+
                         |  Kubernetes manifests |
                         |  (deployment, HPA,    |
                         |   service, NetPol)    |
                         +-----------------------+
                                          |
                                          v
                              +---------------+
                              |  Prometheus   |
                              +---------------+
```

The repo holds every box on the diagram except the actual cluster.

## Quickstart (local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements-base.txt
pip install pytest httpx
SKIP_MODEL_LOAD=1 PYTHONPATH=. pytest -q
SKIP_MODEL_LOAD=1 uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Sample request once the API is up:

```bash
curl -X POST http://127.0.0.1:8000/infer \
  -H 'content-type: application/json' \
  -d '{"temperature":60,"vibration":0.3,"pressure":30,"rpm":1500}'
```

For the full training + register path:

```bash
mlflow ui --backend-store-uri ./mlruns --port 5000 &
python -m app.pipeline.cli train --framework sklearn --register --stage Production
```

The TensorFlow and PyTorch training entry points exist (`app/pipeline/train_tensorflow.py`, `train_pytorch.py`) but their heavy dependencies stay out of CI on purpose.

## Service layout

- `app/main.py` — FastAPI app with `/healthz`, `/metrics`, `/infer`. The `/infer` 500 path logs the exception and returns a fixed-string detail; it does not echo `str(e)` to the client.
- `app/model_registry.py` — MLflow load/predict boundary. The `predict_proba` fallback is what `/infer` actually calls.
- `app/monitoring/metrics.py` — Prometheus request, error, latency, in-flight counters.
- `app/monitoring/drift.py` — rolling input statistics for drift signal.
- `app/pipeline/` — training CLIs (sklearn baseline + optional TF/PyTorch).
- `infra/docker/` — Dockerfile.
- `infra/k8s/` — example manifests (namespace, deployment, service, HPA, NetworkPolicy, ServiceMonitor).
- `ops/` — incident runbook, SRE playbook, data-privacy notes, Grafana dashboard JSON.

## CI

- `ci.yml` runs `flake8` + `pytest` against `requirements-dev.txt` (the lightweight set, no TF or PyTorch).
- `docker.yml` builds and pushes the image to GHCR on push to `main`. PRs do not push.
- `Secret Scan` runs gitleaks.

## Docker and Kubernetes

```bash
docker build -t ghcr.io/<your-user>/mlops-factory:latest -f infra/docker/Dockerfile .
```

To run the manifests against your own cluster:

```bash
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/configmap.yaml
kubectl apply -f infra/k8s/
kubectl -n mlops-factory port-forward svc/inference 8080:80
```

The manifests assume Prometheus is in the cluster (the `ServiceMonitor` resource targets the kube-prometheus-stack CRDs).

## What's not deployed

- No live MLflow tracking server. Local file backend (`file:./mlruns`) is the default.
- No live Kubernetes cluster. The manifests are reviewable text.
- No real training data. The pipeline uses a synthetic generator (`app/pipeline/data.py`).
- The optional TF and PyTorch training paths are not exercised in CI by design (the dependency surface and runtime cost are not worth it on a public demo repo).

## Security and operational notes

- `ops/security.md` — secret handling, least-privilege CI, registry posture.
- `ops/incident_runbook.md` — detection, triage, mitigation, rollback, postmortem.
- `ops/sre_playbook.md` — SLOs, scaling, canary releases.
- `ops/data_privacy.md` — what to confirm before pointing this at real data.
- `docs/architecture.md` — design notes.

## License

MIT © 2025
