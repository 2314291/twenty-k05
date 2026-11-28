#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 39-patch-notes-id-restore-missing_required_header.sh
# Operation : PATCH /notes/{id}/restore
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 400 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/notes/8d38c373-a1a0-4337-bbaf-6f0dd56c04ae/restore?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
