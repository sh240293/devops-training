# CI/CD Pipeline Setup Guide

This repository contains a complete CI/CD pipeline using GitHub Actions that includes:
1. Unit Tests (ci.yml)
2. SonarQube Scan (sonar.yml)
3. Docker Build and Container Scan (container-scan.yml)
4. Kubernetes Deployment (deploy.yml)

## Required GitHub Secrets

Configure the following secrets in your GitHub repository settings (Settings → Secrets and variables → Actions):

### SonarQube Secrets
- `SONAR_TOKEN`: Your SonarQube authentication token
- `SONAR_HOST_URL`: Your SonarQube server URL (e.g., https://sonarcloud.io)

### Container Registry Secrets (Optional)
- `CONTAINER_REGISTRY`: Container registry URL
  - **For Docker Hub**: Leave empty or set to `docker.io` (both work the same)
  - **For GitHub Container Registry**: Set to `ghcr.io`
  - **For other registries**: Set to your registry URL (e.g., `registry.example.com`)
- `REGISTRY_USERNAME`: Username for container registry
  - **For Docker Hub**: Your Docker Hub username
  - **For GitHub Container Registry**: Your GitHub username
- `REGISTRY_PASSWORD`: Password or token for container registry
  - **For Docker Hub**: Your Docker Hub password or access token
  - **For GitHub Container Registry**: A Personal Access Token (PAT) with `write:packages` permission

**Docker Hub Example:**
- `CONTAINER_REGISTRY`: (leave empty) or `docker.io`
- `REGISTRY_USERNAME`: `your-dockerhub-username`
- `REGISTRY_PASSWORD`: `your-dockerhub-password` or access token

**Note:** If `CONTAINER_REGISTRY` is not set, the image will be built locally and scanned without pushing to a registry.

### Kubernetes Secrets
- `KUBE_CONFIG`: Base64-encoded Kubernetes config file
  - To generate: `cat ~/.kube/config | base64 -w 0` (Linux) or `cat ~/.kube/config | base64` (macOS)
- `K8S_NAMESPACE`: Kubernetes namespace for deployment (optional, defaults to 'default')

## Pipeline Flow

1. **CI - Unit Tests** (`ci.yml`)
   - Runs on push/PR to main/develop branches
   - Executes pytest with coverage
   - Uploads test results and coverage reports

2. **SonarQube Scan** (`sonar.yml`)
   - Triggers after successful CI run
   - Performs code quality analysis
   - Checks quality gate status
   - Blocks pipeline if quality gate fails

3. **Container Build and Scan** (`container-scan.yml`)
   - Triggers after successful SonarQube scan
   - Builds Docker image
   - Scans image with Trivy for CRITICAL and HIGH vulnerabilities
   - Blocks deployment if vulnerabilities found

4. **Kubernetes Deployment** (`deploy.yml`)
   - Triggers after successful container scan
   - Deploys application to Kubernetes cluster
   - Waits for rollout completion
   - Verifies deployment status

## Manual Trigger

All workflows can be manually triggered using `workflow_dispatch` event from the GitHub Actions UI.

## Kubernetes Manifests

The `k8s/` directory contains:
- `deployment.yaml`: Kubernetes deployment manifest
- `service.yaml`: Kubernetes service manifest (LoadBalancer type)

## Testing Locally

```bash
# Run unit tests
pytest test/ -v

# Build Docker image
docker build -t flask-app:latest .

# Run container locally
docker run -p 5000:5000 flask-app:latest
```

