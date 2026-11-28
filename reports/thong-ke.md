# Thống kê kết quả K05 (Phần G)

Tạo bởi `python scripts/thong_ke.py` từ `reports/*/*/summary.json`. Mỗi dòng là lần chạy mới nhất; cột tái lập so tập nhóm lỗi (operation, check, loại) với lần chạy trước đó của cùng kịch bản và object.

## 1. Tổng quan theo kịch bản và object

| Kịch bản | Object | Lần chạy | Operation đã test | Test case | Operation ≥ 50 ca | 5xx | Nhóm lỗi | Tái lập |
|---|---|---|---|---|---|---|---|---|
| SC1 | companies | `20261128-120704-seed20261020-companies` | 13/13 | 2435 | 12/13 | 0 | 61 | chưa chạy lần 2 |
| SC1 | people | `20261128-122610-seed20261020-people` | 13/13 | 2499 | 12/13 | 0 | 61 | chưa chạy lần 2 |
| SC1 | opportunities | `20261128-124700-seed20261020-opportunities` | 13/13 | 1853 | 12/13 | 0 | 60 | chưa chạy lần 2 |
| SC1 | notes | `20261128-153719-seed20261020-notes` | 13/13 | 1637 | 13/13 | 0 | 59 | 98% (20261128-130049-seed20261020-notes) |
| SC1 | tasks | `20261128-130650-seed20261020-tasks` | 13/13 | 1752 | 13/13 | 0 | 58 | chưa chạy lần 2 |

## 2. Lỗi theo loại kiểm tra và object

Mỗi ô: số lần check báo lỗi / số lần check được chạy.

### SC1

| Check | companies | people | opportunities | notes | tasks |
|---|---|---|---|---|---|
| I1 không 5xx | 0/2413 | 0/2477 | 0/1831 | 0/1615 | 0/1730 |
| I2 mã trạng thái | 135/2343 | 140/2407 | 148/1761 | 129/1545 | 156/1660 |
| I3 body đúng schema | 1068/3239 | 604/2859 | 921/2523 | 759/2082 | 1080/2519 |
| I4 từ chối dữ liệu sai | 74/2343 | 135/2407 | 35/1761 | 13/1545 | 11/1660 |
| I5 nhận dữ liệu đúng | 561/2343 | 502/2407 | 486/1761 | 516/1545 | 539/1660 |
| I6 xác thực (ignored_auth) | 0/2343 | 0/2407 | 0/1761 | 0/1545 | 0/1660 |
| I6 xác thực (thiếu header) | 13/2413 | 13/2477 | 13/1831 | 13/1615 | 13/1730 |
| I7 Content-Type | 0/2343 | 0/2407 | 0/1761 | 0/1545 | 0/1660 |
| object_level_authorization | 0/2413 | 0/2477 | 0/1831 | 0/1615 | 0/1730 |
| max_response_time | 0/2413 | 0/2477 | 0/1831 | 0/1615 | 0/1730 |
| ensure_resource_availability | 0/2343 | 0/2407 | 0/1761 | 0/1545 | 0/1660 |
| response_headers_conformance | 0/2343 | 0/2407 | 0/1761 | 0/1545 | 0/1660 |
| unsupported_method | 39/2413 | 39/2477 | 39/1831 | 39/1615 | 39/1730 |
| use_after_free | 0/2343 | 0/2407 | 0/1761 | 0/1545 | 0/1660 |
| allow_header_conformance | 0/2413 | 0/2477 | 0/1831 | 0/1615 | 0/1730 |

## 3. Nhóm lỗi gộp xuyên object

Cùng một operation (đổi tên object thành `{obj}`), cùng check và loại lỗi được gộp một dòng.

| Kịch bản | Operation | Check | Loại lỗi | Số object | Object | Lần gặp |
|---|---|---|---|---|---|---|
| SC1 | `DELETE /{obj}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `DELETE /{obj}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 49 |
| SC1 | `DELETE /{obj}` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `DELETE /{obj}/{id}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `DELETE /{obj}/{id}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 95 |
| SC1 | `DELETE /{obj}/{id}` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 51 |
| SC1 | `GET /{obj}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `GET /{obj}` | I4 từ chối dữ liệu sai | AcceptedNegativeData | 5 | companies, people, opportunities, notes, tasks | 11 |
| SC1 | `GET /{obj}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 95 |
| SC1 | `GET /{obj}` | I3 body đúng schema | JsonSchemaError | 5 | companies, people, opportunities, notes, tasks | 1301 |
| SC1 | `GET /{obj}` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `GET /{obj}/groupBy` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `GET /{obj}/groupBy` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 319 |
| SC1 | `GET /{obj}/groupBy` | I3 body đúng schema | JsonSchemaError | 5 | companies, people, opportunities, notes, tasks | 50 |
| SC1 | `GET /{obj}/groupBy` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 580 |
| SC1 | `GET /{obj}/groupBy` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 30 |
| SC1 | `GET /{obj}/{id}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `GET /{obj}/{id}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 60 |
| SC1 | `GET /{obj}/{id}` | I3 body đúng schema | JsonSchemaError | 5 | companies, people, opportunities, notes, tasks | 747 |
| SC1 | `GET /{obj}/{id}` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 18 |
| SC1 | `GET /{obj}/{id}` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 10 |
| SC1 | `PATCH /{obj}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `PATCH /{obj}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 181 |
| SC1 | `PATCH /{obj}` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `PATCH /{obj}/merge` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `PATCH /{obj}/merge` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 216 |
| SC1 | `PATCH /{obj}/merge` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 6 |
| SC1 | `PATCH /{obj}/merge` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 30 |
| SC1 | `PATCH /{obj}/restore` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `PATCH /{obj}/restore` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 209 |
| SC1 | `PATCH /{obj}/restore` | I3 body đúng schema | JsonSchemaError | 5 | companies, people, opportunities, notes, tasks | 67 |
| SC1 | `PATCH /{obj}/restore` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `PATCH /{obj}/restore` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 30 |
| SC1 | `PATCH /{obj}/{id}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `PATCH /{obj}/{id}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 258 |
| SC1 | `PATCH /{obj}/{id}` | I3 body đúng schema | JsonSchemaError | 5 | companies, people, opportunities, notes, tasks | 657 |
| SC1 | `PATCH /{obj}/{id}/restore` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `PATCH /{obj}/{id}/restore` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 60 |
| SC1 | `PATCH /{obj}/{id}/restore` | I3 body đúng schema | JsonSchemaError | 5 | companies, people, opportunities, notes, tasks | 762 |
| SC1 | `PATCH /{obj}/{id}/restore` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 20 |
| SC1 | `POST /batch/{obj}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `POST /batch/{obj}` | I4 từ chối dữ liệu sai | AcceptedNegativeData | 5 | companies, people, opportunities, notes, tasks | 18 |
| SC1 | `POST /batch/{obj}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 352 |
| SC1 | `POST /batch/{obj}` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `POST /batch/{obj}` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 30 |
| SC1 | `POST /{obj}` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `POST /{obj}` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 349 |
| SC1 | `POST /{obj}` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `POST /{obj}` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 15 |
| SC1 | `POST /{obj}/duplicates` | I6 xác thực (thiếu header) | MissingHeaderNotRejected | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `POST /{obj}/duplicates` | I5 nhận dữ liệu đúng | RejectedPositiveData | 5 | companies, people, opportunities, notes, tasks | 361 |
| SC1 | `POST /{obj}/duplicates` | I2 mã trạng thái | UndefinedStatusCode | 5 | companies, people, opportunities, notes, tasks | 5 |
| SC1 | `POST /{obj}/duplicates` | unsupported_method | UnsupportedMethodResponse | 5 | companies, people, opportunities, notes, tasks | 30 |
| SC1 | `DELETE /{obj}` | I4 từ chối dữ liệu sai | AcceptedNegativeData | 4 | companies, people, opportunities, notes | 27 |
| SC1 | `PATCH /{obj}/{id}` | I2 mã trạng thái | UndefinedStatusCode | 4 | companies, people, opportunities, tasks | 9 |
| SC1 | `PATCH /{obj}/{id}/restore` | I2 mã trạng thái | UndefinedStatusCode | 4 | companies, people, opportunities, notes | 9 |
| SC1 | `POST /{obj}` | I4 từ chối dữ liệu sai | AcceptedNegativeData | 4 | companies, people, notes, tasks | 12 |
| SC1 | `PATCH /{obj}` | I4 từ chối dữ liệu sai | AcceptedNegativeData | 3 | companies, people, opportunities | 133 |
| SC1 | `PATCH /{obj}` | I3 body đúng schema | JsonSchemaError | 3 | companies, notes, tasks | 384 |
| SC1 | `PATCH /{obj}/{id}` | I4 từ chối dữ liệu sai | AcceptedNegativeData | 3 | companies, people, opportunities | 61 |
| SC1 | `POST /batch/{obj}` | I3 body đúng schema | JsonSchemaError | 3 | opportunities, notes, tasks | 101 |
| SC1 | `POST /{obj}` | I3 body đúng schema | JsonSchemaError | 3 | people, notes, tasks | 363 |
| SC1 | `POST /{obj}/duplicates` | I4 từ chối dữ liệu sai | AcceptedNegativeData | 3 | companies, people, opportunities | 6 |

