#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 28-patch-companies-restore-status_code_conformance.sh
# Operation : PATCH /companies/restore
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/restore?filter=createdAt%5Bgte%5D%3A%222023-01-01%22&depth=0&fields=id%2Cname'
