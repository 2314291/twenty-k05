#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 03-delete-tasks-id-negative_data_rejection.sh
# Operation : DELETE /tasks/{id}
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 2
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer)

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/tasks/ab187122-7370-4178-a0a5-313a90ef891a?soft_delete=-36213' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
