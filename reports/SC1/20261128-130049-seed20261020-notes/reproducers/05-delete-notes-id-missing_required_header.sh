#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 05-delete-notes-id-missing_required_header.sh
# Operation : DELETE /notes/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/notes/141a64fa-ebc8-0a8d-1b97-c064d560d1b6?soft_delete=true'
