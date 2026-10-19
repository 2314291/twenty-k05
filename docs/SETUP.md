# Hướng dẫn cài đặt Twenty v2.45.6 bằng Docker (Báo cáo Phần C và H)

Người phụ trách: Tuấn. Mục tiêu: máy sạch → Twenty chạy tại `http://localhost:3001` → có API key → tải được OpenAPI.
Phiên bản: tag `twenty/v2.45.6`, SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`, image `twentycrm/twenty:v2.45.6`
(ghi trong `env/VERSION.txt`). **Không pull `main`.**

> Cách nhanh nhất để chạy được mà không cần clone mã nguồn Twenty: dùng ngay `env/docker-compose.yml` và `env/.env.example` của repo này
> (bước 2A). Chỉ cần clone mã nguồn (bước 2B) khi Thuận cần đọc code hoặc muốn chạy đúng thư mục `packages/twenty-docker`.

## 1. Yêu cầu

| Thành phần | Yêu cầu |
|---|---|
| Hệ điều hành | Windows 10/11 (WSL2), macOS hoặc Linux |
| Docker | Docker Desktop (Windows/macOS) hoặc Docker Engine + Compose v2; kiểm tra `docker --version`, `docker compose version` |
| RAM trống | Nên từ 8 GB (PostgreSQL + Redis + server + worker) |
| Cổng | **3001** (ngoài) phải rảnh; 3000 trong container |
| Python | 3.9 trở lên, để chạy Schemathesis và script (`python --version`) |
| Git | Để clone repo nhóm; Windows: `git config --global core.longpaths true` |

## 2. Dựng instance

### 2A. Dùng file trong repo nhóm (khuyến nghị)

```bash
cd env
cp .env.example .env            # Windows PowerShell: Copy-Item .env.example .env
# Sửa .env: đặt PG_DATABASE_PASSWORD và ENCRYPTION_KEY (xem bước 3). KHÔNG commit .env
docker compose pull
docker compose up -d
docker compose ps               # chờ server ở trạng thái healthy
```

### 2B. Dùng mã nguồn Twenty (để đọc code)

```bash
git config --global core.longpaths true
git clone https://github.com/twentyhq/twenty.git
cd twenty
git checkout twenty/v2.45.6
git rev-parse HEAD              # phải ra 6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e
cd packages/twenty-docker
cp .env.example .env            # rồi sửa như bảng bước 3
# Nếu cổng 3000 bị chiếm: trong docker-compose.yml đổi "3000:3000" thành "3001:3000"
docker compose pull && docker compose up -d
```

Repo của nhóm Tiến đã sửa sẵn `ports: "3001:3000"`.

## 3. Biến môi trường (`.env`)

| Biến | Giá trị | Ghi chú |
|---|---|---|
| `TAG` | `v2.45.6` | Ghim phiên bản image |
| `PG_DATABASE_USER` / `PASSWORD` / `HOST` / `PORT` / `NAME` | `postgres` / mật khẩu mạnh, **không ký tự đặc biệt** / `db` / `5432` / `default` | Compose có sẵn mặc định |
| `REDIS_URL` | `redis://redis:6379` | |
| `SERVER_URL` | `http://localhost:3001` | **Phải khớp cổng ngoài.** Giá trị này cũng nằm trong `servers` của OpenAPI |
| `ENCRYPTION_KEY` | chuỗi ngẫu nhiên | `openssl rand -base64 32`; PowerShell: `[Convert]::ToBase64String((1..32 \| ForEach-Object { Get-Random -Maximum 256 }))` |
| `STORAGE_TYPE` | `local` | Lưu tệp vào volume Docker |

## 4. Khởi động lần đầu

1. Lần đầu server chạy migration vài phút; trạng thái `unhealthy`/`starting` ban đầu là bình thường (healthcheck gọi `http://localhost:3000/healthz` trong container).
2. Theo dõi: `docker compose logs -f server`. Khi thấy server lắng nghe là xong.
3. Mở `http://localhost:3001`, tạo tài khoản và workspace. Bước "Install apps" chọn **Bỏ qua** (Skip); nếu trang đứng yên, gõ thẳng `http://localhost:3001/objects/companies` (xem [ENV_01](su_co_moi_truong/ENV_01_install_apps_bo_qua.md)). Bước "Mời đội" cũng chọn **Bỏ qua**: instance chỉ chạy ở `localhost` và chưa cấu hình gửi mail.
4. `docker compose` in khoảng 10 dòng `WARN ... variable is not set` (`STORAGE_S3_*`, `FALLBACK_ENCRYPTION_KEY`, `DISABLE_DB_MIGRATIONS`, `DISABLE_CRON_JOBS_REGISTRATION`). **Vô hại**: đó là biến tuỳ chọn nhóm không dùng (`STORAGE_TYPE=local`; để trống nghĩa là migration và cron vẫn bật).
5. `docker compose ps`: `db`, `redis`, `server` hiện `(healthy)`; `worker` chỉ hiện `Up` vì compose không khai báo healthcheck cho nó. Muốn biết worker có lỗi không: `docker compose logs worker`.

## 5. Tạo API key và tải schema

1. Trong Twenty: **Settings** → mục API (tên menu theo ghi chú nhóm là "MCP & APIs", **cần xác nhận trên v2.45.6**) → tạo API key, chọn hạn dùng, **role đầy đủ quyền**.
2. Sao chép key **một lần duy nhất** vào file `.env` ở gốc repo nhóm (`TWENTY_API_KEY=...`). Không dán vào chat/Git.
3. Tạo thêm key thứ hai gắn **role chỉ đọc** (tạo role mới trong Settings → Roles) → `TWENTY_API_KEY_LIMITED` (dùng cho SC5).
4. Tải schema: `python scripts/fetch_schema.py` → `schema/core.openapi.json`. Script cảnh báo nếu schema không có đường dẫn (thiếu key).

## 6. Dữ liệu mẫu

- Workspace mới **có sẵn 5 công ty mẫu** (Airbnb, Anthropic, Stripe, Figma, Notion), người tạo `System` (xác nhận 17/10/2026). Sau `seed.py --count 30` sẽ có **35** công ty; `seed.py --cleanup` chỉ xoá bản ghi tiền tố `K05-`, không xoá 5 bản ghi mẫu.
- Dữ liệu K05: `python scripts/seed.py --count 30` tạo 30 công ty, 30 người, 30 cơ hội tiền tố `K05-`; `python scripts/seed.py --cleanup` dọn lại.

## 7. Bằng chứng cần chụp (Phần C)

Lưu trong `evidence/` (đặt tên `NN_mo_ta.png`, dùng dấu gạch dưới):

| # | Chụp gì |
|---|---|
| 01 | `docker compose ps` với 4 dịch vụ chạy, server healthy |
| 02 | Trang đăng nhập/đăng ký ở `http://localhost:3001` |
| 03 | Giao diện Companies có dữ liệu |
| 04 | Màn hình tạo API key (che key) |
| 05 | Kết quả `python scripts/fetch_schema.py` (số đường dẫn, số operation) |
| 06 | Kết quả `python scripts/business_flows.py` (3 luồng) |
| 07 | `git rev-parse HEAD` ra đúng SHA (nếu dùng 2B) |

Ngoài ảnh nên quay video 1–2 phút (đăng nhập, tạo Company, chạy `run_k05.py SC1`) làm dự phòng cho buổi demo.

## 8. Dừng, reset, chạy lại

| Việc | Lệnh |
|---|---|
| Dừng, giữ dữ liệu | `docker compose stop` |
| Chạy lại | `docker compose up -d` |
| **Xoá sạch dữ liệu** (về trạng thái ban đầu) | `docker compose down -v` (xoá cả volume DB) |
| Xem log | `docker compose logs -f server` |

Sau `down -v` phải tạo lại tài khoản, workspace và **API key mới**; key cũ không dùng được.

## 9. Sự cố đã gặp

| Sự cố | Cách xử lý |
|---|---|
| `Filename too long` khi clone trên Windows | `git config --global core.longpaths true`, `git restore --source=HEAD :/`, clone vào đường dẫn ngắn (ví dụ `C:\k\`) |
| `port is already allocated` ở cổng 3000 | Dùng `3001:3000` (đã có sẵn trong `env/docker-compose.yml`) |
| `could not translate host name "db"` | `docker compose down` rồi `up -d` để tạo lại mạng; nếu còn, restart Docker Desktop |
| `docker ps` không kết nối được | Mở Docker Desktop, chờ "Engine running" |
| Schema tải về không có đường dẫn của object | Thiếu hoặc sai Bearer key; xem lại bước 5 |
| Đăng nhập lại báo sai sau `down -v` | Dữ liệu đã bị xoá, tạo tài khoản mới |
| Trang "Install apps" bấm Bỏ qua không chuyển trang; F5 báo lỗi | Gõ thẳng `http://localhost:3001/objects/companies` ([ENV_01](su_co_moi_truong/ENV_01_install_apps_bo_qua.md)) |
| Nhãn giao diện trộn Việt/Anh (`"Tên riêng"`, `Last name`, `"Lọc"`) | Lỗi dịch của Twenty, không ảnh hưởng chức năng ([ENV_02](su_co_moi_truong/ENV_02_nhan_dich_tron_ngon_ngu.md)) |

## 10. Chạy lại trên máy mới (Phần H)

```bash
git clone <repo twenty-k05> && cd twenty-k05
pip install -r requirements.txt            # Schemathesis 4.31.1
cp .env.example .env                       # điền TWENTY_API_KEY sau khi dựng Twenty và tạo key
cd env && cp .env.example .env && docker compose up -d && cd ..
python scripts/fetch_schema.py
python scripts/seed.py --count 30
python scripts/run_k05.py SC1
```
