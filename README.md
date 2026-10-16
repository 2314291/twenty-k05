# twenty-k05 — Kiểm thử API dựa trên schema cho Twenty CRM (R10 + K05)

**Phiên bản bị test (SUT):** `twenty/v2.45.6` · SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e` · image `twentycrm/twenty:v2.45.6`
**Công cụ:** Schemathesis 4.31.1 · Python ≥ 3.9 · Docker (để chạy Twenty)

Nhóm: Tiến (trưởng nhóm), Tuấn, Thuận, Trung, Quang. Môn Kiểm thử phần mềm, ĐH Đà Lạt. Repo này chỉ chứa tài liệu và mã test; **không sửa mã Twenty**.
Mọi script chỉ chạy với `localhost`.

## Chạy lại trên máy mới

```bash
git clone <repo twenty-k05> && cd twenty-k05
python -m venv .venv && . .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) Dựng Twenty (xem docs/SETUP.md)
cd env && cp .env.example .env && docker compose up -d && cd ..
#    mở http://localhost:3001, tạo workspace, tạo API key

# 2) Cấu hình test
cp .env.example .env                                 # điền TWENTY_API_KEY (không commit)

# 3) Lấy schema, nạp dữ liệu, chạy
python scripts/fetch_schema.py
python scripts/list_operations.py --md docs/operations.md
python scripts/seed.py --count 30
python scripts/run_k05.py SC1                        # PoC giữa kỳ
python scripts/probe_boundaries.py                   # ca biên SC3/SC4/SC5
```

Kết quả nằm ở `reports/<SC>/<lần chạy>/` (`summary.md`, `REPRODUCERS.md`, `reproducers/*.sh`). Kiểm tra tái lập:
`python scripts/summarize.py --compare <lần chạy A> <lần chạy B>`.

## Bố cục

| Thư mục | Nội dung |
|---|---|
| `docs/` | `SPEC.md`, `PHAN_CONG.md`, `architecture.md` (A, B), `SETUP.md` (C, H), `test-plan.md` (D), `scenarios.md` (E), `business-flows.md`, `bao-cao-giua-ky.md`, `demo-script.md`, `email-hoi-thay.md`, `board-cards.csv` |
| `env/` | `docker-compose.yml` (cổng 3001), `.env.example`, `VERSION.txt` |
| `schema/` | `core.openapi.json` (tải về), `core.red.openapi.json` (ca đỏ) |
| `scripts/` | `fetch_schema.py`, `list_operations.py`, `seed.py`, `business_flows.py`, `run_k05.py`, `summarize.py`, `probe_boundaries.py`, `make_red_case.py`, `selftest/` |
| `hooks/` | Dành cho hook Schemathesis (cuối kỳ) |
| `reports/` | Log, thống kê, reproducer (key đã redact) |
| `evidence/` | Ảnh, video, bằng chứng 3 luồng |

## Kịch bản

| ID | Nội dung | Lệnh |
|---|---|---|
| SC1 | Quét Companies (PoC giữa kỳ) | `python scripts/run_k05.py SC1` |
| SC2 | Dữ liệu sai trên 5 đối tượng | `python scripts/run_k05.py SC2` |
| SC3 | Phân trang/lọc/sắp xếp | `run_k05.py SC3` + `probe_boundaries.py --only sc3` |
| SC4 | Batch 0/1/200/201 | `run_k05.py SC4` + `probe_boundaries.py --only sc4` |
| SC5 | Xác thực (`--variant none\|wrong\|limited`) | `run_k05.py SC5 --variant none` |
| Ca đỏ | Schema sửa kiểu một trường | `make_red_case.py` rồi `run_k05.py SC1 --schema schema/core.red.openapi.json --label RED` |

## Tự kiểm tra bộ script (không cần Twenty)

`python scripts/selftest/run_selftest.py` chạy toàn bộ đường ống trên máy chủ **giả**. Kết quả này không phải kết quả của Twenty.

## Bảo mật

`.env` nằm trong `.gitignore`; API key không được commit hay gửi qua chat; mọi tệp trong `reports/` và `evidence/` do script tạo đã được thay key bằng `<REDACTED>`
(kiểm tra lại bằng `grep -r "eyJ" reports evidence` trước khi push).
