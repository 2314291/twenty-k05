# Thống kê lần chạy `20261016-213452-seed20261020`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-10-16T14:34:54.392037+00:00 |
| Thời gian chạy (giây) | 301.1 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1248 |
| Lỗi duy nhất | 52 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /companies` | 77 | 42 | 35 | 17 | 60 | 0 | 30 | có |
| `DELETE /companies/{id}` | 64 | 43 | 21 | 0 | 64 | 0 | 51 | có |
| `GET /companies` | 81 | 45 | 36 | 43 | 38 | 0 | 19 | có |
| `GET /companies/groupBy` | 137 | 77 | 60 | 12 | 125 | 0 | 133 | có |
| `GET /companies/{id}` | 84 | 49 | 35 | 1 | 83 | 0 | 53 | có |
| `PATCH /companies` | 74 | 45 | 29 | 13 | 61 | 0 | 35 | có |
| `PATCH /companies/merge` | 92 | 23 | 69 | 2 | 90 | 0 | 30 | có |
| `PATCH /companies/restore` | 90 | 53 | 37 | 21 | 69 | 0 | 39 | có |
| `PATCH /companies/{id}` | 101 | 27 | 74 | 0 | 101 | 0 | 33 | có |
| `PATCH /companies/{id}/restore` | 87 | 51 | 36 | 1 | 86 | 0 | 58 | có |
| `POST /batch/companies` | 96 | 38 | 58 | 23 | 73 | 0 | 22 | có |
| `POST /companies` | 177 | 34 | 143 | 3 | 174 | 0 | 36 | có |
| `POST /companies/duplicates` | 88 | 39 | 49 | 29 | 59 | 0 | 20 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 134 |
| 201 | 23 |
| 204 | 8 |
| 400 | 881 |
| 401 | 8 |
| 403 | 21 |
| 404 | 173 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 1232 | 0 |
| content_type_conformance | 1175 | 0 |
| ensure_resource_availability | 1175 | 0 |
| ignored_auth | 1175 | 0 |
| max_response_time | 1232 | 0 |
| missing_required_header | 1219 | 13 |
| negative_data_rejection | 1170 | 5 |
| not_a_server_error | 1232 | 0 |
| object_level_authorization | 1232 | 0 |
| positive_data_acceptance | 899 | 276 |
| response_headers_conformance | 1175 | 0 |
| response_schema_conformance | 1153 | 72 |
| status_code_conformance | 892 | 283 |
| unsupported_method | 1193 | 39 |
| use_after_free | 1175 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /companies` | positive_data_acceptance | RejectedPositiveData | medium | 29 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 3 | `DELETE /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 4 | `DELETE /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 5 | `DELETE /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 51 | Documented: 200, 400, 401 |
| 6 | `GET /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 7 | `GET /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `limit` in query - limit: Value greater than maximum |
| 8 | `GET /companies` | positive_data_acceptance | RejectedPositiveData | medium | 6 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 9 | `GET /companies` | response_schema_conformance | JsonSchemaError | high | 62 |     null |
| 10 | `GET /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 11 | `GET /companies/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 12 | `GET /companies/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 65 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 13 | `GET /companies/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 14 | `GET /companies/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 117 | Documented: 200 |
| 15 | `GET /companies/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 16 | `GET /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 17 | `GET /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 18 | `GET /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 42 | Documented: 200, 400, 401 |
| 19 | `GET /companies/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 20 | `PATCH /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 21 | `PATCH /companies` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - accountOwnerId: Incorrect type; Invalid component: in body - updatedBy -> source: Incorrect type |
| 22 | `PATCH /companies` | positive_data_acceptance | RejectedPositiveData | medium | 32 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, `f`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+6) |
| 23 | `PATCH /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 24 | `PATCH /companies/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 25 | `PATCH /companies/merge` | positive_data_acceptance | RejectedPositiveData | medium | 23 | 񲼱𡽱z®`, `ç`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 26 | `PATCH /companies/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 27 | `PATCH /companies/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 28 | `PATCH /companies/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 29 | `PATCH /companies/restore` | positive_data_acceptance | RejectedPositiveData | medium | 32 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 30 | `PATCH /companies/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 31 | `PATCH /companies/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 32 | `PATCH /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 33 | `PATCH /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 13 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`Ò¥򯐔Ð`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 34 | `PATCH /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 20 | Documented: 200, 400, 401 |
| 35 | `PATCH /companies/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 36 | `PATCH /companies/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 37 | `PATCH /companies/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 45 | Documented: 200, 400, 401 |
| 38 | `PATCH /companies/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 39 | `POST /batch/companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 40 | `POST /batch/companies` | positive_data_acceptance | RejectedPositiveData | medium | 15 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 41 | `POST /batch/companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 42 | `POST /batch/companies` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 43 | `POST /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 44 | `POST /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - accountOwnerId: Incorrect type |
| 45 | `POST /companies` | positive_data_acceptance | RejectedPositiveData | medium | 31 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 2 additional properties not defined in the schema (`¼ 򳪌¬Ò끘`, `ã`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (`ù󺮝򥵀𗺉񹪘ñÚj`, `𝓣𝓱𝓮 𝓺𝓾𝓲𝓬𝓴 𝓫𝓻𝓸𝔀𝓷 𝓯𝓸𝔁 𝓳𝓾𝓶𝓹𝓼 𝓸𝓿𝓮𝓻 𝓽𝓱𝓮 𝓵𝓪𝔃𝔂 𝓭𝓸𝓰`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+3) |
| 46 | `POST /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 47 | `POST /companies` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 48 | `POST /companies/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 49 | `POST /companies/duplicates` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - ids -> Array with invalid items: Incorrect type |
| 50 | `POST /companies/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 12 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (`þ򀂙`, `·`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 51 | `POST /companies/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 52 | `POST /companies/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
