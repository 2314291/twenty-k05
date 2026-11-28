# Thống kê lần chạy `20261128-124700-seed20261020-opportunities`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T05:48:38.587918+00:00 |
| Thời gian chạy (giây) | 727.5 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1853 |
| Lỗi duy nhất | 60 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /opportunities` | 77 | 41 | 36 | 62 | 15 | 0 | 24 | có |
| `DELETE /opportunities/{id}` | 40 | 23 | 17 | 0 | 40 | 0 | 24 | chưa |
| `GET /opportunities` | 114 | 56 | 58 | 65 | 49 | 0 | 61 | có |
| `GET /opportunities/groupBy` | 136 | 78 | 58 | 12 | 124 | 0 | 132 | có |
| `GET /opportunities/{id}` | 87 | 59 | 28 | 42 | 45 | 0 | 54 | có |
| `PATCH /opportunities` | 211 | 75 | 136 | 70 | 141 | 0 | 34 | có |
| `PATCH /opportunities/merge` | 113 | 54 | 59 | 3 | 110 | 0 | 61 | có |
| `PATCH /opportunities/restore` | 90 | 56 | 34 | 21 | 69 | 0 | 44 | có |
| `PATCH /opportunities/{id}` | 210 | 105 | 105 | 50 | 160 | 0 | 88 | có |
| `PATCH /opportunities/{id}/restore` | 89 | 63 | 26 | 41 | 48 | 0 | 54 | có |
| `POST /batch/opportunities` | 230 | 102 | 128 | 38 | 192 | 0 | 77 | có |
| `POST /opportunities` | 221 | 77 | 144 | 12 | 209 | 0 | 69 | có |
| `POST /opportunities/duplicates` | 235 | 103 | 132 | 35 | 200 | 0 | 81 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 398 |
| 201 | 45 |
| 204 | 8 |
| 400 | 1331 |
| 401 | 11 |
| 403 | 21 |
| 404 | 39 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 1831 | 0 |
| content_type_conformance | 1761 | 0 |
| ensure_resource_availability | 1761 | 0 |
| ignored_auth | 1761 | 0 |
| max_response_time | 1831 | 0 |
| missing_required_header | 1818 | 13 |
| negative_data_rejection | 1726 | 35 |
| not_a_server_error | 1831 | 0 |
| object_level_authorization | 1831 | 0 |
| positive_data_acceptance | 1275 | 486 |
| response_headers_conformance | 1761 | 0 |
| response_schema_conformance | 1602 | 921 |
| status_code_conformance | 1613 | 148 |
| unsupported_method | 1792 | 39 |
| use_after_free | 1761 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /opportunities` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /opportunities` | negative_data_rejection | AcceptedNegativeData | medium | 13 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became number); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string) |
| 3 | `DELETE /opportunities` | positive_data_acceptance | RejectedPositiveData | medium | 10 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 4 | `DELETE /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 5 | `DELETE /opportunities/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 6 | `DELETE /opportunities/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 12 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 7 | `DELETE /opportunities/{id}` | status_code_conformance | UndefinedStatusCode | medium | 12 | Documented: 200, 400, 401 |
| 8 | `GET /opportunities` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 9 | `GET /opportunities` | negative_data_rejection | AcceptedNegativeData | medium | 3 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `maximum` at /properties/limit |
| 10 | `GET /opportunities` | positive_data_acceptance | RejectedPositiveData | medium | 13 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 11 | `GET /opportunities` | response_schema_conformance | JsonSchemaError | high | 429 |     null;     } |
| 12 | `GET /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `GET /opportunities/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 14 | `GET /opportunities/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 63 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 15 | `GET /opportunities/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 16 | `GET /opportunities/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 116 | Documented: 200 |
| 17 | `GET /opportunities/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 18 | `GET /opportunities/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 19 | `GET /opportunities/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 10 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 20 | `GET /opportunities/{id}` | response_schema_conformance | JsonSchemaError | high | 145 |     null;     } |
| 21 | `GET /opportunities/{id}` | status_code_conformance | UndefinedStatusCode | medium | 8 | Documented: 200, 400, 401 |
| 22 | `GET /opportunities/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 23 | `PATCH /opportunities` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 24 | `PATCH /opportunities` | negative_data_rejection | AcceptedNegativeData | medium | 14 | Invalid component: in body - amount -> amountMicros: Incorrect type; Invalid component: in body - amount -> currencyCode: Incorrect type; Invalid component: in body - amount: Incorrect type (+10) |
| 25 | `PATCH /opportunities` | positive_data_acceptance | RejectedPositiveData | medium | 19 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 2 additional properties not defined in the schema (`Q`, `Ö򹓜ì`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 4 additional properties not defined in the schema (`^+`, `/`, `îðUÙ` and 1 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 26 | `PATCH /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 27 | `PATCH /opportunities/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 28 | `PATCH /opportunities/merge` | positive_data_acceptance | RejectedPositiveData | medium | 54 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`î󮖕𸰍`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+7) |
| 29 | `PATCH /opportunities/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 30 | `PATCH /opportunities/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 31 | `PATCH /opportunities/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 32 | `PATCH /opportunities/restore` | positive_data_acceptance | RejectedPositiveData | medium | 35 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 33 | `PATCH /opportunities/restore` | response_schema_conformance | JsonSchemaError | high | 18 |     null |
| 34 | `PATCH /opportunities/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 35 | `PATCH /opportunities/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 36 | `PATCH /opportunities/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 37 | `PATCH /opportunities/{id}` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - ownerId: Incorrect type |
| 38 | `PATCH /opportunities/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 52 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`h򸞆`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+6) |
| 39 | `PATCH /opportunities/{id}` | response_schema_conformance | JsonSchemaError | high | 164 |     null |
| 40 | `PATCH /opportunities/{id}` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 41 | `PATCH /opportunities/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 42 | `PATCH /opportunities/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 14 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 43 | `PATCH /opportunities/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 146 |     null;     } |
| 44 | `PATCH /opportunities/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 45 | `PATCH /opportunities/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 46 | `POST /batch/opportunities` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 47 | `POST /batch/opportunities` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - array with invalid items: Incorrect type |
| 48 | `POST /batch/opportunities` | positive_data_acceptance | RejectedPositiveData | medium | 67 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 49 | `POST /batch/opportunities` | response_schema_conformance | JsonSchemaError | high | 9 |     null |
| 50 | `POST /batch/opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 51 | `POST /batch/opportunities` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 52 | `POST /opportunities` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 53 | `POST /opportunities` | positive_data_acceptance | RejectedPositiveData | medium | 65 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, ` Zï`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+3) |
| 54 | `POST /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 55 | `POST /opportunities` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 56 | `POST /opportunities/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 57 | `POST /opportunities/duplicates` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - data: Incorrect type; Invalid component: in body - ids -> Array with invalid items: Incorrect type |
| 58 | `POST /opportunities/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 72 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 3 additional properties not defined in the schema (`򇺀⚨A`, `lx`, `Ú`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 59 | `POST /opportunities/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 60 | `POST /opportunities/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
