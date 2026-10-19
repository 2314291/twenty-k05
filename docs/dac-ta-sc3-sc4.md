# Đặc tả SC3, SC4 và dữ liệu test (Trung)

Bổ sung cho `scenarios.md` và `SPEC.md` mục 4. Cột "Kỳ vọng" đọc từ schema và mã nguồn v2.45.6; ô "Kết quả" để trống cho tới khi chạy trên instance thật.
Ca nào lệch kỳ vọng thì kiểm chứng tay bằng `curl` trước khi ghi thành defect.

## 1. Dữ liệu test dùng chung

| Hạng mục | Giá trị |
|---|---|
| Tiền tố bản ghi | `K05-` (công ty, người, cơ hội, ghi chú, việc) |
| Seed ngẫu nhiên | `20261020` (cố định để chạy lại ra cùng dữ liệu) |
| Số bản ghi | SC3: `python scripts/seed.py --count 120` (chia 3 lô, mỗi lô ≤ 50); SC4: DB bất kỳ, probe tự tạo và tự xoá |
| Đối tượng | Companies, People, Opportunities, Notes, Tasks (seed cả 5) |
| Dọn dẹp | `python scripts/seed.py --cleanup` (xoá theo `reports/seed-manifest.json`, bản ghi phụ thuộc xoá trước) |
| Khoá API | Chỉ đọc từ `.env`, không ghi vào tệp báo cáo |

## 2. SC3: phân trang, lọc, sắp xếp

Mục tiêu: xác nhận `limit`, con trỏ phân trang, lọc và sắp xếp xử lý đúng giá trị biên, không trả 5xx, phân trang nhất quán.
Điều kiện đầu: có ≥ 120 công ty (để `limit` 60 và 200 có ý nghĩa). Lệnh dự kiến (Sprint 3–4): `python scripts/probe_boundaries.py --only sc3` cùng `python scripts/run_k05.py SC3`.

| Mã ca | Request | Kỳ vọng | Kết quả |
|---|---|---|---|
| P3-01 | `GET /companies?limit=0` | Quan sát (không có kỳ vọng chắc) | |
| P3-02 | `limit=1` | 200, đúng 1 bản ghi | |
| P3-03 | `limit=60` | 200 (giá trị mặc định) | |
| P3-04 | `limit=200` | 200 (tối đa theo mã nguồn) | |
| P3-05 | `limit=201` | Quan sát: mã nguồn cắt về 200 âm thầm (H1) | |
| P3-06 | `limit=100000` | Quan sát | |
| P3-07 | `limit=-1` | 400 | |
| P3-08 | `limit=abc` | 400 | |
| P3-09 | `limit=1.5` | Quan sát | |
| P3-10 | `limit=` (rỗng) | Quan sát | |
| P3-11 | `starting_after=khong-phai-cursor` | Quan sát | |
| P3-12 | `ending_before=%00` | Quan sát | |
| P3-13 | `order_by=khongtontai` | Quan sát | |
| P3-14 | `filter=name[eq` (sai cú pháp) | Quan sát | |
| P3-15 | `depth=99` | Quan sát | |
| P3-16 | `GET /companies/not-a-uuid` | Quan sát | |
| P3-17 | `GET /companies/<UUID không tồn tại>` | 404 | |

Bất biến chung (do Schemathesis kiểm): không 5xx; body đúng schema; số bản ghi trả về ≤ `limit` hiệu lực.

## 3. SC4: batch

Mục tiêu: xác nhận ngưỡng batch 200 bản ghi và cách từ chối khi vượt ngưỡng hoặc body sai.
Điều kiện đầu: key đủ quyền. Lệnh dự kiến (Sprint 3–4): `python scripts/probe_boundaries.py --only sc4` cùng `python scripts/run_k05.py SC4`. Bản ghi probe tên `K05-PROBE-*`, tự xoá sau khi chạy.

| Mã ca | Body gửi tới `POST /batch/companies` | Kỳ vọng | Kết quả |
|---|---|---|---|
| P4-01 | `[]` | Quan sát | |
| P4-02 | 1 bản ghi | 200 hoặc 201 | |
| P4-03 | 200 bản ghi (biên trên) | 200 hoặc 201 | |
| P4-04 | 201 bản ghi | 400/413/422, thông điệp `Maximum number of records to upsert is 200` | |
| P4-05 | 61 bản ghi (kiểm tra giả thuyết ban đầu ngưỡng batch là 60) | 200 hoặc 201 (H2: ngưỡng thật là 200) | |
| P4-06 | Object thay vì mảng | Quan sát | |
| P4-07 | Mảng có phần tử sai: `[{"name":123}, null, "x"]` | Quan sát | |
| P4-08 | JSON hỏng | Quan sát | |

Bất biến chung: không 5xx; từ chối rõ ràng bằng 4xx, không nhận một phần rồi báo lỗi mơ hồ.

## 4. Triển khai ở Sprint 3–4

1. Chạy `seed.py --count 5` rồi `--count 120` trên instance thật; nếu API trả 400, so lại tên trường với `schema/core.openapi.json`.
2. Chạy các ca biên P3, P4 và điền cột "Kết quả".
3. Ca "Quan sát" nào có kết quả bất thường thì xác minh tay bằng `curl`, ghi vào danh sách lỗi.
