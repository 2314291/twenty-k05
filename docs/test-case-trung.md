# Test case phần dữ liệu, SC3, SC4, SC6 (Trung)

Tập hợp mọi ca kiểm thử trong phần của Trung. Mỗi ca ghi: **phương pháp** kiểm thử, **căn cứ đối chiếu** (dựa vào đâu để biết đúng hay sai),
kỳ vọng, kết quả thực tế các lần chạy tay ngày 02/11 và 12/11/2026, và **bằng chứng** (mã E-xx trỏ tới output nguyên văn trong
`evidence/kiem-thu-tay-20261102.md`). Chi tiết lỗi G-01 đến G-05 ở `dac-ta-sc3-sc4.md`, G-06 ở `du-lieu-sc5-sc6.md`, G-07 ở mục 8 file này.

## 1. Môi trường và cách chạy lại

| Mục | Giá trị |
|---|---|
| Hệ thống | Twenty v2.45.6 (`twentycrm/twenty:v2.45.6`), Docker theo `env/docker-compose.yml`, `http://localhost:3001` |
| Workspace | Mới tạo, có sẵn 5 công ty mẫu |
| Khoá API | Role Admin, trong `.env` là `TWENTY_API_KEY` |
| Công cụ | Python 3, PowerShell, `curl.exe` |
| Nhịp gửi | Tối đa 1 request mỗi giây (Twenty giới hạn 100 request mỗi 60 giây cho mỗi khoá, G-01) |

Chạy lại tự động: `python scripts/kiem_thu_sc3_sc4_sc6.py` (khoảng 12 phút, tự dọn dữ liệu). Mỗi ca in kết luận so với kỳ vọng và so
với lần chạy tay 02/11 (GIỐNG / KHÁC). Ba luồng nghiệp vụ: `python scripts/business_flows.py`. Dữ liệu mẫu: `python scripts/seed.py`.

## 2. Phương pháp kiểm thử

| Mã | Phương pháp | Áp dụng cho |
|---|---|---|
| PP-1 | **Phân tích giá trị biên**: chọn giá trị tại biên, sát biên và vượt biên | `limit` (SC3), số bản ghi mỗi batch (SC4) |
| PP-2 | **Phân vùng tương đương**: chia đầu vào thành vùng hợp lệ và không hợp lệ, mỗi vùng thử một đại diện | SC3, SC4 |
| PP-3 | **Kiểm thử dữ liệu sai (negative)**: cố tình gửi giá trị sai kiểu, sai cú pháp, không tồn tại | SC3, SC4, SC6 |
| PP-4 | **Kiểm thử theo trạng thái**: đưa bản ghi qua các trạng thái và kiểm hành vi ở từng trạng thái | SC6 |
| PP-5 | **Kiểm thử luồng nghiệp vụ (end-to-end)**: làm chuỗi thao tác như người dùng rồi đọc lại để xác nhận | F1–F3, dữ liệu mẫu |
| PP-6 | **Đối chiếu hợp đồng API (schema)**: so mã trả về và dữ liệu với `schema/core.openapi.json` | Mọi ca |

## 3. Căn cứ đối chiếu (oracle)

Một ca được coi là sai khi kết quả thực tế mâu thuẫn với ít nhất một căn cứ dưới đây. Theo `test-plan.md` mục D.3, schema là nguồn chân lý.

| Mã | Căn cứ | Nội dung dùng để so | Nguồn |
|---|---|---|---|
| CC-1 | Schema, tham số `limit` | `integer`, `minimum: 0`, `maximum: 200`, `default: 60` | `schema/core.openapi.json`, `components.parameters.limit` (trích ở E-11) |
| CC-2 | Schema, batch | Body phải là **mảng** các `Company`; mã trả về khai báo 201, 400, 401 | `paths./batch/companies.post` (E-11) |
| CC-3 | Schema, thao tác trên một bản ghi | `GET`, `PATCH`, `DELETE /companies/{id}` và `PATCH .../restore` chỉ khai báo 200, 400, 401 | `paths./companies/{id}` (E-11) |
| CC-4 | Schema, xoá | `soft_delete` kiểu `boolean`, mặc định `false` (xoá vĩnh viễn) | `components.parameters.softDelete` (E-11) |
| CC-5 | Mã nguồn Twenty | Batch tối đa 200 bản ghi, vượt thì báo `Maximum number of records to upsert is 200` | `SPEC.md` mục 3.6, phát hiện H2 |
| CC-6 | Chuẩn HTTP (RFC 9110) | 2xx là thành công; 201 nghĩa là **đã tạo** tài nguyên; 4xx là yêu cầu sai; 404 là không tìm thấy; 5xx là lỗi server | RFC 9110 mục 15 |
| CC-7 | Nhất quán dữ liệu | Đọc lại phải bằng dữ liệu đã ghi; sửa một trường không đổi trường khác; xoá xong không đọc được; khôi phục xong đọc được | Yêu cầu nghiệp vụ của CRM |
| CC-8 | Cách Twenty tự báo lỗi kiểm tra dữ liệu | Khi Twenty chủ động từ chối dữ liệu sai, `error` là `BadRequestException` hoặc `Bad Request` kèm thông điệp mô tả (như P4-04, P4-08) | E-05, E-07 |
| CC-9 | Tài liệu bộ test | `seed.py --cleanup` phải xoá mọi bản ghi đã tạo, ghi trong `reports/seed-manifest.json` | Docstring `scripts/seed.py` |
| CC-10 | Tiêu chí pass/fail của nhóm | Không 5xx; dữ liệu sai bị 4xx; mã trả về nằm trong khai báo của schema | `test-plan.md` mục D.5 |

## 4. Dữ liệu mẫu và ba luồng nghiệp vụ

| Mã TC | PP | Bước | Căn cứ | Kỳ vọng | Thực tế 02/11 | Bằng chứng | Kết luận |
|---|---|---|---|---|---|---|---|
| TC-SEED-01 | PP-5 | `seed.py --count 5` (bản 3 đối tượng) | CC-9 | Tạo 5 công ty, 5 người, 5 cơ hội | Đúng | E-01 | Đạt |
| TC-SEED-02 | PP-5 | `seed.py --cleanup` khi dưới giới hạn tốc độ (15 lệnh xoá) | CC-9 | Mọi lệnh xoá trả 200, báo đã dọn | 15 dòng `-> 200`, `Đã dọn xong.` | E-01 | Đạt |
| TC-SEED-03 | PP-5 | `seed.py --count 120` rồi `--cleanup` bản cũ (360 lệnh xoá, vượt 100/phút) | CC-9 | Xoá hết 360 bản ghi | Gặp 429, manifest vẫn bị xoá; còn sót 3 cơ hội, 115 người, 115 công ty | E-02, E-03, E-04 | **Lệch (G-02)** |
| TC-SEED-04 | PP-5 | `seed.py --count 30` bản đã sửa (5 đối tượng) | CC-9 | Tạo 30 bản ghi mỗi loại, kể cả ghi chú và việc | `Đã tạo 30 công ty, 30 người, 30 cơ hội, 30 ghi chú, 30 việc` | E-12 | Đạt |
| TC-SEED-05 | PP-5 | `seed.py --cleanup` bản đã sửa (150 lệnh xoá, vượt 100/phút) | CC-9 | Gặp 429 thì chờ rồi gửi lại; cuối cùng dọn hết | 15 lần gặp 429 và tự chờ; `Đã dọn xong.` | E-12 | Đạt |
| TC-F1 | PP-5 | `POST /companies` | CC-6 | 201, có `id` | 201 | E-01 | Đạt |
| TC-F2 | PP-5 | `POST /people` có `companyId`, rồi `GET /people/{id}` | CC-6, CC-7 | 201; đọc lại đúng `companyId` | 201, 200 | E-01 | Đạt |
| TC-F3 | PP-5 | Tạo cơ hội `NEW`, `PATCH` sang `MEETING`, đọc lại | CC-6, CC-7 | 200; `stage = MEETING` | 200, `'MEETING'` | E-01 | Đạt |

## 5. SC3: phân trang, lọc, sắp xếp

Mọi ca là `GET /rest/companies`. Các ca P3-04 đến P3-06 chạy lại khi có 468 công ty (E-06); các ca khác chạy khi có 125 công ty (E-02).

| Mã TC | PP | Tham số | Căn cứ | Kỳ vọng | Thực tế 02/11 | Bằng chứng | Kết luận |
|---|---|---|---|---|---|---|---|
| P3-01 | PP-1 | `limit=0` | CC-1 (0 nằm trong khoảng hợp lệ) | Quan sát (schema cho phép 0 nhưng không nói trả gì) | 200 | E-02 | Quan sát |
| P3-02 | PP-1 | `limit=1` | CC-1 | 200, 1 bản ghi | 200, 1 bản ghi | E-02 | Đạt |
| P3-03 | PP-2 | `limit=60` | CC-1 | 200, 60 bản ghi | 200, 60 bản ghi | E-02 | Đạt |
| P3-04 | PP-1 | `limit=200` | CC-1 | 200, 200 bản ghi | 200, 200 bản ghi | E-06 | Đạt |
| P3-05 | PP-1 | `limit=201` | CC-1, CC-10 | 400 vì vượt `maximum: 200` | 200, trả 200 bản ghi | E-06, E-11 | **Lệch (G-04)** |
| P3-06 | PP-1 | `limit=100000` | CC-1, CC-10 | 400 vì vượt `maximum: 200` | 200, trả 200 bản ghi | E-06, E-11 | **Lệch (G-04)** |
| P3-07 | PP-3 | `limit=-1` | CC-1 (`minimum: 0`) | 400 | 400 | E-02 | Đạt |
| P3-08 | PP-3 | `limit=abc` | CC-1 (`integer`) | 400 | 400 | E-02 | Đạt |
| P3-09 | PP-3 | `limit=1.5` | CC-1 (`integer`) | Quan sát | 400 | E-02 | Quan sát |
| P3-10 | PP-3 | `limit=` rỗng | CC-1 | Quan sát | 200 | E-02 | Quan sát |
| P3-11 | PP-3 | `starting_after=khong-phai-cursor` | CC-6 | Quan sát | 400 | E-02 | Quan sát |
| P3-12 | PP-3 | `ending_before=%00` | CC-6 | Quan sát | 400 | E-02 | Quan sát |
| P3-13 | PP-3 | `order_by=khongtontai` | CC-6 | Quan sát | 400 | E-02 | Quan sát |
| P3-14 | PP-3 | `filter=name[eq` | CC-6 | Quan sát | 400 | E-02 | Quan sát |
| P3-15 | PP-1 | `depth=99` | CC-6 | Quan sát | 400 | E-02 | Quan sát |
| P3-16 | PP-3 | `/companies/not-a-uuid` | CC-6 | Quan sát | 400 | E-02 | Quan sát |
| P3-17 | PP-3 | `/companies/<UUID không tồn tại>` | CC-6; CC-3 | 404 theo HTTP | 404 | E-02 | Đạt; lệch schema (G-07) |

## 6. SC4: batch

Mọi ca là `POST /rest/batch/companies`, mỗi bản ghi `{"name": "K05-..."}`. Ba vùng tương đương: rỗng (0), hợp lệ (1 đến 200), vượt ngưỡng (từ 201).

| Mã TC | PP | Body | Căn cứ | Kỳ vọng | Thực tế 02/11 | Bằng chứng | Kết luận |
|---|---|---|---|---|---|---|---|
| P4-01 | PP-1 | `[]` | CC-2, CC-6 | Quan sát | 201, không tạo gì | E-05, E-08 | Quan sát (G-03) |
| P4-02 | PP-1 | 1 bản ghi | CC-2, CC-5 | 201, tạo 1 | 201 | E-05 | Đạt |
| B-03 | PP-1 | 2 bản ghi | CC-2, CC-5 | 201, tạo 2 | 201 | E-05 | Đạt |
| P4-05 | PP-2 | 61 bản ghi | CC-5 | 201 (ngưỡng thật 200, không phải 60) | 201 | E-05 | Đạt |
| B-05 | PP-1 | 199 bản ghi | CC-5 | 201, tạo 199 | 201 | E-05 | Đạt |
| P4-03 | PP-1 | 200 bản ghi | CC-5 | 201, tạo 200 | 201 | E-05 | Đạt |
| P4-04 | PP-1 | 201 bản ghi | CC-5, CC-8 | 400, `Maximum number of records to upsert is 200`, không tạo gì | 400 `BadRequestException`, đúng thông điệp | E-05, E-08 | Đạt |
| P4-06 | PP-3 | `{"name":"x"}` | CC-2, CC-8 | 400 do kiểm tra dữ liệu (`BadRequestException`) | 400 nhưng `error: TypeError`, `args.data.forEach is not a function` | E-07 | **Lệch (G-05)** |
| P4-07 | PP-3 | `[{"name":123},null,"x"]` | CC-2, CC-8 | 400 do kiểm tra dữ liệu (`BadRequestException`) | 400 nhưng `error: TypeError`, `Cannot read properties of null (reading 'position')` | E-07 | **Lệch (G-05)** |
| P4-08 | PP-3 | `{khong phai json` | CC-6, CC-8 | 400 | 400 `Bad Request`, thông điệp lỗi cú pháp JSON | E-07 | Đạt |

Kiểm tra không tạo dở (CC-7): số công ty `K05` xoá được sau SC4 là 463 (E-08), đúng bằng 1 + 2 + 61 + 199 + 200 bản ghi của các batch được nhận.
Vậy batch 201 và hai body sai không tạo bản ghi nào.

## 7. SC6: vòng đời một bản ghi

Phương pháp PP-4 (theo trạng thái) trên Companies (02/11/2026), mục 7.1 lặp lại cho 4 đối tượng còn lại (12/11/2026). Trạng thái: tồn tại, đã sửa, đã xoá vĩnh viễn, đã xoá mềm, đã khôi phục.

| Mã TC | Trạng thái và bước | Căn cứ | Kỳ vọng | Thực tế 02/11 | Bằng chứng | Kết luận |
|---|---|---|---|---|---|---|
| S6-01 | Tạo, `domainName.primaryLinkUrl = https://k05-sc6.example.com` | CC-6 | 201 | 201 | E-09 | Đạt |
| S6-02 | Đọc lại | CC-7 | 200, dữ liệu khớp | 200; tên khớp; domain thành `k05-sc6.example.com` | E-09 | Đạt (G-06 quan sát) |
| S6-03 | Sửa tên | CC-6 | 200 | 200 | E-09 | Đạt |
| S6-04 | Đọc sau sửa | CC-7 | Tên mới, domain giữ nguyên | Đúng | E-09 | Đạt |
| S6-05 | Lọc theo id | CC-7 | 200, 1 bản ghi | 200, 1 bản ghi | E-09 | Đạt |
| S6-06 | Xoá (mặc định) | CC-4, CC-6 | 200, xoá vĩnh viễn | 200 | E-09 | Đạt |
| S6-07 | Đọc sau xoá | CC-6, CC-7; CC-3 | 404 | 404 | E-09 | Đạt; lệch schema (G-07) |
| S6-08 | Xoá lần hai | CC-6; CC-3 | 404, không 5xx | 404 | E-09 | Đạt; lệch schema (G-07) |
| S6-09 | Sửa sau xoá | CC-6; CC-3 | 404, không 5xx | 404 | E-09 | Đạt; lệch schema (G-07) |
| S6-10 | Khôi phục sau xoá vĩnh viễn | CC-4; CC-3 | 404 (không còn gì để khôi phục) | 404 | E-09 | Đạt; lệch schema (G-07) |
| S6-11 | Xoá công ty đang có người, đọc người | CC-7 | Quan sát | Người còn (200), `companyId` rỗng | E-09 | Quan sát |
| S6-12a | `GET` UUID không tồn tại | CC-6; CC-3 | 404 | 404 | E-09 | Đạt; lệch schema (G-07) |
| S6-12b | `PATCH` UUID không tồn tại | CC-6; CC-3 | 404 | 404 | E-09 | Đạt; lệch schema (G-07) |
| S6-12c | `DELETE` UUID không tồn tại | CC-6; CC-3 | 404 | 404 | E-09 | Đạt; lệch schema (G-07) |
| S6-13b | Tạo mới, xoá mềm `?soft_delete=true` | CC-4 | 200 | 200 | E-10 | Đạt |
| S6-13c | Đọc sau xoá mềm | CC-7; CC-3 | 404 | 404 | E-10 | Đạt; lệch schema (G-07) |
| S6-13d | Khôi phục | CC-7 | 200 | 200 | E-10 | Đạt |
| S6-13e | Đọc sau khôi phục | CC-7 | 200 | 200 | E-10 | Đạt |

Ghi chú: thiết kế ban đầu của S6-10 kỳ vọng khôi phục được. Lần chạy 02/11 trả 404; đối chiếu CC-4 cho thấy `DELETE` mặc định xoá vĩnh viễn,
nên đây là kỳ vọng sai của người thiết kế, không phải lỗi. Kỳ vọng S6-10 đã sửa và thêm S6-13 để kiểm khôi phục sau xoá mềm.

### 7.1. SC6 cho People, Opportunities, Notes, Tasks (chạy ngày 12/11/2026)

Cùng 14 bước như Companies (trừ S6-11 và S6-12 chỉ chạy trên Companies), mỗi đối tượng sửa một trường khác nhau để kiểm "sửa một trường không đổi trường khác".

| Mã TC | Bước | Căn cứ | Kỳ vọng | Thực tế 12/11 | Bằng chứng | Kết luận |
|---|---|---|---|---|---|---|
| Person-01 đến Person-05 | People: tạo, đọc lại, sửa một trường, đọc sau sửa, lọc theo id | CC-6, CC-7 | 201; 200 khớp; 200; 200 (tên đổi, email giữ nguyên); 200, 1 bản ghi | Đúng cả năm | E-13 | Đạt (5 ca) |
| Person-06 đến Person-10 | People: xoá, rồi đọc, xoá lần hai, sửa, khôi phục sau xoá vĩnh viễn | CC-4, CC-6; CC-3 | 200; rồi 404 cả bốn | 200; 404, 404, 404, 404 | E-13 | Đạt (5 ca); 4 ca 404 lệch schema (G-07) |
| Person-13b đến Person-13e | People: xoá mềm, đọc, khôi phục, đọc | CC-4, CC-7; CC-3 | 200; 404; 200; 200 | Đúng cả bốn | E-13 | Đạt (4 ca); 1 ca 404 lệch schema (G-07) |
| Opportunity-01 đến Opportunity-05 | Opportunities: tạo, đọc lại, sửa một trường, đọc sau sửa, lọc theo id | CC-6, CC-7 | 201; 200 khớp; 200; 200 (stage đổi sang MEETING, amount giữ nguyên); 200, 1 bản ghi | Đúng cả năm | E-13 | Đạt (5 ca) |
| Opportunity-06 đến Opportunity-10 | Opportunities: xoá, rồi đọc, xoá lần hai, sửa, khôi phục sau xoá vĩnh viễn | CC-4, CC-6; CC-3 | 200; rồi 404 cả bốn | 200; 404, 404, 404, 404 | E-13 | Đạt (5 ca); 4 ca 404 lệch schema (G-07) |
| Opportunity-13b đến Opportunity-13e | Opportunities: xoá mềm, đọc, khôi phục, đọc | CC-4, CC-7; CC-3 | 200; 404; 200; 200 | Đúng cả bốn | E-13 | Đạt (4 ca); 1 ca 404 lệch schema (G-07) |
| Note-01 đến Note-05 | Notes: tạo, đọc lại, sửa một trường, đọc sau sửa, lọc theo id | CC-6, CC-7 | 201; 200 khớp; 200; 200 (title đổi, body giữ nguyên); 200, 1 bản ghi | Đúng cả năm | E-13 | Đạt (5 ca) |
| Note-06 đến Note-10 | Notes: xoá, rồi đọc, xoá lần hai, sửa, khôi phục sau xoá vĩnh viễn | CC-4, CC-6; CC-3 | 200; rồi 404 cả bốn | 200; 404, 404, 404, 404 | E-13 | Đạt (5 ca); 4 ca 404 lệch schema (G-07) |
| Note-13b đến Note-13e | Notes: xoá mềm, đọc, khôi phục, đọc | CC-4, CC-7; CC-3 | 200; 404; 200; 200 | Đúng cả bốn | E-13 | Đạt (4 ca); 1 ca 404 lệch schema (G-07) |
| Task-01 đến Task-05 | Tasks: tạo, đọc lại, sửa một trường, đọc sau sửa, lọc theo id | CC-6, CC-7 | 201; 200 khớp; 200; 200 (status đổi sang DONE, title giữ nguyên); 200, 1 bản ghi | Đúng cả năm | E-13 | Đạt (5 ca) |
| Task-06 đến Task-10 | Tasks: xoá, rồi đọc, xoá lần hai, sửa, khôi phục sau xoá vĩnh viễn | CC-4, CC-6; CC-3 | 200; rồi 404 cả bốn | 200; 404, 404, 404, 404 | E-13 | Đạt (5 ca); 4 ca 404 lệch schema (G-07) |
| Task-13b đến Task-13e | Tasks: xoá mềm, đọc, khôi phục, đọc | CC-4, CC-7; CC-3 | 200; 404; 200; 200 | Đúng cả bốn | E-13 | Đạt (4 ca); 1 ca 404 lệch schema (G-07) |

Cả 56 ca đều đạt về chức năng; 20 ca trả 404 cho bản ghi không còn tồn tại, mã này không có trong schema của từng đối tượng (G-07).

## 8. Nhật ký lỗi và lỗi G-07

| Lỗi | Loại | Căn cứ bị vi phạm | Test case tái hiện | Bằng chứng | Trạng thái |
|---|---|---|---|---|---|
| G-01 | Môi trường | Không vi phạm (giới hạn có chủ ý); nhưng 429 không khai báo trong schema | TC-SEED-03 | E-03 | Ghi nhận |
| G-02 | Bộ test của nhóm | CC-9 | TC-SEED-03 (trước sửa), TC-SEED-05 (sau sửa) | E-03, E-04, E-12 | Đã sửa, kiểm thử lại đạt |
| G-03 | Twenty, quan sát | CC-6 (201 nghĩa là đã tạo) | P4-01 | E-05, E-08 | Ghi nhận |
| G-04 | Twenty, lệch schema | CC-1, CC-10 | P3-05, P3-06 | E-06, E-11 | Báo nhóm |
| G-05 | Twenty, thiếu kiểm tra đầu vào | CC-2, CC-8 | P4-06, P4-07 | E-07 | Báo nhóm |
| G-06 | Twenty, quan sát | CC-7 | S6-01, S6-02 | E-09 | Ghi nhận |
| G-07 | Twenty, lệch schema | CC-3, CC-10 | P3-17, S6-07 đến S6-10, S6-12a–c, S6-13c và các ca tương ứng ở mục 7.1 | E-02, E-09, E-10, E-11, E-13 | Báo nhóm |

### G-07. Mã 404 không được khai báo trong schema

| Mục | Nội dung |
|---|---|
| Loại | Twenty, lệch schema (hợp đồng API) |
| Căn cứ | CC-3: `GET`, `PATCH`, `DELETE /companies/{id}` và `PATCH /companies/{id}/restore` chỉ khai báo 200, 400, 401; schema của `/people`, `/opportunities`, `/notes`, `/tasks` cũng vậy; CC-10: mã trả về phải nằm trong khai báo |
| Bước tái hiện | `GET /rest/companies/00000000-0000-4000-8000-000000000000` |
| Mong đợi theo schema | Một trong 200, 400, 401 |
| Thực tế | `404 {"statusCode":404,"error":"NotFoundException","messages":["Record not found"]}` |
| Đánh giá | Về chức năng, 404 là đúng chuẩn HTTP (CC-6), nên 29 ca liên quan (9 trên Companies, 20 trên 4 đối tượng còn lại) vẫn **đạt về chức năng**. Lỗi nằm ở schema: thiếu khai báo 404, nên công cụ kiểm thử dựa trên schema sẽ báo `status_code_conformance` ở các thao tác này. Tương tự, 429 (G-01) cũng không được khai báo |
| Mức độ | Thấp |
| Trạng thái | Đã xác nhận bằng tay. Báo Quang để đối chiếu với kết quả `status_code_conformance` của SC1 |

## 9. Tổng hợp và bằng chứng còn thiếu

| Phần | Số ca | Đạt | Lệch | Quan sát | Đạt về chức năng nhưng lệch schema (G-07) |
|---|---|---|---|---|---|
| Dữ liệu mẫu và ba luồng | 8 | 7 | 1 (G-02) | 0 | 0 |
| SC3 | 17 | 6 | 2 (G-04) | 9 | 1 |
| SC4 | 10 | 7 | 2 (G-05) | 1 | 0 |
| SC6 Companies | 18 | 17 | 0 | 1 | 8 |
| SC6 People, Opportunities, Notes, Tasks | 56 | 56 | 0 | 0 | 20 |
| **Tổng** | **109** | **93** | **5** | **11** | **29** |

Không ca nào trả lỗi 5xx.

Bằng chứng còn thiếu: ảnh chụp màn hình lần chạy ba luồng (`evidence/09_business_flows_trung.png`); output dạng văn bản đã có ở E-01.
