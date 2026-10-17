# ENV_01. Trang Install apps: bấm "Bỏ qua" không chuyển trang

| Mục | Nội dung |
|---|---|
| Ngày gặp | 17/10/2026, Tuấn |
| Môi trường | Twenty `v2.45.6` (image `twentycrm/twenty:v2.45.6`) qua `env/docker-compose.yml`, cổng 3001; Windows 11, Docker Desktop, Chrome |
| Mức độ | Trung bình: chặn người mới ở bước onboarding, nhưng có cách đi vòng |
| Tần suất | 1/1 lần thử ở `/install-apps`. Ở trang `/invite-team`, nút "Bỏ qua" cùng kiểu chạy bình thường |
| Trạng thái | Mới |

## Các bước tái hiện

1. Dựng instance sạch: `docker compose down -v`, rồi `docker compose up -d` trong `env/`, chờ server `healthy`.
2. Mở `http://localhost:3001`, chọn "Tiếp tục với Email", tạo tài khoản và workspace mới.
3. Đến trang `http://localhost:3001/install-apps` ("Start with the essentials").
4. Bấm **Bỏ qua**.

## Kết quả

| Mong đợi | Thực tế |
|---|---|
| Chuyển sang bước onboarding tiếp theo (`/create/profile`) | Trang đứng yên, không chuyển, không hiện thông báo |

Khoanh vùng:

| Thử | Kết quả |
|---|---|
| Nhấn F5 tải lại trang | Báo lỗi (nội dung chưa ghi lại) |
| Gõ thẳng địa chỉ `http://localhost:3001/objects/companies` | Vào được, hệ thống chuyển sang `/create/profile`, onboarding tiếp tục bình thường |

Kết luận tạm: thao tác "Bỏ qua" đã được server ghi nhận (lần vào sau hệ thống đi tiếp đúng bước), lỗi nằm ở **điều hướng phía giao diện** của trang `/install-apps`.

## Workaround

Khi kẹt ở trang Install apps, gõ thẳng `http://localhost:3001/objects/companies` vào thanh địa chỉ. Không cần tạo lại workspace.

## Bằng chứng

- `anh/ENV_01_install_apps.png`: trang `/install-apps` trước khi bấm.

## Chưa biết

- Nội dung lỗi khi nhấn F5 (lần sau chụp lại).
- Lỗi có lặp lại trên instance sạch khác không: cần một người khác thử theo các bước trên (Thuận dựng lại ngày 19/10).
- Lỗi trong tab Console của trình duyệt (F12) lúc bấm.
