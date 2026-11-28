#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 25-patch-companies-positive_data_acceptance.sh
# Operation : PATCH /companies
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 26
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 7 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies?depth=1&fields=id%2Cname%2Cemails%2Ccompany&filter=and%28name%5Blike%5D%3A%22%25value%25%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T01%3A04%3A01.000Z%22%29' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
