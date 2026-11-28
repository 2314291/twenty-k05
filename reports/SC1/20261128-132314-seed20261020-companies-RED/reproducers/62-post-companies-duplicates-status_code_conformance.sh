#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 62-post-companies-duplicates-status_code_conformance.sh
# Operation : POST /companies/duplicates
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/companies/duplicates?depth=0&fields=id%2Cname' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["ee893990-174a-4894-a58e-0678e2645fc4"]}'
