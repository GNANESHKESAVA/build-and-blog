#!/bin/bash
# Linux/Mac helper script to run codeinspector in Docker

# Check if image exists, if not build it
if [[ "$(docker images -q codeinspector 2> /dev/null)" == "" ]]; then
  echo "Building Docker image..."
  docker build -t codeinspector .
fi

# Run the container with current directory mounted to /workspace
# And mount the codeinspector code to /app (so it works from anywhere)
# We need to find the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

docker run --rm -it \
  -v "$(pwd)":/workspace \
  -v "$SCRIPT_DIR":/app \
  -w /workspace \
  -e GOOGLE_API_KEY="$GOOGLE_API_KEY" \
  -e GITHUB_TOKEN="$GITHUB_TOKEN" \
  -e PYTHONPATH=/app \
  codeinspector "$@"
