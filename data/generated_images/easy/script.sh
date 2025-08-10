#!/bin/bash
# remove-metadata.sh
# Removes all files ending with 'metadata.json' from a given directory (recursively)
# Usage: ./remove-metadata.sh /path/to/folder

set -euo pipefail

TARGET_DIR="${1:-.}"

# Check if fd is installed; if not, fall back to find
if command -v fd >/dev/null 2>&1; then
    echo "Using fd (fast mode)..."
    fd 'metadata\.json$' -t f "$TARGET_DIR" -x rm
else
    echo "Using find (standard mode)..."
    find "$TARGET_DIR" -type f -name '*metadata.json' -delete
fi

echo "✅ All '*metadata.json' files removed from $TARGET_DIR"
