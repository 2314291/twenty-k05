#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 41-post-companies-response_schema_conformance.sh
# Operation : POST /companies
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: examples   Số lần gặp: 1
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
  'http://localhost:3001/rest/companies?depth=1&upsert=false&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
