#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 25-patch-opportunities-positive_data_acceptance.sh
# Operation : PATCH /opportunities
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 19
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 2 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/opportunities?depth=1&fields=id%2Cname%2Cemails%2Ccompany&filter=and%28name%5Blike%5D%3A%22%25value%25%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T05%3A48%3A35.000Z%22%29' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
