# Phần E. Mô tả kịch bản kiểm thử K05

Đề tài R10 Twenty CRM + K05 Schema-Based API / Fuzz. Twenty `v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`),
REST `http://localhost:3001/rest`, schema `schema/core.openapi.json` (tải từ `GET /open-api/core`), công cụ Schemathesis 4.31.1 và script Python.

Người ghép: Trung. Ghép từ `Phan_Cong_module/KICH_BAN_K05.md`, `docs/dac-ta-sc1-sc2-red.md` (Quang), nhánh `feat/sc2-thuan` (Thuận),
`docs/dac-ta-sc3-sc4.md`, `docs/du-lieu-sc5-sc6.md`, `docs/test-case-trung.md` (Trung), `docs/kiem-thu-tien-sc3-sc4.md` (Tiến),
nhánh `feat/sc5-tuan` (Tuấn). Phần này chỉ mô tả thiết kế; số liệu chạy và danh sách lỗi ở Phần G (`reports/bang-loi.md`).

## E.1. Nguyên tắc chung

K05 không viết tay từng input. Schemathesis đọc OpenAPI, tự sinh dữ liệu đúng và sai cho từng operation, rồi kiểm phản hồi theo
**bất biến**. Với giá trị biên mà Schemathesis không chắc chạm tới (phân trang, batch, chuỗi vòng đời, loại key), nhóm viết thêm
**ca tay** bằng script hoặc `curl`. Mỗi chỗ lệch được tái hiện bằng `curl` rồi phân loại: **lệch schema** (tài liệu sai, máy chủ đúng),
**lỗi chức năng** (máy chủ sai) hoặc **quan sát** (chưa đủ căn cứ gọi là lỗi).

### Bất biến

| Mã | Bất biến | Check Schemathesis | Kịch bản dùng |
|---|---|---|---|
| I1 | Không trả 5xx với bất kỳ input nào | `not_a_server_error` | Tất cả |
| I2 | Mã trạng thái nằm trong danh sách schema khai báo | `status_code_conformance` | Tất cả |
| I3 | Body phản hồi đúng cấu trúc và kiểu của schema | `response_schema_conformance` | SC1, SC2, SC3, SC4, RED |
| I4 | Dữ liệu sai schema bị từ chối bằng 4xx | `negative_data_rejection` | SC1, SC2, SC3, SC4 |
| I5 | Dữ liệu đúng schema được chấp nhận | `positive_data_acceptance` | SC1, SC3, SC6 |
| I6 | Thiếu hoặc sai API key thì không truy cập được | `missing_required_header`, `ignored_auth` | SC1, SC5 |
| I7 | `Content-Type` đúng khai báo | `content_type_conformance` | SC1 |

Ca tay dùng thêm hai bất biến không có trong Schemathesis: **I8** nhất quán dữ liệu (đọc lại bằng dữ liệu đã ghi, sửa một trường không
đổi trường khác, xoá xong không đọc được; SC6) và **I9** không nhận một phần (batch bị từ chối thì không tạo bản ghi nào; SC4).

### Điều kiện đầu và dữ liệu test chung

| Hạng mục | Giá trị |
|---|---|
| Môi trường | Docker theo `env/docker-compose.yml`, `http://localhost:3001`; chỉ chạy với `localhost` |
| Khoá | `TWENTY_API_KEY` (role Admin), `TWENTY_API_KEY_LIMITED` (role chỉ đọc 5 object), đọc từ `.env`, không ghi vào file kết quả |
| Reset | `python scripts/reset_env.py` (Tuấn) hoặc `python scripts/seed.py --cleanup` rồi `--count 30` |
| Dữ liệu | Tiền tố `K05-`; seed cố định `20261020`; 30 bản ghi mỗi object (SC3 cần hơn 200, script tự tạo thêm) |
| Tiền tố riêng | SC3/SC4 của Tiến `K05-TIEN-`; script SC3/SC4/SC6 của Trung `K05-CB-`; SC5 `K05-SC5-`; SC2 ca tay `K05-A-`, `K05-B-` |
| Nhịp gửi | Tối đa 100 request mỗi 60 giây mỗi khoá: Schemathesis `--workers 1 --rate-limit auto`, script đi chậm 1 request/giây và chờ khi gặp 429 |
| Tái lập | `--generation-deterministic`; mỗi kịch bản chạy hai lần cùng cấu hình, hai lần phải cùng mã trả về và cùng kết luận |

### Phạm vi và tiêu chí đạt (SPEC.md)

5 object (Companies, People, Opportunities, Notes, Tasks) × 13 operation = 65 operation. Mỗi object phủ ≥ 11/13 operation; mỗi operation
≥ 50 test case (ngoại lệ `DELETE /{obj}/{id}`, xem E.3); mỗi lỗi có reproducer; hai lần chạy cùng cấu hình cho cùng tập lỗi.
Ngoài phạm vi: GraphQL, metadata API, giao diện web.

## E.2. Bảng kịch bản

| Mã | Nội dung | Kỹ thuật | Bất biến | Object | Người chạy | Công cụ |
|---|---|---|---|---|---|---|
| SC1 | Quét 13 operation với dữ liệu theo schema | Kiểm thử dựa trên schema | I1–I7 | Cả 5 | Quang | Schemathesis `run_k05.py SC1` |
| RED | Ca đỏ cố ý: schema sửa sai một trường | Kiểm chứng bộ test | I3 | Companies | Quang | `run_k05.py SC1 --schema` bản sửa |
| SC2 | Dữ liệu sai | Kiểm thử âm, phân vùng tương đương | I1–I4 | Cả 5 | Thuận | Schemathesis `run_k05.py SC2` + ca tay P2 |
| SC3 | Phân trang, lọc, sắp xếp | Giá trị biên, kiểm thử âm | I1–I3 | Companies, People, Opportunities (Trung); Notes, Tasks (Tiến) | Trung, Tiến | `kiem_thu_sc3_sc4_sc6.py`, `kiem_thu_tien_sc3_sc4.py` |
| SC4 | Batch | Giá trị biên, phân vùng tương đương | I1–I4, I9 | Companies, Opportunities, Tasks (Trung); People, Notes (Tiến) | Trung, Tiến | Như SC3 |
| SC5 | Xác thực, 4 loại key | Phân vùng tương đương trên đầu vào `Authorization` | I1, I2, I6 | Cả 5 | Tuấn | `kiem_thu_sc5.py` + ca tay P5 |
| SC6 | Chuỗi vòng đời bản ghi | Kiểm thử theo trạng thái | I1, I2, I8 | Cả 5 | Trung | `kiem_thu_sc3_sc4_sc6.py --only sc6 --objects all` |

## E.3. SC1 và ca đỏ (Quang)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Gọi mọi operation với dữ liệu đúng và sai, tìm chỗ hành vi lệch schema |
| Phạm vi | 13 operation mỗi object: `POST /batch/{obj}`; `GET`, `POST`, `DELETE`, `PATCH /{obj}`; `POST /{obj}/duplicates`; `GET /{obj}/groupBy`; `PATCH /{obj}/merge`; `PATCH /{obj}/restore`; `GET`, `DELETE`, `PATCH /{obj}/{id}`; `PATCH /{obj}/{id}/restore` |
| Điều kiện đầu | Twenty chạy; key đủ quyền; reset dữ liệu trước mỗi object |
| Input | Schemathesis sinh: `--mode all`, `--phases examples,coverage,fuzzing`, `--max-examples 50`, `--checks all`, `--generation-deterministic`, `--workers 1`, `--rate-limit auto` |
| Lệnh | `python scripts/run_k05.py SC1` |
| Kỳ vọng | I1 đến I7 không bị vi phạm; mọi vi phạm được tái hiện bằng `curl` và phân loại |
| Đầu ra | `reports/SC1/<thời điểm>/summary.md`, `REPRODUCERS.md`, báo cáo JSON/JUnit/HTML |
| Rủi ro | Phase `examples` có bộ lọc khớp mọi bản ghi; `DELETE /{obj}` hoặc `PATCH /{obj}` hàng loạt có thể xoá hoặc sửa toàn bộ dữ liệu. Hook chặn thao tác hàng loạt và reset trước mỗi lần chạy |

**Ca đỏ (RED):** tạo bản sao schema, đổi `CompanyForResponse.name` từ `string` sang `integer` (không sửa schema gốc), chạy SC1 trên bản sao.
Kỳ vọng: I3 đỏ ở các operation trả Company; lần chạy với schema gốc không có lỗi đó. Ca này chứng minh bộ test bắt được lệch schema thật.

## E.4. SC2. Dữ liệu sai (Thuận)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Mọi input vi phạm schema bị từ chối rõ ràng bằng 4xx, không nhận nhầm, không 5xx |
| Phạm vi | 5 object × 13 operation = 65 operation |
| Điều kiện đầu | Như SC1; seed lại trước mỗi object (`--reset`) |
| Dữ liệu test | 30 bản ghi `K05-` mỗi object, seed `20261020`; id lấy từ `reports/seed-manifest.json`; ca tay P2 tạo bản ghi riêng `K05-A-`, `K05-B-` rồi xoá |
| Input | `--mode negative`, `--phases coverage,fuzzing`, `--max-examples 50`, `--generation-deterministic`, `--workers 1`, `--rate-limit auto`; hook chặn `DELETE`/`PATCH` hàng loạt |
| Lệnh | `python scripts/run_k05.py SC2 --object <obj> --reset`; tái lập: `python scripts/summarize.py --compare <lần 1> <lần 2>` |
| Kỳ vọng | I1, I2, I3, I4 |

| Loại dữ liệu sai | Ví dụ | Kỳ vọng |
|---|---|---|
| Sai kiểu | `"name": 123`, `"position": "abc"` | 400 |
| `null` ở trường không cho `null` | `"accountOwnerId": null` | 400 |
| Ngoài tập giá trị | `"stage": "KHONG_CO"` | 400 |
| Sai định dạng | `id` không phải UUID, ngày sai | 400 |
| Ngoài biên | `limit=-1` | 400 |
| Thuộc tính thừa, chuỗi rất dài, Unicode lạ, byte `\x00` | | 400, không 5xx |
| Body sai cấu trúc | Object thay vì mảng ở `/batch/...`, JSON hỏng | 400 |

Ca tay P2 (trên Companies, kiểm chứng các nhóm lỗi Schemathesis báo):

| Ca | Request | Kỳ vọng theo schema |
|---|---|---|
| P2-01 | `DELETE ?soft_delete=true` rồi `PATCH /{id}/restore` | 200; khôi phục được |
| P2-02 | `DELETE ?soft_delete=abc` | 400 (`boolean`) |
| P2-03 | `DELETE ?soft_delete=1` hoặc `TRUE` | 400 |
| P2-04 | `POST /batch/companies?upsert=-1`, id mới | 400 (`boolean`) |
| P2-05 | `POST /batch/companies?upsert=abc`, id đã có | 400 (sai tham số) |
| P2-06 | `GET /companies?limit=201` (> 200 bản ghi) | 400 (`maximum: 200`) |
| P2-07 | `GET /companies?limit=1.5` | 400, thông điệp về `limit` |
| P2-08 | `POST /batch/companies` body `[{"name": 123}]` | 400 |
| P2-09 | `GET /companies?limit=1&depth=0`, so body với `CompanyForResponse` | Không có `null` ở trường không khai `nullable` |
| P2-10 | `GET /companies/groupBy?group_by=[{"updatedAt":true}]` | 200, body đúng cấu trúc khai báo |
| P2-11 | `GET /companies/groupBy` thiếu `group_by` | Mã có khai báo trong schema |
| P2-12 | `GET /companies/<UUID không tồn tại>` | Mã có khai báo (200, 400, 401) |
| P2-13 | `GET /companies/abc` | 400 |

Ngoại lệ tiêu chí 50 ca: `DELETE /{obj}/{id}` chỉ có 2 đầu vào (`id`, `soft_delete`) nên Schemathesis dừng ở khoảng 17 ca dù cho phép 500;
đã kiểm chứng đây là giới hạn của không gian input.

Lưu ý: máy chủ đổi lỗi nội bộ thành 400, nên với 400 khả nghi phải đọc `messages` trong body.

## E.5. SC3. Phân trang, lọc, sắp xếp (Trung, Tiến)

| Mục | Nội dung |
|---|---|
| Mục tiêu | `limit`, con trỏ, lọc, sắp xếp xử lý đúng giá trị biên; không 5xx; số bản ghi trả về không vượt `limit` hiệu lực |
| Phạm vi | `GET /{obj}` và `GET /{obj}/{id}`. Trung: Companies, People, Opportunities. Tiến: Notes, Tasks |
| Điều kiện đầu | Hơn 200 bản ghi trên object đang kiểm (script tự tạo thêm bằng batch nếu thiếu) |
| Lệnh | Companies: `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc3`. Object khác: `python scripts/kiem_thu_tien_sc3_sc4.py --only sc3 --objects <obj>` |
| Căn cứ | Schema: `limit` `integer`, `minimum 0`, `maximum 200`, mặc định 60; `depth` chỉ 0, 1; HTTP: 404 khi không tìm thấy |

| Ca | Request | Kỹ thuật | Kỳ vọng |
|---|---|---|---|
| P3-01 | `limit=0` | Biên dưới | Quan sát |
| P3-02 | `limit=1` | Biên dưới | 200, đúng 1 bản ghi |
| P3-03 | `limit=60` | Giá trị mặc định | 200, 60 bản ghi |
| P3-04 | `limit=200` | Biên trên | 200, 200 bản ghi |
| P3-05 | `limit=201` | Vượt biên trên | 400 (vượt `maximum`) |
| P3-06 | `limit=100000` | Vượt biên xa | 400 |
| P3-07 | `limit=-1` | Dữ liệu sai | 400 |
| P3-08 | `limit=abc` | Dữ liệu sai | 400 |
| P3-09 | `limit=1.5` | Dữ liệu sai | Quan sát |
| P3-10 | `limit=` rỗng | Dữ liệu sai | Quan sát |
| P3-11 | `starting_after=khong-phai-cursor` | Dữ liệu sai | Quan sát |
| P3-12 | `ending_before=%00` | Dữ liệu sai | Quan sát |
| P3-13 | `order_by=khongtontai` | Dữ liệu sai | Quan sát |
| P3-14 | `filter=name[eq` (sai cú pháp) | Dữ liệu sai | Quan sát |
| P3-15 | `depth=99` | Vượt biên | Quan sát |
| P3-16 | `GET /{obj}/not-a-uuid` | Dữ liệu sai | Quan sát |
| P3-17 | `GET /{obj}/<UUID không tồn tại>` | Dữ liệu sai | 404 |

## E.6. SC4. Batch (Trung, Tiến)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Xác nhận ngưỡng 200 bản ghi mỗi batch và cách từ chối khi vượt ngưỡng hoặc body sai; bị từ chối thì không tạo dở bản ghi nào (I9) |
| Phạm vi | `POST /batch/{obj}`. Trung: Companies, Opportunities, Tasks. Tiến: People, Notes |
| Điều kiện đầu | Key đủ quyền; bản ghi do ca tạo ra tự xoá sau khi chạy |
| Dữ liệu | Mỗi phần tử là body tạo tối thiểu hợp lệ của object: `{"name": "K05-..."}` (Companies, Opportunities), `{"name": {"firstName": "K05-...", "lastName": "<số>"}}` (People), `{"title": "K05-..."}` (Notes, Tasks) |
| Lệnh | Companies: `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc4`. Object khác: `python scripts/kiem_thu_tien_sc3_sc4.py --only sc4 --objects <obj>` |
| Căn cứ | Schema: body là mảng; mã khai báo 201, 400, 401. Mã nguồn: tối đa 200 bản ghi, vượt thì `Maximum number of records to upsert is 200` |

Ba vùng tương đương của số bản ghi: rỗng (0), hợp lệ (1 đến 200), vượt ngưỡng (từ 201).

| Ca | Body | Kỹ thuật | Kỳ vọng |
|---|---|---|---|
| P4-01 | `[]` | Dưới biên dưới | Quan sát |
| P4-02 | 1 bản ghi | Biên dưới | 200 hoặc 201, tạo 1 |
| B-03 | 2 bản ghi | Sát biên dưới | 200 hoặc 201, tạo 2 |
| P4-05 | 61 bản ghi | Đối chiếu giả thuyết ngưỡng 60 | 200 hoặc 201, tạo 61 |
| B-05 | 199 bản ghi | Sát biên trên | 200 hoặc 201, tạo 199 |
| P4-03 | 200 bản ghi | Biên trên | 200 hoặc 201, tạo 200 |
| P4-04 | 201 bản ghi | Vượt biên trên | 4xx, `Maximum number of records to upsert is 200`, không tạo gì |
| P4-06 | Object thay vì mảng | Sai cấu trúc | 400 do kiểm tra dữ liệu (`BadRequestException`) |
| P4-07 | `[{"name":123}, null, "x"]` | Sai kiểu | 400 do kiểm tra dữ liệu |
| P4-08 | JSON hỏng | Sai cú pháp | 400 |

## E.7. SC5. Xác thực (Tuấn)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Không có quyền thì không đọc, không ghi được; key chỉ đọc không ghi được |
| Phạm vi | 5 object × 13 operation × 4 loại key |
| Điều kiện đầu | ≥ 1 bản ghi mỗi object (`reset_env.py`); đã tạo role chỉ đọc 5 object và key gán role đó (Trung cấp), lưu `TWENTY_API_KEY_LIMITED`; script tự kiểm tra key chỉ đọc hợp lệ trước khi chạy |
| Lệnh | `python scripts/kiem_thu_sc5.py`; khi chưa có key chỉ đọc: `--variants none,wrong,full`; so hai lần chạy: `--compare A.json B.json` |
| Thứ tự trong một operation | none → wrong → limited → full (ba loại đầu phải bị chặn nên không đổi dữ liệu) |
| Chấm điểm | Ba cột độc lập: **Chặn** (I6; 2xx ở chỗ phải chặn là lỗi bảo mật), **Mã** (đúng mã kỳ vọng), **Schema** (mã có khai báo, I2) |

| Loại key (vùng tương đương) | Cách có | Kỳ vọng |
|---|---|---|
| Đủ quyền | Settings → APIs, role Admin, `TWENTY_API_KEY` | Thành công (đối chứng) |
| Chỉ đọc | Role chỉ bật quyền xem 5 object, `TWENTY_API_KEY_LIMITED` | Đọc → 200; ghi → 403 |
| Sai | Chuỗi bất kỳ, ví dụ `k05-sai-key-000000` | 401 |
| Không có | Không gửi `Authorization` | 401 theo schema |

| Ca biên tay | Request | Kỳ vọng |
|---|---|---|
| P5-00 | `GET /companies?limit=1`, key đủ quyền | 200 (đối chứng) |
| P5-01 | Như trên, không key | 401 |
| P5-02 | `Bearer k05-sai-key-000000` | 401 |
| P5-03 | `Authorization: Basic <key>` | 401 |
| P5-04 | `Authorization: Bearer ` rỗng | 401 |
| P5-05 | `POST /companies`, không key | 401 |
| P5-06 | `GET /open-api/core` không key so với có key | Quan sát |
| P5-07 | `GET`, key chỉ đọc | 200 |
| P5-08 | `POST`, key chỉ đọc | 403 |

## E.8. SC6. Chuỗi vòng đời bản ghi (Trung)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Kiểm tra điều request rời rạc khó chạm tới, vì mỗi bước cần `id` do bước trước tạo ra |
| Phạm vi | 5 object; `POST`, `GET`, `PATCH`, `DELETE /{obj}/{id}`, `PATCH /{obj}/{id}/restore`, `GET /{obj}?filter=` |
| Điều kiện đầu | Key đủ quyền; không cần dữ liệu có sẵn |
| Lệnh | `python scripts/kiem_thu_sc3_sc4_sc6.py --only sc6 --objects all` (khoảng 5 phút, tự dọn) |
| Căn cứ | Schema: `soft_delete` mặc định `false` (xoá vĩnh viễn); HTTP: 404 khi không tìm thấy; I8 nhất quán dữ liệu |

Dữ liệu tạo và trường sửa của từng object (mỗi object sửa một trường, kiểm một trường khác phải giữ nguyên):

| Object | Body tạo | Trường sửa | Trường phải giữ nguyên |
|---|---|---|---|
| Companies | `name`, `domainName.primaryLinkUrl = https://k05-sc6.example.com` | `name` | `domainName.primaryLinkUrl` |
| People | `name.firstName`, `name.lastName`, `emails.primaryEmail` | `name.firstName` | `emails.primaryEmail` |
| Opportunities | `name`, `stage = NEW`, `amount.amountMicros = 1000000` | `stage` sang `MEETING` | `amount.amountMicros` |
| Notes | `title`, `bodyV2.markdown` | `title` | `bodyV2.markdown` |
| Tasks | `title`, `status = TODO`, `dueAt` | `status` sang `DONE` | `title` |

| Ca | Trạng thái và bước | Request | Kỳ vọng |
|---|---|---|---|
| S6-01 | Tạo | `POST /{obj}` | 201, có `id` |
| S6-02 | Đọc lại | `GET /{obj}/{id}` | 200, dữ liệu khớp |
| S6-03 | Sửa một trường | `PATCH /{obj}/{id}` | 200 |
| S6-04 | Đọc sau sửa | `GET /{obj}/{id}` | Trường sửa đã đổi, trường kia giữ nguyên |
| S6-05 | Có trong danh sách | `GET /{obj}?filter=id[eq]:<id>` | 200, đúng 1 bản ghi |
| S6-06 | Xoá (mặc định) | `DELETE /{obj}/{id}` | 200 |
| S6-07 | Đọc sau xoá | `GET /{obj}/{id}` | 404 |
| S6-08 | Xoá lần hai | `DELETE /{obj}/{id}` | 404, không 5xx |
| S6-09 | Sửa sau xoá | `PATCH /{obj}/{id}` | 404, không 5xx |
| S6-10 | Khôi phục sau xoá vĩnh viễn | `PATCH /{obj}/{id}/restore` | 404 |
| S6-11 | Quan hệ (chỉ Companies) | Tạo công ty, tạo người gắn công ty, xoá công ty, đọc người | Quan sát, không 5xx |
| S6-12a–c | Id không tồn tại | `GET`, `PATCH`, `DELETE` UUID không tồn tại | 404 |
| S6-13b–e | Xoá mềm rồi khôi phục | `DELETE ?soft_delete=true`; `GET`; `PATCH .../restore`; `GET` | 200; 404; 200; 200 |

## E.9. Truy vết kịch bản, bất biến và lỗi

| Kịch bản | Bất biến kiểm | Lỗi liên quan (mã ở `reports/bang-loi.md`) |
|---|---|---|
| SC1 | I1–I7 | D-03, D-09, D-11 |
| SC2 | I1–I4 | D-01, D-03, D-07, D-08, D-09, D-10 |
| SC3 | I1–I3 | D-01, D-03 |
| SC4 | I1–I4, I9 | D-04, D-05 |
| SC5 | I1, I2, I6 | D-02, D-12 |
| SC6 | I1, I2, I8 | D-03, D-06 |

Số test case và kết quả từng kịch bản, theo object: xem Phần G. Bảng test case chi tiết của SC3, SC4, SC6 kèm căn cứ đối chiếu và bằng chứng:
`docs/test-case-trung.md`, `docs/kiem-thu-tien-sc3-sc4.md`.
