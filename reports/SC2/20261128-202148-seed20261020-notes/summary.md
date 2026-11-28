# Thống kê lần chạy `20261128-202148-seed20261020-notes`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T13:23:26.334779+00:00 |
| Thời gian chạy (giây) | 170.8 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1201 |
| Lỗi duy nhất | 24 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /notes` | 57 | 0 | 57 | 48 | 9 | 0 | 32 | có |
| `DELETE /notes/{id}` | 27 | 2 | 25 | 0 | 27 | 0 | 6 | chưa |
| `GET /notes` | 79 | 0 | 79 | 26 | 53 | 0 | 27 | có |
| `GET /notes/groupBy` | 97 | 0 | 97 | 13 | 84 | 0 | 89 | có |
| `GET /notes/{id}` | 68 | 28 | 40 | 25 | 43 | 0 | 31 | có |
| `PATCH /notes` | 112 | 0 | 112 | 1 | 111 | 0 | 1 | có |
| `PATCH /notes/merge` | 95 | 0 | 95 | 2 | 93 | 0 | 1 | có |
| `PATCH /notes/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /notes/{id}` | 117 | 28 | 89 | 27 | 90 | 0 | 28 | có |
| `PATCH /notes/{id}/restore` | 70 | 34 | 36 | 30 | 40 | 0 | 31 | có |
| `POST /batch/notes` | 141 | 0 | 141 | 30 | 111 | 0 | 29 | có |
| `POST /notes` | 133 | 0 | 133 | 9 | 124 | 0 | 9 | có |
| `POST /notes/duplicates` | 140 | 9 | 131 | 28 | 112 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 196 |
| 201 | 36 |
| 204 | 8 |
| 400 | 920 |
| 403 | 13 |
| 404 | 28 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1068 | 63 |
| not_a_server_error | 1201 | 0 |
| response_schema_conformance | 998 | 422 |
| status_code_conformance | 1028 | 103 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /notes` | negative_data_rejection | AcceptedNegativeData | medium | 31 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer) |
| 2 | `DELETE /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 6 | Documented: 200, 400, 401 |
| 4 | `GET /notes` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `maximum` at /properties/limit |
| 5 | `GET /notes` | response_schema_conformance | JsonSchemaError | high | 104 |     null |
| 6 | `GET /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 7 | `GET /notes/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 8 | `GET /notes/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 9 | `GET /notes/{id}` | response_schema_conformance | JsonSchemaError | high | 72 |     null |
| 10 | `GET /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 7 | Documented: 200, 400, 401 |
| 11 | `PATCH /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 12 | `PATCH /notes/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `PATCH /notes/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /notes/{id}` | response_schema_conformance | JsonSchemaError | high | 81 |     null |
| 15 | `PATCH /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 16 | `PATCH /notes/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 87 |     null |
| 17 | `PATCH /notes/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 18 | `POST /batch/notes` | negative_data_rejection | AcceptedNegativeData | medium | 25 | Invalid component: parameter `upsert` in query - upsert: Incorrect type; Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became string) |
| 19 | `POST /batch/notes` | response_schema_conformance | JsonSchemaError | high | 36 |     null |
| 20 | `POST /batch/notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 21 | `POST /notes` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 22 | `POST /notes` | response_schema_conformance | JsonSchemaError | high | 32 |     null |
| 23 | `POST /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 24 | `POST /notes/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
