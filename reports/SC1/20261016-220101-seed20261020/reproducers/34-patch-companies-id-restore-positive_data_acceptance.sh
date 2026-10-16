#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 34-patch-companies-id-restore-positive_data_acceptance.sh
# Operation : PATCH /companies/{id}/restore
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 9
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/736ae8fb-d1c4-43d7-a9f2-d7560e2b0950/restore?depth=1&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
