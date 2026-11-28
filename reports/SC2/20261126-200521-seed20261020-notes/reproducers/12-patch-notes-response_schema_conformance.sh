#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 12-patch-notes-response_schema_conformance.sh
# Operation : PATCH /notes
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 4
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
  'http://localhost:3001/rest/notes?x-schemathesis-unknown-property=42&filter=createdAt%5Bgte%5D%3A%222026-11-26T13%3A06%3A52.000Z%22' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{}'
