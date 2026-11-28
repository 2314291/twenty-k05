#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 06-delete-people-id-positive_data_acceptance.sh
# Operation : DELETE /people/{id}
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 11
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/people/262cfa10-14fe-0e98-8330-e9279ab64cd9?soft_delete=false' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
