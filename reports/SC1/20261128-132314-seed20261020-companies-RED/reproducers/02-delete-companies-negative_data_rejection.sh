#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 02-delete-companies-negative_data_rejection.sh
# Operation : DELETE /companies
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 1
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer)

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/companies?soft_delete=-15406416&filter=and%28createdAt%5Bgte%5D%3A%222026-11-28T06%3A24%3A47.000Z%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T06%3A24%3A47.000Z%22%29' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
