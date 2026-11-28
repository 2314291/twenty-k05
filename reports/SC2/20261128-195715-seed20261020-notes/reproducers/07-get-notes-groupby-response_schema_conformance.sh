#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 07-get-notes-groupby-response_schema_conformance.sh
# Operation : GET /notes/groupBy
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 10
# [{"groupByDimensionValues":["2026-11-28T12:58:46.048Z"]}] is not of type "object"
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
#                 "2026-11-28T12:58:46.048Z"
#             ]
#         }
#     ]

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/notes/groupBy?group_by=%5B%7B%22updatedAt%22%3A+true%7D%5D&limit=0.5&view_id=0&include_records_sample=null&include_records_sample=null' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
