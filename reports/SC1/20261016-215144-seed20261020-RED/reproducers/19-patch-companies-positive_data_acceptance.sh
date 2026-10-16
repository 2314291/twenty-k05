#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 19-patch-companies-positive_data_acceptance.sh
# Operation : PATCH /companies
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 24
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 3 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies?depth=1&fields=id%2Cname%2Cemails%2Ccompany&filter=name%5Blike%5D%3A%22%25value%25%22' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
