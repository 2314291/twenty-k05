#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 26-post-notes-duplicates-status_code_conformance.sh
# Operation : POST /notes/duplicates
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/notes/duplicates?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["0e51bece-648f-468d-a01b-4c86f963da04"]}'
