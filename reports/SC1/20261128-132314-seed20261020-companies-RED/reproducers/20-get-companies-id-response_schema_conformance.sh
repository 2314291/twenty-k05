#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 20-get-companies-id-response_schema_conformance.sh
# Operation : GET /companies/{id}
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 267
# "K05-Company-008" is not of type "integer"
# 
# Validated against the response schema for status code 200.
# 
# Schema at /components/schemas/CompanyForResponse/properties/name:
# 
#     {
#         "type": "integer",
#         "x-k05-red-case": "was {\"type\": \"string\", \"description\": \"The comp...
#     }
# 
# Value:
# 
#     "K05-Company-008"
# Còn 7 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies/99429a49-dedc-4cae-a9ab-980e84add110?fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
