# Thống kê lần chạy `20261128-153719-seed20261020-notes`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T08:37:57.533342+00:00 |
| Thời gian chạy (giây) | 251.2 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1637 |
| Lỗi duy nhất | 59 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /notes` | 77 | 45 | 32 | 49 | 28 | 0 | 11 | có |
| `DELETE /notes/{id}` | 64 | 50 | 14 | 0 | 64 | 0 | 52 | có |
| `GET /notes` | 114 | 47 | 67 | 45 | 69 | 0 | 71 | có |
| `GET /notes/groupBy` | 136 | 75 | 61 | 12 | 124 | 0 | 132 | có |
| `GET /notes/{id}` | 87 | 55 | 32 | 33 | 54 | 0 | 50 | có |
| `PATCH /notes` | 163 | 74 | 89 | 28 | 135 | 0 | 73 | có |
| `PATCH /notes/merge` | 113 | 50 | 63 | 2 | 111 | 0 | 57 | có |
| `PATCH /notes/restore` | 90 | 57 | 33 | 2 | 88 | 0 | 62 | có |
| `PATCH /notes/{id}` | 162 | 72 | 90 | 25 | 137 | 0 | 71 | có |
| `PATCH /notes/{id}/restore` | 89 | 66 | 23 | 43 | 46 | 0 | 62 | có |
| `POST /batch/notes` | 182 | 56 | 126 | 17 | 165 | 0 | 67 | có |
| `POST /notes` | 173 | 67 | 106 | 36 | 137 | 0 | 79 | có |
| `POST /notes/duplicates` | 187 | 70 | 117 | 21 | 166 | 0 | 60 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 255 |
| 201 | 50 |
| 204 | 8 |
| 400 | 1272 |
| 401 | 11 |
| 403 | 21 |
| 404 | 20 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 1615 | 0 |
| content_type_conformance | 1545 | 0 |
| ensure_resource_availability | 1545 | 0 |
| ignored_auth | 1545 | 0 |
| max_response_time | 1615 | 0 |
| missing_required_header | 1602 | 13 |
| negative_data_rejection | 1532 | 13 |
| not_a_server_error | 1615 | 0 |
| object_level_authorization | 1615 | 0 |
| positive_data_acceptance | 1029 | 516 |
| response_headers_conformance | 1545 | 0 |
| response_schema_conformance | 1323 | 759 |
| status_code_conformance | 1416 | 129 |
| unsupported_method | 1576 | 39 |
| use_after_free | 1545 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /notes` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /notes` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string) |
| 3 | `DELETE /notes` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 4 | `DELETE /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 5 | `DELETE /notes/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 6 | `DELETE /notes/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 49 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 7 | `DELETE /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 8 | `GET /notes` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 9 | `GET /notes` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `minimum`, `maximum` at /properties/limit |
| 10 | `GET /notes` | positive_data_acceptance | RejectedPositiveData | medium | 26 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 11 | `GET /notes` | response_schema_conformance | JsonSchemaError | high | 176 |     null |
| 12 | `GET /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `GET /notes/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 14 | `GET /notes/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 60 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 15 | `GET /notes/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 16 | `GET /notes/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 116 | Documented: 200 |
| 17 | `GET /notes/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 18 | `GET /notes/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 19 | `GET /notes/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 15 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 20 | `GET /notes/{id}` | response_schema_conformance | JsonSchemaError | high | 96 |     null |
| 21 | `GET /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 22 | `GET /notes/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 23 | `PATCH /notes` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 24 | `PATCH /notes` | positive_data_acceptance | RejectedPositiveData | medium | 48 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (`ﺖ2𻅱ãU৘¤򍓤d`, `Öüላ`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 25 | `PATCH /notes` | response_schema_conformance | JsonSchemaError | high | 96 |     null |
| 26 | `PATCH /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 27 | `PATCH /notes/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 28 | `PATCH /notes/merge` | positive_data_acceptance | RejectedPositiveData | medium | 50 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`ᠤ`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+5) |
| 29 | `PATCH /notes/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 30 | `PATCH /notes/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 31 | `PATCH /notes/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 32 | `PATCH /notes/restore` | positive_data_acceptance | RejectedPositiveData | medium | 54 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 33 | `PATCH /notes/restore` | response_schema_conformance | JsonSchemaError | high | 4 |     null |
| 34 | `PATCH /notes/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 35 | `PATCH /notes/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 36 | `PATCH /notes/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 37 | `PATCH /notes/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 46 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (`0..0`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`æ`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+3) |
| 38 | `PATCH /notes/{id}` | response_schema_conformance | JsonSchemaError | high | 75 |     null |
| 39 | `PATCH /notes/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 40 | `PATCH /notes/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 15 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 41 | `PATCH /notes/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 126 |     null |
| 42 | `PATCH /notes/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 43 | `PATCH /notes/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 44 | `POST /batch/notes` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 45 | `POST /batch/notes` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 46 | `POST /batch/notes` | positive_data_acceptance | RejectedPositiveData | medium | 51 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 47 | `POST /batch/notes` | response_schema_conformance | JsonSchemaError | high | 36 |     null |
| 48 | `POST /batch/notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 49 | `POST /batch/notes` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 50 | `POST /notes` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 51 | `POST /notes` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 52 | `POST /notes` | positive_data_acceptance | RejectedPositiveData | medium | 40 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (`¢`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 53 | `POST /notes` | response_schema_conformance | JsonSchemaError | high | 140 |     null |
| 54 | `POST /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 55 | `POST /notes` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 56 | `POST /notes/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 57 | `POST /notes/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 53 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (`􏷴\Åáç>`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, `􏷴\Åáç>`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 58 | `POST /notes/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 59 | `POST /notes/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
