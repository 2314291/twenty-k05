# Thống kê lần chạy `20261126-111735-seed20261020-notes`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-26T04:19:13.141931+00:00 |
| Thời gian chạy (giây) | 171.1 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1195 |
| Lỗi duy nhất | 26 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /notes` | 57 | 0 | 57 | 48 | 9 | 0 | 32 | có |
| `DELETE /notes/{id}` | 21 | 5 | 16 | 6 | 15 | 0 | 6 | chưa |
| `GET /notes` | 79 | 0 | 79 | 26 | 53 | 0 | 27 | có |
| `GET /notes/groupBy` | 97 | 0 | 97 | 12 | 85 | 0 | 89 | có |
| `GET /notes/{id}` | 68 | 28 | 40 | 25 | 43 | 0 | 31 | có |
| `PATCH /notes` | 112 | 0 | 112 | 1 | 111 | 0 | 2 | có |
| `PATCH /notes/merge` | 95 | 0 | 95 | 1 | 94 | 0 | 1 | có |
| `PATCH /notes/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /notes/{id}` | 117 | 28 | 89 | 27 | 90 | 0 | 28 | có |
| `PATCH /notes/{id}/restore` | 70 | 31 | 39 | 31 | 39 | 0 | 33 | có |
| `POST /batch/notes` | 141 | 0 | 141 | 29 | 112 | 0 | 29 | có |
| `POST /notes` | 133 | 0 | 133 | 9 | 124 | 0 | 9 | có |
| `POST /notes/duplicates` | 140 | 9 | 131 | 27 | 113 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 199 |
| 201 | 36 |
| 204 | 8 |
| 400 | 911 |
| 403 | 13 |
| 404 | 28 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1061 | 64 |
| not_a_server_error | 1195 | 0 |
| response_schema_conformance | 990 | 429 |
| status_code_conformance | 1022 | 103 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /notes` | negative_data_rejection | AcceptedNegativeData | medium | 31 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer) |
| 2 | `DELETE /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /notes/{id}` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became number) |
| 4 | `DELETE /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 5 | Documented: 200, 400, 401 |
| 5 | `GET /notes` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `maximum` at /properties/limit |
| 6 | `GET /notes` | response_schema_conformance | JsonSchemaError | high | 104 |     null |
| 7 | `GET /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 8 | `GET /notes/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 9 | `GET /notes/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 10 | `GET /notes/{id}` | response_schema_conformance | JsonSchemaError | high | 72 |     null |
| 11 | `GET /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 7 | Documented: 200, 400, 401 |
| 12 | `PATCH /notes` | response_schema_conformance | JsonSchemaError | high | 4 |     null |
| 13 | `PATCH /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /notes/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 15 | `PATCH /notes/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 16 | `PATCH /notes/{id}` | response_schema_conformance | JsonSchemaError | high | 81 |     null |
| 17 | `PATCH /notes/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 18 | `PATCH /notes/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 90 |     null |
| 19 | `PATCH /notes/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 20 | `POST /batch/notes` | negative_data_rejection | AcceptedNegativeData | medium | 25 | Invalid component: parameter `upsert` in query - upsert: Incorrect type; Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became string) |
| 21 | `POST /batch/notes` | response_schema_conformance | JsonSchemaError | high | 36 |     null |
| 22 | `POST /batch/notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 23 | `POST /notes` | negative_data_rejection | AcceptedNegativeData | medium | 5 | Invalid component: parameter `upsert` in query - upsert: Incorrect type |
| 24 | `POST /notes` | response_schema_conformance | JsonSchemaError | high | 32 |     null |
| 25 | `POST /notes` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 26 | `POST /notes/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
