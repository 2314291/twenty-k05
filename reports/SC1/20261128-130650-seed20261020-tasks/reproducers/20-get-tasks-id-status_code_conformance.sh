#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 20-get-tasks-id-status_code_conformance.sh
# Operation : GET /tasks/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 404
# Documented: 200, 400, 401

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/tasks/736ae8fb-d1c4-43d7-a9f2-d7560e2b0950?depth=1&x-schemathesis-unknown-property=42' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
