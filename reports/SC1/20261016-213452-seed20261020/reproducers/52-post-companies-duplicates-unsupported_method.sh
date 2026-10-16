#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 52-post-companies-duplicates-unsupported_method.sh
# Operation : POST /companies/duplicates
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 6
# Unsupported method TRACE returned 404, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X TRACE \
  'http://localhost:3001/rest/companies/duplicates?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["3c8fad72-391d-4e91-9dae-b4536b9f82b7"]}'
