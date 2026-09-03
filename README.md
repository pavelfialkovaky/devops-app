
Runs the app against a local Postgres container (separate from the AWS RDS instance used in production).

## Deployment

Fully automated. A push to `main` runs the test suite, builds a Docker image, pushes it to GHCR, and deploys it to the EC2 instance via AWS Systems Manager — no manual steps required.

## Tech stack

Flask · PostgreSQL · Docker · GitHub Actions · AWS (EC2, RDS, IAM, Systems Manager)