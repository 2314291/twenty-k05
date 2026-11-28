#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 01-delete-notes-negative_data_rejection.sh
# Operation : DELETE /notes
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 31
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer)

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/notes?soft_delete=-531979&filter=createdAt%5Bgte%5D%3A%222026-11-28T13%3A23%3A21.000Z%22' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
