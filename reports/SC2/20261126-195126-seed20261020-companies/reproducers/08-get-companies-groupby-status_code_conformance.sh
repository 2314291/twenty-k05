#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 08-get-companies-groupby-status_code_conformance.sh
# Operation : GET /companies/groupBy
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 79
# Received: 400
# Documented: 200

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies/groupBy?group_by=&view_id=e3e70682-c209-1cac-a29f-6fbed82c07cd&x-schemathesis-unknown-property=42' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
