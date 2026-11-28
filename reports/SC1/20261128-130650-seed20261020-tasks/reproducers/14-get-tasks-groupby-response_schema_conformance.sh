#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 14-get-tasks-groupby-response_schema_conformance.sh
# Operation : GET /tasks/groupBy
# Check     : response_schema_conformance  (JsonSchemaError, mức high)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 10
# [{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:19:11.132Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:19:11.295Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:54.509Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:54.595Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:55.729Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:55.793Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:56.914Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:56.996Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:58.135Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:58.320Z"],"records":[]},{"countNotEmptyId":"1","groupByDimensionValues":["2026-10-19T13:22:58.728Z"],"records":[]},{"countNotEmptyId":"30","groupByDimensionValues":["2026-11-28T06:08:24.055Z"],"records":[]}] is not of type "object"
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
#                     "tasksGroupBy": {
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
#             "countNotEmptyId": "1",
#             "groupByDimensionValues": [
#                 "2026-10-19T13:19:11.132Z"
#             ],
#             "records": []
#         },
#         {
#             "countNotEmptyId": "1",
#             "groupByDimensionValues": [
#                 "2026-10-19T13:19:11.295Z"
#             ],
#             "records": []
#         },
#         {
#             "countNotEmptyId": "1",
#             "groupByDimensionValues": [
#                 "2026-10-19T13:22:54.509Z"
#         // Output truncated...
#     ]

curl -sS -i \
  -X GET \
  'http://localhost:3001/rest/tasks/groupBy?group_by=%5B%7B%22updatedAt%22%3A+true%7D%5D&filter=createdAt%5Bgte%5D%3A%222023-01-01%22&limit=60&aggregate=%5B%22countNotEmptyId%22%5D&include_records_sample=true' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
