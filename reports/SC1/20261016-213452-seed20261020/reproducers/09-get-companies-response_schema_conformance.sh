#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 09-get-companies-response_schema_conformance.sh
# Operation : GET /companies
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 62
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
  'http://localhost:3001/rest/companies?depth=0&ending_before=' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
