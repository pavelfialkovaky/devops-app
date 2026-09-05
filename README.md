
Runs the app against a local Postgres container (separate from the AWS RDS instance used in production).

## Deployment

Fully automated. A push to `main` runs the test suite, builds a Docker image, pushes it to GHCR, and deploys it to the EC2 instance via AWS Systems Manager — no manual steps required.

## Tech stack

Flask · PostgreSQL · Docker · GitHub Actions · AWS (EC2, RDS, IAM, Systems Manager)

## Kubernetes (local)

Manifests in `k8s/` deploy this app to a local Kubernetes cluster (tested with minikube):

kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/app-deployment.yaml

Runs 2 replicas of the app behind a Service, backed by a single Postgres Pod.
The app runs under gunicorn (not Flask's dev server) so it shuts down
gracefully on SIGTERM during Pod termination and rolling updates.