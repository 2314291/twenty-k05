#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 39-patch-companies-id-response_schema_conformance.sh
# Operation : PATCH /companies/{id}
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 170
# null is not of type "string"
# 
# Validated against the response schema for status code 200.
# 
# Schema at /components/schemas/CompanyForResponse/properties/deletedAt:
# 
#     {
#         "type": "string",
#         "format": "date-time",
#         "description": "Date when the record was deleted"
#     }
# 
# Value:
# 
#     null

curl -sS -i \
  -X PATCH \
  http://localhost:3001/rest/companies/45cafa5c-1aae-4953-8712-8df00e3218cb \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
