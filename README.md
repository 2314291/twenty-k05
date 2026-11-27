# twenty-k05: Kiểm thử API dựa trên schema cho Twenty CRM (R10 + K05)

**Phiên bản bị test (SUT):** `twenty/v2.45.6` · SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e` · image `twentycrm/twenty:v2.45.6`
**Công cụ:** Schemathesis 4.31.1 · Python ≥ 3.9 · Docker (để chạy Twenty)

Nhóm: Tiến (trưởng nhóm), Tuấn, Thuận, Trung, Quang. Môn Kiểm thử phần mềm, ĐH Đà Lạt. Repo này chỉ chứa tài liệu và mã test; **không sửa mã Twenty**.
Mọi script chỉ chạy với `localhost` (gọi tới địa chỉ khác sẽ bị từ chối).

## 1. Cài đặt (dependency)

| Thành phần | Phiên bản | Dùng cho |
|---|---|---|
| Docker + Docker Compose | Docker Desktop hoặc Engine, Compose v2 | Chạy Twenty (`env/docker-compose.yml`, cổng 3001) |
| Python | ≥ 3.9 | Mọi script trong `scripts/` |
| Schemathesis | 4.31.1 (`requirements.txt`) | Sinh và chạy test K05 (`run_k05.py`) |
| Thư viện chuẩn Python | | Các script còn lại không cần cài thêm gì |

```bash
git clone https://github.com/2314291/twenty-k05.git && cd twenty-k05
python -m venv .venv && . .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Dựng Twenty (chi tiết: docs/SETUP.md)
cd env && cp .env.example .env && docker compose up -d && cd ..
# Mở http://localhost:3001, tạo workspace, vào Settings → API tạo key

cp .env.example .env            # điền TWENTY_API_KEY (và TWENTY_API_KEY_LIMITED cho SC5); KHÔNG commit .env
python scripts/fetch_schema.py  # tải OpenAPI về schema/core.openapi.json
python scripts/seed.py --count 30
python scripts/business_flows.py  # 3 luồng nghiệp vụ F1, F2, F3
```

## 2. Chạy bộ test K05

Harness `scripts/run_k05.py` gọi Schemathesis với cấu hình của từng kịch bản, nạp hook bảo vệ dữ liệu, rồi tự thống kê và tạo lệnh `curl` tái hiện cho từng nhóm lỗi.

| Kịch bản | Lệnh | Người chạy |
|---|---|---|
| SC1 quét 13 operation (dữ liệu đúng và sai), 5 object | `python scripts/run_k05.py SC1 --object all --reset` | Quang |
| Ca đỏ RED | `python scripts/make_red_case.py` rồi `python scripts/run_k05.py SC1 --object companies --reset --schema schema/core.red.openapi.json --label RED` | Quang |
| SC2 dữ liệu sai, 5 object | `python scripts/run_k05.py SC2 --object all --reset` | Thuận |
| SC3 phân trang, lọc, sắp xếp | `python scripts/run_k05.py SC3 --object <obj>`; ca tay: `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc3` (Trung), `python scripts/kiem_thu_tien_sc3_sc4.py --only sc3 --objects notes,tasks` (Tiến) | Trung, Tiến |
| SC4 batch | `python scripts/run_k05.py SC4 --object <obj>`; ca tay: `--only sc4` của hai script trên | Trung, Tiến |
| SC5 xác thực, 4 loại key | `python scripts/run_k05.py SC5 --object all --variant valid`, rồi `--variant limited`, `--variant wrong`, `--variant none` | Tuấn |
| SC6 chuỗi vòng đời | `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc6` | Trung |
| Ca biên P3–P5 | `python scripts/probe_boundaries.py` (hoặc `--only sc3`, `sc4`, `sc5`) | |

Tuỳ chọn hay dùng của `run_k05.py`:

| Tuỳ chọn | Ý nghĩa |
|---|---|
| `--object <obj>` / `--object all` | Một object (`companies`, `people`, `opportunities`, `notes`, `tasks`) hoặc lần lượt cả 5, mỗi object một thư mục kết quả |
| `--reset` | Dọn và seed lại dữ liệu K05 trước khi chạy (`seed.py --cleanup` rồi `--count 30`). Nên dùng cho mọi lần chạy chính thức |
| `--variant valid\|limited\|wrong\|none` | Loại key (SC5): đủ quyền, chỉ đọc, sai, không gửi |
| `--seed`, `--max-examples`, `--max-time` | Ghi đè seed (mặc định `20261020`), số ca mỗi operation (mặc định 50), giới hạn thời gian |
| `--dry-run` | Chỉ in lệnh `st run` sẽ chạy |
| `--no-protect`, `--no-real-ids`, `--no-hooks` | Tắt từng phần của hook (không nên dùng khi chạy chính thức) |

Hook `hooks/k05_hooks.py` được nạp tự động:
- `DELETE`/`PATCH /{obj}` hàng loạt chỉ chạm bản ghi tạo sau mốc bắt đầu (mốc lấy theo đồng hồ máy chủ, chống lệch giờ Docker và Windows).
- `DELETE /{obj}/{id}` và `PATCH /{obj}/merge` không được chạm bản ghi seed.
- Ca dương theo `{id}` dùng id seed thật thay vì UUID ngẫu nhiên.

Chi tiết ở `hooks/README.md`.

Giới hạn tốc độ của Twenty là 100 request mỗi 60 giây mỗi key: harness chạy `--workers 1 --rate-limit auto`. Không chạy cùng lúc hai kịch bản trên cùng một key.

## 3. Kết quả, tái lập và thống kê (Phần G)

Mỗi lần chạy tạo `reports/<SCx>/<thời điểm>-seed<seed>-<object>[-<variant>][-<nhãn>]/` gồm:

| File | Nội dung |
|---|---|
| `summary.md`, `summary.json` | Test case theo operation, mã trạng thái, số đạt/lỗi theo check, nhóm lỗi duy nhất, độ phủ operation |
| `REPRODUCERS.md`, `reproducers/*.sh` | Lệnh `curl` tái hiện từng nhóm lỗi |
| `run-config.json` | Kịch bản, object, seed, mốc dữ liệu, số bản ghi seed, hook bật/tắt, lệnh đã chạy |
| `st-output.txt`, `json-*`, `ndjson-*`, `junit-*`, `html-*` | Log và báo cáo gốc của Schemathesis (key đã thay bằng `<REDACTED>`) |

```bash
python scripts/summarize.py --compare reports/SC1/<lần 1> reports/SC1/<lần 2>   # kiểm tra tái lập (trùng ≥ 90% nhóm lỗi)
python scripts/thong_ke.py                                                    # gộp mọi lần chạy -> reports/thong-ke.md
```

`reports/thong-ke.md` có ba bảng cho Phần G:
1. Tổng quan theo kịch bản và object: operation đã test, test case, operation đủ 50 ca, 5xx, nhóm lỗi, tỷ lệ trùng với lần chạy trước.
2. Lỗi theo loại kiểm tra (bất biến I1 đến I7) và object.
3. Nhóm lỗi gộp xuyên object.

Bảng lỗi chung và RCA do Thuận gộp ở `reports/bang-loi.md`.

## 4. Tự kiểm tra bộ test (không cần Twenty)

```bash
python scripts/selftest/test_hooks.py      # logic hook bảo vệ dữ liệu, id seed
python scripts/selftest/test_run_k05.py    # mốc dữ liệu khi đồng hồ máy chủ lệch
python scripts/selftest/test_thong_ke.py   # thống kê gộp Phần G
python scripts/selftest/run_selftest.py    # chạy cả ba, rồi chạy run_k05.py thật trên máy chủ giả (cần Schemathesis)
```

## 5. Bố cục

| Thư mục | Nội dung |
|---|---|
| `Phan_Cong_module/` | Phân công, checklist, mô tả kịch bản SC1 đến SC6 (`KICH_BAN_K05.md`) |
| `docs/` | `SPEC.md`, `architecture.md` (A, B), `SETUP.md` (C, H), `test-plan.md` (D), `dac-ta-sc1-sc2-red.md`, `dac-ta-sc3-sc4.md` (E), `business-flows.md`, `operations.md` |
| `env/` | `docker-compose.yml` (cổng 3001), `.env.example`, `VERSION.txt` |
| `schema/` | `core.openapi.json` (tải từ instance); `core.red.openapi.json` do `make_red_case.py` tạo, không commit |
| `scripts/` | Harness K05: `run_k05.py`, `summarize.py`, `thong_ke.py`, `make_red_case.py`, `probe_boundaries.py`; dữ liệu và luồng: `fetch_schema.py`, `list_operations.py`, `seed.py`, `business_flows.py`, `k05_common.py`; ca tay: `kiem_thu_sc3_sc4_sc6.py` (Trung), `kiem_thu_tien_sc3_sc4.py` (Tiến); `selftest/` |
| `hooks/` | `k05_hooks.py`: hook Schemathesis bảo vệ dữ liệu và gắn id seed |
| `reports/` | Kết quả chạy (đã redact key), `thong-ke.md`, `bang-loi.md` |
| `evidence/` | Ảnh và bằng chứng môi trường, luồng nghiệp vụ |

## 6. Bảo mật

`.env` nằm trong `.gitignore`; API key không được commit hay gửi qua chat. `run_k05.py` thay key bằng `<REDACTED>` trong mọi file kết quả. Kiểm tra lại bằng `grep -r "eyJ" reports evidence` trước khi push.
