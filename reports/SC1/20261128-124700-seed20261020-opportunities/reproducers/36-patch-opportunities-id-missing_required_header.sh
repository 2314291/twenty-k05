#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 36-patch-opportunities-id-missing_required_header.sh
# Operation : PATCH /opportunities/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 400 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/opportunities/6e660081-566a-4f97-a378-38e9c3654335?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": "", "amount": {"amountMicros": 0, "currencyCode": ""}, "closeDate": "2000-01-01T00:00:00Z", "stage": "NEW", "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": "bd76b6c8-6c0f-4ad7-81f8-49d0825e6bf1", "pointOfContactId": "0fbd6155-8088-4005-982c-1c473cb19d57", "ownerId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}'
