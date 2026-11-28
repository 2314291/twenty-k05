#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 54-post-people-response_schema_conformance.sh
# Operation : POST /people
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: examples   Số lần gặp: 3
# null is not of type "string"
# 
# Validated against the response schema for status code 201.
# 
# Schema at /components/schemas/PersonForResponse/properties/companyId:
# 
#     {
#         "type": "string",
#         "format": "uuid"
#     }
# 
# Value:
# 
#     null

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/people?depth=1&upsert=false&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
