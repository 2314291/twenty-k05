# SC3 và SC4 trên People, Notes, Tasks (Tiến)

Phần của Tiến trong bảng phân công: **SC3** (phân trang, lọc, sắp xếp) trên **Notes, Tasks**; **SC4** (batch) trên **People, Notes**.
Bộ ca giống hệt bộ Trung đã chạy trên Companies (`docs/dac-ta-sc3-sc4.md`), chỉ đổi object, để so được hành vi giữa các object.
Dùng cho Báo cáo Phần E (thiết kế ca) và Phần G (kết quả, lỗi).

## 1. Cách chạy

| Mục | Giá trị |
|---|---|
| Môi trường | Twenty `v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`) chạy Docker ở `http://localhost:3001` |
| Khoá | `TWENTY_API_KEY` role Admin trong `.env` |
| Điều kiện đầu | `python scripts/seed.py --cleanup` rồi `python scripts/seed.py --count 30`; script tự tạo thêm bản ghi để mỗi object có hơn 200 bản ghi khi chạy SC3 |
| Lệnh | `python scripts/kiem_thu_tien_sc3_sc4.py` (cả hai kịch bản, khoảng 15 đến 20 phút, phần lớn là xoá dữ liệu vì giới hạn 100 request mỗi phút) |
| Chạy riêng | `--only sc3 --objects notes`, `--only sc4 --objects people` |
| Dữ liệu tạo ra | Tiền tố `K05-TIEN-`, tự xoá vĩnh viễn ở cuối |
| Kết quả | `reports/kiem-thu-tien/<thời điểm>.md` và `.json`, có lệnh `curl` tái hiện cho mọi ca LỆCH và QUAN SÁT, khoá API đã che |
| Tái lập | Chạy hai lần; hai bảng kết quả phải cùng mã trả về và cùng kết luận |

## 2. Thiết kế ca (Phần E)

Kết luận: **ĐẠT** = đúng kỳ vọng; **LỆCH** = khác kỳ vọng, phải xác minh bằng `curl` rồi ghi lỗi; **QUAN SÁT** = chưa có kỳ vọng chắc, ghi lại hành vi.
Bất biến chung: không trả 5xx; body đúng schema; số bản ghi trả về không vượt `limit` hiệu lực; batch sai thì từ chối rõ ràng bằng 4xx.

### SC3 trên Notes, Tasks: `GET /{obj}`

| Ca | Request | Kỳ vọng | Trên Companies (Trung, 02/11) |
|---|---|---|---|
| P3-01 | `limit=0` | Quan sát | 200 |
| P3-02 | `limit=1` | 200, đúng 1 bản ghi | 200 |
| P3-03 | `limit=60` | 200, 60 bản ghi | 200 |
| P3-04 | `limit=200` | 200, 200 bản ghi | 200 |
| P3-05 | `limit=201` | 400 (vượt tối đa) | 200, bị cắt về 200 (G-04) |
| P3-06 | `limit=100000` | 400 | 200, bị cắt về 200 (G-04) |
| P3-07 | `limit=-1` | 400 | 400 |
| P3-08 | `limit=abc` | 400 | 400 |
| P3-09 | `limit=1.5` | Quan sát | 400 |
| P3-10 | `limit=` (rỗng) | Quan sát | 200 |
| P3-11 | `starting_after=khong-phai-cursor` | Quan sát | 400 |
| P3-12 | `ending_before=%00` | Quan sát | 400 |
| P3-13 | `order_by=khongtontai` | Quan sát | 400 |
| P3-14 | `filter=title[eq` (sai cú pháp) | Quan sát | 400 |
| P3-15 | `depth=99` (schema chỉ cho 0, 1) | Quan sát | 400 |
| P3-16 | `GET /{obj}/not-a-uuid` | Quan sát | 400 |
| P3-17 | `GET /{obj}/<UUID không tồn tại>` | 404 | 404 |

### SC4 trên People, Notes: `POST /batch/{obj}`

Body một bản ghi: People `{"name":{"firstName":"K05-TIEN-..","lastName":".."}}`; Notes `{"title":"K05-TIEN-.."}`.

| Ca | Body | Kỳ vọng | Trên Companies (Trung, 02/11) |
|---|---|---|---|
| P4-01 | `[]` | Quan sát | 201 (G-03) |
| P4-02 | 1 bản ghi | 200 hoặc 201, tạo đúng 1 | 201 |
| P4-05 | 61 bản ghi | 200 hoặc 201, tạo đúng 61 | 201 |
| P4-03 | 200 bản ghi | 200 hoặc 201, tạo đúng 200 | 201 |
| P4-04 | 201 bản ghi | 4xx, thông điệp `Maximum number of records to upsert is 200`, không tạo bản ghi nào | 400 |
| P4-06 | Object thay vì mảng | 4xx, không lộ `TypeError` | 400, lộ `TypeError` (G-05) |
| P4-07 | `[{"<trường>":123}, null, "x"]` | 4xx, không lộ `TypeError` | 400, lộ `TypeError` (G-05) |
| P4-08 | JSON hỏng | 4xx | 400 |

Tổng: SC3 17 ca × 2 object = 34 ca; SC4 8 ca × 2 object = 16 ca; cộng 50 ca.

## 3. Kết quả

Chạy ngày 25/11/2026 trên máy Tiến (Twenty `v2.45.6`, Docker, Windows), sau `seed.py --cleanup` và `seed.py --count 30`.

| Lần chạy | Thời điểm | ĐẠT | LỆCH | QUAN SÁT | File kết quả |
|---|---|---|---|---|---|
| 1 | 25/11/2026 21:25 | 22 | 8 | 20 | `reports/kiem-thu-tien/20261125-212504.md` |
| 2 | 25/11/2026 21:38 | 22 | 8 | 20 | `reports/kiem-thu-tien/20261125-213803.md` |

**Tái lập:** hai lần chạy cho cùng mã trả về và cùng kết luận ở cả 50 ca. Không ca nào trả 5xx (bất biến I1 giữ). Dữ liệu `K05-TIEN-` đã được dọn sau mỗi lần (people 262, notes 262, tasks 169 bản ghi ở lần 2).

**So với Companies (Trung, 02/11):** cả 50 ca có cùng mã trả về với ca tương ứng trên Companies. Hành vi phân trang và batch của Twenty là chung cho mọi object, nên các lỗi đã thấy trên Companies cũng có trên People, Notes, Tasks.

### SC3 trên Notes, Tasks (34 ca)

| Ca | Notes | Tasks | Kết luận |
|---|---|---|---|
| P3-01 `limit=0` | 200, 0 bản ghi | 200, 0 bản ghi | Quan sát |
| P3-02 `limit=1` | 200, 1 bản ghi | 200, 1 bản ghi | Đạt |
| P3-03 `limit=60` | 200, 60 bản ghi | 200, 60 bản ghi | Đạt |
| P3-04 `limit=200` | 200, 200 bản ghi | 200, 200 bản ghi | Đạt |
| P3-05 `limit=201` | 200, 200 bản ghi | 200, 200 bản ghi | **Lệch** (D-01/G-04) |
| P3-06 `limit=100000` | 200, 200 bản ghi | 200, 200 bản ghi | **Lệch** (D-01/G-04) |
| P3-07 `limit=-1` | 400 | 400 | Đạt |
| P3-08 `limit=abc` | 400 | 400 | Đạt |
| P3-09 `limit=1.5` | 400 | 400 | Quan sát |
| P3-10 `limit=` (rỗng) | 200, 60 bản ghi (dùng mặc định) | 200, 60 bản ghi | Quan sát |
| P3-11 đến P3-16 (con trỏ rác, `%00`, `order_by` sai, `filter` sai cú pháp, `depth=99`, id không phải UUID) | 400 | 400 | Quan sát: đều bị từ chối rõ ràng |
| P3-17 UUID không tồn tại | 404 | 404 | Đạt |

### SC4 trên People, Notes (16 ca)

| Ca | People | Notes | Kết luận |
|---|---|---|---|
| P4-01 `[]` | 201, tạo 0 | 201, tạo 0 | Quan sát (G-03) |
| P4-02 1 bản ghi | 201, tạo 1 | 201, tạo 1 | Đạt |
| P4-05 61 bản ghi | 201, tạo 61 | 201, tạo 61 | Đạt: ngưỡng không phải 60 |
| P4-03 200 bản ghi | 201, tạo 200 | 201, tạo 200 | Đạt |
| P4-04 201 bản ghi | 400, tạo 0, có thông điệp ngưỡng 200 | 400, tạo 0 | Đạt |
| P4-06 object thay vì mảng | 400, `error=TypeError` | 400, `error=TypeError` | **Lệch** (G-05) |
| P4-07 phần tử sai kiểu, `null`, chuỗi | 400, `error=TypeError` | 400, `error=TypeError` | **Lệch** (G-05) |
| P4-08 JSON hỏng | 400, `error=Bad Request` | 400, `error=Bad Request` | Đạt |

## 4. Lỗi tìm được

Không có lỗi mới. Cả ba lỗi đều là lỗi đã ghi trên Companies (`docs/dac-ta-sc3-sc4.md` mục 5); lần chạy này xác nhận chúng **không riêng Companies** mà có ở People, Notes, Tasks, nên phạm vi các lỗi được mở rộng.

| Mã | Object | Ca | Mô tả | Kỳ vọng | Thực tế | Loại | Nguyên nhân | Mức độ |
|---|---|---|---|---|---|---|---|---|
| D-01 (G-04) | Notes, Tasks | P3-05, P3-06 | `limit` lớn hơn 200 bị cắt âm thầm về 200 | Schema khai báo `limit` tối đa 200, nên `limit=201` phải bị từ chối 400 như `limit=-1` | 200, trả đúng 200 bản ghi, không báo lỗi | Lệch schema | Tầng REST chỉ chặn giá trị âm hoặc không phải số, còn giá trị lớn thì bị kẹp về hằng số tối đa 200 dùng chung cho mọi object, thay vì kiểm tra theo `maximum` trong schema | Thấp |
| G-05 | People, Notes | P4-06, P4-07 | Body batch sai kiểu gây lỗi JavaScript nội bộ | 400 với thông điệp kiểm tra dữ liệu rõ ràng | 400 nhưng `error` là `TypeError` | Lỗi chức năng (thiếu kiểm tra đầu vào) | Endpoint batch không kiểm tra body là mảng các object trước khi xử lý; lỗi `TypeError` bị tầng xử lý lỗi đổi thành 400, nên trông như từ chối đúng nhưng thực chất là lỗi nội bộ và lộ thông điệp của mã nguồn | Trung bình |
| G-03 | People, Notes | P4-01 | Batch rỗng `[]` trả 201 dù không tạo bản ghi nào | 200 hoặc 400 | 201, tạo 0 bản ghi | Quan sát | Endpoint trả mã "Created" cố định cho mọi batch thành công, kể cả khi danh sách rỗng | Thấp |

Lệnh `curl` tái hiện từng ca nằm ở cuối file kết quả lần 2 (`reports/kiem-thu-tien/20261125-213803.md`). Bảng này gửi Thuận gộp vào bảng lỗi chung: không tạo mã mới, chỉ thêm People, Notes, Tasks vào cột phạm vi của D-01, G-03, G-05.
