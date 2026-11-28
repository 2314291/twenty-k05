#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 42-patch-people-id-restore-positive_data_acceptance.sh
# Operation : PATCH /people/{id}/restore
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 5
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/people/568d8626-76ab-4109-9b0f-2de08a140a60/restore?depth=0&fields=' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
