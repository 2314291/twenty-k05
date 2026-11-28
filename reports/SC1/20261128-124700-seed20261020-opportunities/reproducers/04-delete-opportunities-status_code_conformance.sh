#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 04-delete-opportunities-status_code_conformance.sh
# Operation : DELETE /opportunities
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/opportunities?filter=and%28createdAt%5Bgte%5D%3A%222023-01-01%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T05%3A48%3A35.000Z%22%29&soft_delete=true'
