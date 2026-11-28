#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 15-patch-people-id-response_schema_conformance.sh
# Operation : PATCH /people/{id}
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 104
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

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/people/a8fd3d1e-bffc-4ad7-8aa6-0f6d65bdd622?depth=0&=null' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
