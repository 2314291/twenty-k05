#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 50-post-batch-opportunities-status_code_conformance.sh
# Operation : POST /batch/opportunities
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 201, 400, 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/batch/opportunities?depth=0&fields=id%2Cname&upsert=true' \
  -H 'Content-Type: application/json' \
  --data-binary '[{"name": "", "amount": {"amountMicros": 0, "currencyCode": ""}, "closeDate": "2000-01-01T00:00:00Z", "stage": "NEW", "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": "e3e70682-c209-1cac-a29f-6fbed82c07cd", "pointOfContactId": "e3e70682-c209-1cac-a29f-6fbed82c07cd", "ownerId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}]'
