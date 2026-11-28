#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 39-patch-people-id-response_schema_conformance.sh
# Operation : PATCH /people/{id}
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 133
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
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/people/bafc6f42-2c74-43d9-a387-c6d6b06fe027?depth=1&x-schemathesis-unknown-property=42' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": {"firstName": "", "lastName": ""}, "emails": {"primaryEmail": "", "additionalEmails": []}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "jobTitle": "", "phones": {"additionalPhones": [], "primaryPhoneCountryCode": "", "primaryPhoneCallingCode": "", "primaryPhoneNumber": ""}, "avatarUrl": "", "avatarFile": [], "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": "bd7b1b6e-1d4a-4787-a191-fda42d4e47b5"}'
