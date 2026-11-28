#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 49-post-notes-missing_required_header.sh
# Operation : POST /notes
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/notes?depth=0&fields=id%2Cname&upsert=true' \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
