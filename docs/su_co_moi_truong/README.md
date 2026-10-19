# Sự cố môi trường và giao diện (ngoài phạm vi K05)

Người phụ trách: Tuấn. Thư mục này ghi lỗi gặp khi **dựng và dùng** Twenty `v2.45.6` (cài đặt, onboarding, giao diện).
Lỗi **API** do Schemathesis tìm ra (cuối kỳ) ghi ở danh sách lỗi của Phần G, không ghi ở đây.
Nhóm không sửa mã Twenty: mục tiêu là ghi nhận và đưa ra cách đi vòng (workaround) để người sau dựng lại không bị kẹt.

## Danh sách

| ID | Tiêu đề | Mức độ | Tần suất | Workaround | Trạng thái |
|---|---|---|---|---|---|
| [ENV_01](ENV_01_install_apps_bo_qua.md) | Trang Install apps: bấm "Bỏ qua" không chuyển trang | Trung bình | 1/1 lần (17/10) | Gõ thẳng `localhost:3001/objects/companies` | Mới |
| [ENV_02](ENV_02_nhan_dich_tron_ngon_ngu.md) | Nhãn giao diện trộn tiếng Việt và tiếng Anh, có dấu ngoặc kép thừa | Thấp | Luôn luôn | Không cần | Mới |

## Mẫu ghi một lỗi

Mỗi lỗi một file `ENV_NN_ten_ngan.md`, ảnh để trong `anh/`. Các mục bắt buộc:

- **Môi trường:** phiên bản, hệ điều hành, trình duyệt
- **Các bước tái hiện:** đánh số, người khác làm theo được
- **Kết quả mong đợi** và **kết quả thực tế**
- **Mức độ** (ảnh hưởng tới người dùng) và **tần suất** (bao nhiêu lần gặp / bao nhiêu lần thử)
- **Bằng chứng:** ảnh, nội dung thông báo lỗi
- **Workaround** nếu có, và **điều chưa biết**
