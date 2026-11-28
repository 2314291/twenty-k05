#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 11-patch-tasks-status_code_conformance.sh
# Operation : PATCH /tasks
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/tasks?depth=0.5&filter=createdAt%5Bgte%5D%3A%222026-11-28T13%3A27%3A54.000Z%22' \
  -H 'Content-Type: application/json' \
  --data-binary '{"status": "TODO"}'
