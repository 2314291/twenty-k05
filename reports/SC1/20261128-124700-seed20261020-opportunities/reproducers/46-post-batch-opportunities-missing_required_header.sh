#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 46-post-batch-opportunities-missing_required_header.sh
# Operation : POST /batch/opportunities
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/batch/opportunities?depth=0&fields=id%2Cname&upsert=true' \
  -H 'Content-Type: application/json' \
  --data-binary '[{"name": "", "amount": {"amountMicros": 0, "currencyCode": ""}, "closeDate": "2000-01-01T00:00:00Z", "stage": "NEW", "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": "e3e70682-c209-1cac-a29f-6fbed82c07cd", "pointOfContactId": "e3e70682-c209-1cac-a29f-6fbed82c07cd", "ownerId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}]'
