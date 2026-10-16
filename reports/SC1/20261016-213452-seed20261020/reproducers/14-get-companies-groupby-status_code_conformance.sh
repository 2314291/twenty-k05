#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 14-get-companies-groupby-status_code_conformance.sh
# Operation : GET /companies/groupBy
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 117
# Received: 400
# Documented: 200

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies/groupBy?limit=60&include_records_sample=false&group_by=%5B%7B%22updatedAt%22%3A+true%7D%5D&filter=name%5Blike%5D%3A%22%25value%25%22&order_by=id%5BAscNullsFirst%5D%2CcreatedAt%5BDescNullsLast%5D&aggregate=%5B%22countNotEmptyId%22%2C+%22sumAmount%22%5D&order_by_for_records=createdAt' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
