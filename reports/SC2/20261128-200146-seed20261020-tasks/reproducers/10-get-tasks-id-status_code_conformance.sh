#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 10-get-tasks-id-status_code_conformance.sh
# Operation : GET /tasks/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 8
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/tasks/0?depth=0.5'
