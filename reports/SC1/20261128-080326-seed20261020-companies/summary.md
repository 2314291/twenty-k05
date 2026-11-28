# Thống kê lần chạy `20261128-080326-seed20261020-companies`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T01:04:02.433313+00:00 |
| Thời gian chạy (giây) | 1100.1 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 2472 |
| Lỗi duy nhất | 60 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /companies` | 77 | 53 | 24 | 57 | 20 | 0 | 15 | có |
| `DELETE /companies/{id}` | 64 | 36 | 28 | 0 | 64 | 0 | 39 | có |
| `GET /companies` | 114 | 61 | 53 | 58 | 56 | 0 | 49 | có |
| `GET /companies/groupBy` | 136 | 80 | 56 | 12 | 124 | 0 | 132 | có |
| `GET /companies/{id}` | 87 | 53 | 34 | 40 | 47 | 0 | 48 | có |
| `PATCH /companies` | 330 | 109 | 221 | 142 | 188 | 0 | 86 | có |
| `PATCH /companies/merge` | 113 | 57 | 56 | 3 | 110 | 0 | 64 | có |
| `PATCH /companies/restore` | 90 | 58 | 32 | 14 | 76 | 0 | 52 | có |
| `PATCH /companies/{id}` | 329 | 130 | 199 | 39 | 290 | 0 | 121 | có |
| `PATCH /companies/{id}/restore` | 89 | 59 | 30 | 45 | 44 | 0 | 53 | có |
| `POST /batch/companies` | 349 | 112 | 237 | 39 | 310 | 0 | 88 | có |
| `POST /companies` | 340 | 104 | 236 | 13 | 327 | 0 | 97 | có |
| `POST /companies/duplicates` | 354 | 122 | 232 | 41 | 313 | 0 | 97 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 448 |
| 201 | 47 |
| 204 | 8 |
| 400 | 1883 |
| 401 | 11 |
| 403 | 21 |
| 404 | 54 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 2450 | 0 |
| content_type_conformance | 2380 | 0 |
| ensure_resource_availability | 2380 | 0 |
| ignored_auth | 2380 | 0 |
| max_response_time | 2450 | 0 |
| missing_required_header | 2437 | 13 |
| negative_data_rejection | 2311 | 69 |
| not_a_server_error | 2450 | 0 |
| object_level_authorization | 2450 | 0 |
| positive_data_acceptance | 1783 | 597 |
| response_headers_conformance | 2380 | 0 |
| response_schema_conformance | 2242 | 815 |
| status_code_conformance | 2217 | 163 |
| unsupported_method | 2411 | 39 |
| use_after_free | 2380 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer) |
| 3 | `DELETE /companies` | positive_data_acceptance | RejectedPositiveData | medium | 13 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 4 | `DELETE /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 5 | `DELETE /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 6 | `DELETE /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 7 | `DELETE /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 30 | Documented: 200, 400, 401 |
| 8 | `GET /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 9 | `GET /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `limit` in query - limit: Value greater than maximum |
| 10 | `GET /companies` | positive_data_acceptance | RejectedPositiveData | medium | 16 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 11 | `GET /companies` | response_schema_conformance | JsonSchemaError | high | 242 |     null |
| 12 | `GET /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `GET /companies/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 14 | `GET /companies/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 65 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 15 | `GET /companies/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 16 | `GET /companies/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 116 | Documented: 200 |
| 17 | `GET /companies/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 18 | `GET /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 19 | `GET /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 20 | `GET /companies/{id}` | response_schema_conformance | JsonSchemaError | high | 190 |     null |
| 21 | `GET /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 4 | Documented: 200, 400, 401 |
| 22 | `GET /companies/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 23 | `PATCH /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 24 | `PATCH /companies` | negative_data_rejection | AcceptedNegativeData | medium | 59 | Invalid component: in body - accountOwnerId: Incorrect type; Invalid component: in body - address -> addressCity: Incorrect type; Invalid component: in body - address -> addressCountry: Incorrect type (+30) |
| 25 | `PATCH /companies` | positive_data_acceptance | RejectedPositiveData | medium | 26 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 2 additional properties not defined in the schema (``, `Ã`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 3 additional properties not defined in the schema (`.`, `<8󝴗象񕬰𒟤`, `𦻷`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+5) |
| 26 | `PATCH /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 27 | `PATCH /companies/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 28 | `PATCH /companies/merge` | positive_data_acceptance | RejectedPositiveData | medium | 56 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`÷򵣕󩧐!`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+4) |
| 29 | `PATCH /companies/merge` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 30 | `PATCH /companies/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 31 | `PATCH /companies/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 32 | `PATCH /companies/restore` | positive_data_acceptance | RejectedPositiveData | medium | 44 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 33 | `PATCH /companies/restore` | response_schema_conformance | JsonSchemaError | high | 6 |     null |
| 34 | `PATCH /companies/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 35 | `PATCH /companies/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 36 | `PATCH /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 400 when missing required 'Authorization' header, expected 401 |
| 37 | `PATCH /companies/{id}` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - accountOwnerId: Incorrect type; Invalid component: in body - violates `type` (was object, became array) |
| 38 | `PATCH /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 89 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; ⠇󢼗t򣰻` and 2 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+1) |
| 39 | `PATCH /companies/{id}` | response_schema_conformance | JsonSchemaError | high | 170 |     null |
| 40 | `PATCH /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 41 | `PATCH /companies/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 42 | `PATCH /companies/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 12 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 43 | `PATCH /companies/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 197 |     null |
| 44 | `PATCH /companies/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 45 | `PATCH /companies/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 46 | `POST /batch/companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 47 | `POST /batch/companies` | negative_data_rejection | AcceptedNegativeData | medium | 3 | Invalid component: in body - array with invalid items: Incorrect type; Invalid component: in body - array with invalid items: accountOwnerId: Incorrect type |
| 48 | `POST /batch/companies` | positive_data_acceptance | RejectedPositiveData | medium | 78 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 49 | `POST /batch/companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 50 | `POST /batch/companies` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 51 | `POST /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 52 | `POST /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - accountOwnerId: Incorrect type |
| 53 | `POST /companies` | positive_data_acceptance | RejectedPositiveData | medium | 92 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; i`, `x`, `å"VM` and 2 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 54 | `POST /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 55 | `POST /companies` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 56 | `POST /companies/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 57 | `POST /companies/duplicates` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - data: Incorrect type; Invalid component: in body - ids -> Array with invalid items: Incorrect type |
| 58 | `POST /companies/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 88 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 3 additional properties not defined in the schema (``, `6æÎ`, `𮄤`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 4 additional properties not defined in the schema (`c W	¿`, ``, `Ú` and 1 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+1) |
| 59 | `POST /companies/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 60 | `POST /companies/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
