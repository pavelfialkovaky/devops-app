Runs the app against a local Postgres container (separate from the AWS RDS instance used in production).

## Deployment

Fully automated. A push to `main` runs the test suite, builds a Docker image, pushes it to GHCR, and deploys it to the EC2 instance via AWS Systems Manager — no manual steps required.

## Tech stack

Flask · PostgreSQL · Docker · GitHub Actions · AWS (EC2, RDS, IAM, Systems Manager, EKS)

## Kubernetes (local)

Manifests in `k8s/` deploy this app to a local Kubernetes cluster (tested with minikube):

kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/app-deployment.yaml


Runs 2 replicas of the app behind a Service, backed by a single Postgres Pod.
The app runs under gunicorn (not Flask's dev server) so it shuts down
gracefully on SIGTERM during Pod termination and rolling updates.

## Kubernetes (AWS EKS)

The same manifests were also deployed, unchanged, to a real AWS EKS cluster
running on Fargate (no self-managed EC2 worker nodes) — demonstrating that
Kubernetes manifests are portable across environments.

Notable issue hit and resolved: on a Fargate-only cluster, CoreDNS (Kubernetes'
internal DNS) has no EC2 node to run on by default, causing service-name
resolution (e.g. `postgres`) to fail and the app to crash-loop. Fixed by
adding a Fargate profile for the `kube-system` namespace and removing
CoreDNS's EC2-only scheduling restriction:

eksctl create fargateprofile --cluster <cluster-name> --region <region>
--name fp-kube-system --namespace kube-system

kubectl patch deployment coredns -n kube-system --type json
-p '[{"op": "remove", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]'


This cluster was created temporarily to validate the deployment and torn down
afterward (`eksctl delete cluster`) to avoid ongoing EKS control-plane costs.