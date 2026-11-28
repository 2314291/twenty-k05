#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 26-patch-companies-response_schema_conformance.sh
# Operation : PATCH /companies
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 150
# null is not of type "string"
# 
# Validated against the response schema for status code 200.
# 
# Schema at /components/schemas/CompanyForResponse/properties/deletedAt:
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
  'http://localhost:3001/rest/companies?jg%C2%B2p%17%24%C2%84%C2%A5%7BK%C2%BA%C3%BD5=&%13%3B=259&%13%3B=null&%1C%C2%90+%F2%88%A4%AC%F3%A1%95%B8%1A%C2%B1%5C%C2%B1%C3%8B%C3%B4%C2%A2f%2C%2A9%C2%9B%C3%93w%C2%A1%C3%8A%3D=none&%1C%C2%90+%F2%88%A4%AC%F3%A1%95%B8%1A%C2%B1%5C%C2%B1%C3%8B%C3%B4%C2%A2f%2C%2A9%C2%9B%C3%93w%C2%A1%C3%8A%3D=%C2%A0%C2%B3%F3%80%89%B5%C3%A4&=null&depth=1&%C3%BF=none&%C3%BF=%C2%A0%C2%B3%F3%80%89%B5%C3%A4&filter=and%28createdAt%5Bgte%5D%3A%222026-11-28T05%3A07%3A39.000Z%22%2CcreatedAt%5Bgte%5D%3A%222026-11-28T05%3A07%3A39.000Z%22%29' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"address": {"addressStreet2": "", "addressCountry": "", "addressCity": ""}, "position": 0.0, "updatedBy": {}}'
