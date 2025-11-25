#!/bin/bash
# Helper script to run codeinspector locally using the current python environment
# Usage: ./run_local.sh [command] [options]

python3 -m codeinspector.cli "$@"
