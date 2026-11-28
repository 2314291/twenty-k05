#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 21-get-tasks-id-unsupported_method.sh
# Operation : GET /tasks/{id}
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 2
# Unsupported method PUT returned 400, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X PUT \
  'http://localhost:3001/rest/tasks/af2acf4c-6f2f-4d4d-a1d4-7a7e84f30841?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
