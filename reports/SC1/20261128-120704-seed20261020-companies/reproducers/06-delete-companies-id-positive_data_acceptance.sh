#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 06-delete-companies-id-positive_data_acceptance.sh
# Operation : DELETE /companies/{id}
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 8
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/companies/e9061a45-6983-765c-faac-f4503bdbd65c?soft_delete=false' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
