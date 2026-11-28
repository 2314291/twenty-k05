#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 19-get-people-id-positive_data_acceptance.sh
# Operation : GET /people/{id}
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 7
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/people/f949cb06-4d69-4e6b-b44b-063dc6eb2637?depth=1&fields=' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
