#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 04-delete-notes-status_code_conformance.sh
# Operation : DELETE /notes
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/notes?filter=and%28createdAt%5Bgte%5D%3A%222023-01-01%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T08%3A37%3A54.000Z%22%29&soft_delete=true'
