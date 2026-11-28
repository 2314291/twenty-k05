# Kiểm chứng tay vấn đề E (`groupBy`) và F (404 không khai báo)

Ngày: 26/11/2026. Twenty v2.45.6 local. Người kiểm: Thuận. Chỉ đọc hoặc dùng id không tồn tại, không thay đổi dữ liệu.

## E. `GET /{object}/groupBy`: schema mô tả sai cả mã trạng thái lẫn cấu trúc body

Schema khai: chỉ có response `200`; body `{"data": {"companiesGroupBy": [ {groupByDimensionValues: [string], ...số tổng hợp: number} ]}}`.

| Ca | Request | Thực tế | Trái schema ở đâu |
|---|---|---|---|
| E1 | `group_by=[{"updatedAt":true}]` (ví dụ có sẵn trong schema) | 200, body là **mảng trần** `[{"groupByDimensionValues":[...]}]` | Thiếu lớp `data.companiesGroupBy`; schema khai object, thực tế là array |
| E1b | thêm `aggregate=["countNotEmptyId"]` | 200, `"countNotEmptyId": "1"` | Giá trị tổng hợp là **chuỗi** `"1"`, schema khai `number` |
| E1c | nhóm theo `name` | có phần tử `"groupByDimensionValues": [null]` | `items` khai `string`, không cho `null` (cùng gốc với C) |
| E2 | thiếu `group_by` / `group_by=` rỗng | 400 `Invalid group_by query parameter - should be a valid array of objects…` | Từ chối đúng, nhưng **mã 400 không được khai** (schema chỉ có 200) |
| E2b | `group_by=[{"khongCo":true}]` | 400 `Unidentified field in groupBy: khongCo` | Như trên |
| E3 | `limit=0.5` | 200, bỏ qua `limit` | Nhận dữ liệu sai (khác `GET /companies`, nơi `limit=1.5` gây lỗi DB — B2) |
| E3b | `view_id=0` (không phải UUID) | 200, bỏ qua | Nhận dữ liệu sai |

- **Phân loại:** chủ yếu **lệch schema**: tài liệu `groupBy` mô tả sai cấu trúc body, sai kiểu số tổng hợp, thiếu mã 400. Hành vi từ chối của server ở E2 là đúng.
  E3/E3b là **lỗi chức năng nhỏ** (tham số sai bị lặng lẽ bỏ qua), cùng họ với A.
- **Mức độ:** trung bình. Client sinh code từ schema sẽ **không đọc được** kết quả `groupBy` (tìm `data.companiesGroupBy` mà không có).
- **Phạm vi:** cả 5 object (Schemathesis báo y hệt: 79 lần mã không khai + 10 lần body sai ở mỗi object).
- **Module nghi ngờ:** `core-modules/open-api/` (phần sinh schema cho `groupBy`); E3 ở `api/rest/input-request-parsers/` (parser riêng của `groupBy`).

## F. Operation theo `{id}`: trả 404 nhưng schema không khai 404

Schema khai cho `GET`, `PATCH`, `DELETE /{object}/{id}` và `PATCH /{object}/{id}/restore`: chỉ `200, 400, 401`.

| Ca | Request | Thực tế |
|---|---|---|
| F1 | `GET/PATCH/DELETE /companies/{uuid không tồn tại}`, `PATCH …/restore` | 404 `{"error":"NotFoundException","messages":["Record not found"]}` |
| F1b | `GET /people/{uuid không tồn tại}`, `GET /tasks/{…}` | 404, như trên |
| F2 (đối chứng) | `GET /companies/abc`, `DELETE /companies/123` | 400 `'abc' is not a valid UUID` (đúng, có khai) |

- **Hiện tượng:** server phân biệt đúng "id sai định dạng" (400) và "id hợp lệ nhưng không có" (404) — đây là **hành vi đúng theo chuẩn HTTP**. Chỉ có tài liệu quên khai 404.
- **Phân loại:** **lệch schema** (thiếu response `404`). Server không sai.
- **Mức độ:** thấp. Client sinh code từ schema có thể coi 404 là "lỗi không mong đợi".
- **Phạm vi:** cả 5 object, 4 operation theo id mỗi object (20 operation).
- **Module nghi ngờ:** `core-modules/open-api/` (danh sách response sinh cho operation theo id không có 404).

## Reproducer

```bash
# E1: body groupBy không có data.companiesGroupBy
curl -s -G -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/groupBy' \
  --data-urlencode 'group_by=[{"updatedAt":true}]'
# E2: 400 không khai báo
curl -s -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/groupBy'
# F1: 404 không khai báo
curl -s -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/00000000-0000-4000-8000-000000000000'
```
