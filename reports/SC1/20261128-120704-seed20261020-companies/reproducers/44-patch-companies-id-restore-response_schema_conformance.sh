#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 44-patch-companies-id-restore-response_schema_conformance.sh
# Operation : PATCH /companies/{id}/restore
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 197
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
  'http://localhost:3001/rest/companies/b83d077c-6139-4bfc-b777-e8fa28233c30/restore?depth=1&x-schemathesis-unknown-property=42' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
