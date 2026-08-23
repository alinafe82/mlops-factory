# CI/CD operations

## Required checks

Lightweight model API tests, Flake8, dependency integrity, and a provenance-enabled GHCR container build.

All workflows use explicit token permissions, bounded runtimes, concurrency controls, and
immutable commit pins for external actions where actions are used.

## Zero-cost publication policy

Every pull request and default-branch push builds and scans the container on GitHub's free
public-repository runners. GHCR publication is disabled by default so a package-storage quota
cannot create charges. The publish job runs only when the repository variable
`ENABLE_GHCR_PUBLISH` is explicitly set to `true`; keep it unset while the account uses a hard
$0 Packages budget. The disabled path remains available as a reviewed release specification and
adds immutable tags, an SBOM, and provenance attestations when deliberately enabled.

## Failure notifications

The `CI Failure Alert` workflow creates or updates an issue assigned to the repository owner
when a monitored workflow fails or times out, and closes the issue after recovery. Assignment and
repository watching provide a durable GitHub notification trail.

For email delivery, enable **Settings → Notifications → System → Actions → Email**, select
**Only notify for failed workflows**, and watch this repository. GitHub owns this setting; workflow
YAML cannot force an account email destination. No SMTP credentials are required by this repo.

## Incident response

1. Open the linked failed run and identify the first failing job.
2. Reproduce its named command locally before changing the workflow.
3. Fix the product or workflow on a pull request; do not bypass a required check.
4. Confirm the default-branch recovery run closes the alert issue.
