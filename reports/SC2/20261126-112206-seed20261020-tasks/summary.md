# Thống kê lần chạy `20261126-112206-seed20261020-tasks`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-26T04:23:40.136772+00:00 |
| Thời gian chạy (giây) | 178.3 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1282 |
| Lỗi duy nhất | 26 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /tasks` | 57 | 0 | 57 | 42 | 15 | 0 | 33 | có |
| `DELETE /tasks/{id}` | 18 | 2 | 16 | 6 | 12 | 0 | 4 | chưa |
| `GET /tasks` | 79 | 0 | 79 | 30 | 49 | 0 | 31 | có |
| `GET /tasks/groupBy` | 97 | 0 | 97 | 12 | 85 | 0 | 89 | có |
| `GET /tasks/{id}` | 68 | 29 | 39 | 22 | 46 | 0 | 29 | có |
| `PATCH /tasks` | 130 | 0 | 130 | 1 | 129 | 0 | 2 | có |
| `PATCH /tasks/merge` | 95 | 0 | 95 | 1 | 94 | 0 | 1 | có |
| `PATCH /tasks/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /tasks/{id}` | 135 | 29 | 106 | 16 | 119 | 0 | 17 | có |
| `PATCH /tasks/{id}/restore` | 70 | 28 | 42 | 25 | 45 | 0 | 30 | có |
| `POST /batch/tasks` | 159 | 0 | 159 | 36 | 123 | 0 | 9 | có |
| `POST /tasks` | 151 | 0 | 151 | 9 | 142 | 0 | 9 | có |
| `POST /tasks/duplicates` | 158 | 27 | 131 | 23 | 135 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 173 |
| 201 | 43 |
| 204 | 8 |
| 400 | 1016 |
| 403 | 13 |
| 404 | 29 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1147 | 65 |
| not_a_server_error | 1282 | 0 |
| response_schema_conformance | 1094 | 550 |
| status_code_conformance | 1108 | 104 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 32 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string) |
| 2 | `DELETE /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /tasks/{id}` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer) |
| 4 | `DELETE /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 2 | Documented: 200, 400, 401 |
| 5 | `GET /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 21 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `maximum` at /properties/limit |
| 6 | `GET /tasks` | response_schema_conformance | JsonSchemaError | high | 182 |     null |
| 7 | `GET /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 8 | `GET /tasks/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 9 | `GET /tasks/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 10 | `GET /tasks/{id}` | response_schema_conformance | JsonSchemaError | high | 88 |     null |
| 11 | `GET /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 8 | Documented: 200, 400, 401 |
| 12 | `PATCH /tasks` | response_schema_conformance | JsonSchemaError | high | 6 |     null |
| 13 | `PATCH /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /tasks/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 15 | `PATCH /tasks/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 16 | `PATCH /tasks/{id}` | response_schema_conformance | JsonSchemaError | high | 66 |     null |
| 17 | `PATCH /tasks/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 18 | `PATCH /tasks/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 98 |     null |
| 19 | `PATCH /tasks/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 6 | Documented: 200, 400, 401 |
| 20 | `POST /batch/tasks` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 21 | `POST /batch/tasks` | response_schema_conformance | JsonSchemaError | high | 50 |     null |
| 22 | `POST /batch/tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 23 | `POST /tasks` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 24 | `POST /tasks` | response_schema_conformance | JsonSchemaError | high | 50 |     null |
| 25 | `POST /tasks` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 26 | `POST /tasks/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
