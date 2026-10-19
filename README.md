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

# 3) Lấy schema, nạp dữ liệu, chạy 3 luồng nghiệp vụ
python scripts/fetch_schema.py
python scripts/list_operations.py --md docs/operations.md
python scripts/seed.py --count 30
python scripts/business_flows.py
```

Giữa kỳ, kho mã gồm môi trường, schema, dữ liệu mẫu, 3 luồng nghiệp vụ và đặc tả kịch bản kiểm thử.
Bộ test K05 (chạy kịch bản, thống kê, lệnh tái hiện lỗi) được bổ sung ở Sprint 3–4.

## Bố cục

| Thư mục | Nội dung |
|---|---|
| `docs/` | `SPEC.md`, `PHAN_CONG.md`, `architecture.md` (A, B), `SETUP.md` (C, H), `test-plan.md` (D), `scenarios.md`, `dac-ta-sc1-sc2-red.md`, `dac-ta-sc3-sc4.md` (E), `business-flows.md`, `operations.md`, `demo-script.md`, `email-hoi-thay.md`, `board-cards.csv` |
| `env/` | `docker-compose.yml` (cổng 3001), `.env.example`, `VERSION.txt` |
| `schema/` | `core.openapi.json` (tải về từ instance) |
| `scripts/` | `fetch_schema.py`, `list_operations.py`, `seed.py`, `business_flows.py`, `k05_common.py` |
| `evidence/` | Ảnh, bằng chứng 3 luồng nghiệp vụ |

## Kịch bản (đặc tả giữa kỳ, triển khai Sprint 3–4)

| ID | Nội dung | Đặc tả |
|---|---|---|
| SC1 | Quét toàn bộ Companies | `docs/dac-ta-sc1-sc2-red.md` |
| SC2 | Dữ liệu sai trên 5 đối tượng | `docs/dac-ta-sc1-sc2-red.md` |
| SC3 | Phân trang, lọc, sắp xếp (17 ca biên P3) | `docs/dac-ta-sc3-sc4.md` |
| SC4 | Batch 0/1/200/201 (8 ca biên P4) | `docs/dac-ta-sc3-sc4.md` |
| SC5 | Xác thực: không key, key sai, key chỉ đọc (6 ca biên P5) | `docs/scenarios.md` |
| Ca đỏ | Schema sửa kiểu một trường | `docs/dac-ta-sc1-sc2-red.md` |

## Bảo mật

`.env` nằm trong `.gitignore`; API key không được commit hay gửi qua chat; mọi tệp trong `evidence/` do script tạo đã được thay key bằng `<REDACTED>`
(kiểm tra lại bằng `grep -r "eyJ" evidence` trước khi push).
