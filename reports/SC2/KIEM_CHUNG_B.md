# Kiểm chứng tay vấn đề B: `limit` vượt `maximum` (và phát hiện thêm B2)

Ngày: 26/11/2026. Twenty v2.45.6 local. Người kiểm: Thuận. Tạo tạm 200 công ty `K05-B-*` (tổng 236), kiểm xong đã xóa (còn 36 như trước).

## Schema khai báo

`GET /{object}` tham số `limit`: `{"type": "integer", "minimum": 0, "maximum": 200, "default": 60}`.

## B1. `limit` > 200 bị cắt âm thầm về 200

| `limit=` | Mã | Số bản ghi trả về | Kỳ vọng theo schema |
|---|---|---|---|
| (không gửi) | 200 | 60 | 60 (default) ✅ |
| `200` | 200 | 200 | 200 ✅ |
| `201` | 200 | **200** | 400 ❌ |
| `500` | 200 | **200** | 400 ❌ |
| `99999` | 200 | **200** | 400 ❌ |
| `0` | 200 | 0 | 0 ✅ |

- **Hiện tượng:** giá trị vượt `maximum` không bị từ chối mà bị cắt về 200, không có thông báo. `hasNextPage=true` nên người gọi vẫn phân trang tiếp được.
- **Phân loại:** lệch schema (đúng dự đoán H1 trong `docs/SPEC.md`). Hành vi là thiết kế có chủ ý trong mã (`QueryMaxRecords`, `parse-limit-rest-request.util.ts`), nhưng schema lại khai `maximum: 200` nên Schemathesis coi là "nhận dữ liệu sai".
- **Mức độ:** thấp. Không mất dữ liệu; rủi ro là người gọi tưởng nhận đủ số đã xin.
- **Hướng sửa:** hoặc server trả 400 khi `limit > 200`, hoặc schema bỏ `maximum` và ghi rõ "giá trị lớn hơn bị cắt về 200".

## B2 (mới). `limit` thập phân làm lộ lỗi database

| `limit=` | Mã | `messages` |
|---|---|---|
| `1.5` | 400 | `invalid input syntax for type bigint: "2.5"` |
| `10.7` | 400 | `invalid input syntax for type bigint: "11.7"` |
| `0.1` | 400 | `invalid input syntax for type bigint: "1.1"` |

- **Hiện tượng:** mã 400 trông như "từ chối đúng", nhưng thông điệp là **lỗi của PostgreSQL**. Parser không kiểm tra `limit` là số nguyên; giá trị đi thẳng xuống câu SQL (cộng thêm 1, để biết còn trang sau), database báo lỗi, rồi bộ lọc lỗi đổi thành 400.
- **Đây đúng là bẫy H3** (lỗi nội bộ hiện thành 400). Schemathesis không báo vì mã 400 hợp lệ; chỉ đọc `messages` mới thấy.
- **Phân loại:** lỗi chức năng: thiếu kiểm tra input, và lộ chi tiết nội bộ (kiểu cột `bigint`, cách tính `limit + 1`).
- **Mức độ:** trung bình. Không làm hỏng dữ liệu, nhưng lộ thông tin bên trong. Lẽ ra phải báo như `limit=abc`: `limit '1.5' is invalid. Should be an integer`.
- **Module nghi ngờ:** `api/rest/input-request-parsers/` (parse `limit`) và `rest-api-exception.filter.ts` (đổi lỗi DB thành 400).

## Reproducer

```bash
# B1: xin 500, nhận 200 bản ghi (cần > 200 bản ghi trong DB để thấy)
curl -s -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=500&fields=id'
# B2: lộ lỗi PostgreSQL
curl -s -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=1.5'
# -> 400 {"messages":["invalid input syntax for type bigint: \"2.5\""]}
```
