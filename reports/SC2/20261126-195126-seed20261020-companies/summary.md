# Thống kê lần chạy `20261126-195126-seed20261020-companies`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-26T12:52:12.853682+00:00 |
| Thời gian chạy (giây) | 182.8 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1801 |
| Lỗi duy nhất | 22 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /companies` | 57 | 0 | 57 | 42 | 15 | 0 | 8 | có |
| `DELETE /companies/{id}` | 17 | 3 | 14 | 4 | 13 | 0 | 3 | chưa |
| `GET /companies` | 79 | 0 | 79 | 34 | 45 | 0 | 35 | có |
| `GET /companies/groupBy` | 97 | 0 | 97 | 12 | 85 | 0 | 89 | có |
| `GET /companies/{id}` | 68 | 31 | 37 | 27 | 41 | 0 | 24 | có |
| `PATCH /companies` | 234 | 7 | 227 | 1 | 233 | 0 | 1 | có |
| `PATCH /companies/merge` | 95 | 0 | 95 | 1 | 94 | 0 | 1 | có |
| `PATCH /companies/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /companies/{id}` | 239 | 39 | 200 | 26 | 213 | 0 | 27 | có |
| `PATCH /companies/{id}/restore` | 70 | 40 | 30 | 41 | 29 | 0 | 38 | có |
| `POST /batch/companies` | 263 | 0 | 263 | 22 | 241 | 0 | 22 | có |
| `POST /companies` | 255 | 4 | 251 | 1 | 254 | 0 | 1 | có |
| `POST /companies/duplicates` | 262 | 2 | 260 | 19 | 243 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 202 |
| 201 | 21 |
| 204 | 8 |
| 400 | 1536 |
| 403 | 13 |
| 404 | 21 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1702 | 29 |
| not_a_server_error | 1801 | 0 |
| response_schema_conformance | 1603 | 798 |
| status_code_conformance | 1635 | 96 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /companies` | negative_data_rejection | AcceptedNegativeData | medium | 7 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became number); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string) |
| 2 | `DELETE /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 4 | `GET /companies` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `limit` in query - limit: Value greater than maximum |
| 5 | `GET /companies` | response_schema_conformance | JsonSchemaError | high | 282 |     null |
| 6 | `GET /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 7 | `GET /companies/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 8 | `GET /companies/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 9 | `GET /companies/{id}` | response_schema_conformance | JsonSchemaError | high | 126 |     null |
| 10 | `GET /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 11 | `PATCH /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 12 | `PATCH /companies/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `PATCH /companies/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /companies/{id}` | response_schema_conformance | JsonSchemaError | high | 156 |     null |
| 15 | `PATCH /companies/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 16 | `PATCH /companies/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 216 |     null |
| 17 | `PATCH /companies/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 18 | `POST /batch/companies` | negative_data_rejection | AcceptedNegativeData | medium | 21 | Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became integer) |
| 19 | `POST /batch/companies` | response_schema_conformance | JsonSchemaError | high | 8 |     null |
| 20 | `POST /batch/companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 21 | `POST /companies` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 22 | `POST /companies/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
