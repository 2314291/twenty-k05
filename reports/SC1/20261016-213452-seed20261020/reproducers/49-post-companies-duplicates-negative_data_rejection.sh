#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 49-post-companies-duplicates-negative_data_rejection.sh
# Operation : POST /companies/duplicates
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: in body - ids -> Array with invalid items: Incorrect type

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/companies/duplicates?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": [null]}'
