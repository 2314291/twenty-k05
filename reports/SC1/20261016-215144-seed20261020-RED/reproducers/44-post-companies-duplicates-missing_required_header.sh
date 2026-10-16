#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 44-post-companies-duplicates-missing_required_header.sh
# Operation : POST /companies/duplicates
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/companies/duplicates?depth=0&fields=id%2Cname' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["3c8fad72-391d-4e91-9dae-b4536b9f82b7"]}'
