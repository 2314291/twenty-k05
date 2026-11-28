#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 44-patch-people-id-restore-status_code_conformance.sh
# Operation : PATCH /people/{id}/restore
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: examples   Số lần gặp: 4
# Received: 404
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/people/736ae8fb-d1c4-43d7-a9f2-d7560e2b0950/restore?depth=1&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
