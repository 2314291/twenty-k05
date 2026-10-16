#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 43-post-companies-positive_data_acceptance.sh
# Operation : POST /companies
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 30
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 5 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/companies?depth=1&upsert=false&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
