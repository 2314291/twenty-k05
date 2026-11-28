# Thống kê lần chạy `20261128-120704-seed20261020-companies`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T05:07:43.209839+00:00 |
| Thời gian chạy (giây) | 1103.4 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 2435 |
| Lỗi duy nhất | 61 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /companies` | 77 | 44 | 33 | 58 | 19 | 0 | 17 | có |
| `DELETE /companies/{id}` | 27 | 10 | 17 | 0 | 27 | 0 | 12 | chưa |
| `GET /companies` | 114 | 54 | 60 | 60 | 54 | 0 | 44 | có |
| `GET /companies/groupBy` | 136 | 79 | 57 | 12 | 124 | 0 | 132 | có |
| `GET /companies/{id}` | 87 | 59 | 28 | 50 | 37 | 0 | 56 | có |
| `PATCH /companies` | 330 | 104 | 226 | 157 | 173 | 0 | 96 | có |
| `PATCH /companies/merge` | 113 | 50 | 63 | 3 | 110 | 0 | 57 | có |
| `PATCH /companies/restore` | 90 | 53 | 37 | 19 | 71 | 0 | 45 | có |
| `PATCH /companies/{id}` | 329 | 128 | 201 | 41 | 288 | 0 | 118 | có |
| `PATCH /companies/{id}/restore` | 89 | 58 | 31 | 45 | 44 | 0 | 55 | có |
| `POST /batch/companies` | 349 | 118 | 231 | 36 | 313 | 0 | 96 | có |
| `POST /companies` | 340 | 100 | 240 | 13 | 327 | 0 | 93 | có |
| `POST /companies/duplicates` | 354 | 125 | 229 | 43 | 311 | 0 | 97 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 485 |
| 201 | 44 |
| 204 | 8 |
| 400 | 1840 |
| 401 | 11 |
| 403 | 21 |
| 404 | 26 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 2413 | 0 |
| content_type_conformance | 2343 | 0 |
| ensure_resource_availability | 2343 | 0 |
| ignored_auth | 2343 | 0 |
| max_response_time | 2413 | 0 |
| missing_required_header | 2400 | 13 |
| negative_data_rejection | 2269 | 74 |
| not_a_server_error | 2413 | 0 |
| object_level_authorization | 2413 | 0 |
| positive_data_acceptance | 1782 | 561 |
| response_headers_conformance | 2343 | 0 |
| response_schema_conformance | 2171 | 1068 |
| status_code_conformance | 2208 | 135 |
| unsupported_method | 2374 | 39 |
| use_after_free | 2343 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /companies` | negative_data_rejection | AcceptedNegativeData | medium | 7 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer) |
| 3 | `DELETE /companies` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 4 | `DELETE /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 5 | `DELETE /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 6 | `DELETE /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 8 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 7 | `DELETE /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 4 | Documented: 200, 400, 401 |
| 8 | `GET /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 9 | `GET /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `limit` in query - limit: Value greater than maximum |
| 10 | `GET /companies` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 11 | `GET /companies` | response_schema_conformance | JsonSchemaError | high | 282 |     null |
| 12 | `GET /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `GET /companies/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 14 | `GET /companies/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 64 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 15 | `GET /companies/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 16 | `GET /companies/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 116 | Documented: 200 |
| 17 | `GET /companies/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 18 | `GET /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 19 | `GET /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 8 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 20 | `GET /companies/{id}` | response_schema_conformance | JsonSchemaError | high | 242 |     null |
| 21 | `GET /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 22 | `GET /companies/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 23 | `PATCH /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 24 | `PATCH /companies` | negative_data_rejection | AcceptedNegativeData | medium | 59 | Invalid component: in body - accountOwnerId: Incorrect type; Invalid component: in body - address -> addressCity: Incorrect type; Invalid component: in body - address -> addressCountry: Incorrect type (+30) |
| 25 | `PATCH /companies` | positive_data_acceptance | RejectedPositiveData | medium | 21 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 3 additional properties not defined in the schema (`.`, `<8󝴗象񕬰𒟤`, `𦻷`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 26 | `PATCH /companies` | response_schema_conformance | JsonSchemaError | high | 150 |     null |
| 27 | `PATCH /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 28 | `PATCH /companies/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 29 | `PATCH /companies/merge` | positive_data_acceptance | RejectedPositiveData | medium | 50 | 񲼱𡽱z®`, `ç`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (`ý`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+8) |
| 30 | `PATCH /companies/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 31 | `PATCH /companies/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 32 | `PATCH /companies/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 33 | `PATCH /companies/restore` | positive_data_acceptance | RejectedPositiveData | medium | 34 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 34 | `PATCH /companies/restore` | response_schema_conformance | JsonSchemaError | high | 32 |     null |
| 35 | `PATCH /companies/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 36 | `PATCH /companies/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 37 | `PATCH /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 38 | `PATCH /companies/{id}` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - accountOwnerId: Incorrect type |
| 39 | `PATCH /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 84 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, `Üt𙌔åø\|񓮒ùHÕG󠐁`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 40 | `PATCH /companies/{id}` | response_schema_conformance | JsonSchemaError | high | 155 |     null |
| 41 | `PATCH /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 42 | `PATCH /companies/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 43 | `PATCH /companies/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 12 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 44 | `PATCH /companies/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 197 |     null |
| 45 | `PATCH /companies/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 46 | `PATCH /companies/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 47 | `POST /batch/companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 48 | `POST /batch/companies` | negative_data_rejection | AcceptedNegativeData | medium | 3 | Invalid component: in body - array with invalid items: Incorrect type; Invalid component: in body - array with invalid items: accountOwnerId: Incorrect type |
| 49 | `POST /batch/companies` | positive_data_acceptance | RejectedPositiveData | medium | 86 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 50 | `POST /batch/companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 51 | `POST /batch/companies` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 52 | `POST /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 53 | `POST /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - accountOwnerId: Incorrect type |
| 54 | `POST /companies` | positive_data_acceptance | RejectedPositiveData | medium | 88 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 3 additional properties not defined in the schema (`T/nèüv#þ9𯐏?ÿ.x>`, ``ç𧇖`, `¤`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+1) |
| 55 | `POST /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 56 | `POST /companies` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 57 | `POST /companies/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 58 | `POST /companies/duplicates` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - data: Incorrect type; Invalid component: in body - ids -> Array with invalid items: Incorrect type |
| 59 | `POST /companies/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 88 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 60 | `POST /companies/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 61 | `POST /companies/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
