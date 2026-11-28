#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 18-get-companies-id-missing_required_header.sh
# Operation : GET /companies/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 200 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies/99429a49-dedc-4cae-a9ab-980e84add110?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
