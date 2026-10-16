#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 19-patch-companies-negative_data_rejection.sh
# Operation : PATCH /companies
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 2
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: in body - accountOwnerId: Incorrect type
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies?depth=0&fields=id%2Cname&filter=createdAt%5Bgte%5D%3A%222023-01-01%22' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": "", "domainName": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "address": {"addressStreet1": "", "addressStreet2": "", "addressCity": "", "addressPostcode": "", "addressState": "", "addressCountry": "", "addressLat": 0, "addressLng": 0}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "annualRevenue": {"amountMicros": 0, "currencyCode": ""}, "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "accountOwnerId": null}'
