#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 12-patch-notes-merge-status_code_conformance.sh
# Operation : PATCH /notes/merge
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/notes/merge?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["1c26a3af-547c-449d-9b66-08626968cdde"], "conflictPriorityIndex": 0, "dryRun": false}'
