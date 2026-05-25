# Architecture

## Problem

ML services fail operationally when training, registry state, serving, metrics, and rollout
documents are disconnected. This repo keeps those concerns in one small reference service so
the operational boundaries are visible.

## Intended User

The intended user is a platform or MLOps engineer reviewing how a model moves from training to
serving and monitoring.

## Components

- Training CLI: creates synthetic data and trains a baseline model.
- MLflow boundary: tracks runs and loads staged models.
- FastAPI inference service: exposes health, metrics, and inference endpoints.
- Monitoring: Prometheus metrics and simple input drift statistics.
- Kubernetes manifests: reviewable deployment, service, HPA, and network policy examples.
- Operations docs: incident, security, privacy, and SRE notes.

## Data Flow

Synthetic data feeds the training CLI. The trained model is logged or registered through
MLflow. The inference service loads a configured model lazily and serves predictions while
emitting metrics.

## Design Choices

I kept CI on the lightweight dependency set because MLflow, TensorFlow, and PyTorch wheels make
routine validation slow. The optional registry and ML framework examples remain available for
local exploration.

The inference app returns a safe fallback probability when no model is loaded so API tests can
run without a registry.

## What Is Not Built

This repo is not a full production MLOps platform. It does not include a real feature store,
online/offline consistency checks, release approval, or live cluster deployment.

## Extension Points

- Add MLflow integration tests with a temporary tracking directory.
- Add model promotion and rollback commands.
- Add batch scoring and feature-store examples.
- Add canary routing and release metrics.

## Operational Considerations

A production system should pin image digests, isolate registry credentials, record model
lineage, measure data quality, and define rollback criteria before rollout.

## Testing Strategy

Tests cover API behavior and synthetic data generation. CI uses the lightweight dependency set
for fast feedback. The next useful layer is an MLflow integration test for register/load paths.
