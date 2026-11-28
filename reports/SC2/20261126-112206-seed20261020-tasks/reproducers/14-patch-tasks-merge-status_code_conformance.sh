#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 14-patch-tasks-merge-status_code_conformance.sh
# Operation : PATCH /tasks/merge
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/tasks/merge?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["7710b9d3-61cc-41f0-a900-e33f306f4ffb"], "conflictPriorityIndex": 0, "dryRun": false}'
