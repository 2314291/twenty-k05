#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 61-post-companies-duplicates-positive_data_acceptance.sh
# Operation : POST /companies/duplicates
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 88
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 3 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/companies/duplicates?depth=1&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["ee893990-174a-4894-a58e-0678e2645fc4"]}'
