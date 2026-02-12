[![Sentinel CI Pipeline](https://github.com/f-bguiga/the_sentinel/actions/workflows/mlops-ci.yml/badge.svg)](https://github.com/f-bguiga/the_sentinel/actions/workflows/mlops-ci.yml)
🛡️ Project: The Sentinel

Production-Grade Fraud Detection with Automated Governance & Shadow Deployments
🎯 Goal

The Sentinel is not just a model; it is a closed-loop MLOps ecosystem. It handles the entire lifecycle of a fraud detection model—from data versioning and schema validation to shadow deployments and automated retraining.
🏗️ The Architecture

    Data Governance: DVC for data versioning and Great Expectations for schema/quality enforcement.

    Feature Store (Light): A centralized features.py module ensuring 100% Feature Parity between training and serving.

    Experimentation: MLflow for tracking hyperparameters and metrics.

    Model Registry: Automated aliasing (@champion and @candidate) to manage model promotion.

    Deployment: FastAPI microservice serving predictions with Shadow Deployment logic.

    Infrastructure: Fully containerized via Docker Compose for environment parity.

    Testing: Pytest suite for model logic validation and Locust for load testing.

🛡️ Key MLOps Features

    Shadow Deployment: The API simultaneously evaluates a candidate model alongside the production model to validate performance on live traffic without impacting users.

    Drift-Triggered Retraining: Automated monitoring detects data drift and initiates the retraining pipeline.

    Zero-Downtime Updates: Swapping models is as simple as updating an MLflow alias; the API automatically pulls the latest artifacts.

🚀 Quick Start (Docker)

The entire stack is orchestrated. You don't need to install Python locally if you have Docker.

1. Clone and Initialize
Bash

git clone https://github.com/your-username/the-sentinel
cd the-sentinel

2. Launch Infrastructure
Bash

docker compose up -d

3. Seed the Model Registry
Bash

# Train the model inside the container
docker compose run --rm sentinel_api python -m src.train

# Promote to Champion/Candidate
docker compose run --rm sentinel_api python -m src.promote_model

4. Test the API
Bash

curl -X 'POST' 'http://localhost:8000/predict' \
-H 'Content-Type: application/json' \
-d '{"id": 1, "amount": 150000.0}'

🧪 Quality Gates

Every deployment passes through four automated gates:

    Data Gate: GX validates schema and range.

    Training Gate: F1-Score must exceed the baseline.

    Promotion Gate: Model is registered and aliased in MLflow.

    Logic Gate: Pytest verifies the output shape and data types.