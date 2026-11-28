#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 20-post-batch-people-response_schema_conformance.sh
# Operation : POST /batch/people
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 5
# null is not of type "string"
# 
# Validated against the response schema for status code 201.
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
  -X POST \
  'http://localhost:3001/rest/batch/people?upsert=null&depth=0' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '[{}]'
