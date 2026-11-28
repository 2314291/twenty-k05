#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 15-get-opportunities-groupby-response_schema_conformance.sh
# Operation : GET /opportunities/groupBy
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 10
# [{"countNotEmptyId":"31","groupByDimensionValues":["2026-11-28T05:48:40.342Z"],"records":[]}] is not of type "object"
# 
# Validated against the response schema for status code 200.
# 
# Schema:
# 
#     {
#         "type": "object",
#         "properties": {
#             "data": {
#                 "type": "object",
#                 "properties": {
#                     "opportunitiesGroupBy": {
#                         "type": "array",
#                         "items": {
#                             "type": "object",
#                             "properties": {
#                                 "groupByDimensionValues": {
#                                     "type": "array",
#                                     "description": "Array of values representing ...
#                                     "items": {
#                                         "type": "string"
#                                     }
#                                 },
#                                 "records": {
#         // Output truncated...
#     }
# 
# Value:
# 
#     [
#         {
#             "countNotEmptyId": "31",
#             "groupByDimensionValues": [
#                 "2026-11-28T05:48:40.342Z"
#             ],
#             "records": []
#         }
#     ]

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/opportunities/groupBy?group_by=%5B%7B%22updatedAt%22%3A+true%7D%5D&filter=createdAt%5Bgte%5D%3A%222023-01-01%22&limit=60&aggregate=%5B%22countNotEmptyId%22%5D&include_records_sample=true' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
