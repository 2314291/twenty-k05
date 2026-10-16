#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 48-post-companies-duplicates-positive_data_acceptance.sh
# Operation : POST /companies/duplicates
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 13
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 4 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/companies/duplicates?depth=1&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["3c8fad72-391d-4e91-9dae-b4536b9f82b7"]}'
