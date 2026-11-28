#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 46-patch-companies-id-restore-unsupported_method.sh
# Operation : PATCH /companies/{id}/restore
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 4
# Unsupported method PUT returned 400, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X PUT \
  'http://localhost:3001/rest/companies/04f75f30-de31-4f4e-865b-439816f73d22/restore?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
