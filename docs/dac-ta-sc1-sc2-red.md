# Đặc tả SC1 (5 object), ca đỏ và bảng bất biến (Quang)

Bổ sung cho `Phan_Cong_module/KICH_BAN_K05.md` (mục SC1) và Phần E. K05 không viết từng giá trị input: Schemathesis sinh request từ OpenAPI, nhóm khai báo **bất biến** (điều phải luôn đúng) và cấu hình từng kịch bản.
Cập nhật 27/11/2026: SC1 mở rộng từ Companies ra 5 object; mã bất biến theo `KICH_BAN_K05.md`; mã lỗi theo bảng lỗi chung (`reports/bang-loi.md`, Thuận gộp).

## 1. Bảng bất biến I1–I7

Đánh số như `KICH_BAN_K05.md` và Phần E.

| Mã | Bất biến | Check Schemathesis | Kịch bản |
|---|---|---|---|
| I1 | Không trả 5xx với bất kỳ input nào | `not_a_server_error` | SC1, SC2, SC3, SC4, SC5 |
| I2 | Mã trạng thái nằm trong danh sách schema khai báo | `status_code_conformance` | SC1, SC2, SC3, SC4, SC5 |
| I3 | Body phản hồi đúng cấu trúc và kiểu của schema | `response_schema_conformance` | SC1, SC2, SC3, SC4, RED |
| I4 | Dữ liệu sai schema bị từ chối bằng 4xx | `negative_data_rejection` | SC1, SC2, SC3, SC4 |
| I5 | Dữ liệu đúng schema được chấp nhận | `positive_data_acceptance` | SC1, SC3 |
| I6 | Thiếu hoặc sai API key thì không truy cập được | `missing_required_header`, `ignored_auth` | SC1, SC5 |
| I7 | `Content-Type` đúng khai báo | `content_type_conformance` | SC1 |

Vi phạm một bất biến được ghi là "lệch tài liệu", sau đó kiểm chứng tay bằng `curl` để phân loại: lỗi của máy chủ hay lỗi của tài liệu OpenAPI.

## 2. SC1: quét 13 operation trên cả 5 object

| Mục | Nội dung |
|---|---|
| Người chạy | Quang (review: Thuận) |
| Mục tiêu | Gọi mọi operation của 5 object với dữ liệu đúng và sai do Schemathesis sinh từ schema, tìm chỗ hành vi lệch schema |
| Phạm vi | Companies, People, Opportunities, Notes, Tasks; mỗi object 13 operation (xem mục 2.2), tổng **65 operation**. Mỗi object chạy riêng một lần với `--include-path-regex ^/(batch/)?<object>(/\|$)` |
| Điều kiện đầu | Twenty `v2.45.6` chạy ở `localhost:3001`; `TWENTY_API_KEY` role Admin trong `.env`; đã có `schema/core.openapi.json` (`python scripts/fetch_schema.py`); **reset dữ liệu trước từng object** (`--reset`) |
| Dữ liệu test | `seed.py --count 30`, seed `20261020`: 30 bản ghi tiền tố `K05-` cho mỗi object (Person gắn Company, Opportunity gắn Company và Person). Id ghi ở `reports/seed-manifest.json` |
| Input | Schemathesis sinh: `--mode all` (dữ liệu đúng và sai), `--phases examples,coverage,fuzzing`, `--max-examples 50`, `--checks all`, `--seed 20261020`, `--generation-deterministic`, `--workers 1`, `--rate-limit auto` |
| Hook (`hooks/k05_hooks.py`) | Ca dương theo `{id}` (GET, PATCH, restore) dùng id seed thay UUID ngẫu nhiên để chạm bản ghi thật; `DELETE`/`PATCH` hàng loạt chỉ chạm bản ghi tạo sau mốc bắt đầu; `DELETE /{id}` và `merge` không được chạm bản ghi seed |
| Lệnh | Cả 5 object một lệnh: `python scripts/run_k05.py SC1 --object all --reset`. Một object: `python scripts/run_k05.py SC1 --object people --reset` |
| Kỳ vọng | I1 đến I7 không bị vi phạm. Mỗi vi phạm được tái hiện bằng `curl` (`reproducers/*.sh`) rồi phân loại lệch schema, lỗi chức năng hay quan sát |
| Đầu ra | Mỗi object một thư mục `reports/SC1/<thời điểm>-seed20261020-<object>/`: `summary.md`, `summary.json`, `REPRODUCERS.md`, `reproducers/*.sh`, `run-config.json`, báo cáo JSON/JUnit/HTML. Gộp 5 object: `python scripts/thong_ke.py` ghi `reports/thong-ke.md` |
| Tiêu chí đạt | Mỗi object phủ ≥ 11/13 operation; mỗi operation ≥ 50 test case (ngoại lệ `DELETE /{obj}/{id}` chỉ có 2 đầu vào, xem SC2 trong `KICH_BAN_K05.md`); chạy lần 2 cùng cấu hình, `summarize.py --compare` trùng ≥ 90% nhóm lỗi; mỗi nhóm lỗi có reproducer |

Rủi ro và biện pháp:

| Rủi ro | Biện pháp |
|---|---|
| Phase `examples` dùng ví dụ `filter` của schema, khớp mọi bản ghi; `DELETE /{obj}` kèm `soft_delete=false` xoá vĩnh viễn cả bảng (đã xảy ra 16/10: 209 công ty) | Hook bọc filter của ghi hàng loạt bằng `createdAt[gte]:"<mốc>"`; `--reset` trước từng object |
| Check `unsupported_method` gửi `DELETE`/`PATCH`/`PUT` tới `/{obj}/groupBy`, `/duplicates`, `/merge`, `/batch/{obj}`; Twenty hiểu thành ghi hàng loạt theo filter (D-11: SC1 27/11 xoá sạch cả 5 object, các ca theo id seed sau đó nhận 404 nên I2, I5 bị đếm lệch) | Hook bọc filter cho mọi request Twenty hiểu thành ghi hàng loạt (đường dẫn và phương thức lấy từ `parse-core-path.utils.ts`); sau mỗi lần chạy đếm lại seed, mất seed thì `thong_ke.py` loại lần chạy đó |
| Đồng hồ container Docker đi trước Windows làm bản ghi seed lọt qua mốc (SC2 26/11 mất 6/30 task) | Mốc = max(giờ máy + 1 giây, `createdAt` mới nhất trong DB + 1 ms); ghi nguồn mốc ở `run-config.json` |
| Giới hạn 100 request mỗi 60 giây mỗi key (429) | `--workers 1 --rate-limit auto`; không chạy cùng lúc với người khác trên cùng key |
| Bộ lọc lỗi của máy chủ đổi lỗi nội bộ thành 400, trông như "từ chối đúng" | Đọc `messages` trong body của các ca 400 khả nghi (ví dụ lộ `TypeError`, lỗi PostgreSQL) |

### 2.1. Đầu vào theo object

Schemathesis sinh body theo schema tạo của từng object (đếm từ `schema/core.openapi.json`). Trường liên kết (`…Id`) ở ca dương nhận UUID ngẫu nhiên, nên tạo bản ghi có liên kết tới id không tồn tại cũng là một tình huống được thử.

| Object | Schema body | Số trường | Trường tập giá trị (enum) | Trường phức hợp | Trường liên kết |
|---|---|---|---|---|---|
| Companies | `Company` | 9 | | `domainName`, `address`, `linkedinLink`, `annualRevenue`, `createdBy`, `updatedBy` | `accountOwnerId` |
| People | `Person` | 11 | | `name`, `emails`, `linkedinLink`, `phones`, `createdBy`, `updatedBy` | `companyId` |
| Opportunities | `Opportunity` | 10 | `stage` | `amount`, `createdBy`, `updatedBy` | `companyId`, `pointOfContactId`, `ownerId` |
| Notes | `Note` | 5 | | `bodyV2`, `createdBy`, `updatedBy` | |
| Tasks | `Task` | 8 | `status` | `bodyV2`, `createdBy`, `updatedBy` | `assigneeId` |

Không trường nào khai `required`, nên body rỗng `{}` là dữ liệu đúng theo schema và phải được nhận (I5).

### 2.2. 13 operation và điều được kiểm

| Operation | Ca dương Schemathesis gửi | Ca âm Schemathesis gửi | Bất biến chính |
|---|---|---|---|
| `GET /{obj}` | `limit`, `filter`, `order_by`, `depth`, con trỏ hợp lệ | `limit` ngoài 0–200, `depth` ngoài 0–1, chuỗi rác | I1, I2, I3, I4 |
| `POST /{obj}` | Body đúng kiểu | Sai kiểu, `null`, enum lạ | I1–I5 |
| `POST /batch/{obj}` | Mảng bản ghi đúng | Object thay vì mảng, phần tử sai kiểu | I1–I5 |
| `PATCH /{obj}` (hàng loạt) | Body và `filter` hợp lệ (đã bọc mốc) | Body sai kiểu | I1–I5 |
| `DELETE /{obj}` (hàng loạt) | `filter`, `soft_delete` hợp lệ (đã bọc mốc) | `soft_delete` không phải boolean | I1, I2, I4 |
| `GET /{obj}/{id}` | Id seed | Id không phải UUID | I1, I2, I3 |
| `PATCH /{obj}/{id}` | Id seed, body đúng | Body sai kiểu | I1–I5 |
| `DELETE /{obj}/{id}` | UUID không phải seed | Id không phải UUID, `soft_delete` lạ | I1, I2, I4 |
| `PATCH /{obj}/{id}/restore` | Id seed | Id không phải UUID | I1, I2, I3 |
| `PATCH /{obj}/restore` | `filter` hợp lệ | `filter` sai kiểu | I1, I2, I4 |
| `POST /{obj}/duplicates` | `ids` là mảng UUID | `ids` chứa `null`, sai kiểu | I1–I4 |
| `PATCH /{obj}/merge` | `ids`, `conflictPriorityIndex` | Sai kiểu | I1–I4 |
| `GET /{obj}/groupBy` | `group_by`, `aggregate` hợp lệ | Thiếu hoặc sai `group_by` | I1–I4 |

Mọi operation đều chịu thêm I6 (Schemathesis gửi lại request khi bỏ key) và I7 (`Content-Type` của phản hồi).

### 2.3. Kết quả

| Object | Lần chạy | Operation | Test case | 5xx | Nhóm lỗi | Tái lập |
|---|---|---|---|---|---|---|
| Companies | 16/10/2026, harness giữa kỳ (chưa có hook) | 13/13 | 1248 | 0 | 52 | 50/52 nhóm trùng lần 2; cả hai lần chạy trên bảng gần rỗng sau request thứ 34 |
| Companies | 27/11/2026 (Quang, Thuận) | | | | | **Loại**: D-11 xoá sạch seed giữa lần chạy (hook cũ), số lỗi I2, I5 bị lệch; lưu ở `reports/SC1/_lech-D11/` làm bằng chứng D-11 |
| Companies | Chạy chính thức (chờ, sau khi sửa hook 28/11) | | | | | |
| People | Chạy chính thức (chờ) | | | | | |
| Opportunities | Chạy chính thức (chờ) | | | | | |
| Notes | Chạy chính thức (chờ) | | | | | |
| Tasks | Chạy chính thức (chờ) | | | | | |

Điền bảng này từ `reports/thong-ke.md` sau khi chạy `python scripts/run_k05.py SC1 --object all --reset` hai lần rồi `python scripts/thong_ke.py`.

## 3. SC2: dữ liệu sai trên 5 object (Thuận chạy, Quang hỗ trợ harness)

SC2 do Thuận chạy và đặc tả chi tiết (Phần E mục SC2, `KICH_BAN_K05.md` nhánh `feat/sc2-thuan`). Harness dùng chung với SC1:
`python scripts/run_k05.py SC2 --object all --reset` (`--mode negative`, `--phases coverage,fuzzing`, `--max-examples 50`, bất biến I1 đến I4).

Các loại dữ liệu sai Schemathesis sinh và kỳ vọng:

| Loại | Ví dụ | Kỳ vọng |
|---|---|---|
| Sai kiểu | `"name": 123`, `"position": "abc"` | 400 |
| `null` ở trường không cho `null` | `"accountOwnerId": null` | 400 theo schema; thực tế máy chủ nhận, vì schema không khai `nullable` (D-09) |
| Ngoài tập giá trị cho phép | `"stage": "KHONG_CO"`, `createdBy.source` lạ | 400 |
| Sai định dạng | `id` không phải UUID, ngày sai định dạng | 400 |
| Ngoài biên | `limit=-1` | 400 |
| Ngoài biên | `limit=201` | 400 theo schema; thực tế cắt về 200, không báo lỗi (D-01) |
| Thuộc tính thừa, chuỗi rất dài, Unicode lạ | Khóa lạ trong body, chuỗi hàng nghìn ký tự, emoji, byte `\x00` | 400, không 5xx |
| Body sai cấu trúc | Object thay vì mảng ở `/batch/...`, JSON hỏng | 400 |

Lưu ý H3: server đổi mọi lỗi không phải `HttpException` thành 400, nên một lỗi nội bộ có thể trông như "từ chối đúng". Với mỗi 400 khả nghi phải đọc `messages` trong body, không chỉ mã trạng thái.

## 4. Ca đỏ cố ý (RED)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Chứng minh bộ test thật sự bắt được lỗi: cố tình làm schema sai một chỗ biết trước rồi xem bộ test có báo đỏ đúng chỗ đó không |
| Điều kiện đầu | Đã chạy SC1 với schema gốc để có kết quả đối chứng |
| Cách làm | `python scripts/make_red_case.py` tạo `schema/core.red.openapi.json`, đổi `CompanyForResponse.name` từ `string` sang `integer` và ghi chú `x-k05-red-case`; không sửa schema gốc |
| Lệnh | `python scripts/run_k05.py SC1 --object companies --reset --schema schema/core.red.openapi.json --label RED` |
| Bất biến | I3 |
| Kỳ vọng | I3 (`response_schema_conformance`) đỏ ở các operation trả về Company, thông điệp dạng `"..." is not of type "integer"`; lần chạy với schema gốc không có lỗi này |
| Kết quả | 16/10/2026 (harness giữa kỳ): **đạt**, I3 đỏ ở 4 operation trả Company (`GET /companies`, `POST /companies`, `PATCH /companies`, `PATCH /companies/restore`) với `"" is not of type "integer"`; lần chạy schema gốc không có lỗi này. Chạy lại với harness hiện tại: chờ |

## 5. Ca biên viết tay P5 (xác thực, nay thuộc SC5 của Tuấn)

Ca biên gọi thẳng những giá trị mà Schemathesis không chắc chạm tới. Ca P3 (phân trang) và P4 (batch) đặc tả ở `dac-ta-sc3-sc4.md`; tổng P3–P5 là 31 ca.
Cách kết luận khi chạy: **MATCH** = đúng kỳ vọng, **DIFF** = lệch kỳ vọng (ứng viên lỗi, phải xác minh tay), **OBSERVE** = chưa có kỳ vọng chắc, ghi lại hành vi.

| Mã ca | Request | Kỳ vọng | Căn cứ |
|---|---|---|---|
| P5-01 | `GET /companies` không gửi key | 401 | Tài liệu OpenAPI chỉ khai báo 401; thực tế 403 (D-02) |
| P5-02 | `GET /companies` key sai | 401 | `jwt.auth.strategy.ts`: key hỏng → 401 |
| P5-03 | `GET /companies` scheme `Basic` | 401 | Không có Bearer = không có key |
| P5-04 | `GET /companies` `Bearer` rỗng | 401 | Như P5-03 |
| P5-05 | `POST /companies` không key | 401 | Như P5-01, với thao tác ghi |
| P5-06 | `GET /open-api/core` không key | Quan sát | Endpoint công khai, không key chỉ trả khung schema |

Khi có key chỉ đọc (`TWENTY_API_KEY_LIMITED`) bổ sung P5-07 (đọc → 200) và P5-08 (ghi → 403).

## 6. Còn phải làm (Quang)

0. ~~Sửa hook để `unsupported_method` không xoá dữ liệu (D-11, Thuận báo 28/11)~~: xong 28/11, thêm đếm seed sau mỗi lần chạy.
1. Chạy chính thức SC1 trên 5 object hai lần: `python scripts/run_k05.py SC1 --object all --reset` (hai lần), rồi `python scripts/thong_ke.py`; điền mục 2.3.
2. Chạy lại RED với harness hiện tại.
3. Tái hiện từng nhóm lỗi mới của SC1 bằng `curl`, phân loại, ghi vào bảng lỗi chung (mã D-11 trở đi, báo Thuận).
4. So nhóm lỗi SC1 với SC2: lỗi nào đã có mã D thì chỉ ghi thêm "SC1" vào cột kịch bản.
