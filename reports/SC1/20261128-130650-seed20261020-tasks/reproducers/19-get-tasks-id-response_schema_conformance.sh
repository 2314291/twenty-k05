#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 19-get-tasks-id-response_schema_conformance.sh
# Operation : GET /tasks/{id}
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 132
# null is not of type "string"
# 
# Validated against the response schema for status code 200.
# 
# Schema at /components/schemas/TaskForResponse/properties/deletedAt:
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
  -X GET \
  'http://localhost:3001/rest/tasks/af2acf4c-6f2f-4d4d-a1d4-7a7e84f30841?depth=0' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
