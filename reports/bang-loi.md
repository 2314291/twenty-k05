# Bảng lỗi chung K05 (Báo cáo Phần G: danh sách lỗi và RCA)

Người gộp: Thuận. Cập nhật: 28/11/2026. Twenty `v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`), REST `http://localhost:3001/rest`.

Quy tắc (theo `Phan_Cong_module/KE_HOACH_PHAN_CONG_V2.md` mục 7):
- Mỗi lỗi **một mã D-xx duy nhất**; mã G-xx cũ ghi ở cột "Mã cũ". Một lỗi gặp ở nhiều kịch bản vẫn chỉ một mã.
- Mỗi lỗi phải có: kịch bản và object, reproducer (`curl` hoặc ca Schemathesis), kỳ vọng theo schema, thực tế, loại, nguyên nhân (RCA), mức độ, người phát hiện.
- **Loại:** *Lỗi chức năng* (máy chủ xử lý sai) · *Lệch schema* (tài liệu OpenAPI mô tả sai, máy chủ đúng) · *Quan sát* (hành vi đáng ghi nhận, chưa đủ căn cứ gọi là lỗi).
- **Trạng thái:** *Đã xác nhận* (có reproducer chạy lại được) · *Chờ xác nhận* (người phát hiện cần kiểm lại sau lần chạy chính thức).

Người phát hiện điền phần của mình vào đúng dòng, rồi gửi Thuận. Lỗi mới: lấy mã tiếp theo còn trống (D-13, D-14…) và báo nhóm để tránh trùng. D-11 đã dùng cho lỗi SC1 ở trên; lỗi SC1 khác của Quang lấy D-13 trở đi.

## 1. Tổng quan

| Mã | Mã cũ | Mô tả ngắn | Kịch bản | Object | Loại | Mức | Module code (RCA) | Người phát hiện | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| D-01 | G-04 | `limit` > 200 bị cắt âm thầm về 200 | SC3, SC2 | cả 5 | Lệch schema | Thấp | `input-request-parsers` | Trung; Tiến, Thuận xác nhận | Đã xác nhận |
| D-02 | | Thiếu API key trả 403, schema chỉ khai 401 | SC5, SC2 | cả 5 | Lệch schema | Thấp | `auth` + `open-api` | Tuấn (P5); Thuận thấy lại ở SC2 | Đã xác nhận |
| D-03 | G-07 | Schema không khai 404 (và 403, 429) ở mọi operation | SC3, SC6, SC2 | cả 5 | Lệch schema | Thấp | `open-api` | Trung; Thuận xác nhận | Đã xác nhận |
| D-04 | G-05 | Body batch sai kiểu lộ `TypeError` nội bộ (400) | SC4 | cả 5 | Lỗi chức năng | Trung bình | `rest/core` + bộ lọc lỗi | Trung; Tiến xác nhận | Đã xác nhận |
| D-05 | G-03 | Batch rỗng `[]` trả 201 dù không tạo gì | SC4 | cả 5 | Quan sát | Thấp | `rest/core` | Trung; Tiến xác nhận | Đã xác nhận |
| D-06 | G-06 | `domainName.primaryLinkUrl` bị bỏ `https://` | SC6 | Companies | Quan sát | Thấp | (chuẩn hoá dữ liệu) | Trung | Đã xác nhận |
| D-07 | | Tham số `boolean` (`soft_delete`, `upsert`) nhận mọi giá trị; `soft_delete=1` xoá vĩnh viễn | SC2 | cả 5 | Lỗi chức năng | **Cao** | `input-request-parsers` | Thuận | Đã xác nhận |
| D-08 | | `limit` thập phân lộ lỗi PostgreSQL (`invalid input syntax for type bigint`) | SC2 | cả 5 | Lỗi chức năng | Trung bình | `input-request-parsers` + bộ lọc lỗi | Thuận | Đã xác nhận |
| D-09 | | Schema không khai `nullable` ở bất kỳ trường nào; response trả `null` | SC2 (cả SC1, SC3, SC4) | cả 5 | Lệch schema | Trung bình | `open-api` | Thuận | Đã xác nhận |
| D-10 | | `groupBy`: body sai cấu trúc, số tổng hợp là chuỗi, thiếu mã 400; tham số sai bị bỏ qua | SC2 | cả 5 | Lệch schema (+ chức năng nhỏ) | Trung bình | `open-api` + `input-request-parsers` | Thuận | Đã xác nhận |
| D-11 | | `DELETE /{obj}/groupBy` (và `/duplicates`, `/merge`) bị hiểu thành xoá hàng loạt: **xoá vĩnh viễn** mọi bản ghi khớp filter | SC1 | cả 5 | Lỗi chức năng | **Cao** | `input-request-parsers` (đọc đường dẫn) | Thuận (khi chạy lại SC1 bằng harness của Quang) | Đã xác nhận |
| D-12 | | Key đã xác thực nhưng thiếu quyền ghi trả **400** `PERMISSION_DENIED` thay vì 403 | SC5 | cả 5 | Lỗi chức năng (sai mã trạng thái) | Thấp | `permissions` + bộ lọc lỗi REST (R3) | Trung (27/11); Tuấn xác nhận 5 object (28/11) | Đã xác nhận |

Không phải lỗi của Twenty (ghi riêng, không đánh mã D):

| Mã cũ | Mô tả | Loại | Xử lý |
|---|---|---|---|
| G-01 | Giới hạn 100 request / 60 giây mỗi key (429 `RATE_LIMITED`) | Môi trường (thiết kế có chủ ý) | `--rate-limit auto`, `--workers 1`, mỗi người một key |
| G-02 | `seed.py --cleanup` bỏ qua 429 và xoá manifest | Bộ test của nhóm | Đã sửa 02/11/2026 (chờ theo `retryAfterSeconds`) |
| (mới) | Hook `k05_hooks.py` chặn xoá hàng loạt nhưng không chặn `DELETE /{obj}/{id}`: SC2 xoá 6/30 task seed | Bộ test của nhóm | Quang đã sửa (commit `632dab4`, PR #20) |
| (mới) | `summarize.py --compare` lỗi `UnicodeEncodeError` trên console Windows | Bộ test của nhóm | Quang đã sửa (commit `26e0092`, PR #20) |
| (mới) | Hook không chặn phương thức ghi trên `/{obj}/groupBy`, `/duplicates`, `/merge`: check `unsupported_method` của SC1 gửi `DELETE /{obj}/groupBy` và xoá sạch dữ liệu (D-11), các ca theo id seed sau đó nhận 404 nên kết quả SC1 27/11 bị đếm lệch | Bộ test của nhóm | Quang đã sửa (commit `3eda5d9`, PR #20); SC1 chạy lại trên máy Tiến 28/11 (PR #21) |

## 2. Thống kê

| Theo loại | Số lỗi | Mã |
|---|---|---|
| Lỗi chức năng | 5 | D-04, D-07, D-08, D-11, D-12 |
| Lệch schema | 5 | D-01, D-02, D-03, D-09, D-10 |
| Quan sát | 2 | D-05, D-06 |

| Theo module code | Số lỗi | Mã |
|---|---|---|
| `api/rest/input-request-parsers/` | 5 | D-01, D-07, D-08, D-10 (một phần), D-11 |
| `core-modules/open-api/` | 4 | D-02 (một phần), D-03, D-09, D-10 |
| `api/rest/core/` + `rest-api-exception.filter.ts` | 4 | D-04, D-05, D-08 (một phần), D-12 |
| `core-modules/auth/` | 1 | D-02 (một phần) |

*(Cập nhật khi có D-13 trở đi.)*

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
| Nguyên nhân | **[mã]** `api/rest/input-request-parsers/limit-parser-utils/parse-limit-rest-request.util.ts:30` trả `Math.min(limit, maxLimit)` với `QUERY_MAX_RECORDS = 200` (`twenty-shared/src/constants/QueryMaxRecords.ts`): cắt thay vì từ chối, trong khi bộ sinh OpenAPI vẫn ghi `maximum: 200` (H1) |
| Người phát hiện, ngày | Trung 02/11/2026; Tiến, Thuận xác nhận 25–26/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc3-sc4.md` (G-04); `docs/kiem-thu-tien-sc3-sc4.md`; `reports/SC2/KIEM_CHUNG_B.md` |

### D-02. Thiếu API key trả 403, schema chỉ khai 401

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC5: ma trận 260 ca, cột `none` 65/65 ca (5 object × 13 operation) trả 403, 2 lần chạy 28/11; ca tay P5-01, P5-03, P5-04, P5-05 (một nguyên nhân, tính là một lỗi). SC1, SC2 thấy ở mọi operation của cả 5 object |
| Reproducer | `curl -i 'http://localhost:3001/rest/companies?limit=1'` (không gửi key); `curl -i -H 'Authorization: Bearer ' '…'` (Bearer rỗng); `Authorization: Basic <key>` cũng cho kết quả như vậy |
| Kỳ vọng | 401 (schema chỉ khai 200/400/401; RFC 9110: chưa xác thực là 401) |
| Thực tế | 403 `{"statusCode":403,"messages":["Missing authentication token"],"error":"FORBIDDEN_EXCEPTION"}`. Đối chứng: key **sai** (P5-02) ra 401 đúng, nên server chỉ gắn sai mã khi **không có** token |
| Loại, mức | Lệch schema (server vẫn chặn đúng, không lộ dữ liệu); thấp. Tác hại: client nhận 403 hiểu là "thiếu quyền", không biết cần gắn key |
| Nguyên nhân | **[mã]** `core-modules/auth/token/services/access-token.service.ts:195–221` (`validateTokenByRequest`): không có Bearer token và không có cookie phiên thì ném `AuthException('Missing authentication token', AuthExceptionCode.FORBIDDEN_EXCEPTION)` (dòng 217–220); token có nhưng sai thì đi nhánh `UNAUTHENTICATED`. `middlewares/middleware.service.ts` (`getStatus`) đổi lỗi qua `core-modules/auth/utils/get-auth-exception-rest-status.util.ts`: `FORBIDDEN_EXCEPTION` → 403, `UNAUTHENTICATED` → 401. `Basic …` và `Bearer ` rỗng không khớp mẫu `Bearer <chuỗi>` nên cũng bị coi là không có token. Phía schema: `open-api/utils/path.utils.ts` không khai 403 (cùng gốc với D-03) |
| Người phát hiện, ngày | Tuấn (17/10/2026, xác nhận lại 25–26/11/2026 với 4 reproducer); Thuận thấy lại trong SC2 26/11/2026; Thuận đối chiếu mã nguồn 27/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc5.md` mục 5, 7; `evidence/sc5-thu-cong-20261126.md`; `reports/sc5/20261128-010047.md`, `reports/sc5/20261128-010929.md` |

### D-03 (G-07). Schema không khai 404, 403, 429

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC3 (P3-17), SC6 (S6-07 → S6-12), SC2 (P2-12); cả 5 object, 4 operation theo id mỗi object |
| Reproducer | `curl -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/00000000-0000-4000-8000-000000000000'` |
| Kỳ vọng | Mã nằm trong danh sách khai báo (`200, 400, 401`) |
| Thực tế | 404 `Record not found` (đúng chuẩn HTTP; id sai định dạng thì 400, cũng đúng) |
| Loại, mức | Lệch schema; thấp |
| Nguyên nhân | **[mã]** `core-modules/open-api/utils/path.utils.ts`: mọi operation chỉ khai `'200'`/`'201'`, `'400'`, `'401'` (ví dụ find-one dòng 140–142, delete-one 154–156); không có nhánh nào sinh 403, 404, 429 dù máy chủ có trả |
| Người phát hiện, ngày | Trung (G-07); Thuận xác nhận 26/11/2026 |
| Nguồn chi tiết | `docs/test-case-trung.md` mục 8; `reports/SC2/KIEM_CHUNG_E_F.md` |

### D-04 (G-05). Body batch sai kiểu lộ `TypeError` nội bộ

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC4 (P4-06, P4-07); cả 5 object (Companies, People, Notes đến 25/11; Opportunities, Tasks ngày 27/11) |
| Reproducer | `curl -X POST -H 'Authorization: Bearer <KEY>' -H 'Content-Type: application/json' -d '{"name":"x"}' 'http://localhost:3001/rest/batch/companies'` |
| Kỳ vọng | 400 với thông điệp kiểm tra dữ liệu ("body phải là mảng") |
| Thực tế | 400, `error` = `TypeError`, `args.data.forEach is not a function` / `Cannot read properties of null (reading 'position')` |
| Loại, mức | Lỗi chức năng; trung bình |
| Nguyên nhân | **[mã]** `api/rest/core/handlers/rest-api-create-many.handler.ts:89` lấy thẳng `data: request.body`, không kiểm tra là mảng các object; `api/common/common-query-runners/common-create-many-query-runner/common-create-many-query-runner.service.ts:259` gọi `args.data.forEach(...)` → `TypeError` với object; bộ lọc lỗi đổi thành 400 (R3) |
| Người phát hiện, ngày | Trung 02/11/2026; Tiến xác nhận 25/11/2026; Trung xác nhận trên Opportunities, Tasks 27/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc3-sc4.md` (G-05); `docs/kiem-thu-tien-sc3-sc4.md`; `docs/ket-qua-trung-sc3-sc4.md` mục 3 |

### D-05 (G-03). Batch rỗng trả 201

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC4 (P4-01); cả 5 object (Companies, People, Notes đến 25/11; Opportunities, Tasks ngày 27/11) |
| Reproducer | `curl -X POST -H 'Authorization: Bearer <KEY>' -H 'Content-Type: application/json' -d '[]' 'http://localhost:3001/rest/batch/companies'` |
| Kỳ vọng | Không có kỳ vọng chắc (200 hoặc 400 hợp lý hơn) |
| Thực tế | 201, không tạo bản ghi |
| Loại, mức | Quan sát; thấp |
| Nguyên nhân | Endpoint luôn trả "Created" sau khi xử lý mảng, kể cả mảng rỗng |
| Người phát hiện, ngày | Trung 02/11/2026; Tiến xác nhận; Trung xác nhận trên Opportunities, Tasks 27/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc3-sc4.md` (G-03); `docs/ket-qua-trung-sc3-sc4.md` mục 3 |

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
| Nguyên nhân | **[mã]** `api/rest/input-request-parsers/soft-delete-parser-utils/parse-soft-delete-rest-request.util.ts:12` là `return request.query.soft_delete === 'true';` và `upsert-parser-utils/parse-upsert-rest-request.util.ts:12` là `return request.query.upsert === 'true';`. So sánh đúng chuỗi `'true'`, không kiểm tra kiểu, không ném lỗi: mọi giá trị khác thành `false`. Cùng kiểu ở `group-by-with-records/parse-include-records-sample-rest-request.util.ts:12` (`include_records_sample`) |
| Người phát hiện, ngày | Thuận 26/11/2026 (Schemathesis `negative_data_rejection` + kiểm tay) |
| Nguồn chi tiết | `Phan_Cong_module/KICH_BAN_K05.md` SC2 (P2); `reports/SC2/KIEM_CHUNG_A.md` |

### D-08. `limit` thập phân lộ lỗi PostgreSQL

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC2 (P2-07); cả 5 object (`GET /{obj}`) |
| Reproducer | `curl -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=1.5'` |
| Kỳ vọng | 400 với thông điệp về `limit` (như `limit=abc`: `Should be an integer`) |
| Thực tế | 400 `invalid input syntax for type bigint: "2.5"` (giá trị = `limit + 1`) |
| Loại, mức | Lỗi chức năng; trung bình (lộ chi tiết nội bộ: kiểu cột, cách tính trang sau) |
| Nguyên nhân | **[mã]** `parse-limit-rest-request.util.ts:21–23`: `const limit = +request.query.limit;` rồi chỉ chặn `isNaN(limit) \|\| limit < 0`. Không kiểm tra số nguyên, dù thông điệp lỗi ghi "Should be an integer". `1.5` lọt qua, tới `api/common/common-query-runners/common-find-many-query-runner.service.ts:188` `queryBuilder.limit(limit + 1)` → PostgreSQL báo `bigint: "2.5"` → bộ lọc lỗi đổi thành 400 (R3). Schemathesis không bắt được vì mã 400 hợp lệ |
| Người phát hiện, ngày | Thuận 26/11/2026 (kiểm tay) |
| Nguồn chi tiết | KICH_BAN_K05 SC2 (P2-07); `reports/SC2/KIEM_CHUNG_B.md` |

### D-09. Schema không khai `nullable`

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC2 (P2-09, ~800 lần `response_schema_conformance`); sẽ gặp lại ở SC1, SC3, SC4; cả 5 object |
| Reproducer | `curl -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=1&depth=0'` → `"deletedAt": null`, `"accountOwnerId": null`, `"addressLat": null` |
| Kỳ vọng | Trường có thể `null` thì schema khai `nullable` / `type: [..., "null"]` |
| Thực tế | Toàn bộ `components` có 0 lần `nullable`; `deletedAt`, `*.workspaceMemberId`, `accountOwnerId`, `ownerId`, `assigneeId`, `avatarFile`, `addressLat/Lng`… trả `null` |
| Loại, mức | Lệch schema; trung bình (client sinh từ schema sẽ lỗi khi gặp `null`) |
| Nguyên nhân | **[mã]** `core-modules/open-api/utils/components.utils.ts`: cờ `field.isNullable` chỉ được dùng ở dòng 56 (chọn ví dụ) và dòng 180 (`getRequiredFields`); phần sinh kiểu cho từng property không đọc `isNullable`, nên không trường nào được khai `nullable` / `type: [..., "null"]` |
| Người phát hiện, ngày | Thuận 26/11/2026 |
| Nguồn chi tiết | `reports/SC2/KIEM_CHUNG_C.md` |

### D-10. `groupBy` mô tả sai trong schema

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC2 (P2-10, P2-11); cả 5 object (`GET /{obj}/groupBy`) |
| Reproducer | `curl -G -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/groupBy' --data-urlencode 'group_by=[{"updatedAt":true}]'` |
| Kỳ vọng | 200, body `{"data":{"companiesGroupBy":[…]}}`, số tổng hợp kiểu `number`; mã lỗi có khai báo |
| Thực tế | Body là mảng trần `[…]`; `"countNotEmptyId": "1"` (chuỗi); thiếu `group_by` trả 400 (schema chỉ khai 200); `limit=0.5`, `view_id=0` bị bỏ qua (200) |
| Loại, mức | Lệch schema (chính) + lỗi chức năng nhỏ (tham số sai bị bỏ qua); trung bình |
| Nguyên nhân | **[mã]** Schema: `core-modules/open-api/utils/responses.utils.ts:487` (`getGroupByResponse200`) bọc kết quả trong `data.{namePlural}GroupBy` và khai số tổng hợp `additionalProperties: {type: 'number'}`; `path.utils.ts:306–307` chỉ khai `'200'`. Máy chủ: `api/rest/core/handlers/rest-api-group-by.handler.ts:66` `return results;` trả mảng trần. Tham số: `limit` dùng chung `parseLimitRestRequest` (không kiểm số nguyên, như D-08). Thêm: schema khai `view_id`, nhưng `input-request-parsers/view-id-parser-utils/parse-view-id-rest-request.util.ts:9` đọc `request.query.viewId`, nên `view_id` theo tài liệu không bao giờ được đọc *(quan sát từ mã, chưa chứng minh được trên instance vì view không tồn tại cũng bị bỏ qua)* |
| Người phát hiện, ngày | Thuận 26/11/2026 |
| Nguồn chi tiết | `reports/SC2/KIEM_CHUNG_E_F.md` |

### D-11. `DELETE /{obj}/groupBy` xoá vĩnh viễn mọi bản ghi khớp filter

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC1 (check `unsupported_method`); cả 5 object. Cũng đúng với `DELETE /{obj}/duplicates` |
| Reproducer | **An toàn** (filter chỉ khớp id không tồn tại, xoá mềm): `curl -X DELETE -G -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies/groupBy' --data-urlencode 'filter=id[eq]:"00000000-0000-4000-8000-000000000000"' --data-urlencode 'soft_delete=true'` → `200 {"data":{"deleteCompanies":[]}}`. Ca gốc của Schemathesis (**không chạy trên dữ liệu thật**): `DELETE /rest/tasks/groupBy?group_by=[{"updatedAt":true}]&filter=createdAt[gte]:"2023-01-01"&…` |
| Kỳ vọng | 405 Method Not Allowed (schema chỉ khai `GET` cho `/{obj}/groupBy`), hoặc ít nhất 4xx |
| Thực tế | 200, body `{"data":{"deleteTasks":[…]}}`: server chạy **xoá cứng hàng loạt** theo `filter`. Lần chạy SC1 27/11 xoá sạch cả 5 object (47 công ty, 50 người, 45 cơ hội, 41 ghi chú, 39 việc, gồm toàn bộ 30 bản ghi seed mỗi object). `DELETE /{obj}/duplicates` cho cùng kết quả (`deleteCompanies`). `PATCH /{obj}/groupBy` vào nhánh cập nhật hàng loạt và lộ `TypeError` (400). Đối chứng: `DELETE /companies/abc` → 400 `'abc' is not a valid UUID` |
| Loại, mức | Lỗi chức năng; **cao**: mất dữ liệu không khôi phục được, chỉ cần một request sai phương thức. Request vẫn cần key hợp lệ có quyền xoá, nên không phải lỗ hổng cho người ngoài |
| Nguyên nhân | **[mã]** `api/rest/input-request-parsers/path-parser-utils/parse-core-path.utils.ts:42–47`: đoạn thứ hai là `duplicates`, `groupBy` hoặc `merge` thì trả `{ object }` (không id) **với mọi phương thức HTTP**. Route `@Delete('*path')` của `api/rest/core/controllers/rest-api-core.controller.ts` bắt mọi đường dẫn, rồi `api/rest/core/services/rest-api-core.service.ts:85–88`: không id và không `soft_delete=true` → `restApiDestroyManyHandler` (xoá cứng). Chính đội Twenty đã chặn đúng lỗi này cho `/restore` (comment dòng 15: *"other methods' wildcard routes would read the id as a target (DELETE would destroy it)"*) nhưng chưa chặn cho `groupBy`, `duplicates`, `merge` |
| Người phát hiện, ngày | Thuận 27/11/2026, khi chạy lại SC1 bằng harness nhánh `feat/sc1-harness-quang` |
| Nguồn chi tiết | `reports/SC1/20261127-*-seed20261020-{companies,…,tasks}/ndjson-*.ndjson` (bản ghi request/response của ca `GET /{obj}/groupBy`, check `unsupported_method`), chưa đưa lên git |

### D-12. Key đã xác thực nhưng thiếu quyền ghi trả 400 thay vì 403

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC5; cả 5 object × 9 thao tác ghi (`POST`, `POST /batch`, `PATCH /{id}`, `PATCH`, `PATCH /merge`, `PATCH /{id}/restore`, `PATCH /restore`, `DELETE /{id}`, `DELETE`): 42 ca (3 ca `merge` trên Opportunities, Notes, Tasks không áp dụng), cộng ca tay P5-08 |
| Reproducer | `curl -X POST -H 'Authorization: Bearer <KEY_CHI_DOC>' -H 'Content-Type: application/json' --data-binary '{"name":"K05-D12"}' 'http://localhost:3001/rest/companies'` (key gán role **K05 Chi doc**, chỉ bật `canReadObjectRecords` cho 5 object) |
| Đối chứng | Cùng request bằng key đủ quyền: 200/201 (request hợp lệ). Đọc bằng key chỉ đọc: 200 (key hợp lệ). Ma trận 260 ca chạy 2 lần (28/11 01:00 và 01:09): **GIỐNG 260, KHÁC 0** |
| Kỳ vọng | 403 (RFC 9110 mục 15.5.4: đã xác thực nhưng không được phép) |
| Thực tế | `400 {"statusCode":400,"error":"Error","messages":["Entity performing the request does not have permission"],"code":"PERMISSION_DENIED"}` ở cả 42 ca ghi |
| Loại, mức | Lỗi chức năng (sai mã trạng thái); thấp: thao tác ghi vẫn bị chặn (cột Chặn của SC5: ĐẠT 248, LỖI BẢO MẬT 0). Schema có khai 400 nên I2 không báo, nhưng 400 trong schema mang nghĩa dữ liệu sai: client không phân biệt được "thiếu quyền" với "dữ liệu sai", dễ thử lại vô ích |
| Nguyên nhân | **[mã]** (Thuận đối chiếu theo đề nghị của Tuấn) `metadata-modules/permissions/permissions.exception.ts:166`: `PermissionsException extends CustomException`; `utils/custom-exception.ts:19–22`: `CustomException extends CustomError`, không phải `HttpException`. Bộ lọc `api/rest/rest-api-exception.filter.ts:27–28` trả 400 cho mọi lỗi không phải `HttpException` (R3). Trường `"error":"Error"` trong body (thay vì `ForbiddenException`) khớp với đường đi này. Ngược với D-02: thiếu token bị gắn 403, còn thiếu quyền thật lại ra 400 |
| Đề xuất sửa | Ánh xạ `PermissionsExceptionCode.PERMISSION_DENIED` sang 403 ở tầng REST; khai 403 trong schema (gộp với đề xuất R2) |
| Người phát hiện, ngày | Trung 27/11/2026 (1 ca `POST /companies`, máy Trung); Tuấn xác nhận trên 5 object × 9 thao tác ghi 28/11/2026 (2 lần chạy, máy Tuấn); Thuận đối chiếu mã nguồn 27/11/2026 |
| Nguồn chi tiết | `docs/dac-ta-sc5.md` mục 5 (P5-08), 6, 7; `reports/sc5/20261128-010047.md`, `reports/sc5/20261128-010929.md`; `docs/ket-qua-trung-sc3-sc4.md` mục 5 |

## 4. RCA xuyên module (khung)

Quan sát chung: **mọi lỗi SC2 lặp y hệt ở cả 5 object**, vì Twenty sinh REST API và OpenAPI từ metadata theo một khuôn. Lỗi nằm ở mã dùng chung, không ở từng object. Các lỗi dồn về 4 nguyên nhân gốc (R1 đến R4):

Đã đối chiếu với mã nguồn Twenty tag `twenty/v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`) ngày 26–27/11/2026. Đường dẫn dưới đây tính từ `packages/twenty-server/src/engine/`. **[mã]** = đọc trực tiếp từ mã nguồn.

| Nguyên nhân gốc | Bằng chứng trong mã | Lỗi | Hệ quả |
|---|---|---|---|
| **R1. Không có tầng kiểm tra tham số query theo schema.** Mỗi tham số có một hàm parse viết tay riêng, mỗi hàm tự quyết định cách xử lý giá trị sai: so chuỗi rồi rơi về `false`, cắt về giá trị tối đa, chỉ chặn `NaN`, hoặc đọc sai tên | `api/rest/input-request-parsers/`: `parse-soft-delete-rest-request.util.ts:12`, `parse-upsert-rest-request.util.ts:12` (`=== 'true'`); `parse-limit-rest-request.util.ts:21–30` (chỉ chặn `NaN`/âm, rồi `Math.min`); `parse-view-id-rest-request.util.ts:9` (đọc `viewId`, schema khai `view_id`); `path-parser-utils/parse-core-path.utils.ts:42–47` (bỏ qua `groupBy`/`duplicates`/`merge` mà không xét phương thức) | D-01, D-07, D-08, D-10 (một phần), D-11 | Nhận dữ liệu sai mà vẫn báo thành công; **mất dữ liệu** (D-07, D-11); giá trị sai lọt xuống SQL (D-08) |
| **R2. Bộ sinh OpenAPI viết tay, tách rời khỏi mã xử lý thật.** Schema không sinh từ cùng nguồn với handler, nên lệch ở nhiều chỗ | `core-modules/open-api/utils/components.utils.ts` (`isNullable` chỉ dùng cho `required` và ví dụ, dòng 56, 180); `path.utils.ts` (mọi operation chỉ khai 200/201, 400, 401; `groupBy` chỉ 200, dòng 306–307); `responses.utils.ts:487` (`groupBy` bọc `data.*GroupBy`, trong khi `rest-api-group-by.handler.ts:66` trả mảng trần) | D-02 (một phần), D-03, D-09, D-10 | Phần lớn báo động của Schemathesis (~800 lần `response_schema_conformance` ở SC2); client sinh từ schema đọc sai kết quả |
| **R3. Bộ lọc lỗi REST đổi mọi lỗi không phải `HttpException` thành 400.** Lỗi JavaScript và lỗi PostgreSQL trông như "từ chối dữ liệu sai" | `api/rest/rest-api-exception.filter.ts:27–28`: `exception instanceof HttpException ? exception.getStatus() : 400;`. Comment của chính đội Twenty ngay dòng đó: *"should actually default to 500 but we dont have input validation yet and dont want to be flooded with errors from input"* (issue `twentyhq/core-team-issues#1027`). Lỗi phân quyền `PermissionsException` (kế thừa `CustomException`, không phải `HttpException`) cũng rơi vào nhánh này | D-04, D-08, D-12 | Lỗi nội bộ bị che thành ca "đạt" (Schemathesis không báo); lộ thông điệp nội bộ (`TypeError`, `bigint`); thiếu quyền ra 400 thay vì 403 (D-12) |
| **R4. Gắn sai mã lỗi xác thực.** "Không có token" là lỗi xác thực nhưng bị dán nhãn `FORBIDDEN_EXCEPTION` (dành cho thiếu quyền) | `core-modules/auth/token/services/access-token.service.ts:217–220`; bảng đổi mã `core-modules/auth/utils/get-auth-exception-rest-status.util.ts` (`FORBIDDEN_EXCEPTION` → 403) | D-02 (cùng với R2: schema không khai 403) | Mọi request thiếu key ở mọi operation của cả 5 object đều lệch schema; client không phân biệt được "thiếu key" với "thiếu quyền" |

**Liên hệ giữa R1, R2, R3:** comment ở R3 cho thấy đội Twenty **biết** REST API chưa có kiểm tra input (R1), và chọn trả 400 cho mọi lỗi để giảm nhiễu. Hệ quả kép: dữ liệu sai hoặc bị nhận âm thầm (R1), hoặc gây lỗi nội bộ rồi bị che thành 400 (R3). Vì schema (R2) lại được viết tay riêng, nó mô tả một API "chặt" hơn API thật, nên công cụ kiểm thử dựa trên schema báo lệch hàng loạt. Cả ba cùng nằm ở mã dùng chung cho mọi object, nên **mọi lỗi lặp y hệt ở cả 5 object**.

Đề xuất sửa:

| Nguyên nhân | Đề xuất |
|---|---|
| R1 | Kiểm tra query bằng chính schema đã sinh (hoặc DTO có validation) trước khi gọi handler; `boolean` chỉ nhận `true`/`false`, `limit` phải là số nguyên trong `[0, 200]`, trả 400 với thông điệp rõ ràng; thống nhất tên `view_id`; `parseCorePath` chỉ nhận `groupBy` với `GET`, `duplicates` với `POST`, `merge` với `PATCH` (như đã làm cho `/restore`), phương thức khác trả 405 |
| R2 | Sinh `nullable` từ `isNullable`; thêm response 403, 404, 429 dùng chung; sửa `getGroupByResponse200` cho khớp mảng thật (hoặc sửa handler bọc `data`) và kiểu số tổng hợp |
| R3 | Sau khi có R1, trả 500 cho lỗi không phải `HttpException` (đúng như comment trong mã đề xuất) và không đưa thông điệp nội bộ ra ngoài; đổi các lỗi đã biết sang mã đúng trước khi rơi vào mặc định (`PermissionsException` → 403) |
| R4 | Đổi mã ở `access-token.service.ts:219` thành `AuthExceptionCode.UNAUTHENTICATED` (401); hoặc giữ 403 và khai thêm 403 cho mọi operation (gộp với đề xuất R2) |

*(Bổ sung khi có kết quả SC1 và ma trận 260 ca SC5: thêm dòng hoặc gắn D-11, D-12 vào R1–R4.)*
