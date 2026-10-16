#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 20-patch-companies-response_schema_conformance.sh
# Operation : PATCH /companies
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: examples   Số lần gặp: 2
# "" is not of type "integer"
# 
# Validated against the response schema for status code 200.
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
  -X PATCH \
  'http://localhost:3001/rest/companies?depth=1&fields=id%2Cname&filter=or%28createdAt%5Bgte%5D%3A%222024-01-01%22%2CcreatedAt%5Blte%5D%3A%222023-01-01%22%2Cnot%28id%5Bis%5D%3ANULL%29%29' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
