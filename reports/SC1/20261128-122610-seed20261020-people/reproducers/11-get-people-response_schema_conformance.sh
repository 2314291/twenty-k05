#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 11-get-people-response_schema_conformance.sh
# Operation : GET /people
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: examples   Số lần gặp: 190
# {"accountOwnerId":null,"address":{"addressCity":"Ho Chi Minh","addressCountry":"","addressLat":null,"addressLng":null,"addressPostcode":"","addressState":"","addressStreet1":"","addressStreet2":""},"annualRevenue":{"amountMicros":175000000,"currencyCode":"USD"},"createdAt":"2026-11-28T05:27:40.116Z","createdBy":{"context":{},"name":"k05-tien-2","source":"API","workspaceMemberId":null},"deletedAt":null,"domainName":{"primaryLinkLabel":"","primaryLinkUrl":"k05-company-024.example.com","secondaryLinks":[]},"id":"329b243a-7d59-473c-ba0a-28398bef394e","linkedinLink":{"primaryLinkLabel":"","primaryLinkUrl":"","secondaryLinks":[]},"name":"K05-Company-024","position":-289,"searchVector":"'024':4 'company':3 'k05':2 'k05-company':1 'k05-company-024.example.com':5","updatedAt":"2026-11-28T05:27:40.116Z","updatedBy":{"context":{},"name":"k05-tien-2","source":"API","workspaceMemberId":null}} is not valid under any of the schemas listed in the 'oneOf' keyword
# 
# Validated against the response schema for status code 200.
# 
# Schema at /components/schemas/PersonForResponse/properties/company:
# 
#     {
#         "oneOf": [
#             {
#                 "$ref": "#/components/schemas/CompanyForResponse"
#             }
#         ],
#         "type": "object",
#         "description": "Contact's company"
#     }
# 
# Value:
# 
#     {
#         "accountOwnerId": null,
#         "address": {
#             "addressCity": "Ho Chi Minh",
#             "addressCountry": "",
#             "addressLat": null,
#             "addressLng": null,
#             "addressPostcode": "",
#             "addressState": "",
#             "addressStreet1": "",
#             "addressStreet2": ""
#         },
#         "annualRevenue": {
#             "amountMicros": 175000000,
#             "currencyCode": "USD"
#         },
#         "createdAt": "2026-11-28T05:27:40.116Z",
#         "createdBy": {
#             "context": {},
#         // Output truncated...
#     }
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/people?limit=60&depth=1&order_by=id%5BAscNullsFirst%5D%2CcreatedAt%5BDescNullsLast%5D&filter=or%28createdAt%5Bgte%5D%3A%222024-01-01%22%2CcreatedAt%5Blte%5D%3A%222023-01-01%22%2Cnot%28id%5Bis%5D%3ANULL%29%29&fields=id%2Cname%2Cemails%2Ccompany' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
