#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 08-get-companies-positive_data_acceptance.sh
# Operation : GET /companies
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 6
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies?limit=60&depth=1&order_by=id%5BAscNullsFirst%5D%2CcreatedAt%5BDescNullsLast%5D&filter=name%5Blike%5D%3A%22%25value%25%22&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
