#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 05-delete-tasks-id-positive_data_acceptance.sh
# Operation : DELETE /tasks/{id}
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 15
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/tasks/d8ce1ef0-dd5f-c5f1-2c52-c16613f9b8e1?soft_delete=false' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
