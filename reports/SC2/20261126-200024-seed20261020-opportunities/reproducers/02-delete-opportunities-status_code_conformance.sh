#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 02-delete-opportunities-status_code_conformance.sh
# Operation : DELETE /opportunities
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/opportunities?soft_delete=2&filter=createdAt%5Bgte%5D%3A%222026-11-26T13%3A01%3A55.000Z%22'
