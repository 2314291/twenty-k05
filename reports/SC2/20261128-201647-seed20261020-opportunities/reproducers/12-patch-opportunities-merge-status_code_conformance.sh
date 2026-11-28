#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 12-patch-opportunities-merge-status_code_conformance.sh
# Operation : PATCH /opportunities/merge
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/opportunities/merge?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["dadebe80-7193-4e87-8d5c-9be644cf1822"], "conflictPriorityIndex": 0, "dryRun": false}'
