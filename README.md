## Deployment

Fully automated. A push to `main` runs the test suite, builds a Docker image, pushes it to GHCR, and deploys it to the EC2 instance via AWS Systems Manager — no manual steps required.

Since the whole file's changed a bit from your original, here's the complete replacement:

markdown
# DevOps App

![CI](https://github.com/pavlofialkovskyi/devops-app/actions/workflows/ci.yml/badge.svg)

A Flask + Postgres app with fully automated CI/CD, deployed on AWS.

**Live:** http://13.58.204.111:5000/notes

## Architecture

- **App:** Flask (`app.py`), two endpoints — `GET /notes`, `POST /notes`
- **Database:** AWS RDS (PostgreSQL 16), reached only from the app's EC2 instance (locked down by security group, not public)
- **Hosting:** EC2 (Amazon Linux 2023, Free Tier), Docker container pulled from GHCR
- **CI/CD:** GitHub Actions — every push to `main` runs the test suite against a throwaway Postgres container, builds and pushes a Docker image to GHCR if tests pass, then deploys it straight to EC2 via AWS Systems Manager

GitHub push → GitHub Actions (test → build → push image to GHCR → deploy via SSM)
↓
EC2 (Docker) ←→ RDS (Postgres)


## Run locally

docker compose up -d


Runs the app against a local Postgres container (separate from the AWS RDS instance used in production).

## Deployment

Fully automated. A push to `main` runs the test suite, builds a Docker image, pushes it to GHCR, and deploys it to the EC2 instance via AWS Systems Manager — no manual steps required.

## Tech stack

Flask · PostgreSQL · Docker · GitHub Actions · AWS (EC2, RDS, IAM, Systems Manager)