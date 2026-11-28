#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 49-post-batch-opportunities-response_schema_conformance.sh
# Operation : POST /batch/opportunities
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 9
# null is not of type "string"
# 
# Validated against the response schema for status code 201.
# 
# Schema at /components/schemas/OpportunityForResponse/properties/deletedAt:
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
  http://localhost:3001/rest/batch/opportunities \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '[{"stage": "NEW"}]'
