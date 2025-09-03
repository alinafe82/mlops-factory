# Security Checklist

- Least privilege for CI/CD, registry, and K8s access.
- Secrets stored in K8s Secrets or a managed secret store.
- No PII by default; follow data privacy guidelines if using real data.
- NetworkPolicy denies all by default.
- Enable image scanning/SBOM in CI.
- MLflow + container digests provide an audit trail.
