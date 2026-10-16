#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 24-patch-companies-merge-missing_required_header.sh
# Operation : PATCH /companies/merge
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/merge?depth=0&fields=id%2Cname' \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["9073f47e-cef7-4a46-adf6-92aac3cd90e0"], "conflictPriorityIndex": 0, "dryRun": false}'
