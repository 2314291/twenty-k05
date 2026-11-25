# Dữ liệu SC5 và thiết kế SC6 (Trung)

Bổ sung cho `dac-ta-sc3-sc4.md`. Mục 1 chuẩn bị dữ liệu và khoá cho SC5 (xác thực), mục 2 thiết kế SC6 (chuỗi vòng đời bản ghi, kịch bản mở rộng).
Cột "Kỳ vọng" lấy từ schema và mã nguồn v2.45.6; cột "Kết quả" ghi lần chạy tay ngày 02/11/2026 trên instance thật.
SC6 đã chạy tay trên cả 5 đối tượng (02/11 và 12/11/2026); SC5 chưa chạy.

## 1. Dữ liệu cho SC5 (xác thực)

| Loại khoá | Cách có | Dùng để |
|---|---|---|
| Đủ quyền | Settings → API → tạo key, dán vào `.env` là `TWENTY_API_KEY` | Đối chứng: mọi thao tác thành công |
| Chỉ đọc | Tạo role chỉ bật quyền đọc 5 đối tượng, tạo key gán role đó, dán vào `.env` là `TWENTY_API_KEY_LIMITED` (xem `business-flows.md`) | Đọc → 200, ghi → 403 |
| Sai | Chuỗi bất kỳ, ví dụ `k05-sai-key-000000` | Kỳ vọng 401 |
| Không có | Không gửi header `Authorization` | Kỳ vọng 401 |

Điều kiện đầu: có ít nhất 1 công ty (chạy `seed.py --count 30`). Khoá thật không ghi vào bất kỳ tệp báo cáo nào.

## 2. Thiết kế SC6: chuỗi vòng đời bản ghi

Mục tiêu: kiểm tra những điều mà request rời rạc khó chạm tới, vì mỗi request cần id do request trước tạo ra.
Bất biến: bản ghi đã xoá thì không đọc lại được; sửa một trường không làm mất trường khác; id ổn định suốt chuỗi.
Áp dụng cho Companies, People, Opportunities, Notes, Tasks (cùng khuôn, khác body tạo, lấy từ các hàm `build_*` trong `seed.py`). Tên bản ghi dùng tiền tố `K05-SC6-`.

| Ca | Bước | Request | Kỳ vọng | Kết quả 02/11/2026 |
|---|---|---|---|---|
| S6-01 | Tạo | `POST /{obj}` body hợp lệ | 201, có `id` | 201. **Đạt** |
| S6-02 | Đọc lại | `GET /{obj}/{id}` | 200, trường khớp body đã gửi | 200; tên khớp, domain gửi `https://k05-sc6.example.com` được lưu thành `k05-sc6.example.com` (G-06). **Đạt** |
| S6-03 | Sửa một trường | `PATCH /{obj}/{id}` chỉ trường tên hoặc tiêu đề | 200 | 200. **Đạt** |
| S6-04 | Đọc sau sửa | `GET /{obj}/{id}` | 200, trường đã đổi, trường khác giữ nguyên | 200, tên mới, domain giữ nguyên. **Đạt** |
| S6-05 | Có trong danh sách | `GET /{obj}?filter=id[eq]:<id>` | 200, đúng 1 bản ghi | 200, 1 bản ghi. **Đạt** |
| S6-06 | Xoá | `DELETE /{obj}/{id}` (mặc định `soft_delete=false`, xoá vĩnh viễn) | 200 | 200. **Đạt** |
| S6-07 | Đọc sau xoá | `GET /{obj}/{id}` | 404 | 404. **Đạt** |
| S6-08 | Xoá lần hai | `DELETE /{obj}/{id}` | 404, không 5xx | 404. **Đạt** |
| S6-09 | Sửa sau xoá | `PATCH /{obj}/{id}` | 404, không 5xx | 404. **Đạt** |
| S6-10 | Khôi phục sau xoá vĩnh viễn | `PATCH /{obj}/{id}/restore` | 404 (sửa lại sau lần chạy, xem ghi chú) | 404. **Đạt** |
| S6-11 | Quan hệ | Tạo Company, tạo Person gắn Company, xoá Company, đọc Person | Quan sát: không 5xx; ghi lại `companyId` của Person | Person vẫn còn (200), `companyId` rỗng |
| S6-12 | Id lạ | `GET`, `PATCH`, `DELETE` với UUID không tồn tại | 404 | Cả ba 404. **Đạt** |
| S6-13 | Xoá mềm rồi khôi phục | Tạo mới; `DELETE ?soft_delete=true`; `GET`; `PATCH .../restore`; `GET` | 200; 404; 200; 200 | 200; 404; 200; 200. **Đạt** |

Ghi chú: thiết kế ban đầu của S6-10 kỳ vọng khôi phục được. Chạy thật thì 404, vì schema khai báo `DELETE` có tham số `soft_delete`
mặc định `false` (xoá vĩnh viễn). Đây là kỳ vọng sai, không phải lỗi; kỳ vọng S6-10 đã sửa thành 404 và thêm S6-13 để kiểm khôi phục sau xoá mềm.
Chạy tay ngày 02/11/2026 trên Companies và ngày 12/11/2026 trên People, Opportunities, Notes, Tasks (S6-01 đến S6-10 và S6-13, tất cả đạt; bảng chi tiết ở `test-case-trung.md` mục 7.1) (Trung, Twenty v2.45.6, Docker trên máy cá nhân); chạy lại tự động bằng `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc6`.

### G-06. Twenty bỏ phần `https://` khỏi `domainName.primaryLinkUrl`

| Mục | Nội dung |
|---|---|
| Loại | Twenty, quan sát (chuẩn hoá dữ liệu, không phải lỗi chức năng) |
| Bước tái hiện | `POST /rest/companies` với `"domainName":{"primaryLinkUrl":"https://k05-sc6.example.com"}`, rồi `GET /rest/companies/{id}` |
| Thực tế | Giá trị đọc lại là `k05-sc6.example.com` |
| Ảnh hưởng | So sánh "đọc lại bằng đúng giá trị đã gửi" sẽ báo lệch; kiểm thử dựa trên schema có thể coi đây là dữ liệu bị thay đổi |
| Mức độ | Thấp |
| Trạng thái | Ghi nhận |

## 3. Việc còn lại

1. Tạo role chỉ đọc và key thứ hai trên instance thật (mục 1), rồi chạy hai ca: key chỉ đọc đọc được (200), ghi bị từ chối (403).
