# DevOps App

![CI](https://github.com/pavlofialkovskyi/devops-app/actions/workflows/ci.yml/badge.svg)

A Flask + Postgres app with automated CI/CD, deployed on AWS.

**Live:** http://13.58.204.111:5000/notes

## Architecture

- **App:** Flask (`app.py`), two endpoints — `GET /notes`, `POST /notes`
- **Database:** AWS RDS (PostgreSQL 16), reached only from the app's EC2 instance (locked down by security group, not public)
- **Hosting:** EC2 (Amazon Linux 2023, Free Tier), Docker container pulled from GHCR
- **CI/CD:** GitHub Actions — every push to `main` runs the test suite against a throwaway Postgres container, then builds and pushes a Docker image to GHCR (tagged by commit SHA) if tests pass

GitHub push → GitHub Actions (test → build → push image to GHCR)
↓
EC2 (Docker) ←→ RDS (Postgres)


## Run locally

docker compose up -d


Runs the app against a local Postgres container (separate from the AWS RDS instance used in production).

## Deployment

Currently manual: SSM into the EC2 instance, `docker pull` the latest image tag from GHCR, and restart the `devops-app` container. Automating this (push to `main` → live on EC2 with no manual steps) is the next planned improvement.

## Tech stack

Flask · PostgreSQL · Docker · GitHub Actions · AWS (EC2, RDS, IAM, Systems Manager)