#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 09-get-notes-negative_data_rejection.sh
# Operation : GET /notes
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 2
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `limit` in query - limit: Value greater than maximum
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/notes?limit=201' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
