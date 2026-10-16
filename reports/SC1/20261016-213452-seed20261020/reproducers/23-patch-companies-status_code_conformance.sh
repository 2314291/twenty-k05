#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 23-patch-companies-status_code_conformance.sh
# Operation : PATCH /companies
# Check     : status_code_conformance  (UndefinedStatusCode, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Received: 403
# Documented: 200, 400, 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies?depth=0&fields=id%2Cname&filter=createdAt%5Bgte%5D%3A%222023-01-01%22' \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": "", "domainName": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "address": {"addressStreet1": "", "addressStreet2": "", "addressCity": "", "addressPostcode": "", "addressState": "", "addressCountry": "", "addressLat": 0, "addressLng": 0}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "annualRevenue": {"amountMicros": 0, "currencyCode": ""}, "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "accountOwnerId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}'
