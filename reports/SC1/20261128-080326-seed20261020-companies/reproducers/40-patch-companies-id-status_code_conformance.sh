#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 40-patch-companies-id-status_code_conformance.sh
# Operation : PATCH /companies/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 2
# Received: 404
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/311544b2-5fa2-4990-86b8-3674f1050fcf?depth=1&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
