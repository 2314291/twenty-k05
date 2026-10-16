# Thống kê lần chạy `20261016-215144-seed20261020-RED`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-10-16T14:51:48.554162+00:00 |
| Thời gian chạy (giây) | 120.3 |
| Exit code | 1 |
| Phase | examples=failure, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 779 |
| Lỗi duy nhất | 48 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /companies` | 72 | 38 | 34 | 13 | 59 | 0 | 29 | có |
| `DELETE /companies/{id}` | 20 | 8 | 12 | 0 | 20 | 0 | 15 | chưa |
| `GET /companies` | 76 | 39 | 37 | 37 | 39 | 0 | 10 | có |
| `GET /companies/groupBy` | 91 | 61 | 30 | 8 | 83 | 0 | 89 | có |
| `GET /companies/{id}` | 59 | 25 | 34 | 1 | 58 | 0 | 29 | có |
| `PATCH /companies` | 42 | 31 | 11 | 5 | 37 | 0 | 27 | chưa |
| `PATCH /companies/merge` | 79 | 23 | 56 | 2 | 77 | 0 | 30 | có |
| `PATCH /companies/restore` | 58 | 30 | 28 | 11 | 47 | 0 | 27 | có |
| `PATCH /companies/{id}` | 44 | 17 | 27 | 0 | 44 | 0 | 19 | chưa |
| `PATCH /companies/{id}/restore` | 54 | 18 | 36 | 1 | 53 | 0 | 25 | có |
| `POST /batch/companies` | 28 | 12 | 16 | 4 | 24 | 0 | 6 | chưa |
| `POST /companies` | 54 | 26 | 28 | 2 | 52 | 0 | 28 | có |
| `POST /companies/duplicates` | 102 | 18 | 84 | 13 | 89 | 0 | 15 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 86 |
| 201 | 5 |
| 204 | 6 |
| 400 | 581 |
| 401 | 8 |
| 403 | 19 |
| 404 | 74 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| allow_header_conformance | 763 | 0 |
| content_type_conformance | 724 | 0 |
| ensure_resource_availability | 724 | 0 |
| ignored_auth | 724 | 0 |
| max_response_time | 763 | 0 |
| missing_required_header | 752 | 11 |
| negative_data_rejection | 722 | 2 |
| not_a_server_error | 763 | 0 |
| object_level_authorization | 763 | 0 |
| positive_data_acceptance | 520 | 204 |
| response_headers_conformance | 724 | 0 |
| response_schema_conformance | 710 | 14 |
| status_code_conformance | 571 | 153 |
| unsupported_method | 736 | 27 |
| use_after_free | 724 | 0 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 2 | `DELETE /companies` | positive_data_acceptance | RejectedPositiveData | medium | 28 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 3 | `DELETE /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 4 | `DELETE /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 5 | `DELETE /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 15 | Documented: 200, 400, 401 |
| 6 | `GET /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 7 | `GET /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `limit` in query - limit: Value greater than maximum |
| 8 | `GET /companies` | positive_data_acceptance | RejectedPositiveData | medium | 7 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 9 | `GET /companies` | response_schema_conformance | JsonSchemaError | high | 1 |     "" |
| 10 | `GET /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 11 | `GET /companies/groupBy` | positive_data_acceptance | RejectedPositiveData | medium | 51 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 12 | `GET /companies/groupBy` | response_schema_conformance | JsonSchemaError | high | 8 |     [] |
| 13 | `GET /companies/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 81 | Documented: 200 |
| 14 | `GET /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 15 | `GET /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 5 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 16 | `GET /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 22 | Documented: 200, 400, 401 |
| 17 | `GET /companies/{id}` | unsupported_method | UnsupportedMethodResponse | medium | 2 | Return 405 for methods not listed in the OpenAPI spec |
| 18 | `PATCH /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 19 | `PATCH /companies` | positive_data_acceptance | RejectedPositiveData | medium | 24 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 3 additional properties not defined in the schema (`.`, `<8󝴗象񕬰𒟤`, `𦻷`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 5 additional properties not defined in the schema (`S`, `r𭱏(¦Õ`, `:ÇS¡` and 2 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+1) |
| 20 | `PATCH /companies` | response_schema_conformance | JsonSchemaError | high | 2 |     "" |
| 21 | `PATCH /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 22 | `PATCH /companies/merge` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 23 | `PATCH /companies/merge` | positive_data_acceptance | RejectedPositiveData | medium | 23 | 񲼱𡽱z®`, `ç`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+2) |
| 24 | `PATCH /companies/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 25 | `PATCH /companies/merge` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 26 | `PATCH /companies/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 27 | `PATCH /companies/restore` | positive_data_acceptance | RejectedPositiveData | medium | 18 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 28 | `PATCH /companies/restore` | response_schema_conformance | JsonSchemaError | high | 2 |     "" |
| 29 | `PATCH /companies/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 30 | `PATCH /companies/restore` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
| 31 | `PATCH /companies/{id}` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 32 | `PATCH /companies/{id}` | positive_data_acceptance | RejectedPositiveData | medium | 7 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 4 additional properties not defined in the schema (`^1_``, `W9񞳯󙶂ôOG`, `false` and 1 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 5 additional properties not defined in the schema (`E¾𻫒	i𘬯ÿTÁ혵`, `V®`, `ª-Þ񔧹𑲡񀖱` and 2 more). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 33 | `PATCH /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 12 | Documented: 200, 400, 401 |
| 34 | `PATCH /companies/{id}/restore` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 35 | `PATCH /companies/{id}/restore` | positive_data_acceptance | RejectedPositiveData | medium | 5 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 36 | `PATCH /companies/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 16 | Documented: 200, 400, 401 |
| 37 | `PATCH /companies/{id}/restore` | unsupported_method | UnsupportedMethodResponse | medium | 4 | Return 405 for methods not listed in the OpenAPI spec |
| 38 | `POST /batch/companies` | positive_data_acceptance | RejectedPositiveData | medium | 6 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx |
| 39 | `POST /companies` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 40 | `POST /companies` | positive_data_acceptance | RejectedPositiveData | medium | 23 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; 񖒽òM5³`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. |
| 41 | `POST /companies` | response_schema_conformance | JsonSchemaError | high | 1 |     "" |
| 42 | `POST /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 43 | `POST /companies` | unsupported_method | UnsupportedMethodResponse | medium | 3 | Return 405 for methods not listed in the OpenAPI spec |
| 44 | `POST /companies/duplicates` | missing_required_header | MissingHeaderNotRejected | medium | 1 | Got 403 when missing required 'Authorization' header, expected 401 |
| 45 | `POST /companies/duplicates` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: in body - ids -> Array with invalid items: Incorrect type |
| 46 | `POST /companies/duplicates` | positive_data_acceptance | RejectedPositiveData | medium | 7 | Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx; Hint: The request body contains 1 additional property not defined in the schema (``). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields.; Hint: The request body contains 2 additional properties not defined in the schema (`þ򀂙`, `·`). The server appears to reject properties the schema allows. Declare `additionalProperties: false` if extras are not accepted, or make the server ignore unknown fields. (+1) |
| 47 | `POST /companies/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 48 | `POST /companies/duplicates` | unsupported_method | UnsupportedMethodResponse | medium | 6 | Return 405 for methods not listed in the OpenAPI spec |
