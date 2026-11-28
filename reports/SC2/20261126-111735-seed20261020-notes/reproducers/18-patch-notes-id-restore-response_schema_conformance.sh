#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 18-patch-notes-id-restore-response_schema_conformance.sh
# Operation : PATCH /notes/{id}/restore
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 90
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
  'http://localhost:3001/rest/notes/eac1899a-98cf-4518-93b5-8cca8c132566/restore?%C3%B97=&%C3%B97=%F1%8E%88%8D&%C3%B97=COM1&.%F1%BB%83%93%C3%A8%C3%BF%C3%B6%C3%A3%28%C3%84=null&%29=%C3%8F%F2%A6%88%AD%C2%80%F1%B6%BC%9F%C3%B6%23&%29=%19U%F3%94%A6%BE&%29=%C3%A2&%C3%8E%C3%9C%C3%95%08%5B=&%C3%8E%C3%9C%C3%95%08%5B=%C2%A7%C3%8C%C2%85t%C3%A3%C2%922%C3%9A%C3%98%C2%B6%C3%B7%C3%A3K%C2%AD%F2%B6%8B%A7%F3%AB%87%93%C3%B9&%C3%8E%C3%9C%C3%95%08%5B=COM1' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
