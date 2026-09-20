# Enterprise CI/CD Quality Gate Pipeline

A production-style Jenkins CI/CD pipeline demonstrating automated quality gates, build verification, deployment validation, and release-readiness controls.

## Architecture

GitHub → Jenkins → Checkout → Quality Checks → Tests → Coverage Gate → Build → Deployment Validation → Release Readiness → Notification

## What this demonstrates

- Jenkins declarative pipeline
- Automated quality gates
- Python linting and pytest execution
- Coverage threshold enforcement
- Build artifact generation
- Deployment smoke validation
- Release-readiness checkpoint
- JUnit and coverage reports
- Post-build notifications
- Fail-fast behavior for quality failures

## Run locally

```bash
pip install -r requirements.txt
pytest --junitxml=reports/junit.xml --cov=app --cov-report=xml:reports/coverage.xml --cov-report=term
```

## Jenkins

Create a Pipeline job and point it to this repository. The included `Jenkinsfile` runs the complete workflow.

The pipeline is intentionally technology-light so the same quality-gate pattern can be adapted to Java, .NET, UI automation, or API automation projects.
