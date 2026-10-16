#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 34-patch-companies-id-restore-missing_required_header.sh
# Operation : PATCH /companies/{id}/restore
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/736ae8fb-d1c4-43d7-a9f2-d7560e2b0950/restore?depth=0&fields=id%2Cname'
