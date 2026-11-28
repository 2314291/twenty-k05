# Thống kê lần chạy `20261126-200024-seed20261020-opportunities`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-26T13:02:00.844347+00:00 |
| Thời gian chạy (giây) | 198.0 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1338 |
| Lỗi duy nhất | 19 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /opportunities` | 57 | 0 | 57 | 47 | 10 | 0 | 40 | có |
| `DELETE /opportunities/{id}` | 14 | 1 | 13 | 2 | 12 | 0 | 2 | chưa |
| `GET /opportunities` | 79 | 0 | 79 | 34 | 45 | 0 | 35 | có |
| `GET /opportunities/groupBy` | 97 | 0 | 97 | 12 | 85 | 0 | 89 | có |
| `GET /opportunities/{id}` | 68 | 38 | 30 | 33 | 35 | 0 | 36 | có |
| `PATCH /opportunities` | 142 | 2 | 140 | 21 | 121 | 0 | 1 | có |
| `PATCH /opportunities/merge` | 95 | 0 | 95 | 1 | 94 | 0 | 1 | có |
| `PATCH /opportunities/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /opportunities/{id}` | 147 | 4 | 143 | 0 | 147 | 0 | 2 | có |
| `PATCH /opportunities/{id}/restore` | 70 | 36 | 34 | 30 | 40 | 0 | 30 | có |
| `POST /batch/opportunities` | 171 | 0 | 171 | 28 | 143 | 0 | 1 | có |
| `POST /opportunities` | 163 | 8 | 155 | 1 | 162 | 0 | 1 | có |
| `POST /opportunities/duplicates` | 170 | 39 | 131 | 28 | 142 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 203 |
| 201 | 27 |
| 204 | 8 |
| 400 | 1062 |
| 403 | 13 |
| 404 | 25 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1227 | 41 |
| not_a_server_error | 1338 | 0 |
| response_schema_conformance | 1167 | 398 |
| status_code_conformance | 1168 | 100 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /opportunities` | negative_data_rejection | AcceptedNegativeData | medium | 39 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer) |
| 2 | `DELETE /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /opportunities/{id}` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 4 | `GET /opportunities` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `minimum`, `maximum` at /properties/limit |
| 5 | `GET /opportunities` | response_schema_conformance | JsonSchemaError | high | 140 |     null;     } |
| 6 | `GET /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 7 | `GET /opportunities/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 8 | `GET /opportunities/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 9 | `GET /opportunities/{id}` | response_schema_conformance | JsonSchemaError | high | 132 |     null;     } |
| 10 | `GET /opportunities/{id}` | status_code_conformance | UndefinedStatusCode | medium | 6 | Documented: 200, 400, 401 |
| 11 | `PATCH /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 12 | `PATCH /opportunities/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `PATCH /opportunities/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /opportunities/{id}` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 15 | `PATCH /opportunities/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 116 |     null;     } |
| 16 | `PATCH /opportunities/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 17 | `POST /batch/opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 18 | `POST /opportunities` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 19 | `POST /opportunities/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
