#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 05-delete-companies-id-missing_required_header.sh
# Operation : DELETE /companies/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/companies/e9061a45-6983-765c-faac-f4503bdbd65c?soft_delete=true'
