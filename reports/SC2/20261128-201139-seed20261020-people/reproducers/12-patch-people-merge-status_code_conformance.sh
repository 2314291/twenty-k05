#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 12-patch-people-merge-status_code_conformance.sh
# Operation : PATCH /people/merge
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/people/merge?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["72e1f50a-d541-4a9f-892f-acc17f81ed65"], "conflictPriorityIndex": 0, "dryRun": false}'
