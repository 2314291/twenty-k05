#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 05-delete-companies-id-status_code_conformance.sh
# Operation : DELETE /companies/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 51
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/companies/736ae8fb-d1c4-43d7-a9f2-d7560e2b0950?soft_delete=true'
