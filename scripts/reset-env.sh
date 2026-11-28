#!/usr/bin/env bash
# Tên theo PHAN_CONG (scripts/reset-env.sh). Toàn bộ logic nằm ở reset_env.py để chạy được cả trên Windows.
#   bash scripts/reset-env.sh              # khôi phục snapshot + seed
#   bash scripts/reset-env.sh --snapshot   # chụp snapshot (một lần)
set -euo pipefail
cd "$(dirname "$0")/.."
PY="$(command -v python3 || command -v python)"
exec "$PY" scripts/reset_env.py "$@"
