#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 06-delete-companies-id-positive_data_acceptance.sh
# Operation : DELETE /companies/{id}
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 20
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X DELETE \
  http://localhost:3001/rest/companies/6629782f-7275-349e-6c2b-0392f59da65d \
  -H "Authorization: Bearer $TWENTY_API_KEY"
