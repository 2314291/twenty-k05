# Thống kê lần chạy `20261016-220101-seed20261020`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-10-16T15:01:03.138788+00:00 |
| Thời gian chạy (giây) | 301.0 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1257 |
| Lỗi duy nhất | 50 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /companies` | 79 | 44 | 35 | 17 | 62 | 0 | 32 | có |
| `DELETE /companies/{id}` | 64 | 43 | 21 | 0 | 64 | 0 | 51 | có |
| `GET /companies` | 72 | 43 | 29 | 42 | 30 | 0 | 17 | có |
| `GET /companies/groupBy` | 145 | 84 | 61 | 12 | 133 | 0 | 141 | có |
| `GET /companies/{id}` | 86 | 51 | 35 | 1 | 85 | 0 | 55 | có |
| `PATCH /companies` | 77 | 46 | 31 | 13 | 64 | 0 | 36 | có |
| `PATCH /companies/merge` | 92 | 24 | 68 | 2 | 90 | 0 | 31 | có |
| `PATCH /companies/restore` | 91 | 54 | 37 | 21 | 70 | 0 | 40 | có |
| `PATCH /companies/{id}` | 101 | 27 | 74 | 0 | 101 | 0 | 33 | có |
| `PATCH /companies/{id}/restore` | 87 | 51 | 36 | 1 | 86 | 0 | 58 | có |
| `POST /batch/companies` | 97 | 39 | 58 | 24 | 73 | 0 | 22 | có |
| `POST /companies` | 175 | 33 | 142 | 3 | 172 | 0 | 35 | có |
| `POST /companies/duplicates` | 91 | 41 | 50 | 30 | 61 | 0 | 21 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 134 |
| 201 | 24 |
| 204 | 8 |
| 400 | 888 |
| 401 | 8 |
| 403 | 20 |
| 404 | 175 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 1241 | 0 |
| content_type_conformance | 1184 | 0 |
| ensure_resource_availability | 1184 | 0 |
| ignored_auth | 1184 | 0 |
| max_response_time | 1241 | 0 |
| missing_required_header | 1229 | 12 |
| negative_data_rejection | 1179 | 5 |
| not_a_server_error | 1241 | 0 |
| object_level_authorization | 1241 | 0 |
| positive_data_acceptance | 897 | 287 |
| response_headers_conformance | 1184 | 0 |
| response_schema_conformance | 1162 | 72 |
| status_code_conformance | 892 | 292 |
| unsupported_method | 1202 | 39 |
| use_after_free | 1184 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /companies` | positive_data_acceptance | RejectedPositiveData | medium | 31 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 3 | `DELETE /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 4 | `DELETE /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 5 | `DELETE /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 51 | Documented: 200, 400, 401 |
| 6 | `GET /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `limit` in query - limit: Value greater than maximum |
| 7 | `GET /companies` | positive_data_acceptance | RejectedPositiveData | medium | 5 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 8 | `GET /companies` | response_schema_conformance | JsonSchemaError | high | 62 |     null |
| 9 | `GET /companies/groupBy` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 10 | `GET /companies/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 72 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 11 | `GET /companies/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 12 | `GET /companies/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 125 | Documented: 200 |
| 13 | `GET /companies/groupBy` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 14 | `GET /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 15 | `GET /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 16 | `GET /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 44 | Documented: 200, 400, 401 |
| 17 | `GET /companies/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 18 | `PATCH /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 19 | `PATCH /companies` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: in body - accountOwnerId: Incorrect type; Invalid component: in body - updatedBy -> source: Incorrect type |
| 20 | `PATCH /companies` | positive_data_acceptance | RejectedPositiveData | medium | 33 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (``, `f`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+6) |
| 21 | `PATCH /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 22 | `PATCH /companies/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 23 | `PATCH /companies/merge` | positive_data_acceptance | RejectedPositiveData | medium | 24 | 񲼱𡽱z®`, `ç`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 24 | `PATCH /companies/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 25 | `PATCH /companies/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 26 | `PATCH /companies/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 27 | `PATCH /companies/restore` | positive_data_acceptance | RejectedPositiveData | medium | 33 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 28 | `PATCH /companies/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 29 | `PATCH /companies/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 30 | `PATCH /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 31 | `PATCH /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 13 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 1 additional property not defined in the schema (`Ò¥򯐔Ð`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 32 | `PATCH /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 20 | Documented: 200, 400, 401 |
| 33 | `PATCH /companies/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 34 | `PATCH /companies/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 9 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 35 | `PATCH /companies/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 45 | Documented: 200, 400, 401 |
| 36 | `PATCH /companies/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 37 | `POST /batch/companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 38 | `POST /batch/companies` | positive_data_acceptance | RejectedPositiveData | medium | 15 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 39 | `POST /batch/companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 40 | `POST /batch/companies` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 41 | `POST /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 42 | `POST /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - accountOwnerId: Incorrect type |
| 43 | `POST /companies` | positive_data_acceptance | RejectedPositiveData | medium | 30 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 2 additional properties not defined in the schema (`¼ 򳪌¬Ò끘`, `ã`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (`ù󺮝򥵀𗺉񹪘ñÚj`, `𝓣𝓱𝓮 𝓺𝓾𝓲𝓬𝓴 𝓫𝓻𝓸𝔀𝓷 𝓯𝓸𝔁 𝓳𝓾𝓶𝓹𝓼 𝓸𝓿𝓮𝓻 𝓽𝓱𝓮 𝓵𝓪𝔃𝔂 𝓭𝓸𝓰`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+3) |
| 44 | `POST /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 45 | `POST /companies` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 46 | `POST /companies/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 47 | `POST /companies/duplicates` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - ids -> Array with invalid items: Incorrect type |
| 48 | `POST /companies/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 13 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (`þ򀂙`, `·`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 49 | `POST /companies/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 50 | `POST /companies/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
