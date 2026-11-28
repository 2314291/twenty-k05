#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 06-get-people-response_schema_conformance.sh
# Operation : GET /people
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 162
# null is not of type "string"
# 
# Validated against the response schema for status code 200.
# 
# Schema at /components/schemas/PersonForResponse/properties/deletedAt:
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
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/people?limit=60&x-schemathesis-unknown-property=42' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
