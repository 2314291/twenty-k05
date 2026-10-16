#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 15-get-companies-groupby-unsupported_method.sh
# Operation : GET /companies/groupBy
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 6
# Unsupported method TRACE returned 404, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X TRACE \
  'http://localhost:3001/rest/companies/groupBy?group_by=%5B%7B%22updatedAt%22%3A+true%7D%5D&filter=createdAt%5Bgte%5D%3A%222023-01-01%22&order_by=createdAt&limit=60&view_id=e3e70682-c209-1cac-a29f-6fbed82c07cd&aggregate=%5B%22countNotEmptyId%22%5D&include_records_sample=true&order_by_for_records=createdAt' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
