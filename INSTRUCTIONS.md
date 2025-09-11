# mlops-factory: Drop-in Bundle

This bundle contains **ready-to-add** files to make `mlops-factory` fully runnable with Docker/K8s and developer-friendly commands.

## How to apply
1. **Unzip** into your local `mlops-factory` repo root (same level as `app/`, `infra/`, `ops/`, etc.).
2. If a file already exists with the same name/path, **review and overwrite**.
3. Run the smoke tests below.

## Files included
- `Dockerfile` — top-level Docker image to run the FastAPI service.
- `ops/start.sh` — small launcher for uvicorn.
- `Makefile` — easy commands for install/test/run/build.
- `README-QUICKSTART.md` — copy the block into your main README under a Quickstart section.

## Smoke test
```bash
# from repo root
python -m venv .venv && source .venv/bin/activate
make install
make test
make run
curl -s localhost:8000/healthz
curl -s -X POST localhost:8000/infer -H "Content-Type: application/json"   -d '{"temperature":60,"vibration":0.3,"pressure":30,"rpm":1500}'
curl -s localhost:8000/metrics | head

# docker
make docker-build
make docker-run
```

## Notes
- CI will remain fast by installing only `app/requirements-base.txt`. Install `app/requirements-ml.txt` locally if you need TF/Torch.
