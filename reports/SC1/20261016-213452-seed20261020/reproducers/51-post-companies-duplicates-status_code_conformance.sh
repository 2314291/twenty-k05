#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 51-post-companies-duplicates-status_code_conformance.sh
# Operation : POST /companies/duplicates
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/companies/duplicates?depth=0&fields=id%2Cname' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["3c8fad72-391d-4e91-9dae-b4536b9f82b7"]}'
