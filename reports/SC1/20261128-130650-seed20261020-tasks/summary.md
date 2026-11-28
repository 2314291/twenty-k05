# Thống kê lần chạy `20261128-130650-seed20261020-tasks`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T06:08:27.264221+00:00 |
| Thời gian chạy (giây) | 274.8 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1752 |
| Lỗi duy nhất | 58 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /tasks` | 77 | 49 | 28 | 61 | 16 | 0 | 12 | có |
| `DELETE /tasks/{id}` | 64 | 42 | 22 | 0 | 64 | 0 | 45 | có |
| `GET /tasks` | 114 | 57 | 57 | 38 | 76 | 0 | 73 | có |
| `GET /tasks/groupBy` | 136 | 79 | 57 | 12 | 124 | 0 | 132 | có |
| `GET /tasks/{id}` | 87 | 60 | 27 | 34 | 53 | 0 | 56 | có |
| `PATCH /tasks` | 186 | 91 | 95 | 27 | 159 | 0 | 90 | có |
| `PATCH /tasks/merge` | 113 | 19 | 94 | 2 | 111 | 0 | 26 | có |
| `PATCH /tasks/restore` | 90 | 60 | 30 | 2 | 88 | 0 | 65 | có |
| `PATCH /tasks/{id}` | 185 | 84 | 101 | 32 | 153 | 0 | 85 | có |
| `PATCH /tasks/{id}/restore` | 89 | 59 | 30 | 41 | 48 | 0 | 58 | có |
| `POST /batch/tasks` | 205 | 71 | 134 | 16 | 189 | 0 | 81 | có |
| `POST /tasks` | 196 | 91 | 105 | 37 | 159 | 0 | 102 | có |
| `POST /tasks/duplicates` | 210 | 82 | 128 | 27 | 183 | 0 | 66 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 271 |
| 201 | 50 |
| 204 | 8 |
| 400 | 1344 |
| 401 | 11 |
| 403 | 21 |
| 404 | 47 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 1730 | 0 |
| content_type_conformance | 1660 | 0 |
| ensure_resource_availability | 1660 | 0 |
| ignored_auth | 1660 | 0 |
| max_response_time | 1730 | 0 |
| missing_required_header | 1717 | 13 |
| negative_data_rejection | 1649 | 11 |
| not_a_server_error | 1730 | 0 |
| object_level_authorization | 1730 | 0 |
| positive_data_acceptance | 1121 | 539 |
| response_headers_conformance | 1660 | 0 |
| response_schema_conformance | 1439 | 1080 |
| status_code_conformance | 1504 | 156 |
| unsupported_method | 1691 | 39 |
| use_after_free | 1660 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /tasks` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /tasks` | positive_data_acceptance | RejectedPositiveData | medium | 11 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 3 | `DELETE /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 4 | `DELETE /tasks/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 5 | `DELETE /tasks/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 15 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 6 | `DELETE /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 30 | Documented: 200, 400, 401 |
| 7 | `GET /tasks` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 8 | `GET /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `limit` in query - limit: Value greater than maximum |
| 9 | `GET /tasks` | positive_data_acceptance | RejectedPositiveData | medium | 35 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 10 | `GET /tasks` | response_schema_conformance | JsonSchemaError | high | 224 |     null |
| 11 | `GET /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 12 | `GET /tasks/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 13 | `GET /tasks/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 64 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 14 | `GET /tasks/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 15 | `GET /tasks/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 116 | Documented: 200 |
| 16 | `GET /tasks/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 17 | `GET /tasks/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 18 | `GET /tasks/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 20 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 19 | `GET /tasks/{id}` | response_schema_conformance | JsonSchemaError | high | 132 |     null |
| 20 | `GET /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 21 | `GET /tasks/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 22 | `PATCH /tasks` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 23 | `PATCH /tasks` | positive_data_acceptance | RejectedPositiveData | medium | 66 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`å^󑆸鋘¹ g`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+5) |
| 24 | `PATCH /tasks` | response_schema_conformance | JsonSchemaError | high | 138 |     null |
| 25 | `PATCH /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 26 | `PATCH /tasks/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 27 | `PATCH /tasks/merge` | positive_data_acceptance | RejectedPositiveData | medium | 19 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 3 additional properties not defined in the schema (`,g`, `v`, `¦A`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 3 additional properties not defined in the schema (``, `󉎞!󅴨v¥©Â`, `򊍋3è񉌷î󕿛©s`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+1) |
| 28 | `PATCH /tasks/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 29 | `PATCH /tasks/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 30 | `PATCH /tasks/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 31 | `PATCH /tasks/restore` | positive_data_acceptance | RejectedPositiveData | medium | 57 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 32 | `PATCH /tasks/restore` | response_schema_conformance | JsonSchemaError | high | 6 |     null |
| 33 | `PATCH /tasks/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 34 | `PATCH /tasks/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 35 | `PATCH /tasks/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 36 | `PATCH /tasks/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 52 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; õs±ëÿh`, `fÞÕé`, `` and 2 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 37 | `PATCH /tasks/{id}` | response_schema_conformance | JsonSchemaError | high | 130 |     null |
| 38 | `PATCH /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 39 | `PATCH /tasks/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 40 | `PATCH /tasks/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 14 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 41 | `PATCH /tasks/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 164 |     null |
| 42 | `PATCH /tasks/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 43 | `POST /batch/tasks` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 44 | `POST /batch/tasks` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 45 | `POST /batch/tasks` | positive_data_acceptance | RejectedPositiveData | medium | 65 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 46 | `POST /batch/tasks` | response_schema_conformance | JsonSchemaError | high | 56 |     null |
| 47 | `POST /batch/tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 48 | `POST /batch/tasks` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 49 | `POST /tasks` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 50 | `POST /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 51 | `POST /tasks` | positive_data_acceptance | RejectedPositiveData | medium | 62 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (`¥v󗍸`, `򎭴`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+5) |
| 52 | `POST /tasks` | response_schema_conformance | JsonSchemaError | high | 220 |     null |
| 53 | `POST /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 54 | `POST /tasks` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 55 | `POST /tasks/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 56 | `POST /tasks/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 59 | .`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (`NIL`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+5) |
| 57 | `POST /tasks/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 58 | `POST /tasks/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
