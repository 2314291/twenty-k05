#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 16-patch-notes-id-restore-response_schema_conformance.sh
# Operation : PATCH /notes/{id}/restore
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 87
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
  'http://localhost:3001/rest/notes/a0a866bd-e041-4b32-b9a5-103d1f273380/restore?%C2%99%F3%BF%89%B1=%C2%99I%F1%9B%87%85%C2%AAe%C3%BC&%C2%99%F3%BF%89%B1=%C3%B5D%F4%8D%AA%B2r' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
