# Mô tả kịch bản kiểm thử K05 (Báo cáo Phần E)

Đề tài: R10 Twenty CRM + K05 Schema-Based API / Fuzz. Cập nhật 25/11/2026.
Twenty `v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`), REST `http://localhost:3001/rest`, schema `GET /open-api/core` (lưu ở `schema/core.openapi.json`), công cụ Schemathesis.

Tổng hợp từ `docs/scenarios.md`, `docs/dac-ta-sc1-sc2-red.md`, `docs/dac-ta-sc3-sc4.md` (main) và `docs/du-lieu-sc5-sc6.md`, `docs/test-case-trung.md` (PR #11, #12 của Trung).

## 1. Cách K05 hoạt động

K05 không viết tay từng input. Schemathesis đọc file OpenAPI, tự sinh hàng loạt request (dữ liệu đúng và dữ liệu sai) cho từng operation, rồi kiểm tra phản hồi theo các **bất biến** (điều phải luôn đúng). Nhóm chỉ khai báo phạm vi, cấu hình và bất biến; với những giá trị biên mà Schemathesis không chắc chạm tới, nhóm viết thêm ca tay (probe).

Mỗi chỗ phản hồi khác schema được ghi là "lệch", rồi tái hiện bằng `curl` để phân loại: **lệch schema** (tài liệu OpenAPI sai) hay **lỗi chức năng** (máy chủ sai).

## 2. Phạm vi

| Mục | Giá trị |
|---|---|
| Module (object) | Companies, People, Opportunities, Notes, Tasks |
| Operation mỗi object (13) | `POST /batch/{obj}`; `GET`, `POST`, `DELETE`, `PATCH /{obj}`; `POST /{obj}/duplicates`; `GET /{obj}/groupBy`; `PATCH /{obj}/merge`; `PATCH /{obj}/restore`; `GET`, `DELETE`, `PATCH /{obj}/{id}`; `PATCH /{obj}/{id}/restore` |
| Tổng | 65 operation |
| Ngoài phạm vi | GraphQL (SC7, chỉ làm nếu dư thời gian), metadata API, giao diện web |

## 3. Bất biến (I1 đến I7)

| Mã | Bất biến | Check Schemathesis |
|---|---|---|
| I1 | Không trả 5xx với bất kỳ input nào | `not_a_server_error` |
| I2 | Mã trạng thái nằm trong danh sách schema khai báo | `status_code_conformance` |
| I3 | Body phản hồi đúng cấu trúc và kiểu của schema | `response_schema_conformance` |
| I4 | Dữ liệu sai schema bị từ chối bằng 4xx | `negative_data_rejection` |
| I5 | Dữ liệu đúng schema được chấp nhận | `positive_data_acceptance` |
| I6 | Thiếu hoặc sai API key thì không truy cập được | `ignored_auth`, `missing_required_header` |
| I7 | `Content-Type` đúng khai báo | `content_type_conformance` |

## 4. Điều kiện đầu và dữ liệu test chung

| Hạng mục | Giá trị |
|---|---|
| Môi trường | Twenty chạy bằng Docker (`env/docker-compose.yml`), `http://localhost:3001` |
| Khóa | `TWENTY_API_KEY` (đủ quyền), `TWENTY_API_KEY_LIMITED` (role chỉ đọc), đọc từ `.env`, không ghi vào file kết quả |
| Dữ liệu | Tiền tố `K05-`; seed cố định `20261020`; `python scripts/seed.py --cleanup` rồi `python scripts/seed.py --count 30` (SC3 dùng `--count 120`) |
| Tái lập | `--generation-deterministic`; chạy hai lần cùng cấu hình phải ra cùng tập lỗi |
| Giới hạn | 100 request mỗi 60 giây cho mỗi key; chạy `--workers 1 --rate-limit auto` |

## 5. Tiêu chí đạt của nhóm

Do nhóm tự đặt trong `SPEC.md` (thầy không quy định con số): mỗi object phủ ≥ 11/13 operation (≥ 80%); mỗi operation ≥ 50 test case; mỗi lỗi có reproducer; hai lần chạy cùng cấu hình cho cùng tập lỗi.

---

## SC1. Quét 13 operation với dữ liệu theo schema

| Mục | Nội dung |
|---|---|
| Người chạy | Quang |
| Mục tiêu | Gọi mọi operation với dữ liệu đúng và sai, tìm chỗ hành vi lệch schema |
| Phạm vi | 5 object × 13 operation |
| Điều kiện đầu | Twenty chạy; key đủ quyền; đã seed lại |
| Input | Schemathesis sinh: `--mode all`, `--phases examples,coverage,fuzzing`, `--max-examples 50`, `--checks all` |
| Lệnh | `python scripts/run_k05.py SC1` (harness của Quang, cần khôi phục từ lịch sử git) |
| Kỳ vọng / bất biến | I1 đến I7 |
| Đầu ra | `summary.md` (số request, lỗi theo check và operation), reproducer `curl` cho từng nhóm lỗi |
| Rủi ro | Phase `examples` có bộ lọc khớp mọi bản ghi; gửi vào `DELETE /{obj}` hoặc `PATCH /{obj}` có thể xóa hoặc sửa toàn bộ dữ liệu. Seed lại trước mỗi lần chạy |

**Ca đỏ cố ý (RED):** chứng minh bộ test bắt được lỗi. Tạo bản sao schema, đổi `CompanyForResponse.name` từ `string` sang `integer` (không sửa schema gốc), chạy lại SC1 trên bản sao. Kỳ vọng: I3 đỏ ở các operation trả Company, lần chạy với schema gốc không có lỗi đó.

## SC2. Dữ liệu sai (negative)

| Mục | Nội dung |
|---|---|
| Người chạy | Thuận (Quang hỗ trợ harness) |
| Mục tiêu | Mọi input vi phạm schema phải bị từ chối rõ ràng bằng 4xx, không nhận nhầm, không 5xx |
| Phạm vi | 5 object × 13 operation |
| Điều kiện đầu | Như SC1 |
| Input | `--mode negative`, `--phases coverage,fuzzing`, `--max-examples 50` |
| Lệnh | `python scripts/run_k05.py SC2` |
| Kỳ vọng / bất biến | I1, I2, I3, I4 |

| Loại dữ liệu sai | Ví dụ | Kỳ vọng |
|---|---|---|
| Sai kiểu | `"name": 123`, `"position": "abc"` | 400 |
| `null` ở trường không cho `null` | `"accountOwnerId": null` | 400 |
| Ngoài tập giá trị | `"stage": "KHONG_CO"` | 400 |
| Sai định dạng | `id` không phải UUID, ngày sai | 400 |
| Ngoài biên | `limit=-1` | 400 |
| Thuộc tính thừa, chuỗi rất dài, Unicode lạ, byte `\x00` | | 400, không 5xx |
| Body sai cấu trúc | Object thay vì mảng ở `/batch/...`, JSON hỏng | 400 |

Lưu ý: máy chủ đổi mọi lỗi nội bộ thành 400, nên với 400 khả nghi phải đọc `messages` trong body (ví dụ batch sai kiểu lộ `TypeError`).

## SC3. Phân trang, lọc, sắp xếp

| Mục | Nội dung |
|---|---|
| Người chạy | Trung (Companies đã chạy, People, Opportunities); Tiến (Notes, Tasks) |
| Mục tiêu | `limit`, con trỏ, lọc, sắp xếp xử lý đúng giá trị biên, không 5xx, phân trang nhất quán |
| Phạm vi | `GET /{obj}`, `GET /{obj}/{id}` trên 5 object |
| Điều kiện đầu | ≥ 120 bản ghi mỗi object (`seed.py --count 120`) |
| Lệnh | `python scripts/run_k05.py SC3` và `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc3 --object <obj>` |
| Kỳ vọng / bất biến | I1, I2, I3; số bản ghi trả về ≤ `limit` hiệu lực |

| Ca | Request | Kỳ vọng |
|---|---|---|
| P3-01 | `limit=0` | Quan sát |
| P3-02 | `limit=1` | 200, đúng 1 bản ghi |
| P3-03 | `limit=60` | 200 (mặc định) |
| P3-04 | `limit=200` | 200 (tối đa) |
| P3-05 | `limit=201` | Quan sát: bị cắt về 200, không báo lỗi (D-01) |
| P3-06 | `limit=100000` | Quan sát |
| P3-07 | `limit=-1` | 400 |
| P3-08 | `limit=abc` | 400 |
| P3-09 | `limit=1.5` | Quan sát |
| P3-10 | `limit=` (rỗng) | Quan sát |
| P3-11 | `starting_after` không phải con trỏ | Quan sát |
| P3-12 | `ending_before=%00` | Quan sát |
| P3-13 | `order_by` trường không tồn tại | Quan sát |
| P3-14 | `filter=name[eq` (sai cú pháp) | Quan sát |
| P3-15 | `depth=99` (schema chỉ cho 0, 1) | Quan sát |
| P3-16 | `GET /{obj}/not-a-uuid` | Quan sát |
| P3-17 | `GET /{obj}/<UUID không tồn tại>` | 404 |

## SC4. Batch

| Mục | Nội dung |
|---|---|
| Người chạy | Trung (Companies đã chạy, Opportunities, Tasks); Tiến (People, Notes) |
| Mục tiêu | Xác nhận ngưỡng batch 200 bản ghi và cách từ chối khi vượt ngưỡng hoặc body sai |
| Phạm vi | `POST /batch/{obj}` trên 5 object |
| Điều kiện đầu | Key đủ quyền; bản ghi probe tên `K05-PROBE-*`, tự xóa sau khi chạy |
| Lệnh | `python scripts/run_k05.py SC4` và `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc4 --object <obj>` |
| Kỳ vọng / bất biến | I1, I2, I3, I4; từ chối rõ ràng, không nhận một phần rồi báo lỗi mơ hồ |

| Ca | Body | Kỳ vọng |
|---|---|---|
| P4-01 | `[]` | Quan sát (thực tế trả 201, G-03) |
| P4-02 | 1 bản ghi | 200 hoặc 201 |
| P4-03 | 200 bản ghi | 200 hoặc 201 |
| P4-04 | 201 bản ghi | 4xx, `Maximum number of records to upsert is 200` |
| P4-05 | 61 bản ghi | 200 hoặc 201 (ngưỡng thật là 200, không phải 60) |
| P4-06 | Object thay vì mảng | Quan sát |
| P4-07 | `[{"name":123}, null, "x"]` | Quan sát (thực tế lộ `TypeError`, G-05) |
| P4-08 | JSON hỏng | Quan sát |

## SC5. Xác thực

| Mục | Nội dung |
|---|---|
| Người chạy | Tuấn (Trung cấp key chỉ đọc và dữ liệu) |
| Mục tiêu | Không có quyền thì không đọc, không ghi được; key chỉ đọc không ghi được |
| Phạm vi | 5 object × 13 operation, với 4 loại key |
| Điều kiện đầu | Có ≥ 1 bản ghi mỗi object; đã tạo role chỉ đọc và key gán role đó |
| Lệnh | `python scripts/run_k05.py SC5 --variant none`, `--variant wrong`, `--variant limited` |
| Kỳ vọng / bất biến | I1, I2, I6 |

| Loại key | Cách có | Kỳ vọng |
|---|---|---|
| Đủ quyền | Settings → API, lưu `TWENTY_API_KEY` | Mọi thao tác thành công (đối chứng) |
| Chỉ đọc | Role chỉ bật quyền đọc 5 object, lưu `TWENTY_API_KEY_LIMITED` | Đọc → 200; ghi → 403 |
| Sai | Chuỗi bất kỳ, ví dụ `k05-sai-key-000000` | 401 |
| Không có | Không gửi `Authorization` | 401 theo schema; thực tế trả 403 (D-02, lệch schema) |

Ca biên tay: P5-01 `GET` không key; P5-02 key sai; P5-03 scheme `Basic`; P5-04 `Bearer` rỗng; P5-05 `POST` không key; P5-06 `GET /open-api/core` không key (quan sát); P5-07 key chỉ đọc đọc → 200; P5-08 key chỉ đọc ghi → 403.
Lưu ý: với `none` và `wrong`, Schemathesis cảnh báo "Authentication failed". Đó là kết quả mong đợi, không phải lỗi môi trường.

## SC6. Chuỗi vòng đời bản ghi (mở rộng)

| Mục | Nội dung |
|---|---|
| Người chạy | Trung |
| Mục tiêu | Kiểm tra điều request rời rạc khó chạm tới, vì mỗi bước cần `id` do bước trước tạo ra |
| Phạm vi | 5 object; tên bản ghi tiền tố `K05-SC6-` |
| Điều kiện đầu | Key đủ quyền; body tạo lấy từ các hàm `build_*` trong `seed.py` |
| Lệnh | `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc6 --object <obj>` |
| Bất biến | Bản ghi đã xóa không đọc lại được; sửa một trường không làm mất trường khác; `id` ổn định suốt chuỗi; không 5xx |
| Đã chạy | Chạy tay trên 5 object (02/11 và 12/11/2026), tất cả đạt; script mới có Companies |

| Ca | Bước | Request | Kỳ vọng |
|---|---|---|---|
| S6-01 | Tạo | `POST /{obj}` | 201, có `id` |
| S6-02 | Đọc lại | `GET /{obj}/{id}` | 200, trường khớp (domain bị bỏ `https://`, G-06) |
| S6-03 | Sửa một trường | `PATCH /{obj}/{id}` | 200 |
| S6-04 | Đọc sau sửa | `GET /{obj}/{id}` | Trường đã đổi, trường khác giữ nguyên |
| S6-05 | Có trong danh sách | `GET /{obj}?filter=id[eq]:<id>` | Đúng 1 bản ghi |
| S6-06 | Xóa | `DELETE /{obj}/{id}` (mặc định xóa vĩnh viễn) | 200 |
| S6-07 | Đọc sau xóa | `GET /{obj}/{id}` | 404 |
| S6-08 | Xóa lần hai | `DELETE /{obj}/{id}` | 404, không 5xx |
| S6-09 | Sửa sau xóa | `PATCH /{obj}/{id}` | 404, không 5xx |
| S6-10 | Khôi phục sau xóa vĩnh viễn | `PATCH /{obj}/{id}/restore` | 404 |
| S6-11 | Quan hệ | Tạo Company, Person gắn Company, xóa Company, đọc Person | Quan sát, không 5xx |
| S6-12 | Id lạ | `GET`, `PATCH`, `DELETE` UUID không tồn tại | 404 |
| S6-13 | Xóa mềm rồi khôi phục | `DELETE ?soft_delete=true`; `GET`; `restore`; `GET` | 200; 404; 200; 200 |

---

## 6. Lỗi đã ghi nhận đến nay

| Mã | Mô tả | Loại |
|---|---|---|
| D-01 (G-04) | `limit` > 200 bị cắt về 200, không báo lỗi | Quan sát |
| D-02 | Thiếu key trả 403, schema chỉ khai báo 401 | Lệch schema |
| G-03 | Batch mảng rỗng trả 201 | Quan sát |
| G-05 | Batch phần tử sai kiểu lộ `TypeError` trong thông điệp | Lỗi chức năng |
| G-06 | `domainName` bị bỏ `https://` | Quan sát |
| G-07 | Schema không khai báo 404, 403, 429 ở bất kỳ operation nào | Lệch schema |

Các lỗi trên chưa được xác minh lại sau khi chạy chính thức. Khi gộp bảng lỗi, mỗi lỗi giữ một mã D-xx, mã G-xx cũ để ở cột "mã cũ".

## 7. Mỗi lỗi phải ghi

Mã lỗi; kịch bản và object; request tái hiện (`curl`); kết quả mong đợi theo schema; kết quả thực tế; loại (lệch schema hoặc lỗi chức năng); nguyên nhân (RCA); mức độ; người phát hiện.
