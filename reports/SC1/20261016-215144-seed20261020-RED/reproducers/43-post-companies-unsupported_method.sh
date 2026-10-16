#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 43-post-companies-unsupported_method.sh
# Operation : POST /companies
# Check     : unsupported_method  (UnsupportedMethodResponse, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 3
# Unsupported method TRACE returned 404, expected 405 Method Not Allowed
# 
# Return 405 for methods not listed in the OpenAPI spec

curl -sS -i \
  -X TRACE \
  'http://localhost:3001/rest/companies?depth=0&fields=id%2Cname&upsert=true' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": "", "domainName": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "address": {"addressStreet1": "", "addressStreet2": "", "addressCity": "", "addressPostcode": "", "addressState": "", "addressCountry": "", "addressLat": 0, "addressLng": 0}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "annualRevenue": {"amountMicros": 0, "currencyCode": ""}, "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "accountOwnerId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}'
