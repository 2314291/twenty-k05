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
| P3-01 | `GET /companies?limit=0` | Quan sát (không có kỳ vọng chắc) | 200, không lỗi |
| P3-02 | `limit=1` | 200, đúng 1 bản ghi | 200, trả 1 bản ghi. **Đạt** |
| P3-03 | `limit=60` | 200 (giá trị mặc định) | 200, trả 60 bản ghi. **Đạt** |
| P3-04 | `limit=200` | 200 (tối đa theo mã nguồn) | 200, trả 200 bản ghi (có 468 công ty). **Đạt** |
| P3-05 | `limit=201` | Quan sát: mã nguồn cắt về 200 âm thầm (H1) | 200, trả 200 bản ghi, không báo lỗi: bị cắt âm thầm về 200. Lệch schema, xem G-04 |
| P3-06 | `limit=100000` | Quan sát | 200, trả 200 bản ghi, không báo lỗi. Lệch schema, xem G-04 |
| P3-07 | `limit=-1` | 400 | 400. **Đạt** |
| P3-08 | `limit=abc` | 400 | 400. **Đạt** |
| P3-09 | `limit=1.5` | Quan sát | 400 (từ chối số thập phân) |
| P3-10 | `limit=` (rỗng) | Quan sát | 200, không lỗi |
| P3-11 | `starting_after=khong-phai-cursor` | Quan sát | 400 |
| P3-12 | `ending_before=%00` | Quan sát | 400 |
| P3-13 | `order_by=khongtontai` | Quan sát | 400 |
| P3-14 | `filter=name[eq` (sai cú pháp) | Quan sát | 400 |
| P3-15 | `depth=99` | Quan sát | 400 |
| P3-16 | `GET /companies/not-a-uuid` | Quan sát | 400 |
| P3-17 | `GET /companies/<UUID không tồn tại>` | 404 | 404. **Đạt** |

Bất biến chung (do Schemathesis kiểm): không 5xx; body đúng schema; số bản ghi trả về ≤ `limit` hiệu lực.

**Kết quả chạy tay ngày 02/11/2026** (Trung, Twenty v2.45.6 chạy Docker trên máy cá nhân, `curl.exe` với khoá đủ quyền).
Dữ liệu lúc chạy: 125 công ty (120 bản ghi `K05-` từ `seed.py --count 120` và 5 công ty mẫu có sẵn của workspace); riêng P3-04 đến P3-06 chạy lại khi có 468 công ty.

- Không ca nào trả 5xx.
- 6 ca có kỳ vọng rõ đều đạt: P3-02, P3-03, P3-04, P3-07, P3-08, P3-17.
- Các ca quan sát: giá trị sai (số thập phân, con trỏ rác, `order_by` không tồn tại, `filter` sai cú pháp, `depth=99`, id không phải UUID) đều bị từ chối bằng 400; `limit=0` và `limit=` rỗng trả 200.
- P3-04 đến P3-06 chạy lại khi có 468 công ty (sau các ca SC4): cả ba trả đúng 200 bản ghi. `limit=200` đạt; `limit=201` và `limit=100000` không bị từ chối mà bị cắt âm thầm về 200, trong khi schema khai báo `maximum: 200` (G-04).

## 3. SC4: batch

Mục tiêu: xác nhận ngưỡng batch 200 bản ghi và cách từ chối khi vượt ngưỡng hoặc body sai.
Điều kiện đầu: key đủ quyền. Lệnh dự kiến (Sprint 3–4): `python scripts/probe_boundaries.py --only sc4` cùng `python scripts/run_k05.py SC4`. Bản ghi probe tên `K05-PROBE-*`, tự xoá sau khi chạy.

| Mã ca | Body gửi tới `POST /batch/companies` | Kỳ vọng | Kết quả |
|---|---|---|---|
| P4-01 | `[]` | Quan sát | 201, không tạo bản ghi nào. Xem G-03 |
| P4-02 | 1 bản ghi | 200 hoặc 201 | 201. **Đạt** |
| P4-03 | 200 bản ghi (biên trên) | 200 hoặc 201 | 201. **Đạt** |
| P4-04 | 201 bản ghi | 400/413/422, thông điệp `Maximum number of records to upsert is 200` | 400 `BadRequestException`, thông điệp `Maximum number of records to upsert is 200.` **Đạt** |
| P4-05 | 61 bản ghi (kiểm tra giả thuyết ban đầu ngưỡng batch là 60) | 200 hoặc 201 (H2: ngưỡng thật là 200) | 201. **Đạt** (xác nhận ngưỡng không phải 60) |
| P4-06 | Object thay vì mảng | Quan sát | 400, nhưng `error` là `TypeError` với thông điệp nội bộ `args.data.forEach is not a function`. Xem G-05 |
| P4-07 | Mảng có phần tử sai: `[{"name":123}, null, "x"]` | Quan sát | 400, nhưng `error` là `TypeError` với thông điệp nội bộ `Cannot read properties of null (reading 'position')`. Xem G-05 |
| P4-08 | JSON hỏng | Quan sát | 400 `Bad Request`, thông điệp lỗi cú pháp JSON rõ ràng. **Đạt** |

Bất biến chung: không 5xx; từ chối rõ ràng bằng 4xx, không nhận một phần rồi báo lỗi mơ hồ.

**Kết quả chạy tay ngày 02/11/2026** (Trung, cùng môi trường SC3, gửi bằng `curl.exe`, mỗi ca cách nhau 1 giây để tránh giới hạn tốc độ G-01).
Ngoài 8 ca trên còn chạy thêm 2 ca sát biên: 2 bản ghi và 199 bản ghi, cả hai trả 201.

- Không ca nào trả 5xx.
- Ngưỡng batch 200 được xác nhận: 199 và 200 bản ghi được nhận, 201 bị từ chối bằng 400 với thông điệp rõ ràng; 61 bản ghi được nhận nên giả thuyết ngưỡng 60 là sai.
- Mảng rỗng được trả 201 dù không tạo gì (G-03).
- Body sai kiểu (object thay vì mảng, mảng có phần tử `null`) bị từ chối bằng 400 nhưng là do lỗi JavaScript nội bộ chứ không phải do kiểm tra dữ liệu đầu vào (G-05); JSON hỏng thì bị chặn đúng cách.

## 4. Triển khai ở Sprint 3–4

1. Chạy `seed.py --count 5` rồi `--count 120` trên instance thật; nếu API trả 400, so lại tên trường với `schema/core.openapi.json`.
2. Chạy các ca biên P3, P4 và điền cột "Kết quả".
3. Ca "Quan sát" nào có kết quả bất thường thì xác minh tay bằng `curl`, ghi vào danh sách lỗi.

## 5. Nhật ký lỗi và ghi nhận khi chạy

Mỗi mục ghi theo mẫu báo cáo lỗi: môi trường, bước tái hiện, kết quả mong đợi, kết quả thực tế, mức độ, trạng thái.
Phân loại: **Twenty** là lỗi hoặc hành vi của hệ thống được kiểm thử (chỉ ghi lại, không sửa mã Twenty);
**Bộ test** là lỗi trong mã của nhóm (ghi lại rồi sửa); **Môi trường** là giới hạn hoặc cấu hình, không phải lỗi.

Môi trường chung: Twenty v2.45.6 (`twentycrm/twenty:v2.45.6`) chạy Docker trên Windows, `http://localhost:3001`, khoá API role Admin.

### G-01. Giới hạn 100 request mỗi 60 giây cho mỗi khoá API

| Mục | Nội dung |
|---|---|
| Loại | Môi trường (hành vi có chủ ý của Twenty, không phải lỗi) |
| Ngày phát hiện | 02/11/2026 |
| Bước tái hiện | Gửi liên tiếp hơn 100 request bằng cùng một khoá trong vòng 60 giây (ví dụ `seed.py --cleanup` sau khi seed 120 bộ) |
| Mong đợi | Không có kỳ vọng trước; tài liệu nhóm ghi giới hạn này là "chưa kiểm chứng" |
| Thực tế | Request thứ 101 trở đi trả `429`, thân `{"error":"RATE_LIMITED","messages":["Rate limit exceeded for apiKey: 100 requests per 60s."],"retryAfterSeconds":1}` |
| Ảnh hưởng | Test chạy nhanh sẽ ra 429 thay vì kết quả thật; phải đi chậm hoặc dùng `--rate-limit` của Schemathesis |
| Trạng thái | Đã xác nhận |

### G-02. `seed.py --cleanup` bỏ qua lỗi 429 và xoá manifest

| Mục | Nội dung |
|---|---|
| Loại | Bộ test của nhóm |
| Ngày phát hiện | 02/11/2026 |
| Bước tái hiện | `python scripts/seed.py --count 120` rồi `python scripts/seed.py --cleanup` ngay sau đó |
| Mong đợi | Xoá hết bản ghi `K05-` đã tạo; nếu không xoá được thì báo lỗi và giữ lại danh sách id |
| Thực tế | Lệnh `--cleanup` chạm giới hạn 429; mã chỉ in mã trạng thái rồi đi tiếp, cuối cùng vẫn xoá manifest (lần chạy sau báo "Không có reports/seed-manifest.json"). Bản ghi bị 429 khi xoá sẽ còn sót mà không còn danh sách để dọn; số bản ghi sót thực tế (đếm khi dọn tay bằng `curl`): 3 cơ hội, 115 người, 115 công ty, tổng 233 trên 360 bản ghi đã tạo |
| Mức độ | Trung bình: dữ liệu sót làm sai kết quả các lần chạy sau (ví dụ đếm số bản ghi ở SC3) |
| Xử lý | Sửa `seed.py`: gặp 429 thì chờ theo `retryAfterSeconds` rồi gửi lại; id chưa xoá được ghi lại vào manifest |
| Trạng thái | Đã sửa và kiểm thử lại trên Twenty thật ngày 02/11/2026: `seed.py --count 30` (5 loại, 150 bản ghi) rồi `--cleanup` (150 lệnh xoá, vượt giới hạn 100/phút) dọn sạch, số công ty trở về 5 |

### G-03. Batch rỗng trả `201 Created` dù không tạo bản ghi nào

| Mục | Nội dung |
|---|---|
| Loại | Twenty, quan sát (không phải lỗi chức năng) |
| Ngày phát hiện | 02/11/2026 |
| Bước tái hiện | `POST /rest/batch/companies` với body `[]` |
| Mong đợi | Không có kỳ vọng chắc; hợp lý hơn là 200 hoặc 400 |
| Thực tế | `201`, không có bản ghi nào được tạo |
| Mức độ | Thấp |
| Trạng thái | Ghi nhận, không cần xử lý |

### G-04. `limit` lớn hơn 200 bị cắt âm thầm, lệch với schema

| Mục | Nội dung |
|---|---|
| Loại | Twenty, lệch schema |
| Ngày phát hiện | 02/11/2026 |
| Bước tái hiện | Có trên 200 công ty, gọi `GET /rest/companies?limit=201` và `?limit=100000` |
| Mong đợi | Schema `core.openapi.json` khai báo `limit` là `integer`, `minimum: 0`, `maximum: 200`, nên giá trị trên 200 phải bị từ chối bằng 400 (giống `limit=-1` và `limit=abc`) |
| Thực tế | Trả 200 kèm đúng 200 bản ghi, không có lỗi hay cảnh báo |
| Ảnh hưởng | Người gọi xin 201 bản ghi tưởng đã nhận đủ dữ liệu mà không biết bị cắt; công cụ kiểm thử dựa trên schema sẽ báo đây là dữ liệu sai được chấp nhận |
| Mức độ | Thấp |
| Trạng thái | Đã xác nhận bằng tay; trùng với phát hiện H1 khi đọc mã nguồn. Báo Quang để đưa vào danh sách lỗi chung |

### G-05. Body batch sai kiểu gây lỗi nội bộ `TypeError`, lộ thông điệp của mã nguồn

| Mục | Nội dung |
|---|---|
| Loại | Twenty, thiếu kiểm tra dữ liệu đầu vào |
| Ngày phát hiện | 02/11/2026 |
| Bước tái hiện | `POST /rest/batch/companies` với body `{"name":"x"}` (object thay vì mảng); và với body `[{"name":123},null,"x"]` |
| Mong đợi | Bị từ chối bằng 400 với thông điệp kiểm tra dữ liệu rõ ràng, ví dụ "body phải là mảng các object" |
| Thực tế | Trả 400 nhưng `error` là `TypeError` và thông điệp là lỗi JavaScript nội bộ: `args.data.forEach is not a function`, `Cannot read properties of null (reading 'position')`. Nghĩa là dữ liệu sai lọt qua tầng kiểm tra, gây lỗi bên trong rồi mới bị đổi thành 400 |
| Ảnh hưởng | Người gọi API nhận thông điệp khó hiểu; lộ chi tiết cài đặt bên trong; trùng với phát hiện H3 khi đọc mã nguồn (lỗi không phải `HttpException` bị đổi thành 400) |
| Mức độ | Trung bình |
| Trạng thái | Đã xác nhận bằng tay. Đã kiểm tra: hai ca này không tạo dở bản ghi nào (sau khi dọn còn đúng 5 công ty mẫu, số đã xoá 463 khớp tổng các batch được nhận 1 + 2 + 61 + 199 + 200). Báo Quang để đưa vào danh sách lỗi chung |
