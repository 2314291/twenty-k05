#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 36-patch-companies-id-restore-unsupported_method.sh
# Operation : PATCH /companies/{id}/restore
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 4
# Unsupported method PUT returned 400, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X PUT \
  'http://localhost:3001/rest/companies/736ae8fb-d1c4-43d7-a9f2-d7560e2b0950/restore?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
