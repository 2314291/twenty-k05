#!/usr/bin/env bash
# Bọc mỏng cho run_k05.py (Linux/macOS/Git Bash). Trên Windows PowerShell dùng thẳng: python scripts/run_k05.py SC1
set -euo pipefail
cd "$(dirname "$0")/.."
exec python scripts/run_k05.py "$@"
