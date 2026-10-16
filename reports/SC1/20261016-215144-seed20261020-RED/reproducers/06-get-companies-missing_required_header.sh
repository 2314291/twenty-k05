#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 06-get-companies-missing_required_header.sh
# Operation : GET /companies
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies?order_by=createdAt&filter=createdAt%5Bgte%5D%3A%222023-01-01%22&limit=60&depth=0&fields=id%2Cname&starting_after=&ending_before='
