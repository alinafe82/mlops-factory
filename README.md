# MLOps Factory

Production-ready application for **seamless deployment of machine learning models** into automation products.
Includes an end-to-end pipeline (data → train → register → deploy → monitor), a FastAPI inference service,
observability, Kubernetes manifests, CI/CD, security and incident response documentation.

> **Most valuable capability showcased here:** *Seamless, reliable deployment of versioned ML models into production systems.*
> This repo operationalizes models via MLflow (staging/promotions/rollbacks) and a FastAPI service that loads staged models at runtime.

---

## Architecture

```
+------------------+           +-------------------+
|  Data Sources    |  ----->   |  Pipeline (CLI)   |  -- register --> [ MLflow Model Registry ]
+------------------+           +-------------------+
                                    |
                                    v
                          +--------------------+
                          |  Docker Image      |  (FastAPI + Model + Metrics)
                          +--------------------+
                                    |
                                    v
                         +-----------------------+
                         |  Kubernetes (HPA,     |
                         |  Service, NetworkPol) |
                         +-----------------------+
                                    |
                                    v
                         +-----------------------+
                         |  Observability (Prom) |
                         |  + Grafana            |
                         +-----------------------+
```

---

## Features

- **Multiple training backends:** scikit-learn (baseline), **TensorFlow**, **PyTorch** (CPU).
- **MLflow integration:** track runs, log metrics, register and stage models (`Staging`/`Production`) for safe rollouts.
- **Inference microservice:** FastAPI with `/infer`, `/healthz`, `/metrics` (Prometheus).
- **Monitoring:** latency histograms, request counters, error counters, and simple input-drift signals.
- **Kubernetes-first:** Deployment, Service, HPA, NetworkPolicy, ServiceMonitor, ConfigMap.
- **CI/CD:** GitHub Actions — fast unit tests + image build/push to GHCR.
- **Operations:** incident runbook, security & privacy checklists, SRE playbook, Grafana dashboard JSON.
- **Serverless/Edge-ready:** containerized inference (CPU) for portability.

---

## Repository Layout

```
mlops-factory/
├── app/
│   ├── main.py                 # FastAPI service (inference + metrics + health)
│   ├── config.py               # Env-configured runtime
│   ├── model_registry.py       # MLflow load/predict helpers
│   ├── monitoring/
│   │   ├── metrics.py          # Prometheus metrics
│   │   └── drift.py            # Rolling input stats for drift
│   ├── pipeline/
│   │   ├── cli.py              # CLI: train & register with MLflow
│   │   ├── data.py             # Synthetic data generator
│   │   ├── preprocess.py       # Preprocessing utilities
│   │   ├── train_sklearn.py    # Baseline model
│   │   ├── train_tensorflow.py # TensorFlow model
│   │   └── train_pytorch.py    # PyTorch model
│   ├── utils/
│   │   └── logging.py          # Structured logging
│   ├── requirements.txt        # Full runtime (FastAPI+MLflow+sklearn+TF+Torch)
│   ├── requirements-base.txt   # FastAPI+MLflow+sklearn (lighter)
│   └── requirements-ml.txt     # TensorFlow + PyTorch only
├── infra/
│   ├── docker/Dockerfile       # Production image
│   └── k8s/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── hpa.yaml
│       ├── networkpolicy.yaml
│       └── servicemonitor.yaml
├── ops/
│   ├── incident_runbook.md
│   ├── security.md
│   ├── data_privacy.md
│   ├── sre_playbook.md
│   └── grafana_dashboard.json
├── tests/
│   ├── test_api.py
│   └── test_data.py
├── .github/workflows/
│   ├── ci.yml                  # Lint + unit tests (light deps)
│   └── docker.yml              # Build & push image to GHCR
├── docker-compose.mlflow.yml   # Local MLflow tracking server
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quickstart: Local Development

### 1) Create Python environment
```bash
python3 -m venv .venv
source .venv/bin/activate
# Full stack (includes TensorFlow + PyTorch)
pip install -r app/requirements.txt
```

> Note: TensorFlow/PyTorch wheels may be large; on macOS/Linux CPU they install via pip.
> For fast CI cycles, use `requirements-base.txt` only.

### 2) Start MLflow (local file backend)
```bash
mlflow ui --backend-store-uri ./mlruns --host 0.0.0.0 --port 5000
```

### 3) Train + register a model
Use the CLI to train with your preferred framework and register the model.

**scikit-learn**
```bash
python -m app.pipeline.cli train --framework sklearn --register --stage Production
```

**TensorFlow**
```bash
python -m app.pipeline.cli train --framework tensorflow --register --stage Production
```

**PyTorch**
```bash
python -m app.pipeline.cli train --framework pytorch --register --stage Production
```

### 4) Run the inference API
```bash
export MODEL_NAME=factory_defect_model
export MODEL_STAGE=Production
export MLFLOW_TRACKING_URI=file:./mlruns
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

**Endpoints**
- OpenAPI: http://localhost:8080/docs  
- Health:   http://localhost:8080/healthz  
- Metrics:  http://localhost:8080/metrics  

**Sample request**
```bash
curl -s -X POST http://localhost:8080/infer   -H "Content-Type: application/json"   -d '{"temperature":60,"vibration":0.3,"pressure":30,"rpm":1500}'
```

---

## Docker

```bash
docker build -t ghcr.io/<your-user>/mlops-factory:latest -f infra/docker/Dockerfile .
docker run --rm -p 8080:8080   -e MODEL_NAME=factory_defect_model   -e MODEL_STAGE=Production   -e MLFLOW_TRACKING_URI=file:/models/mlruns   ghcr.io/<your-user>/mlops-factory:latest
```

---

## Kubernetes

1) Update the image in `infra/k8s/deployment.yaml`.
2) Apply all manifests:
```bash
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/configmap.yaml
kubectl apply -f infra/k8s/
```
3) Verify
```bash
kubectl -n mlops-factory get pods,svc,hpa
kubectl -n mlops-factory port-forward svc/inference 8080:80
```

---

## CI/CD

- **ci.yml**: lint + unit tests using `requirements-base.txt` (fast).
- **docker.yml**: build and push `ghcr.io/<your-user>/mlops-factory:latest` on push to `main`.

> Make the package public under *GitHub → Packages → mlops-factory → Settings → Change visibility* if needed.

---

## Security, Privacy, Compliance

- Secrets via Kubernetes Secrets or external secret managers.
- Principle of least privilege for CI, registry, and cluster.
- Synthetic data by default; follow `ops/data_privacy.md` before using real data.
- NetworkPolicy denies all by default; open only what you need.
- MLflow + container digests provide an audit trail.

---

## Incident Response & SRE

- `ops/incident_runbook.md` for detection, triage, mitigation, rollback, postmortem.
- `ops/sre_playbook.md` covers SLOs, scaling, resilience, canary/staged releases.

---

## Extending

- Add a feature store, batch scoring job, or pipeline orchestration (TFX/Kubeflow) as needed.
- Swap baseline model for domain-specific architectures (e.g., vision or time-series).

---

## License

MIT © 2025
