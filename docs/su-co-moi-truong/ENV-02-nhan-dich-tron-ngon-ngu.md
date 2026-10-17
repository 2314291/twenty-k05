# ENV-02. Nhãn giao diện trộn tiếng Việt và tiếng Anh, có dấu ngoặc kép thừa

| Mục | Nội dung |
|---|---|
| Ngày gặp | 17/10/2026, Tuấn |
| Môi trường | Twenty `v2.45.6`, cổng 3001; Chrome, ngôn ngữ trình duyệt tiếng Việt (giao diện tự chuyển sang tiếng Việt) |
| Mức độ | Thấp: chỉ ảnh hưởng thẩm mỹ, không chặn chức năng. Ngoài phạm vi K05 (K05 chỉ kiểm thử API) |
| Tần suất | Luôn luôn |
| Trạng thái | Mới |

## Các bước tái hiện

1. Dùng trình duyệt ngôn ngữ tiếng Việt, tạo tài khoản mới ở `http://localhost:3001`.
2. Đến trang `/create/profile` ("Tạo hồ sơ"): quan sát nhãn hai ô tên.
3. Vào trang Công ty (`/objects/companies`): quan sát nút lọc góc trên bên phải.

## Kết quả

| Vị trí | Mong đợi | Thực tế |
|---|---|---|
| `/create/profile`, ô thứ nhất | `Tên riêng` | `"Tên riêng"` (có dấu ngoặc kép) |
| `/create/profile`, ô thứ hai | `Họ` | `Last name` (chưa dịch) |
| `/objects/companies`, nút lọc | `Lọc` | `"Lọc"` (có dấu ngoặc kép) |

Nhận định: bản dịch tiếng Việt của Twenty chưa hoàn chỉnh; dấu ngoặc kép có vẻ nằm sẵn trong chuỗi dịch.

## Bằng chứng

- `anh/ENV-02-create-profile.png`: trang `/create/profile`.
- `../../evidence/03-companies.png`: nút `"Lọc"` trên trang Công ty.

## Workaround

Không cần. Nếu muốn giao diện thống nhất khi chụp bằng chứng cho báo cáo, đổi ngôn ngữ trong Settings của Twenty sang English.
