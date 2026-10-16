#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 09-get-companies-groupby-missing_required_header.sh
# Operation : GET /companies/groupBy
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies/groupBy?group_by=%5B%7B%22updatedAt%22%3A+true%7D%5D&filter=createdAt%5Bgte%5D%3A%222023-01-01%22&order_by=createdAt&limit=60&view_id=e3e70682-c209-1cac-a29f-6fbed82c07cd&aggregate=%5B%22countNotEmptyId%22%5D&include_records_sample=true&order_by_for_records=createdAt'
