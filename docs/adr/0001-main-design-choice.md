# ADR 0001: Keep CI on the Lightweight MLOps Dependency Set

## Status

Accepted

## Context

Large ML frameworks slow down routine validation and make simple pull-request checks fragile.

## Decision

CI installs `app/requirements-dev.txt`, which includes the FastAPI, scikit-learn, test, and
lint dependencies. MLflow, TensorFlow, and PyTorch remain optional local examples outside the
fast pull-request gate.

## Consequences

Pull requests get faster feedback. The tradeoff is that optional framework examples need a
separate validation path before they are treated as supported production code.
