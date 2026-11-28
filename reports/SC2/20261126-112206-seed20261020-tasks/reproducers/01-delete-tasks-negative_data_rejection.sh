#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 01-delete-tasks-negative_data_rejection.sh
# Operation : DELETE /tasks
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 32
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string)
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/tasks?soft_delete=%F3%BE%9B%B2%C3%98%C2%84%C2%8D%C3%BE8%C3%92%C2%B2%C2%A5i%00%11%C3%BA%C2%9B%C2%89%F2%AE%90%97k&filter=createdAt%5Bgte%5D%3A%222026-11-26T04%3A23%3A37.000Z%22' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
