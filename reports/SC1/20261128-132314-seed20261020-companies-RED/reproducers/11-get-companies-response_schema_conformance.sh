#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 11-get-companies-response_schema_conformance.sh
# Operation : GET /companies
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: examples   Số lần gặp: 297
# "K05-Company-029" is not of type "integer"
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
#     "K05-Company-029"
# Còn 2 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/companies?limit=60&depth=1&order_by=createdAt&filter=createdAt%5Bgte%5D%3A%222023-01-01%22&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
