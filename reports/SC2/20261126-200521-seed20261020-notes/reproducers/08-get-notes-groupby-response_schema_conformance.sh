#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 08-get-notes-groupby-response_schema_conformance.sh
# Operation : GET /notes/groupBy
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 10
# [{"groupByDimensionValues":["2026-11-26T04:20:49.160Z"]},{"groupByDimensionValues":["2026-11-26T13:06:50.967Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.010Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.138Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.184Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.227Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.307Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.388Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.466Z"]},{"groupByDimensionValues":["2026-11-26T13:06:59.558Z"]}] is not of type "object"
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
#                     "notesGroupBy": {
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
#             "groupByDimensionValues": [
#                 "2026-11-26T04:20:49.160Z"
#             ]
#         },
#         {
#             "groupByDimensionValues": [
#                 "2026-11-26T13:06:50.967Z"
#             ]
#         },
#         {
#             "groupByDimensionValues": [
#                 "2026-11-26T13:06:59.010Z"
#             ]
#         },
#         {
#             "groupByDimensionValues": [
#                 "2026-11-26T13:06:59.138Z"
#         // Output truncated...
#     ]

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/notes/groupBy?group_by=%5B%7B%22updatedAt%22%3A+true%7D%5D&limit=0.5&view_id=0&include_records_sample=null&include_records_sample=null' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
