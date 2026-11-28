#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 15-patch-opportunities-id-restore-response_schema_conformance.sh
# Operation : PATCH /opportunities/{id}/restore
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 116
# null is not of type "string"
# 
# Validated against the response schema for status code 200.
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
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X PATCH \
  http://localhost:3001/rest/opportunities/961712c2-0ce5-4ed4-b7c9-bc42fc678577/restore \
  -H "Authorization: Bearer $TWENTY_API_KEY"
