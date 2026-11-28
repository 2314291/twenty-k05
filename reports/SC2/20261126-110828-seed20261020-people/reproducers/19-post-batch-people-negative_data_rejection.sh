#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 19-post-batch-people-negative_data_rejection.sh
# Operation : POST /batch/people
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 16
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became null)
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/batch/people?upsert=null&depth=0' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '[]'
