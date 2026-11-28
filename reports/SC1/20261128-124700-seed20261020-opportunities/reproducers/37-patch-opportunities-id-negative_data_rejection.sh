#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 37-patch-opportunities-id-negative_data_rejection.sh
# Operation : PATCH /opportunities/{id}
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: in body - ownerId: Incorrect type

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/opportunities/e8245c4d-8269-4fb7-a56b-fd42a2c8d884?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": "", "amount": {"amountMicros": 0, "currencyCode": ""}, "closeDate": "2000-01-01T00:00:00Z", "stage": "NEW", "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": "bd76b6c8-6c0f-4ad7-81f8-49d0825e6bf1", "pointOfContactId": "0fbd6155-8088-4005-982c-1c473cb19d57", "ownerId": null}'
