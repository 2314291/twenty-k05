#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 02-delete-tasks-positive_data_acceptance.sh
# Operation : DELETE /tasks
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 11
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/tasks?soft_delete=false&filter=and%28name%5Blike%5D%3A%22%25value%25%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T06%3A08%3A25.000Z%22%29' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
