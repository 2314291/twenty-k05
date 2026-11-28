#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 23-post-notes-status_code_conformance.sh
# Operation : POST /notes
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 201, 400, 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/notes?depth=0.5&upsert=2' \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
