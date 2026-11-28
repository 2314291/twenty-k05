#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 11-get-notes-id-status_code_conformance.sh
# Operation : GET /notes/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 7
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/notes/0?depth=0.5'
