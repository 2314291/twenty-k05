#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 12-patch-companies-merge-status_code_conformance.sh
# Operation : PATCH /companies/merge
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/merge?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["d0166d85-e21c-4e4c-80a3-9ca000c8b069"], "conflictPriorityIndex": 0, "dryRun": false}'
