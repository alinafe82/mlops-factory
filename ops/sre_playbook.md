# SRE Playbook

- **SLOs**: 99.9% availability, P95 latency < 250ms, Error rate < 0.1%.
- **Scaling**: HPA targets CPU 70%; review request/limit sizing.
- **Resilience**: multi-replica deployments; staged rollouts.
- **Releases**: model promotions via MLflow (`Staging` → `Production`).
- **Backups**: MLflow metadata/artifacts, configs.
