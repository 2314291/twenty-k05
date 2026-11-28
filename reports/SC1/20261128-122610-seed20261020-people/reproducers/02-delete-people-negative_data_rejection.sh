#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 02-delete-people-negative_data_rejection.sh
# Operation : DELETE /people
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 6
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became number)
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/people?filter=and%28createdAt%5Bgte%5D%3A%222026-11-28T05%3A27%3A43.000Z%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T05%3A27%3A43.000Z%22%29&soft_delete=5e-324' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
