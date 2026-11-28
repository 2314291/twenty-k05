#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 25-patch-notes-response_schema_conformance.sh
# Operation : PATCH /notes
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 96
# null is not of type "string"
# 
# Validated against the response schema for status code 200.
# 
# Schema at /components/schemas/NoteForResponse/properties/deletedAt:
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
  'http://localhost:3001/rest/notes?filter=and%28createdAt%5Bgte%5D%3A%222026-11-28T08%3A37%3A54.000Z%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T08%3A37%3A54.000Z%22%29' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
