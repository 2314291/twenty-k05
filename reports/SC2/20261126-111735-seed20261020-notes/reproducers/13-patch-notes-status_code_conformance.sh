#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 13-patch-notes-status_code_conformance.sh
# Operation : PATCH /notes
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/notes?depth=0.5&filter=createdAt%5Bgte%5D%3A%222026-11-26T04%3A19%3A07.000Z%22' \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
