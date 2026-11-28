#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 16-patch-companies-id-restore-response_schema_conformance.sh
# Operation : PATCH /companies/{id}/restore
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: fuzzing   Số lần gặp: 216
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
  'http://localhost:3001/rest/companies/baa94f2a-aed1-4079-a547-08ccb702a5de/restore?%C2%A5=false&%E0%A4%AA%E0%A4%A8%E0%A5%8D%E0%A4%B9+%E0%A4%AA%E0%A4%A8%E0%A5%8D%E0%A4%B9+%E0%A4%A4%E0%A5%8D%E0%A4%B0+%E0%A4%B0%E0%A5%8D%E0%A4%9A+%E0%A4%95%E0%A5%83%E0%A4%95%E0%A5%83+%E0%A4%A1%E0%A5%8D%E0%A4%A1+%E0%A4%A8%E0%A5%8D%E0%A4%B9%E0%A5%83%E0%A5%87+%D8%A5%D9%84%D8%A7+%D8%A8%D8%B3%D9%85+%D8%A7%D9%84%D9%84%D9%87=%F0%AE%B0%A5%C3%87&%E0%A4%AA%E0%A4%A8%E0%A5%8D%E0%A4%B9+%E0%A4%AA%E0%A4%A8%E0%A5%8D%E0%A4%B9+%E0%A4%A4%E0%A5%8D%E0%A4%B0+%E0%A4%B0%E0%A5%8D%E0%A4%9A+%E0%A4%95%E0%A5%83%E0%A4%95%E0%A5%83+%E0%A4%A1%E0%A5%8D%E0%A4%A1+%E0%A4%A8%E0%A5%8D%E0%A4%B9%E0%A5%83%E0%A5%87+%D8%A5%D9%84%D8%A7+%D8%A8%D8%B3%D9%85+%D8%A7%D9%84%D9%84%D9%87=&%E0%A4%AA%E0%A4%A8%E0%A5%8D%E0%A4%B9+%E0%A4%AA%E0%A4%A8%E0%A5%8D%E0%A4%B9+%E0%A4%A4%E0%A5%8D%E0%A4%B0+%E0%A4%B0%E0%A5%8D%E0%A4%9A+%E0%A4%95%E0%A5%83%E0%A4%95%E0%A5%83+%E0%A4%A1%E0%A5%8D%E0%A4%A1+%E0%A4%A8%E0%A5%8D%E0%A4%B9%E0%A5%83%E0%A5%87+%D8%A5%D9%84%D8%A7+%D8%A8%D8%B3%D9%85+%D8%A7%D9%84%D9%84%D9%87=9496&W%24%C2%A5%C2%A4%C2%86%F4%8F%B7%B5y%1B=%03%3E&W%24%C2%A5%C2%A4%C2%86%F4%8F%B7%B5y%1B=&W%24%C2%A5%C2%A4%C2%86%F4%8F%B7%B5y%1B=%02%E3%9C%8E%C2%92%EC%90%9C%C3%BA&=null&=false&%C2%A5%C3%A8%C3%9A=0&%C2%A5%C3%A8%C3%9A=%F1%9A%88%B9%05%1B%F3%94%9E%B2&%C2%A5%C3%A8%C3%9A=%7F%F3%98%BD%84%C2%AAz3' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
