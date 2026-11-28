#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 14-patch-opportunities-id-status_code_conformance.sh
# Operation : PATCH /opportunities/{id}
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 2
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/opportunities/0?depth=0.5' \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": "", "amount": {"amountMicros": 0, "currencyCode": ""}, "closeDate": "2000-01-01T00:00:00Z", "stage": "NEW", "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": "e3e70682-c209-1cac-a29f-6fbed82c07cd", "pointOfContactId": "e3e70682-c209-1cac-a29f-6fbed82c07cd", "ownerId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}'
