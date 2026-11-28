# Thống kê lần chạy `20261126-110828-seed20261020-people`

| Mục | Giá trị |
|---|---|
| Schemathesis | 4.31.1 |
| Seed | 20261020 |
| Bắt đầu (UTC) | 2026-11-26T04:09:09.032028+00:00 |
| Thời gian chạy (giây) | 207.5 |
| Exit code | 1 |
| Phase | examples=skip, coverage=failure, fuzzing=failure, stateful=skip |
| Test case sinh ra | 1862 |
| Lỗi duy nhất | 23 |

**Độ phủ operation:** 13/13 = 100% trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: 0.

## Theo operation

| Operation | Test case | Dương | Âm | 2xx | 4xx | 5xx | Case lỗi | ≥50 case |
|---|---|---|---|---|---|---|---|---|
| `DELETE /people` | 57 | 0 | 57 | 50 | 7 | 0 | 14 | có |
| `DELETE /people/{id}` | 18 | 3 | 15 | 5 | 13 | 0 | 4 | chưa |
| `GET /people` | 79 | 0 | 79 | 38 | 41 | 0 | 39 | có |
| `GET /people/groupBy` | 97 | 0 | 97 | 12 | 85 | 0 | 89 | có |
| `GET /people/{id}` | 68 | 39 | 29 | 38 | 30 | 0 | 28 | có |
| `PATCH /people` | 246 | 37 | 209 | 17 | 229 | 0 | 1 | có |
| `PATCH /people/merge` | 95 | 0 | 95 | 1 | 94 | 0 | 1 | có |
| `PATCH /people/restore` | 65 | 0 | 65 | 1 | 64 | 0 | 1 | có |
| `PATCH /people/{id}` | 251 | 31 | 220 | 26 | 225 | 0 | 27 | có |
| `PATCH /people/{id}/restore` | 70 | 31 | 39 | 32 | 38 | 0 | 27 | có |
| `POST /batch/people` | 275 | 0 | 275 | 17 | 258 | 0 | 17 | có |
| `POST /people` | 267 | 2 | 265 | 1 | 266 | 0 | 1 | có |
| `POST /people/duplicates` | 274 | 33 | 241 | 32 | 242 | 0 | 1 | có |

## Mã trạng thái

| Mã | Số lần |
|---|---|
| 200 | 246 |
| 201 | 16 |
| 204 | 8 |
| 400 | 1559 |
| 403 | 13 |
| 404 | 20 |

## Theo check

| Check | Đạt | Lỗi |
|---|---|---|
| negative_data_rejection | 1760 | 32 |
| not_a_server_error | 1862 | 0 |
| response_schema_conformance | 1666 | 490 |
| status_code_conformance | 1697 | 95 |

## Lỗi duy nhất

| # | Operation | Check | Loại | Mức | Lần gặp | Biến thể (dòng cuối thông điệp) |
|---|---|---|---|---|---|---|
| 1 | `DELETE /people` | negative_data_rejection | AcceptedNegativeData | medium | 13 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became number); Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became string) |
| 2 | `DELETE /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 3 | `DELETE /people/{id}` | negative_data_rejection | AcceptedNegativeData | medium | 1 | Invalid component: parameter `soft_delete` in query - violates `type` at /properties/soft_delete (was boolean, became integer) |
| 4 | `DELETE /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 5 | `GET /people` | negative_data_rejection | AcceptedNegativeData | medium | 2 | Invalid component: parameter `limit` in query - limit: Value greater than maximum; Invalid component: parameter `limit` in query - violates `minimum`, `maximum` at /properties/limit |
| 6 | `GET /people` | response_schema_conformance | JsonSchemaError | high | 162 |     null;     } |
| 7 | `GET /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 8 | `GET /people/groupBy` | response_schema_conformance | JsonSchemaError | high | 10 |     ] |
| 9 | `GET /people/groupBy` | status_code_conformance | UndefinedStatusCode | medium | 79 | Documented: 200 |
| 10 | `GET /people/{id}` | response_schema_conformance | JsonSchemaError | high | 113 |     null;     } |
| 11 | `GET /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 12 | `PATCH /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 13 | `PATCH /people/merge` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 14 | `PATCH /people/restore` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 15 | `PATCH /people/{id}` | response_schema_conformance | JsonSchemaError | high | 104 |     null |
| 16 | `PATCH /people/{id}` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
| 17 | `PATCH /people/{id}/restore` | response_schema_conformance | JsonSchemaError | high | 96 |     null |
| 18 | `PATCH /people/{id}/restore` | status_code_conformance | UndefinedStatusCode | medium | 3 | Documented: 200, 400, 401 |
| 19 | `POST /batch/people` | negative_data_rejection | AcceptedNegativeData | medium | 16 | Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became null); Invalid component: parameter `upsert` in query - violates `type` at /properties/upsert (was boolean, became string) |
| 20 | `POST /batch/people` | response_schema_conformance | JsonSchemaError | high | 5 |     null |
| 21 | `POST /batch/people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 22 | `POST /people` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 201, 400, 401 |
| 23 | `POST /people/duplicates` | status_code_conformance | UndefinedStatusCode | medium | 1 | Documented: 200, 400, 401 |
