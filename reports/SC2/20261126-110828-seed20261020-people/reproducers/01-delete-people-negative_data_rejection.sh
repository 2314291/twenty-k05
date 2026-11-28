#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 01-delete-people-negative_data_rejection.sh
# Operation : DELETE /people
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 13
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string)
# Còn 2 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/people?soft_delete=&filter=createdAt%5Bgte%5D%3A%222026-11-26T04%3A09%3A04.000Z%22' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
