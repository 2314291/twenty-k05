# Bảng lỗi chung K05 (Báo cáo Phần G: danh sách lỗi và RCA)

Người gộp: Thuận. Cập nhật: 26/11/2026. Twenty `v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`), REST `http://localhost:3001/rest`.

Quy tắc (theo `Phan_Cong_module/KE_HOACH_PHAN_CONG_V2.md` mục 7):
- Mỗi lỗi **một mã D-xx duy nhất**; mã G-xx cũ ghi ở cột "Mã cũ". Một lỗi gặp ở nhiều kịch bản vẫn chỉ một mã.
- Mỗi lỗi phải có: kịch bản và object, reproducer (`curl` hoặc ca Schemathesis), kỳ vọng theo schema, thực tế, loại, nguyên nhân (RCA), mức độ, người phát hiện.
- **Loại:** *Lỗi chức năng* (máy chủ xử lý sai) · *Lệch schema* (tài liệu OpenAPI mô tả sai, máy chủ đúng) · *Quan sát* (hành vi đáng ghi nhận, chưa đủ căn cứ gọi là lỗi).
- **Trạng thái:** *Đã xác nhận* (có reproducer chạy lại được) · *Chờ xác nhận* (người phát hiện cần kiểm lại sau lần chạy chính thức).

Người phát hiện điền phần của mình vào đúng dòng, rồi gửi Thuận. Lỗi mới: lấy mã tiếp theo còn trống (D-11, D-12…) và báo nhóm để tránh trùng.

## 1. Tổng quan

| Mã | Mã cũ | Mô tả ngắn | Kịch bản | Object | Loại | Mức | Module code (RCA) | Người phát hiện | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| D-01 | G-04 | `limit` > 200 bị cắt âm thầm về 200 | SC3, SC2 | cả 5 | Lệch schema | Thấp | `input-request-parsers` | Trung; Tiến, Thuận xác nhận | Đã xác nhận |
| D-02 | | Thiếu API key trả 403, schema chỉ khai 401 | SC5, SC2 | cả 5 | Lệch schema | Thấp | `auth` + `open-api` | Quang (P5) | Chờ SC5 (Tuấn) |
| D-03 | G-07 | Schema không khai 404 (và 403, 429) ở mọi operation | SC3, SC6, SC2 | cả 5 | Lệch schema | Thấp | `open-api` | Trung; Thuận xác nhận | Đã xác nhận |
| D-04 | G-05 | Body batch sai kiểu lộ `TypeError` nội bộ (400) | SC4 | Companies, People, Notes | Lỗi chức năng | Trung bình | `rest/core` + bộ lọc lỗi | Trung; Tiến xác nhận | Đã xác nhận |
| D-05 | G-03 | Batch rỗng `[]` trả 201 dù không tạo gì | SC4 | Companies, People, Notes | Quan sát | Thấp | `rest/core` | Trung; Tiến xác nhận | Đã xác nhận |
| D-06 | G-06 | `domainName.primaryLinkUrl` bị bỏ `https://` | SC6 | Companies | Quan sát | Thấp | (chuẩn hoá dữ liệu) | Trung | Đã xác nhận |
| D-07 | | Tham số `boolean` (`soft_delete`, `upsert`) nhận mọi giá trị; `soft_delete=1` xoá vĩnh viễn | SC2 | cả 5 | Lỗi chức năng | **Cao** | `input-request-parsers` | Thuận | Đã xác nhận |
| D-08 | | `limit` thập phân lộ lỗi PostgreSQL (`invalid input syntax for type bigint`) | SC2 | cả 5 | Lỗi chức năng | Trung bình | `input-request-parsers` + bộ lọc lỗi | Thuận | Đã xác nhận |
| D-09 | | Schema không khai `nullable` ở bất kỳ trường nào; response trả `null` | SC2 (cả SC1, SC3, SC4) | cả 5 | Lệch schema | Trung bình | `open-api` | Thuận | Đã xác nhận |
| D-10 | | `groupBy`: body sai cấu trúc, số tổng hợp là chuỗi, thiếu mã 400; tham số sai bị bỏ qua | SC2 | cả 5 | Lệch schema (+ chức năng nhỏ) | Trung bình | `open-api` + `input-request-parsers` | Thuận | Đã xác nhận |
| D-11 | | *(SC1: Quang điền)* | SC1 | | | | | Quang | |
| D-12 | | *(SC5: Tuấn điền)* | SC5 | | | | | Tuấn | |

Không phải lỗi của Twenty (ghi riêng, không đánh mã D):

| Mã cũ | Mô tả | Loại | Xử lý |
|---|---|---|---|
| G-01 | Giới hạn 100 request / 60 giây mỗi key (429 `RATE_LIMITED`) | Môi trường (thiết kế có chủ ý) | `--rate-limit auto`, `--workers 1`, mỗi người một key |
| G-02 | `seed.py --cleanup` bỏ qua 429 và xoá manifest | Bộ test của nhóm | Đã sửa 02/11/2026 (chờ theo `retryAfterSeconds`) |
| (mới) | Hook `k05_hooks.py` chặn xoá hàng loạt nhưng không chặn `DELETE /{obj}/{id}`: SC2 xoá 6/30 task seed | Bộ test của nhóm | Luôn `--reset` trước khi chạy; báo Quang |
| (mới) | `summarize.py --compare` lỗi `UnicodeEncodeError` trên console Windows | Bộ test của nhóm | Tạm đặt `PYTHONUTF8=1`; báo Quang |

## 2. Thống kê

| Theo loại | Số lỗi | Mã |
|---|---|---|
| Lỗi chức năng | 3 | D-04, D-07, D-08 |
| Lệch schema | 5 | D-01, D-02, D-03, D-09, D-10 |
| Quan sát | 2 | D-05, D-06 |

| Theo module code | Số lỗi | Mã |
|---|---|---|
| `api/rest/input-request-parsers/` | 4 | D-01, D-07, D-08, D-10 (một phần) |
| `core-modules/open-api/` | 4 | D-02 (một phần), D-03, D-09, D-10 |
| `api/rest/core/` + `rest-api-exception.filter.ts` | 3 | D-04, D-05, D-08 (một phần) |
| `core-modules/auth/` | 1 | D-02 (một phần) |

*(Cập nhật khi có D-11 trở đi.)*

## 3. Chi tiết từng lỗi

Mẫu cho mỗi lỗi:

| Mục | Nội dung |
|---|---|
| Kịch bản, object | |
| Reproducer | |
| Kỳ vọng (theo schema) | |
| Thực tế | |
| Loại, mức | |
| Nguyên nhân (RCA) | |
| Người phát hiện, ngày | |
| Nguồn chi tiết | |

### D-01 (G-04). `limit` > 200 bị cắt âm thầm về 200

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC3 (P3-05, P3-06), SC2 (P2-06); cả 5 object |
| Reproducer | `curl -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=201&fields=id'` (cần > 200 bản ghi) |
| Kỳ vọng | 400 (schema: `limit` `integer`, `minimum 0`, `maximum 200`) |
| Thực tế | 200, đúng 200 bản ghi, không báo lỗi |
| Loại, mức | Lệch schema; thấp |
| Nguyên nhân | Mã cố ý cắt về `QueryMaxRecords` = 200 (`parse-limit-rest-request.util.ts`) thay vì từ chối, trong khi bộ sinh OpenAPI vẫn ghi `maximum: 200` (H1) |
| Người phát hiện, ngày | Trung 02/11/2026; Tiến, Thuận xác nhận 25–26/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc3-sc4.md` (G-04); `docs/kiem-thu-tien-sc3-sc4.md`; KIEM_CHUNG_B (SC2) |

### D-02. Thiếu API key trả 403, schema chỉ khai 401

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC5 (P5-01, P5-05); SC2 thấy ở mọi operation của cả 5 object |
| Reproducer | `curl -i 'http://localhost:3001/rest/companies'` (không gửi key) |
| Kỳ vọng | 401 (mã duy nhất schema khai cho lỗi xác thực) |
| Thực tế | 403 `{"messages":["Missing authentication token"],"error":"FORBIDDEN_EXCEPTION"}` |
| Loại, mức | Lệch schema; thấp |
| Nguyên nhân | *(Tuấn điền sau SC5: guard trả `FORBIDDEN_EXCEPTION` thay vì 401? schema thiếu 403?)* |
| Người phát hiện, ngày | Quang (ca P5); Thuận thấy lại trong SC2 26/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc1-sc2-red.md` mục 5; kết quả SC5 *(Tuấn)* |

### D-03 (G-07). Schema không khai 404, 403, 429

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC3 (P3-17), SC6 (S6-07 → S6-12), SC2 (P2-12); cả 5 object, 4 operation theo id mỗi object |
| Reproducer | `curl -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/00000000-0000-4000-8000-000000000000'` |
| Kỳ vọng | Mã nằm trong danh sách khai báo (`200, 400, 401`) |
| Thực tế | 404 `Record not found` (đúng chuẩn HTTP; id sai định dạng thì 400, cũng đúng) |
| Loại, mức | Lệch schema; thấp |
| Nguyên nhân | Bộ sinh OpenAPI chỉ sinh response 200/201, 400, 401 cho mọi operation; không sinh 404, 403, 429 dù máy chủ có trả |
| Người phát hiện, ngày | Trung (G-07); Thuận xác nhận 26/11/2026 |
| Nguồn chi tiết | `docs/test-case-trung.md` mục 8; KIEM_CHUNG_E_F (SC2) |

### D-04 (G-05). Body batch sai kiểu lộ `TypeError` nội bộ

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC4 (P4-06, P4-07); Companies, People, Notes |
| Reproducer | `curl -X POST -H 'Authorization: Bearer <KEY>' -H 'Content-Type: application/json' -d '{"name":"x"}' 'http://localhost:3001/rest/batch/companies'` |
| Kỳ vọng | 400 với thông điệp kiểm tra dữ liệu ("body phải là mảng") |
| Thực tế | 400, `error` = `TypeError`, `args.data.forEach is not a function` / `Cannot read properties of null (reading 'position')` |
| Loại, mức | Lỗi chức năng; trung bình |
| Nguyên nhân | Body batch không được kiểm tra là mảng các object trước khi xử lý; lỗi JavaScript bị bộ lọc lỗi đổi thành 400 (H3) |
| Người phát hiện, ngày | Trung 02/11/2026; Tiến xác nhận 25/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc3-sc4.md` (G-05); `docs/kiem-thu-tien-sc3-sc4.md` |

### D-05 (G-03). Batch rỗng trả 201

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC4 (P4-01); Companies, People, Notes |
| Reproducer | `curl -X POST -H 'Authorization: Bearer <KEY>' -H 'Content-Type: application/json' -d '[]' 'http://localhost:3001/rest/batch/companies'` |
| Kỳ vọng | Không có kỳ vọng chắc (200 hoặc 400 hợp lý hơn) |
| Thực tế | 201, không tạo bản ghi |
| Loại, mức | Quan sát; thấp |
| Nguyên nhân | Endpoint luôn trả "Created" sau khi xử lý mảng, kể cả mảng rỗng |
| Người phát hiện, ngày | Trung 02/11/2026; Tiến xác nhận |
| Nguồn chi tiết | `docs/dac-ta-sc3-sc4.md` (G-03) |

### D-06 (G-06). `domainName` bị bỏ `https://`

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC6 (S6-02); Companies |
| Reproducer | Tạo công ty với `"domainName":{"primaryLinkUrl":"https://k05-sc6.example.com"}`, đọc lại |
| Kỳ vọng | Đọc lại đúng giá trị đã gửi |
| Thực tế | `k05-sc6.example.com` |
| Loại, mức | Quan sát (chuẩn hoá dữ liệu); thấp |
| Nguyên nhân | *(Trung điền nếu có: chuẩn hoá URL khi lưu)* |
| Người phát hiện, ngày | Trung |
| Nguồn chi tiết | `docs/du-lieu-sc5-sc6.md` (G-06) |

### D-07. Tham số `boolean` nhận mọi giá trị; `soft_delete=1` xoá vĩnh viễn

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC2 (P2-02 → P2-05); cả 5 object (`DELETE /{obj}`, `DELETE /{obj}/{id}`, `POST /{obj}`, `POST /batch/{obj}`) |
| Reproducer | Tạo bản ghi `K05-A-repro`, `curl -X DELETE … '/rest/companies/<id>?soft_delete=1'` → 200, rồi `curl -X PATCH … '/rest/companies/<id>/restore'` → 404 |
| Kỳ vọng | 400 (schema: `soft_delete`, `upsert` là `boolean`) |
| Thực tế | 200/201. Chỉ chuỗi đúng `true` được hiểu là bật; `1`, `TRUE`, `True`, `abc`, `-1`, `null` đều bị coi là `false` (default): `soft_delete` → **xoá vĩnh viễn**, `upsert` → không upsert |
| Loại, mức | Lỗi chức năng; **cao** (mất dữ liệu không khôi phục được mà vẫn báo thành công) |
| Nguyên nhân | Parser so sánh chuỗi với `'true'` thay vì kiểm tra kiểu `boolean`; giá trị không hợp lệ rơi về default thay vì bị từ chối |
| Người phát hiện, ngày | Thuận 26/11/2026 (Schemathesis `negative_data_rejection` + kiểm tay) |
| Nguồn chi tiết | `Phan_Cong_module/KICH_BAN_K05.md` SC2 (P2); KIEM_CHUNG_A |

### D-08. `limit` thập phân lộ lỗi PostgreSQL

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC2 (P2-07); cả 5 object (`GET /{obj}`) |
| Reproducer | `curl -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=1.5'` |
| Kỳ vọng | 400 với thông điệp về `limit` (như `limit=abc`: `Should be an integer`) |
| Thực tế | 400 `invalid input syntax for type bigint: "2.5"` (giá trị = `limit + 1`) |
| Loại, mức | Lỗi chức năng; trung bình (lộ chi tiết nội bộ: kiểu cột, cách tính trang sau) |
| Nguyên nhân | Parser không kiểm tra `limit` là số nguyên; giá trị đi xuống câu SQL, PostgreSQL báo lỗi, bộ lọc lỗi đổi thành 400 (H3). Schemathesis không bắt được vì mã 400 hợp lệ |
| Người phát hiện, ngày | Thuận 26/11/2026 (kiểm tay) |
| Nguồn chi tiết | KICH_BAN_K05 SC2 (P2-07); KIEM_CHUNG_B |

### D-09. Schema không khai `nullable`

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC2 (P2-09, ~800 lần `response_schema_conformance`); sẽ gặp lại ở SC1, SC3, SC4; cả 5 object |
| Reproducer | `curl -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=1&depth=0'` → `"deletedAt": null`, `"accountOwnerId": null`, `"addressLat": null` |
| Kỳ vọng | Trường có thể `null` thì schema khai `nullable` / `type: [..., "null"]` |
| Thực tế | Toàn bộ `components` có 0 lần `nullable`; `deletedAt`, `*.workspaceMemberId`, `accountOwnerId`, `ownerId`, `assigneeId`, `avatarFile`, `addressLat/Lng`… trả `null` |
| Loại, mức | Lệch schema; trung bình (client sinh từ schema sẽ lỗi khi gặp `null`) |
| Nguyên nhân | Bộ sinh OpenAPI không chuyển cờ `isNullable` của field metadata sang schema |
| Người phát hiện, ngày | Thuận 26/11/2026 |
| Nguồn chi tiết | KIEM_CHUNG_C |

### D-10. `groupBy` mô tả sai trong schema

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC2 (P2-10, P2-11); cả 5 object (`GET /{obj}/groupBy`) |
| Reproducer | `curl -G -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/groupBy' --data-urlencode 'group_by=[{"updatedAt":true}]'` |
| Kỳ vọng | 200, body `{"data":{"companiesGroupBy":[…]}}`, số tổng hợp kiểu `number`; mã lỗi có khai báo |
| Thực tế | Body là mảng trần `[…]`; `"countNotEmptyId": "1"` (chuỗi); thiếu `group_by` trả 400 (schema chỉ khai 200); `limit=0.5`, `view_id=0` bị bỏ qua (200) |
| Loại, mức | Lệch schema (chính) + lỗi chức năng nhỏ (tham số sai bị bỏ qua); trung bình |
| Nguyên nhân | Bộ sinh OpenAPI mô tả response `groupBy` khác với dữ liệu controller thật trả về; parser `groupBy` không kiểm `limit`, `view_id` |
| Người phát hiện, ngày | Thuận 26/11/2026 |
| Nguồn chi tiết | KIEM_CHUNG_E_F |

## 4. RCA xuyên module (khung)

Quan sát chung: **mọi lỗi SC2 lặp y hệt ở cả 5 object**, vì Twenty sinh REST API và OpenAPI từ metadata theo một khuôn. Lỗi nằm ở mã dùng chung, không ở từng object. Các lỗi dồn về 3 module:

| Nguyên nhân gốc | Module | Lỗi | Hệ quả |
|---|---|---|---|
| R1. Tham số query không được kiểm tra theo kiểu và biên mà schema khai; giá trị sai bị bỏ qua, cắt, hoặc chuyển thẳng xuống DB | `api/rest/input-request-parsers/` | D-01, D-07, D-08, D-10 (một phần) | Nhận dữ liệu sai; mất dữ liệu (D-07); lộ lỗi DB (D-08) |
| R2. Bộ sinh OpenAPI không phản ánh đúng hành vi thật: thiếu `nullable`, thiếu mã 403/404/429, sai cấu trúc `groupBy` | `core-modules/open-api/` | D-02 (một phần), D-03, D-09, D-10 | Phần lớn báo động của Schemathesis; client sinh từ schema dễ lỗi |
| R3. Bộ lọc lỗi đổi mọi lỗi không phải `HttpException` thành 400 (H3), che lỗi nội bộ thành "từ chối đúng" | `api/rest/rest-api-exception.filter.ts` | D-04, D-08 | Lỗi thật trông như ca đạt; lộ thông điệp nội bộ |

*(Bổ sung khi có kết quả SC1, SC5: thêm dòng hoặc gắn D-11, D-12 vào R1–R3.)*

Việc còn lại cho phần RCA:
- Đọc mã nguồn Twenty v2.45.6 ở 3 module trên để dẫn đúng file/hàm cho R1–R3 (hiện là suy luận từ hành vi và `docs/architecture.md`).
- Đề xuất sửa cho từng nguyên nhân gốc (ví dụ R1: kiểm tra query bằng chính schema đã sinh; R2: sinh `nullable` từ `isNullable`, thêm 404).
