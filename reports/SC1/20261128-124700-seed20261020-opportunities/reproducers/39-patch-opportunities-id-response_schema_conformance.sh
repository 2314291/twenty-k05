#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 39-patch-opportunities-id-response_schema_conformance.sh
# Operation : PATCH /opportunities/{id}
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 164
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

curl -sS -i \
  -X PATCH \
  http://localhost:3001/rest/opportunities/e8245c4d-8269-4fb7-a56b-fd42a2c8d884 \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"companyId": "f7428305-e645-4148-8cea-b38ab4449e85", "pointOfContactId": "11d824ba-87ff-46ed-b5ab-201b1e7a4cef"}'
