#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 07-delete-companies-id-status_code_conformance.sh
# Operation : DELETE /companies/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 30
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/companies/4cf549dc-a9f0-c04e-fb74-70baf9f238a9?soft_delete=true'
