#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 07-delete-companies-id-status_code_conformance.sh
# Operation : DELETE /companies/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 35
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/companies/311544b2-5fa2-4990-86b8-3674f1050fcf?soft_delete=true'
