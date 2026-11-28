#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 01-delete-notes-missing_required_header.sh
# Operation : DELETE /notes
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/notes?filter=and%28createdAt%5Bgte%5D%3A%222023-01-01%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T06%3A02%3A23.000Z%22%29&soft_delete=true'
