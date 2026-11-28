#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 50-post-batch-companies-response_schema_conformance.sh
# Operation : POST /batch/companies
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 12
# "" is not of type "integer"
# 
# Validated against the response schema for status code 201.
# 
# Schema at /components/schemas/CompanyForResponse/properties/name:
# 
#     {
#         "type": "integer",
#         "x-k05-red-case": "was {\"type\": \"string\", \"description\": \"The comp...
#     }
# 
# Value:
# 
#     ""

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/batch/companies?depth=0&fields=id%2Cname&upsert=true' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '[{"name": "", "domainName": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "address": {"addressStreet1": "", "addressStreet2": "", "addressCity": "", "addressPostcode": "", "addressState": "", "addressCountry": "", "addressLat": 0, "addressLng": 0}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "annualRevenue": {"amountMicros": 0, "currencyCode": ""}, "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "accountOwnerId": null}]'
