#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 22-post-people-duplicates-status_code_conformance.sh
# Operation : POST /people/duplicates
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/people/duplicates?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["d3ae89a4-55c4-48f5-b20b-4fe994ad223a"]}'
