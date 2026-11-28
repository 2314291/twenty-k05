# Thống kê lần chạy `20261128-122610-seed20261020-people`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T05:27:46.452169+00:00 |
| Thời gian chạy (giây) | 1150.9 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 2499 |
| Lỗi duy nhất | 61 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /people` | 77 | 53 | 24 | 60 | 17 | 0 | 17 | có |
| `DELETE /people/{id}` | 26 | 12 | 14 | 0 | 26 | 0 | 13 | chưa |
| `GET /people` | 114 | 73 | 41 | 69 | 45 | 0 | 58 | có |
| `GET /people/groupBy` | 136 | 83 | 53 | 12 | 124 | 0 | 132 | có |
| `GET /people/{id}` | 87 | 67 | 20 | 51 | 36 | 0 | 48 | có |
| `PATCH /people` | 343 | 109 | 234 | 142 | 201 | 0 | 88 | có |
| `PATCH /people/merge` | 113 | 44 | 69 | 3 | 110 | 0 | 51 | có |
| `PATCH /people/restore` | 90 | 51 | 39 | 22 | 68 | 0 | 39 | có |
| `PATCH /people/{id}` | 342 | 136 | 206 | 164 | 178 | 0 | 120 | có |
| `PATCH /people/{id}/restore` | 89 | 61 | 28 | 46 | 43 | 0 | 45 | có |
| `POST /batch/people` | 362 | 125 | 237 | 46 | 316 | 0 | 93 | có |
| `POST /people` | 353 | 110 | 243 | 17 | 336 | 0 | 100 | có |
| `POST /people/duplicates` | 367 | 129 | 238 | 44 | 323 | 0 | 98 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 610 |
| 201 | 58 |
| 204 | 8 |
| 400 | 1760 |
| 401 | 11 |
| 403 | 21 |
| 404 | 31 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 2477 | 0 |
| content_type_conformance | 2407 | 0 |
| ensure_resource_availability | 2407 | 0 |
| ignored_auth | 2407 | 0 |
| max_response_time | 2477 | 0 |
| missing_required_header | 2464 | 13 |
| negative_data_rejection | 2272 | 135 |
| not_a_server_error | 2477 | 0 |
| object_level_authorization | 2477 | 0 |
| positive_data_acceptance | 1905 | 502 |
| response_headers_conformance | 2407 | 0 |
| response_schema_conformance | 2255 | 604 |
| status_code_conformance | 2267 | 140 |
| unsupported_method | 2438 | 39 |
| use_after_free | 2407 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /people` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /people` | negative_data_rejection | AcceptedNegativeData | medium | 6 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became number) |
| 3 | `DELETE /people` | positive_data_acceptance | RejectedPositiveData | medium | 10 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 4 | `DELETE /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 5 | `DELETE /people/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 6 | `DELETE /people/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 11 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 7 | `DELETE /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 8 | `GET /people` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 9 | `GET /people` | negative_data_rejection | AcceptedNegativeData | medium | 4 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `type` at /properties/limit (was integer, became number) |
| 10 | `GET /people` | positive_data_acceptance | RejectedPositiveData | medium | 12 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 11 | `GET /people` | response_schema_conformance | JsonSchemaError | high | 190 |     null;     } |
| 12 | `GET /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `GET /people/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 14 | `GET /people/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 68 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 15 | `GET /people/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 16 | `GET /people/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 116 | Documented: 200 |
| 17 | `GET /people/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 18 | `GET /people/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 19 | `GET /people/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 7 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 20 | `GET /people/{id}` | response_schema_conformance | JsonSchemaError | high | 132 |     null |
| 21 | `GET /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 5 | Documented: 200, 400, 401 |
| 22 | `GET /people/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 23 | `PATCH /people` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 24 | `PATCH /people` | negative_data_rejection | AcceptedNegativeData | medium | 60 | Invalid component: in body - avatarFile: Incorrect type; Invalid component: in body - avatarUrl: Incorrect type; Invalid component: in body - companyId: Incorrect type (+29) |
| 25 | `PATCH /people` | positive_data_acceptance | RejectedPositiveData | medium | 27 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (`XuÒ`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, `none`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+4) |
| 26 | `PATCH /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 27 | `PATCH /people/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 28 | `PATCH /people/merge` | positive_data_acceptance | RejectedPositiveData | medium | 43 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (`ß򪃇Kï󿠒Æ`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, `O`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+3) |
| 29 | `PATCH /people/merge` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 30 | `PATCH /people/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 31 | `PATCH /people/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 32 | `PATCH /people/restore` | positive_data_acceptance | RejectedPositiveData | medium | 29 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 33 | `PATCH /people/restore` | response_schema_conformance | JsonSchemaError | high | 7 |     null |
| 34 | `PATCH /people/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 35 | `PATCH /people/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 36 | `PATCH /people/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 37 | `PATCH /people/{id}` | negative_data_rejection | AcceptedNegativeData | medium | 59 | Invalid component: in body - avatarFile: Incorrect type; Invalid component: in body - avatarUrl: Incorrect type; Invalid component: in body - companyId: Incorrect type (+28) |
| 38 | `PATCH /people/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 24 | ?®#¥`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+4) |
| 39 | `PATCH /people/{id}` | response_schema_conformance | JsonSchemaError | high | 133 |     null;     } |
| 40 | `PATCH /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 4 | Documented: 200, 400, 401 |
| 41 | `PATCH /people/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 200 when missing required 'Authorization' header, expected 401 |
| 42 | `PATCH /people/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 5 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 43 | `PATCH /people/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 129 |     null;     } |
| 44 | `PATCH /people/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 4 | Documented: 200, 400, 401 |
| 45 | `PATCH /people/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 46 | `POST /batch/people` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 47 | `POST /batch/people` | negative_data_rejection | AcceptedNegativeData | medium | 3 | Invalid component: in body - array with invalid items: Incorrect type; Invalid component: in body - array with invalid items: companyId: Incorrect type |
| 48 | `POST /batch/people` | positive_data_acceptance | RejectedPositiveData | medium | 83 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 49 | `POST /batch/people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 50 | `POST /batch/people` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 51 | `POST /people` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 52 | `POST /people` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - companyId: Incorrect type |
| 53 | `POST /people` | positive_data_acceptance | RejectedPositiveData | medium | 94 | #\|`, `\򔃦񳳠$knF`, `zÊ􊤃𮩑6󘬪` and 2 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; #\|`, `zÊ􊤃𮩑6󘬪`, `{þ°𚸴` and 2 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx (+3) |
| 54 | `POST /people` | response_schema_conformance | JsonSchemaError | high | 3 |     null |
| 55 | `POST /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 56 | `POST /people` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 57 | `POST /people/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 58 | `POST /people/duplicates` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - data: Incorrect type; Invalid component: in body - ids -> Array with invalid items: Incorrect type |
| 59 | `POST /people/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 89 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, `­𗾥Éw􇊅ð󃋼`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 60 | `POST /people/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 61 | `POST /people/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
