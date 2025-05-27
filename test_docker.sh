#!/bin/bash

echo "Building Docker image..."
docker build -t whereis-mcp-app .

echo "Running container..."
docker run -p 8081:8081 \
  -e PORT=8081 \
  -e APP_ENV=production \
  --name whereis-test \
  whereis-mcp-app 