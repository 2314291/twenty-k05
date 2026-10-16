# Trạng thái Mốc 1 (20/10) — cập nhật 16/10/2026

Cột "Đã xong" = có sản phẩm trong repo. Cột "Cần người làm trên máy" = bước **bắt buộc** có Twenty đang chạy, tài khoản hoặc người thật. Chưa có số liệu chạy thật nào.

| Người | Đã xong (trong repo) | Cần người làm trên máy |
|---|---|---|
| **Tiến** | `test-plan.md` (D); `bao-cao-giua-ky.md` (khung A–H, ô `[ĐIỀN]`); `board-cards.csv`; `email-hoi-thay.md`; `demo-script.md`; slide nháp 11 trang (artifact) | Tạo board Trello/Jira và nhập CSV; tạo repo GitHub, đẩy mã, mỗi người ≥3 commit; **gửi email cho thầy**; xác nhận tag/SHA với bản đăng ký 18/9; điền số liệu vào báo cáo/slide sau khi chạy; tổng duyệt 19/10 |
| **Tuấn** | `env/docker-compose.yml` (cổng 3001), `env/.env.example`, `env/VERSION.txt`, `SETUP.md` | `docker compose up -d` trên máy chuẩn (trước 12:00 17/10); đặt mật khẩu/`ENCRYPTION_KEY`; chụp 7 ảnh bằng chứng; quay video dự phòng; kiểm tra tên menu và bước đăng ký trong `SETUP.md` |
| **Thuận** | `architecture.md` (A, B, 5 data flow, 7 phát hiện từ mã nguồn) | Đối chiếu nhanh với instance; vẽ lại 2 sơ đồ Mermaid thành hình nếu thầy yêu cầu; dựng lại từ máy sạch theo README (19/10) |
| **Trung** | `fetch_schema.py`, `list_operations.py`, `seed.py`, `business_flows.py`, `business-flows.md` | Tạo API key (và key role chỉ đọc); chạy `fetch_schema.py` (schema thật chưa có); chạy `seed.py` — **tên trường chưa kiểm chứng trên instance**, sửa nếu 400; chạy `business_flows.py` và chụp bằng chứng |
| **Quang** | `run_k05.py` (SC1–SC5), `summarize.py`, `probe_boundaries.py`, `make_red_case.py`, `scenarios.md`, selftest trên máy chủ giả đạt | `pip install -r requirements.txt`; chạy SC1 thật (sau khi có schema); chạy ca đỏ; chạy `probe_boundaries.py`; chép số liệu từ `summary.md`; hai lần chạy cùng cấu hình để kiểm tra tái lập |

## Điều chưa kiểm chứng

- Mọi script mới được thử với **máy chủ giả**, chưa với Twenty thật. Khi chạy thật có thể phải chỉnh: dạng body (`seed.py`), khóa phản hồi (`createCompany`...), cách chọn operation (`--include-path-regex`), tốc độ (429).
- Tên trường seed, tên menu API key/Roles, giới hạn 100 req/phút trên self-host.
- Kỳ vọng từ mã nguồn (limit cắt về 200, batch 200, lỗi lạ → 400) mới đọc từ code, chưa chạy.
- Schemathesis `--generation-deterministic` bỏ qua `--seed`; nếu muốn dùng seed cụ thể, bỏ cờ này trong `run_k05.py`.
