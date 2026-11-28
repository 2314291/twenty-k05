# Kiểm chứng tay vấn đề A: tham số boolean không được kiểm tra kiểu

Ngày: 26/11/2026. Twenty v2.45.6 local. Người kiểm: Thuận. Mỗi ca dùng bản ghi tạo riêng `K05-A-*`, đã dọn sau khi kiểm.

## Schema khai báo

| Tham số | Operation | Schema |
|---|---|---|
| `soft_delete` | `DELETE /{object}`, `DELETE /{object}/{id}` | `boolean`, default `false`. "If true, soft deletes… If false, permanently deleted" |
| `upsert` | `POST /{object}`, `POST /batch/{object}` | `boolean`, default `false` |

Theo schema, giá trị không phải `true`/`false` phải bị từ chối bằng 400.

## A1. `soft_delete` (DELETE /companies/{id}, sau đó PATCH /companies/{id}/restore)

| `soft_delete=` | DELETE | Restore | Kết luận |
|---|---|---|---|
| `true` | 200 | 200 | Xóa mềm (đúng) |
| `false` | 200 | 404 | Xóa vĩnh viễn (đúng) |
| (không gửi) | 200 | 404 | Xóa vĩnh viễn (đúng default) |
| `abc` | 200 | 404 | **Nhận giá trị sai, xóa vĩnh viễn** |
| `-1` | 200 | 404 | **Nhận giá trị sai, xóa vĩnh viễn** |
| `1` | 200 | 404 | **Nhận, xóa vĩnh viễn** |
| `TRUE`, `True` | 200 | 404 | **Nhận, xóa vĩnh viễn** |

## A2. `upsert` (POST /batch/companies với `id` đã tồn tại)

| `upsert=` | Mã | Kết quả |
|---|---|---|
| `true` | 201 | Cập nhật bản ghi (đúng) |
| `false` | 400 | `A duplicate entry was detected…` (đúng) |
| `abc`, `-1` | 400 | Như `false`: không báo sai tham số mà báo trùng khóa |
| `abc`, `-1`, `null`, `2` với id mới | 201 | Nhận giá trị sai, tạo bình thường |

## Kết luận

- **Hiện tượng:** server không kiểm tra kiểu của tham số boolean. Chỉ đúng chuỗi `true` được hiểu là bật; **mọi giá trị khác (kể cả `1`, `TRUE`) bị lặng lẽ coi là `false`**, không trả 400.
- **Phân loại:** lỗi chức năng (thiếu kiểm tra input), vi phạm bất biến I4 (`negative_data_rejection`). Không phải H3: mã 2xx, không phải 400 che lỗi.
- **Mức độ:** cao với `soft_delete`. Người gọi gửi `soft_delete=1` hoặc `TRUE` với ý xóa mềm thì bản ghi **bị xóa vĩnh viễn, không khôi phục được**, và server vẫn báo thành công.
- **Phạm vi:** cả 5 object (Schemathesis báo cùng lỗi ở Companies, People, Opportunities, Notes, Tasks).
- **Module nghi ngờ:** `api/rest/input-request-parsers/` (phần đọc `soft_delete`, `upsert`). Cần đọc mã nguồn v2.45.6 để xác nhận dòng code.

## Reproducer

```bash
# Thay <KEY>. Tạo bản ghi thử, xóa với soft_delete=1, rồi thử khôi phục.
ID=$(curl -s -X POST -H 'Authorization: Bearer <KEY>' -H 'Content-Type: application/json' \
  -d '{"name":"K05-A-repro"}' http://localhost:3001/rest/companies | python -c "import sys,json;print(json.load(sys.stdin)['data']['createCompany']['id'])")
curl -s -X DELETE -H 'Authorization: Bearer <KEY>' "http://localhost:3001/rest/companies/$ID?soft_delete=1"   # 200 (kỳ vọng 400)
curl -s -X PATCH  -H 'Authorization: Bearer <KEY>' "http://localhost:3001/rest/companies/$ID/restore"        # 404: đã mất vĩnh viễn
```
