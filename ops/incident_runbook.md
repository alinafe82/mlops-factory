# Incident Runbook

## Detection
- Alerts:
  - `inference_errors_total` > 0 for 5m
  - P95 `api_request_latency_seconds` > 500ms for 10m
  - Abnormal input drift (investigate in Grafana)

## Triage
1. `kubectl -n mlops-factory logs deploy/inference`
2. Check `/healthz` and `/metrics`
3. Validate MLflow model version/stage

## Mitigation
- Roll back to previous Deployment image.
- Demote faulty model from `Production` and promote last known-good.
- Scale replicas if CPU/memory constrained.

## Postmortem
- Timeline, root cause, corrective/preventive actions.
- Update tests/monitors to prevent recurrence.
