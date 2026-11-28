#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 02-delete-tasks-status_code_conformance.sh
# Operation : DELETE /tasks
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/tasks?soft_delete=2&filter=createdAt%5Bgte%5D%3A%222026-11-28T13%3A27%3A54.000Z%22'
