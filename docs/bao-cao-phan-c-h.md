# Báo cáo Phần C và Phần H (Tuấn)

Bản để Tiến ghép vào báo cáo cuối kỳ. Chi tiết từng lệnh nằm ở `docs/SETUP.md`; ở đây chỉ giữ phần trình bày và bằng chứng.
Ô có dấu ☐ là chỗ còn phải điền sau khi chạy trên máy (xem "Việc còn lại" cuối file).

---

## Phần C. Môi trường và chạy hệ thống

### C.1 Thành phần và phiên bản

Twenty chạy bằng Docker Compose (`env/docker-compose.yml`), gồm 4 service:

| Service | Image | Vai trò |
|---|---|---|
| `server` | `twentycrm/twenty:v2.45.6` | API REST/GraphQL và giao diện web, cổng ngoài **3001** → 3000 trong container |
| `worker` | `twentycrm/twenty:v2.45.6` | Chạy tác vụ nền (hàng đợi), chỉ khởi động khi `server` đã khoẻ |
| `db` | `postgres:16` | Lưu dữ liệu workspace (database `default`) |
| `redis` | `redis` | Cache metadata của workspace và hàng đợi |

Công cụ kiểm thử: Python ≥ 3.9, Schemathesis 4.31.1 (`requirements.txt`), các script chỉ dùng thư viện chuẩn (`scripts/k05_common.py`).
Yêu cầu máy: Docker Desktop (Windows dùng WSL2), RAM trống từ 8 GB, cổng 3001 rảnh.

### C.2 Lệnh dựng và chạy

```powershell
git clone https://github.com/2314291/twenty-k05.git; cd twenty-k05
pip install -r requirements.txt
cd env; copy .env.example .env      # đặt PG_DATABASE_PASSWORD, ENCRYPTION_KEY
docker compose up -d; cd ..         # lần đầu mất 1-3 phút để migrate DB
```

Sau đó mở `http://localhost:3001`, tạo tài khoản và workspace, vào Settings → APIs tạo key, dán vào `.env` ở gốc repo (`TWENTY_API_KEY=`).
Kiểm tra: `docker compose ps` thấy `db`, `redis`, `server` ở trạng thái `healthy` (bằng chứng `evidence/01_docker_compose_ps.png`).

### C.3 Dữ liệu test (seed)

| Hạng mục | Giá trị |
|---|---|
| Dữ liệu có sẵn | Workspace mới có 5 công ty, 5 người, 6 cơ hội mẫu |
| Seed của nhóm | `python scripts/seed.py --count 30`: 30 bản ghi tiền tố `K05-` cho mỗi object (Companies, People, Opportunities, Notes, Tasks), seed ngẫu nhiên cố định `20261020` |
| Đưa về trạng thái chuẩn | `python scripts/reset_env.py`: khôi phục DB từ snapshot, xoá cache Redis, chờ `/healthz`, kiểm tra API key, seed lại |
| Trạng thái sau reset | 35 / 35 / 36 / 30 / 30 bản ghi; chạy reset 2 lần liên tiếp cho cùng kết quả (`evidence/reset-env-20261125.txt`) |

### C.4 Ba luồng nghiệp vụ chạy được

Chạy bằng `python scripts/business_flows.py` (tạo, kiểm tra, rồi tự dọn dữ liệu của luồng).

| Luồng | Request | Kỳ vọng | 16/10 (Tuấn) | 17/10 (Tuấn) | 21/11 (Trung) |
|---|---|---|---|---|---|
| F1 Tạo Company | `POST /rest/companies` | 201, có `id` | 201 | 201 | 201 |
| F2 Tạo Person gắn Company | `POST /rest/people` có `companyId`, rồi `GET` đọc lại | 201, đọc lại đúng `companyId` | 201, 200 | 201, 200 | 201, 200 |
| F3 Đổi stage Opportunity | Tạo cơ hội stage `NEW`, `PATCH` sang `MEETING`, đọc lại | 200, `stage = MEETING` | 201, 200, 200 | 201, 200, 200 | 201, 200, 200 |

Bằng chứng: `evidence/business-flows-20261016-213042.json`, `-20261017-121256.json`, `-20261121-121329.json` (key đã che), ảnh `06_business_flows.png`, `09_business_flows_trung.png`.
Ba luồng chạy đạt trên **hai máy khác nhau** (máy Tuấn và máy Trung) với cùng repo và cùng phiên bản.

### C.5 Sự cố môi trường đã gặp

Ghi ở `docs/SETUP.md` mục 9 và `docs/su_co_moi_truong/` (ENV_01: trang "Install apps" không chuyển trang; ENV_02: giao diện trộn tiếng Việt và tiếng Anh).
Hai lưu ý quan trọng nhất cho người chạy lại:
- Ngay sau khi bật, server cần 1–3 phút để migrate; gọi API lúc này sẽ ra lỗi kết nối. Đó là **lỗi do môi trường, không phải lỗi của Twenty**; script reset luôn chờ `/healthz` trước khi test.
- Twenty giới hạn 100 request mỗi 60 giây cho mỗi key (G-01). Mọi script đi chậm 1 request/giây.

---

## Phần H. Tái lập: ghim phiên bản, cấu hình, cách chạy lại

### H.1 Phiên bản được ghim

| Thành phần | Giá trị ghim | Nơi ghi |
|---|---|---|
| Twenty | tag `v2.45.6`, SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e` | `env/VERSION.txt`, `env/.env.example` (`TAG=v2.45.6`) |
| Image Twenty | `twentycrm/twenty:v2.45.6`, digest ☐ | `env/VERSION.txt` |
| PostgreSQL | `postgres:16` (ghim bản lớn) | `env/docker-compose.yml` |
| Redis | **chưa ghim** (`image: redis`), phiên bản đang chạy ☐ | `env/docker-compose.yml` |
| Schemathesis | `4.31.1` | `requirements.txt` |
| Python | ≥ 3.9 | `README.md` |

**Đã sửa ngày 26/11:** `docker-compose.yml` trước đây dùng `twentycrm/twenty:${TAG:-latest}`, tức nếu ai quên file `.env` hoặc thiếu biến `TAG` thì Docker sẽ âm thầm kéo bản `latest` chứ không phải bản nhóm đã test. Nay mặc định là `${TAG:-v2.45.6}`.

**Vì sao cần digest:** tag là nhãn có thể bị gắn lại cho bản khác, còn digest `sha256:...` là dấu vân tay của đúng một image. Hai máy cùng ghi `v2.45.6` mà digest khác nhau thì không chắc đang chạy cùng một bản.

### H.2 Cấu hình test được lưu lại

| Cấu hình | Giá trị | Nơi lưu |
|---|---|---|
| Địa chỉ | `TWENTY_BASE_URL=http://localhost:3001`; script từ chối chạy nếu không phải localhost | `.env.example`, `k05_common.assert_localhost` |
| Khoá | `TWENTY_API_KEY` (đủ quyền), `TWENTY_API_KEY_LIMITED` (chỉ đọc); chỉ nằm trong `.env`, không commit | `.gitignore` |
| Seed ngẫu nhiên | `20261020` | `K05_SEED` trong `.env.example`, `seed.py` |
| Nhịp gửi | 1 request/giây, gặp 429 thì chờ theo `retryAfterSeconds` | các script `kiem_thu_*.py` |
| Schema dùng để sinh test | `schema/core.openapi.json`, tải bằng `fetch_schema.py` **có key** (không key chỉ được khung, P5-06) | `schema/` |

### H.3 Đưa hệ thống về cùng trạng thái trước mỗi lần chạy

`scripts/reset_env.py` thay cho `docker compose down -v`. Lý do: `down -v` xoá luôn tài khoản, workspace và API key, phải tạo lại bằng tay nên không tự động hoá được.

1. Một lần, sau khi tạo workspace, key đủ quyền và key chỉ đọc: `python scripts/reset_env.py --snapshot` (lưu DB vào `env/snapshot/`, không commit).
2. Trước mỗi lần test: `python scripts/reset_env.py`. Script dừng `server`/`worker`, xoá và khôi phục DB, xoá cache Redis (nếu không, cache cũ lệch với DB mới gây test chập chờn), bật lại, chờ `/healthz`, kiểm tra key còn dùng được, rồi seed.
3. Bằng chứng idempotent: 2 lần reset liên tiếp cùng ra 35/35/36/30/30 (`evidence/reset-env-20261125.txt`). Nếu reset không thật sự khôi phục DB, lần 2 sẽ ra 65.

### H.4 Chạy lại trên máy mới

```powershell
git clone https://github.com/2314291/twenty-k05.git; cd twenty-k05
pip install -r requirements.txt
cd env; copy .env.example .env; docker compose up -d; cd ..
# tạo workspace + key đủ quyền + role/key chỉ đọc trên giao diện, dán vào .env
python scripts/fetch_schema.py
python scripts/reset_env.py --snapshot
python scripts/reset_env.py
python scripts/business_flows.py          # Phần C: 3 luồng
python scripts/kiem_thu_sc5.py            # ví dụ một kịch bản
```

Thời gian dựng trên máy sạch: ☐ phút (đo khi làm thử trên máy sạch). Cấu hình tối thiểu đã dùng: ☐ (RAM, ổ đĩa, phiên bản Docker Desktop của máy demo).

### H.5 Bằng chứng tái lập

| Bằng chứng | Kết quả |
|---|---|
| Cùng máy, chạy lại (repeatability) | Reset 2 lần liên tiếp cùng số bản ghi; `business_flows.py` trên máy Tuấn ngày 16/10 và 17/10 cùng mã trả về và cùng `stage` (`NEW` → `MEETING`), chỉ khác `id` và thời điểm |
| Khác máy (reproducibility) | 3 luồng F1–F3 đạt trên máy Tuấn (16–17/10) và máy Trung (21/11) |
| SC5 chạy 2 lần | ☐ `kiem_thu_sc5.py --compare` (tiêu chí: KHÁC 0) |

Khi so hai lần chạy, bỏ qua các trường luôn đổi: `id`, `createdAt`, `updatedAt`, thời gian phản hồi.

### H.6 An toàn bí mật

Quét toàn bộ 39 commit trên mọi nhánh ngày 26/11: 0 token JWT, không có file `.env` nào từng bị commit; chỉ có giá trị mẫu (`evidence/quet-bi-mat-20261126.txt`).

### H.7 Giới hạn đã biết

- API key phải tạo bằng tay trên giao diện ở lần dựng đầu; key gắn với đúng instance tạo ra nó (key máy này không dùng được ở máy khác).
- Snapshot phải chụp **sau** khi tạo xong mọi key và role; tạo sau thì reset sẽ xoá mất.
- Giới hạn 100 request mỗi 60 giây cho mỗi key; không chạy song song hai script trên cùng key.
- Redis chưa ghim phiên bản (H.1).
- Windows: Git có thể đổi kiểu xuống dòng (CRLF) làm file báo "đã sửa" dù nội dung không đổi; đặt `git config core.autocrlf true`.

---

## Việc còn lại (cần chạy trên máy Tuấn)

1. Ghi digest và phiên bản Redis vào H.1:
   `docker image inspect --format "{{index .RepoDigests 0}}" twentycrm/twenty:v2.45.6` và `docker compose exec redis redis-server --version`.
2. Chạy `kiem_thu_sc5.py` hai lần, điền H.5.
3. Dựng thử trên máy sạch (thư mục mới + `docker compose -p k05sach up -d`), đo thời gian, điền H.4.
