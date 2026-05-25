# Interview Notes

## 60-Second Explanation

MLOps Factory is a reference ML service showing the path from training to registry-backed
serving and monitoring. It includes a training CLI, MLflow boundary, FastAPI inference service,
Prometheus metrics, Kubernetes manifests, and operations notes.

## Decisions I Can Defend

- Keep CI lightweight so routine checks stay fast.
- Isolate model loading behind `model_registry.py`.
- Emit operational metrics from the inference path.
- Use synthetic data so the public repo contains no private training data.

## Tradeoffs

The repo shows platform shape, not a live production deployment. Optional MLflow, TensorFlow,
and PyTorch examples increase breadth, but the scikit-learn/API path is the practical
CI-supported path.

## Fixes Made During Portfolio Hardening

- Removed tracked `.DS_Store` files.
- Replaced inflated README claims with explicit scope.
- Added a dev requirements file used by CI.
- Added architecture notes, ADR, and interview notes.

## Likely Questions

**Why keep MLflow, TensorFlow, and PyTorch out of fast CI?**
Because routine CI should validate the service shape quickly. Heavy registry and framework
checks can run in a separate scheduled or release workflow.

**What would make this production-ready?**
Model lineage, promotion approvals, rollback commands, feature quality checks, registry
credentials, canary metrics, and integration tests against MLflow.

**What does this show for Engineering Productivity?**
It shows how I structure platform code so training, serving, CI, observability, and operations
are reviewable together.
