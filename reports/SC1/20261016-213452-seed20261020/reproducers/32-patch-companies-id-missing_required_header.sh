#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 32-patch-companies-id-missing_required_header.sh
# Operation : PATCH /companies/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/companies/736ae8fb-d1c4-43d7-a9f2-d7560e2b0950?depth=0&fields=id%2Cname' \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": "", "domainName": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "address": {"addressStreet1": "", "addressStreet2": "", "addressCity": "", "addressPostcode": "", "addressState": "", "addressCountry": "", "addressLat": 0, "addressLng": 0}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "annualRevenue": {"amountMicros": 0, "currencyCode": ""}, "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "accountOwnerId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}'
