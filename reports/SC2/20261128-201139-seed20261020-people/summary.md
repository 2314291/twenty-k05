# Thống kê lần chạy `20261128-201139-seed20261020-people`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-28T13:13:17.126299+00:00 |
| Thời gian chạy (giây) | 205.4 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1871 |
| Lỗi duy nhất | 22 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /people` | 57 | 0 | 57 | 50 | 7 | 0 | 14 | có |
| `DELETE /people/{id}` | 27 | 9 | 18 | 0 | 27 | 0 | 3 | chưa |
| `GET /people` | 79 | 0 | 79 | 38 | 41 | 0 | 39 | có |
| `GET /people/groupBy` | 97 | 0 | 97 | 13 | 84 | 0 | 89 | có |
| `GET /people/{id}` | 68 | 39 | 29 | 38 | 30 | 0 | 28 | có |
| `PATCH /people` | 246 | 1 | 245 | 22 | 224 | 0 | 1 | có |
| `PATCH /people/merge` | 95 | 0 | 95 | 2 | 93 | 0 | 1 | có |
| `PATCH /people/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /people/{id}` | 251 | 31 | 220 | 25 | 226 | 0 | 26 | có |
| `PATCH /people/{id}/restore` | 70 | 31 | 39 | 32 | 38 | 0 | 27 | có |
| `POST /batch/people` | 275 | 0 | 275 | 18 | 257 | 0 | 17 | có |
| `POST /people` | 267 | 2 | 265 | 1 | 266 | 0 | 1 | có |
| `POST /people/duplicates` | 274 | 33 | 241 | 33 | 241 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 249 |
| 201 | 16 |
| 204 | 8 |
| 400 | 1565 |
| 403 | 13 |
| 404 | 20 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1770 | 31 |
| not_a_server_error | 1871 | 0 |
| response_schema_conformance | 1676 | 526 |
| status_code_conformance | 1706 | 95 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /people` | negative_data_rejection | AcceptedNegativeData | medium | 13 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became number); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string) |
| 2 | `DELETE /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 4 | `GET /people` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `minimum`, `maximum` at /properties/limit |
| 5 | `GET /people` | response_schema_conformance | JsonSchemaError | high | 202 |     null;     } |
| 6 | `GET /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 7 | `GET /people/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 8 | `GET /people/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 9 | `GET /people/{id}` | response_schema_conformance | JsonSchemaError | high | 113 |     null;     } |
| 10 | `GET /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 11 | `PATCH /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 12 | `PATCH /people/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `PATCH /people/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /people/{id}` | response_schema_conformance | JsonSchemaError | high | 100 |     null |
| 15 | `PATCH /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 16 | `PATCH /people/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 96 |     null |
| 17 | `PATCH /people/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 18 | `POST /batch/people` | negative_data_rejection | AcceptedNegativeData | medium | 16 | Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became null); Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became string) |
| 19 | `POST /batch/people` | response_schema_conformance | JsonSchemaError | high | 5 |     null |
| 20 | `POST /batch/people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 21 | `POST /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 22 | `POST /people/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
