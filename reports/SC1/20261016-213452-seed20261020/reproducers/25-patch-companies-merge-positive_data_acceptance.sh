#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 25-patch-companies-merge-positive_data_acceptance.sh
# Operation : PATCH /companies/merge
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 23
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 4 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/merge?depth=1&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["9073f47e-cef7-4a46-adf6-92aac3cd90e0"], "conflictPriorityIndex": 0, "dryRun": false}'
