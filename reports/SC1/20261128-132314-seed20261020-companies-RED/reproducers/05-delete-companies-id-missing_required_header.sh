#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 05-delete-companies-id-missing_required_header.sh
# Operation : DELETE /companies/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/companies/311544b2-5fa2-4990-86b8-3674f1050fcf?soft_delete=true'
