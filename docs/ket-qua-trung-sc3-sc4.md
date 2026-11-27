# SC3 trên People, Opportunities và SC4 trên Opportunities, Tasks (Trung)

Phần của Trung trong bảng phân công V2: **SC3** (phân trang, lọc, sắp xếp) trên **People, Opportunities**; **SC4** (batch) trên **Opportunities, Tasks**.
Chạy bằng script của Tiến (`scripts/kiem_thu_tien_sc3_sc4.py`), cùng bộ ca P3-01 đến P3-17 và P4-01 đến P4-08 với Companies
(`docs/dac-ta-sc3-sc4.md`) và Notes, Tasks, People (`docs/kiem-thu-tien-sc3-sc4.md`). Thiết kế ca: Phần E mục E.5, E.6.

## 1. Cách chạy

| Mục | Giá trị |
|---|---|
| Môi trường | Twenty `v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`), Docker, `http://localhost:3001`, máy Trung (Windows) |
| Khoá | `TWENTY_API_KEY` role Admin trong `.env` |
| Lệnh | `python scripts/kiem_thu_tien_sc3_sc4.py --only sc3 --objects people,opportunities` và `python scripts/kiem_thu_tien_sc3_sc4.py --only sc4 --objects opportunities,tasks`, mỗi lệnh chạy 2 lần liên tiếp |
| Dữ liệu | Script tự tạo bản ghi `K05-TIEN-` cho đủ hơn 200 bản ghi mỗi object, xoá vĩnh viễn ở cuối mỗi lần |
| Kết quả | 4 file trong `reports/kiem-thu-tien/`, có lệnh `curl` tái hiện cho mọi ca LỆCH và QUAN SÁT; khoá API đã che |

## 2. Kết quả và tái lập

| Lần | Kịch bản | Thời điểm | ĐẠT | LỆCH | QUAN SÁT | File kết quả |
|---|---|---|---|---|---|---|
| 1 | SC3 People, Opportunities | 27/11/2026 11:05 | 12 | 4 | 18 | `reports/kiem-thu-tien/20261127-110545.md` |
| 2 | SC3 People, Opportunities | 27/11/2026 11:13 | 12 | 4 | 18 | `reports/kiem-thu-tien/20261127-111335.md` |
| 1 | SC4 Opportunities, Tasks | 27/11/2026 11:21 | 10 | 4 | 2 | `reports/kiem-thu-tien/20261127-112125.md` |
| 2 | SC4 Opportunities, Tasks | 27/11/2026 11:30 | 10 | 4 | 2 | `reports/kiem-thu-tien/20261127-113050.md` |

**Tái lập:** hai lần chạy của mỗi lệnh cho cùng mã trả về, cùng số bản ghi trả về và cùng kết luận ở cả 50 ca. Không ca nào trả 5xx (I1 giữ).
Số bản ghi dọn cũng giống nhau giữa hai lần (SC3: people 205, opportunities 204; SC4: opportunities 262, tasks 262), nên không còn dữ liệu sót.

**So với Companies (cột "Comp."):** cả 50 ca cho cùng mã trả về với ca tương ứng trên Companies (02/11). Cùng với kết quả của Tiến trên Notes, Tasks, People,
SC3 và SC4 nay đã phủ đủ 5 object, và hành vi là như nhau ở mọi object.

### SC3 trên People, Opportunities (34 ca)

| Ca | People | Opportunities | Kết luận |
|---|---|---|---|
| P3-01 `limit=0` | 200, 0 bản ghi | 200, 0 bản ghi | Quan sát |
| P3-02 `limit=1` | 200, 1 bản ghi | 200, 1 bản ghi | Đạt |
| P3-03 `limit=60` | 200, 60 bản ghi | 200, 60 bản ghi | Đạt |
| P3-04 `limit=200` | 200, 200 bản ghi | 200, 200 bản ghi | Đạt |
| P3-05 `limit=201` | 200, 200 bản ghi | 200, 200 bản ghi | **Lệch** (D-01) |
| P3-06 `limit=100000` | 200, 200 bản ghi | 200, 200 bản ghi | **Lệch** (D-01) |
| P3-07 `limit=-1` | 400 | 400 | Đạt |
| P3-08 `limit=abc` | 400 | 400 | Đạt |
| P3-09 `limit=1.5` | 400 | 400 | Quan sát (xem D-08 ở mục 3) |
| P3-10 `limit=` rỗng | 200, 60 bản ghi (dùng mặc định) | 200, 60 bản ghi | Quan sát |
| P3-11 đến P3-16 (con trỏ rác, `%00`, `order_by` sai, `filter` sai cú pháp, `depth=99`, id không phải UUID) | 400 | 400 | Quan sát: đều bị từ chối rõ ràng |
| P3-17 UUID không tồn tại | 404 | 404 | Đạt (lệch schema D-03) |

### SC4 trên Opportunities, Tasks (16 ca)

| Ca | Opportunities | Tasks | Kết luận |
|---|---|---|---|
| P4-01 `[]` | 201, tạo 0 | 201, tạo 0 | Quan sát (D-05) |
| P4-02 1 bản ghi | 201, tạo 1 | 201, tạo 1 | Đạt |
| P4-05 61 bản ghi | 201, tạo 61 | 201, tạo 61 | Đạt: ngưỡng không phải 60 |
| P4-03 200 bản ghi | 201, tạo 200 | 201, tạo 200 | Đạt |
| P4-04 201 bản ghi | 400, tạo 0 | 400, tạo 0 | Đạt: từ chối hết, không tạo dở (I9) |
| P4-06 object thay vì mảng | 400, `error=TypeError` | 400, `error=TypeError` | **Lệch** (D-04) |
| P4-07 phần tử sai kiểu, `null`, chuỗi | 400, `error=TypeError` | 400, `error=TypeError` | **Lệch** (D-04) |
| P4-08 JSON hỏng | 400, `error=Bad Request` | 400, `error=Bad Request` | Đạt |

Script của Tiến không có hai ca sát biên B-03 (2 bản ghi) và B-05 (199 bản ghi); hai ca này đã chạy trên Companies (02/11) và đạt.

## 3. Lỗi: không có lỗi mới, mở rộng phạm vi lỗi đã có

Mỗi lỗi đã có reproducer và căn cứ trong `reports/bang-loi.md`; dưới đây chỉ ghi reproducer trên object mới và đề nghị Thuận cập nhật cột phạm vi.

| Mã | Ca | Reproducer trên object mới | Kỳ vọng | Thực tế | Loại | Cập nhật phạm vi |
|---|---|---|---|---|---|---|
| D-01 (G-04) | P3-05, P3-06 | `curl -H "Authorization: Bearer <KEY>" "http://localhost:3001/rest/opportunities?limit=201&fields=id"` (cần > 200 bản ghi) | 400 (`maximum: 200`) | 200, 200 bản ghi | Lệch schema, thấp | Thêm People, Opportunities: đủ 5 object |
| D-04 (G-05) | P4-06, P4-07 | `curl -X POST -H "Authorization: Bearer <KEY>" -H "Content-Type: application/json" -d "{\"title\":\"x\"}" http://localhost:3001/rest/batch/tasks` | 400 do kiểm tra dữ liệu | 400, `error: TypeError` | Lỗi chức năng, trung bình | Thêm Opportunities, Tasks: đủ 5 object |
| D-05 (G-03) | P4-01 | `curl -X POST -H "Authorization: Bearer <KEY>" -H "Content-Type: application/json" -d "[]" http://localhost:3001/rest/batch/opportunities` | 200 hoặc 400 | 201, tạo 0 | Quan sát, thấp | Thêm Opportunities, Tasks: đủ 5 object |
| D-03 (G-07) | P3-17 | `curl -H "Authorization: Bearer <KEY>" http://localhost:3001/rest/people/00000000-0000-4000-8000-000000000000` | Mã có khai báo (200, 400, 401) | 404 | Lệch schema, thấp | Đã ghi cả 5 object |
| D-08 | P3-09 | `curl -H "Authorization: Bearer <KEY>" "http://localhost:3001/rest/people?limit=1.5"` | 400 với thông điệp về `limit` | 400 `BadRequestException`, `invalid input syntax for type bigint: "2.5"` (cả People và Opportunities) | Lỗi chức năng, trung bình | Thêm People, Opportunities |

Lệnh `curl` đầy đủ cho từng ca nằm ở cuối file kết quả lần 2 của mỗi lệnh.

Về D-08: gửi `limit=1.5` nhưng thông điệp lỗi ghi `"2.5"`. Đây không phải chép nhầm: máy chủ cộng thêm 1 vào `limit` (lấy dư một bản ghi để biết còn trang sau hay không)
rồi đưa thẳng giá trị đó vào câu truy vấn PostgreSQL. Điều này củng cố nguyên nhân của D-08: `limit` không được kiểm tra là số nguyên ở tầng REST
trước khi xuống cơ sở dữ liệu, và thông điệp lộ chi tiết bên trong. Bằng chứng (27/11/2026, máy Trung):

```
people :
{"statusCode":400,"error":"BadRequestException","messages":["invalid input syntax for type bigint: \"2.5\""]}
opportunities :
{"statusCode":400,"error":"BadRequestException","messages":["invalid input syntax for type bigint: \"2.5\""]}
```

## 4. Rà soát lại toàn bộ kết quả của Trung theo ba nhóm

Quy tắc: lỗi của Twenty chỉ ghi lại, không sửa mã Twenty; lỗi của mã test nhóm thì sửa rồi chạy lại; kỳ vọng sai thì chỉ sửa khi có căn cứ và phải ghi lý do.

| Kết quả | Kịch bản | Nhóm | Xử lý đã làm | Trạng thái |
|---|---|---|---|---|
| `limit` > 200 bị cắt về 200 (D-01) | SC3, 5 object | Lỗi của Twenty (lệch schema) | Chỉ ghi lại | Đã xác nhận 5 object, 2 lần chạy mỗi object |
| Batch sai kiểu lộ `TypeError` (D-04) | SC4, 5 object | Lỗi của Twenty (chức năng) | Chỉ ghi lại | Đã xác nhận 5 object |
| Batch rỗng trả 201 (D-05) | SC4, 5 object | Quan sát về Twenty | Chỉ ghi lại | Đã xác nhận 5 object |
| 404 không có trong schema (D-03) | SC3, SC6, 5 object | Lỗi của Twenty (lệch schema) | Chỉ ghi lại | Đã xác nhận 5 object |
| `domainName` bị bỏ `https://` (D-06) | SC6, Companies | Quan sát về Twenty | Chỉ ghi lại | Đã xác nhận; chỉ Companies có trường này |
| Thiếu quyền trả 400 `PERMISSION_DENIED` thay vì 403 (mới) | SC5 (ca P5-08), Companies | Lỗi của Twenty (chức năng: sai mã trạng thái) | Chỉ ghi lại, chuyển Tuấn | Đã tái hiện 27/11, có đối chứng (xem mục 5) |
| Giới hạn 100 request mỗi 60 giây (G-01) | Mọi kịch bản | Môi trường, không phải lỗi | Mã test đi chậm 1 request/giây, chờ khi gặp 429 | Đã xử lý trong mọi script |
| `seed.py --cleanup` bỏ qua 429 (G-02) | Dữ liệu mẫu | Lỗi mã test của nhóm | Đã sửa (PR #7), chạy lại đạt (E-12) | Đã đóng |
| S6-10 kỳ vọng khôi phục được sau `DELETE` | SC6 | Kỳ vọng sai của người thiết kế | Sửa kỳ vọng thành 404, căn cứ: schema `soft_delete` mặc định `false`; thêm S6-13 để kiểm khôi phục sau xoá mềm | Đã ghi lý do trong `test-case-trung.md` |
| P3-05, P3-06 trong `KICH_BAN_K05.md` ghi kỳ vọng "Quan sát" | SC3 | Không nhất quán giữa các tài liệu | Theo schema (`maximum: 200`) kỳ vọng là 400; `test-case-trung.md`, `kiem-thu-tien-sc3-sc4.md` và Phần E đều ghi 400 | Đề nghị sửa `KICH_BAN_K05.md` cho khớp |
| Ba luồng nghiệp vụ, SC6 trên 5 object, phần còn lại của SC3, SC4 | | Đạt | | Chạy lại đều ra cùng kết quả |

## 5. Phát hiện mới cho SC5 (chuyển Tuấn)

Phát hiện khi kiểm tra key role chỉ đọc ngày 27/11/2026, máy Trung.

| Mục | Nội dung |
|---|---|
| Reproducer | `curl -X POST -H "Authorization: Bearer <KEY_CHI_DOC>" -H "Content-Type: application/json" --data-binary @body.json http://localhost:3001/rest/companies`, với `body.json` là `{"name":"K05-test-chi-doc"}` |
| Đối chứng | Cùng body, key role Admin: `201`, tạo được (body hợp lệ); đọc `GET /rest/companies?limit=1` bằng key chỉ đọc: `200` |
| Kỳ vọng | 403 (đã xác thực nhưng không có quyền) |
| Thực tế | `400 {"statusCode":400,"error":"Error","messages":["Entity performing the request does not have permission"],"code":"PERMISSION_DENIED"}` |
| Loại, mức | Lỗi chức năng (sai mã trạng thái), thấp: ghi vẫn bị chặn nên không phải lỗ hổng bảo mật; nhưng 400 không có trong ý nghĩa "thiếu quyền" và người gọi không phân biệt được với dữ liệu sai |
| Đề nghị | Tuấn sửa kỳ vọng P5-08, chạy trên 5 object; Thuận cấp mã D mới |
