# Thống kê lần chạy `20261128-200146-seed20261020-tasks`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T13:03:25.248181+00:00 |
| Thời gian chạy (giây) | 193.2 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1325 |
| Lỗi duy nhất | 24 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /tasks` | 57 | 0 | 57 | 42 | 15 | 0 | 33 | có |
| `DELETE /tasks/{id}` | 61 | 32 | 29 | 0 | 61 | 0 | 33 | có |
| `GET /tasks` | 79 | 0 | 79 | 30 | 49 | 0 | 31 | có |
| `GET /tasks/groupBy` | 97 | 0 | 97 | 13 | 84 | 0 | 89 | có |
| `GET /tasks/{id}` | 68 | 29 | 39 | 22 | 46 | 0 | 29 | có |
| `PATCH /tasks` | 130 | 0 | 130 | 1 | 129 | 0 | 1 | có |
| `PATCH /tasks/merge` | 95 | 0 | 95 | 2 | 93 | 0 | 1 | có |
| `PATCH /tasks/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /tasks/{id}` | 135 | 29 | 106 | 16 | 119 | 0 | 17 | có |
| `PATCH /tasks/{id}/restore` | 70 | 28 | 42 | 25 | 45 | 0 | 30 | có |
| `POST /batch/tasks` | 159 | 0 | 159 | 37 | 122 | 0 | 9 | có |
| `POST /tasks` | 151 | 0 | 151 | 9 | 142 | 0 | 9 | có |
| `POST /tasks/duplicates` | 158 | 27 | 131 | 24 | 134 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 171 |
| 201 | 43 |
| 204 | 8 |
| 400 | 1030 |
| 403 | 13 |
| 404 | 60 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1192 | 63 |
| not_a_server_error | 1325 | 0 |
| response_schema_conformance | 1138 | 484 |
| status_code_conformance | 1120 | 135 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 32 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string) |
| 2 | `DELETE /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 33 | Documented: 200, 400, 401 |
| 4 | `GET /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 21 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `maximum` at /properties/limit |
| 5 | `GET /tasks` | response_schema_conformance | JsonSchemaError | high | 122 |     null |
| 6 | `GET /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 7 | `GET /tasks/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 8 | `GET /tasks/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 9 | `GET /tasks/{id}` | response_schema_conformance | JsonSchemaError | high | 88 |     null |
| 10 | `GET /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 8 | Documented: 200, 400, 401 |
| 11 | `PATCH /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 12 | `PATCH /tasks/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `PATCH /tasks/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /tasks/{id}` | response_schema_conformance | JsonSchemaError | high | 66 |     null |
| 15 | `PATCH /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 16 | `PATCH /tasks/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 98 |     null |
| 17 | `PATCH /tasks/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 6 | Documented: 200, 400, 401 |
| 18 | `POST /batch/tasks` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 19 | `POST /batch/tasks` | response_schema_conformance | JsonSchemaError | high | 50 |     null |
| 20 | `POST /batch/tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 21 | `POST /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 22 | `POST /tasks` | response_schema_conformance | JsonSchemaError | high | 50 |     null |
| 23 | `POST /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 24 | `POST /tasks/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
