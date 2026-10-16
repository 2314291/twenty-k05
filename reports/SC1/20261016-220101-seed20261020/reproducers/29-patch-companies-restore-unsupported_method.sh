#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 29-patch-companies-restore-unsupported_method.sh
# Operation : PATCH /companies/restore
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 6
# Unsupported method TRACE returned 404, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X TRACE \
  'http://localhost:3001/rest/companies/restore?filter=createdAt%5Bgte%5D%3A%222023-01-01%22&depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
