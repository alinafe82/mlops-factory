# Linting and Testing Standards

These standards define the checks expected before a pull request is marked ready. Run the sections for the
languages touched by the change.

## Required Gates

- Start from the default branch and keep the PR focused on one reviewable change.
- Run `git diff --check` before committing.
- Run `repowave scan .` when `repowave.toml` is present.
- Run every applicable language command below. If a command needs credentials, a live service, or unavailable
  platform tooling, state that in the PR and run the closest local gate.
- Add or update tests for behavior changes. Documentation-only changes still need the diff and repository gates.

## Python

- Prefer Ruff for linting and Pytest for pipeline, training, and registry behavior.
- Keep tests fast by using small local fixtures instead of remote MLflow, model registry, or cloud resources.
- Add explicit integration tests for Docker or MLflow flows that need services.

## Shell

- Run `shellcheck` and `shfmt -d` on touched shell scripts.

## Current Command Map

- Install: `make install`.
- Lint: `make lint`.
- Tests: `make test`.
- Run gate: `make run` when the local demo flow is part of the change.
- Container checks: `make docker-build` and `make docker-run` when Docker files change.
