# Đặc tả SC1, SC2, ca đỏ và bảng bất biến (Quang)

Bổ sung cho `scenarios.md` và `SPEC.md` mục 4, 5.4. K05 không viết từng giá trị input: Schemathesis sinh request từ OpenAPI, nhóm khai báo **bất biến** (điều phải luôn đúng) và cấu hình từng kịch bản.
Cột "Kết quả" ghi số liệu thật của lần chạy ngày 16/10/2026 trên instance local `twenty/v2.45.6`; ô trống là chưa chạy.

## 1. Bảng bất biến I1–I7

| Mã | Bất biến | Check Schemathesis | Kịch bản | Kết quả SC1 16/10 (đạt / lỗi) |
|---|---|---|---|---|
| I1 | Không trả 5xx với bất kỳ input nào | `not_a_server_error` | SC1, SC2, SC3, SC4, SC5 | 1232 / 0 |
| I2 | Mã trạng thái nằm trong danh sách schema khai báo | `status_code_conformance` | SC1, SC2, SC3, SC4, SC5 | 892 / 283 |
| I3 | `Content-Type` đúng khai báo | `content_type_conformance` | SC1 | 1175 / 0 |
| I4 | Body phản hồi đúng cấu trúc và kiểu của schema | `response_schema_conformance` | SC1, SC2, SC3, SC4 | 1153 / 72 |
| I5 | Dữ liệu sai schema bị từ chối bằng 4xx | `negative_data_rejection` | SC1, SC2, SC4 | 1170 / 5 |
| I6 | Dữ liệu đúng schema được chấp nhận | `positive_data_acceptance` | SC1, SC3 | 899 / 276 |
| I7 | Thiếu hoặc sai API key thì không truy cập được (401/403) | `ignored_auth`, `missing_required_header` | SC1, SC5 | 1175 / 0 và 1219 / 13 |

Cách đọc: I1 và I7 (`ignored_auth`) đạt hoàn toàn. Lỗi ở I2, I4, I5, I6 phần lớn là **lệch schema** (server trả 403, 404 hoặc `null` mà schema không khai báo), xem `defects.md` D-01 đến D-07.

## 2. SC1: quét mọi operation của Companies với dữ liệu theo schema

| Mục | Nội dung |
|---|---|
| Mục tiêu | Chứng minh bộ test chạy được trên schema thật và bắt được lệch giữa schema và hành vi (PoC giữa kỳ) |
| Phạm vi | 13 operation khớp `^/(batch/)?companies(/\|$)`: list, get, create, update, delete (theo id và hàng loạt), batch, duplicates, restore (theo id và hàng loạt), merge, groupBy |
| Điều kiện đầu | Twenty chạy ở `localhost:3001`; API key quyền đầy đủ trong `.env`; đã chạy `python scripts/seed.py --count 30` |
| Lệnh | `python scripts/run_k05.py SC1` |
| Cấu hình | `--checks all`, `--mode all` (cả dữ liệu đúng và sai), `--phases examples,coverage,fuzzing`, `--max-examples 50`, `--seed 20261020`, `--generation-deterministic`, `--workers 1`, `--rate-limit auto` |
| Bất biến | I1 đến I7 |
| Đầu ra | `reports/SC1/<thời điểm>-seed20261020/`: `summary.md` (thống kê theo operation, mã trạng thái, check), `REPRODUCERS.md`, `reproducers/*.sh` (lệnh `curl` cho từng nhóm lỗi) |
| Tiêu chí đạt giữa kỳ | Chạy xong, có thống kê, ít nhất 1 reproducer, có ca đỏ (mục 4) |
| Tiêu chí đạt cuối kỳ | Mỗi operation ≥ 50 test case; chạy hai lần cùng cấu hình cho cùng tập lỗi |

Kết quả 16/10 (`reports/SC1/20261016-213452-seed20261020/`): 13/13 operation, 1248 test case (mỗi operation 64 đến 177), **0 lỗi 5xx**, 52 nhóm lỗi, 52 reproducer. Lần chạy thứ hai (`20261016-220101`) trùng 50/52 nhóm lỗi.

Lưu ý dữ liệu: request thứ 34 của lần chạy (phase `examples`, ví dụ `filter` có sẵn trong schema `or(...,not(id[is]:NULL))` kèm `soft_delete=false`) đã xoá vĩnh viễn 209 công ty, gồm cả dữ liệu seed. Lần chạy sau phải seed lại trước và chặn ghi hàng loạt vào dữ liệu có sẵn; nếu không, phần lớn ca chạy trên bảng rỗng và độ tái lập bị đánh giá cao hơn thực tế.

## 3. SC2: dữ liệu sai trên 5 đối tượng

| Mục | Nội dung |
|---|---|
| Mục tiêu | Xác nhận server từ chối rõ ràng mọi input vi phạm schema, không nhận nhầm và không lỗi 5xx |
| Phạm vi | Mọi operation của Companies, People, Opportunities, Notes, Tasks (65 operation) |
| Điều kiện đầu | Như SC1; seed lại trước khi chạy |
| Lệnh | `python scripts/run_k05.py SC2` |
| Cấu hình | `--mode negative`, `--phases coverage,fuzzing`, `--max-examples 50`, check I1, I2, I4, I5 |
| Kết quả | Chưa chạy (cuối kỳ, Sprint 3) |

Các loại dữ liệu sai Schemathesis sinh và kỳ vọng:

| Loại | Ví dụ | Kỳ vọng |
|---|---|---|
| Sai kiểu | `"name": 123`, `"position": "abc"` | 400 |
| `null` ở trường không cho `null` | `"accountOwnerId": null` | 400 theo schema; thực tế 201 (D-07, lệch schema) |
| Ngoài tập giá trị cho phép | `"stage": "KHONG_CO"`, `createdBy.source` lạ | 400 |
| Sai định dạng | `id` không phải UUID, ngày sai định dạng | 400 |
| Ngoài biên | `limit=-1`, `limit=201` | 400; thực tế `limit=201` trả 200 (D-01) |
| Thuộc tính thừa, chuỗi rất dài, Unicode lạ | Khóa lạ trong body, chuỗi hàng nghìn ký tự, emoji, byte `\x00` | 400, không 5xx |
| Body sai cấu trúc | Object thay vì mảng ở `/batch/...`, JSON hỏng | 400 |

Lưu ý H3: server đổi mọi lỗi không phải `HttpException` thành 400, nên một lỗi nội bộ có thể trông như "từ chối đúng". Với mỗi 400 khả nghi phải đọc `messages` trong body, không chỉ mã trạng thái.

## 4. Ca đỏ cố ý (RED)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Chứng minh công cụ thật sự bắt được lỗi: cố tình làm schema sai rồi xem bộ test có báo đỏ không |
| Cách làm | `python scripts/make_red_case.py` tạo bản sao `schema/core.red.openapi.json`, đổi `CompanyForResponse.name` từ `string` sang `integer`; không sửa schema gốc |
| Lệnh | `python scripts/run_k05.py SC1 --schema schema/core.red.openapi.json --label RED` |
| Kỳ vọng | I4 (`response_schema_conformance`) đỏ ở mọi operation trả về Company, thông điệp dạng `"..." is not of type "integer"` |
| Kết quả 16/10 | **Đạt.** 779 test case, 120 giây. I4 đỏ đúng ở 4 operation: `GET /companies`, `POST /companies`, `PATCH /companies`, `PATCH /companies/restore`, thông điệp `"" is not of type "integer"` tại `/components/schemas/CompanyForResponse/properties/name`. Lần chạy gốc có 0 lỗi kiểu này |
| Thư mục | `reports/SC1/20261016-215144-seed20261020-RED/` |

## 5. 31 ca biên (P3–P5) và kết quả thăm dò

Lệnh: `python scripts/probe_boundaries.py` (hoặc `--only sc3|sc4|sc5`). Probe gọi thẳng những giá trị biên mà Schemathesis không chắc chạm tới. Kết luận: **MATCH** = đúng kỳ vọng, **DIFF** = lệch kỳ vọng (ứng viên lỗi, phải xác minh tay), **OBSERVE** = chưa có kỳ vọng chắc, ghi lại hành vi.
Kết quả lần chạy 16/10 (`reports/probes/20261016-213052.md`): **31 ca, MATCH 11, DIFF 4, OBSERVE 16.**

| Mã ca | Request | Kỳ vọng | Thực tế | Kết luận |
|---|---|---|---|---|
| P3-01 | `GET /companies?limit=0` | — | 200 | OBSERVE |
| P3-02 | `GET /companies?limit=1` | 200 | 200 | MATCH |
| P3-03 | `GET /companies?limit=60` | 200 | 200 | MATCH |
| P3-04 | `GET /companies?limit=200` | 200 | 200 | MATCH |
| P3-05 | `GET /companies?limit=201` | — (mã nguồn cắt về 200) | 200 | OBSERVE (D-01) |
| P3-06 | `GET /companies?limit=100000` | — | 200 | OBSERVE (D-01) |
| P3-07 | `GET /companies?limit=-1` | 400 | 400 | MATCH |
| P3-08 | `GET /companies?limit=abc` | 400 | 400 | MATCH |
| P3-09 | `GET /companies?limit=1.5` | — | 400 | OBSERVE |
| P3-10 | `GET /companies?limit=` | — | 200 | OBSERVE |
| P3-11 | `GET /companies?starting_after=khong-phai-cursor` | — | 400 | OBSERVE |
| P3-12 | `GET /companies?ending_before=%00` | — | 400 | OBSERVE |
| P3-13 | `GET /companies?order_by=khongtontai` | — | 400 | OBSERVE |
| P3-14 | `GET /companies?filter=name[eq` | — | 400 | OBSERVE |
| P3-15 | `GET /companies?depth=99` | — | 400 | OBSERVE |
| P3-16 | `GET /companies/not-a-uuid` | — | 400 | OBSERVE |
| P3-17 | `GET /companies/<UUID không tồn tại>` | 404 | 404 | MATCH |
| P4-01 | `POST /batch/companies` với `[]` | — | 201 | OBSERVE |
| P4-02 | `POST /batch/companies` 1 bản ghi | 200/201 | 201 | MATCH |
| P4-03 | `POST /batch/companies` 200 bản ghi | 200/201 | 201 | MATCH |
| P4-04 | `POST /batch/companies` 201 bản ghi | 400/413/422 | 400 | MATCH |
| P4-05 | `POST /batch/companies` 61 bản ghi | 200/201 | 201 | MATCH |
| P4-06 | `POST /batch/companies` body là object | — | 400 | OBSERVE |
| P4-07 | `POST /batch/companies` phần tử sai | — | 400 | OBSERVE |
| P4-08 | `POST /batch/companies` JSON hỏng | — | 400 | OBSERVE |
| P5-01 | `GET /companies` không gửi key | 401 | 403 | **DIFF** (D-02) |
| P5-02 | `GET /companies` key sai | 401 | 401 | MATCH |
| P5-03 | `GET /companies` scheme `Basic` | 401 | 403 | **DIFF** (D-02) |
| P5-04 | `GET /companies` `Bearer` rỗng | 401 | 403 | **DIFF** (D-02) |
| P5-05 | `POST /companies` không key | 401 | 403 | **DIFF** (D-02) |
| P5-06 | `GET /open-api/core` không key | — (khung schema) | 200 | OBSERVE |

Bốn ca DIFF cùng một nguyên nhân: thiếu thông tin xác thực bị trả 403 thay vì 401 (D-02). Không ca nào trả 5xx (I1 đạt). Ca P5-07, P5-08 (key role chỉ đọc) chưa chạy vì chưa có `TWENTY_API_KEY_LIMITED`; phần SC5 do Tuấn đặc tả.

## 6. Còn phải làm

1. Chạy lại SC1 sau khi seed lại dữ liệu và chặn ghi hàng loạt, để có số liệu không bị bảng rỗng làm sai lệch.
2. Chạy SC2 trên 5 đối tượng, điền cột "Kết quả" ở mục 3, ghi lỗi mới vào `defects.md`.
3. Chạy lại `probe_boundaries.py` sau khi có key role giới hạn để có thêm P5-07, P5-08.
