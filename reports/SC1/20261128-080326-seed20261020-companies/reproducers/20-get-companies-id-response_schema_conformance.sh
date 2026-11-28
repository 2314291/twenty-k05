#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 20-get-companies-id-response_schema_conformance.sh
# Operation : GET /companies/{id}
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 190
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
  -X GET \
  'http://localhost:3001/rest/companies/980a1247-dcaf-4f3c-9af1-5603c987e8eb?depth=0' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
