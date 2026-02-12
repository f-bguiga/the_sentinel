#!/bin/bash

# Exit on any error
set -e

echo "🛡️ Starting The Sentinel: Full System Initialization..."

# 1. Check for Docker
if ! [ -x "$(command -v docker)" ]; then
  echo '❌ Error: docker is not installed.' >&2
  exit 1
fi

# 2. Spin up the infrastructure
echo "🐳 Spinning up Docker containers (Inference API & MLflow)..."
docker compose up -d

# 3. Wait for MLflow to be ready
echo "⏳ Waiting for MLflow server to initialize..."
sleep 10

# 4. Run the MLOps Pipeline inside Docker
echo "🧐 Running Data Validation (Great Expectations)..."
docker compose run --rm sentinel_api python src/setup_gx.py

echo "🚂 Training the Initial Model..."
docker compose run --rm sentinel_api python -m src.train

echo "🚀 Promoting Model to @champion and @candidate..."
docker compose run --rm sentinel_api python -m src.promote_model

# 5. Restart API to load the new models
echo "♻️ Restarting Inference API to load models..."
docker compose restart sentinel_api

echo "✅ SETUP COMPLETE!"
echo "📡 API is running at: http://localhost:8000"
echo "📊 MLflow UI is at: http://localhost:5000"
echo "🔍 Check your docs at: http://localhost:8000/docs"