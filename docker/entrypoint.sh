#!/bin/bash
set -e

# Install qwen-tts in editable mode
if [ -f /workspace/pyproject.toml ]; then
    pip install -e /workspace --no-deps -q 2>/dev/null || true
fi

exec "$@"
