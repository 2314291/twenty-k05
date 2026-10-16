#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 27-patch-companies-merge-unsupported_method.sh
# Operation : PATCH /companies/merge
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 6
# Unsupported method TRACE returned 404, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X TRACE \
  'http://localhost:3001/rest/companies/merge?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["9073f47e-cef7-4a46-adf6-92aac3cd90e0"], "conflictPriorityIndex": 0, "dryRun": false}'
