# Đặc tả SC1, SC2, ca đỏ và bảng bất biến (Quang)

Bổ sung cho `scenarios.md` và `SPEC.md` mục 4, 5.4. K05 không viết từng giá trị input: Schemathesis sinh request từ OpenAPI, nhóm khai báo **bất biến** (điều phải luôn đúng) và cấu hình từng kịch bản.
Đây là đặc tả giữa kỳ. Bộ test được viết và chạy ở Sprint 3–4; khi đó mới điền cột "Kết quả".

## 1. Bảng bất biến I1–I7

Đánh số theo Bảng 12 của báo cáo giữa kỳ.

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

## 2. SC1: quét mọi operation của Companies với dữ liệu theo schema

| Mục | Nội dung |
|---|---|
| Mục tiêu | Kiểm tra mọi operation của Companies với cả dữ liệu đúng và sai, phát hiện chỗ lệch giữa schema và hành vi |
| Phạm vi | 13 operation khớp `^/(batch/)?companies(/\|$)`: list, get, create, update, delete (theo id và hàng loạt), batch, duplicates, restore (theo id và hàng loạt), merge, groupBy |
| Điều kiện đầu | Twenty chạy ở `localhost:3001`; API key quyền đầy đủ trong `.env`; đã chạy `python scripts/seed.py --count 30` |
| Lệnh dự kiến | `python scripts/run_k05.py SC1` |
| Cấu hình dự kiến | `--checks all`, `--mode all` (cả dữ liệu đúng và sai), `--phases examples,coverage,fuzzing`, `--max-examples 50`, `--generation-deterministic`, `--workers 1`, `--rate-limit auto` |
| Bất biến | I1 đến I7 |
| Đầu ra dự kiến | Thống kê theo operation, mã trạng thái và check; lệnh `curl` tái hiện cho từng nhóm lỗi |
| Tiêu chí đạt | Mỗi operation ≥ 50 test case; hai lần chạy cùng cấu hình cho cùng tập lỗi; mỗi nhóm lỗi có lệnh tái hiện |
| Kết quả | Điền ở Sprint 3–4 |

Rủi ro dữ liệu: phase `examples` dùng các ví dụ có sẵn trong schema, trong đó có bộ lọc `filter` có thể khớp mọi bản ghi. Gửi bộ lọc đó vào `DELETE /companies` hoặc `PATCH /companies` có thể xoá hoặc sửa toàn bộ dữ liệu, kể cả dữ liệu mẫu. Biện pháp: seed lại trước mỗi lần chạy và chặn ghi hàng loạt vào dữ liệu có sẵn.

## 3. SC2: dữ liệu sai trên 5 đối tượng

| Mục | Nội dung |
|---|---|
| Mục tiêu | Xác nhận server từ chối rõ ràng mọi input vi phạm schema, không nhận nhầm và không lỗi 5xx |
| Phạm vi | Mọi operation của Companies, People, Opportunities, Notes, Tasks (65 operation) |
| Điều kiện đầu | Như SC1; seed lại trước khi chạy |
| Lệnh dự kiến | `python scripts/run_k05.py SC2` |
| Cấu hình dự kiến | `--mode negative`, `--phases coverage,fuzzing`, `--max-examples 50` |
| Bất biến | I1, I2, I3, I4 |
| Kết quả | Điền ở Sprint 3–4 |

Các loại dữ liệu sai Schemathesis sinh và kỳ vọng:

| Loại | Ví dụ | Kỳ vọng |
|---|---|---|
| Sai kiểu | `"name": 123`, `"position": "abc"` | 400 |
| `null` ở trường không cho `null` | `"accountOwnerId": null` | 400 |
| Ngoài tập giá trị cho phép | `"stage": "KHONG_CO"`, `createdBy.source` lạ | 400 |
| Sai định dạng | `id` không phải UUID, ngày sai định dạng | 400 |
| Ngoài biên | `limit=-1` | 400 |
| Ngoài biên | `limit=201` | Quan sát: mã nguồn cắt về 200, không báo lỗi (H1) |
| Thuộc tính thừa, chuỗi rất dài, Unicode lạ | Khóa lạ trong body, chuỗi hàng nghìn ký tự, emoji, byte `\x00` | 400, không 5xx |
| Body sai cấu trúc | Object thay vì mảng ở `/batch/...`, JSON hỏng | 400 |

Lưu ý H3: server đổi mọi lỗi không phải `HttpException` thành 400, nên một lỗi nội bộ có thể trông như "từ chối đúng". Với mỗi 400 khả nghi phải đọc `messages` trong body, không chỉ mã trạng thái.

## 4. Ca đỏ cố ý (RED)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Chứng minh bộ test thật sự bắt được lỗi: cố tình làm schema sai một chỗ biết trước rồi xem bộ test có báo đỏ đúng chỗ đó không |
| Điều kiện đầu | Đã chạy SC1 với schema gốc để có kết quả đối chứng |
| Cách làm dự kiến | Tạo bản sao schema, đổi `CompanyForResponse.name` từ `string` sang `integer`; không sửa schema gốc |
| Lệnh dự kiến | `python scripts/run_k05.py SC1 --schema schema/core.red.openapi.json --label RED` |
| Bất biến | I3 |
| Kỳ vọng | I3 (`response_schema_conformance`) đỏ ở các operation trả về Company, thông điệp dạng `"..." is not of type "integer"`; lần chạy với schema gốc không có lỗi này |
| Kết quả | Điền ở Sprint 3–4 |

## 5. Ca biên viết tay P5 (xác thực)

Ca biên gọi thẳng những giá trị mà Schemathesis không chắc chạm tới. Ca P3 (phân trang) và P4 (batch) đặc tả ở `dac-ta-sc3-sc4.md`; tổng P3–P5 là 31 ca.
Cách kết luận khi chạy: **MATCH** = đúng kỳ vọng, **DIFF** = lệch kỳ vọng (ứng viên lỗi, phải xác minh tay), **OBSERVE** = chưa có kỳ vọng chắc, ghi lại hành vi.

| Mã ca | Request | Kỳ vọng | Căn cứ |
|---|---|---|---|
| P5-01 | `GET /companies` không gửi key | 401 | Tài liệu OpenAPI chỉ khai báo 401 |
| P5-02 | `GET /companies` key sai | 401 | `jwt.auth.strategy.ts`: key hỏng → 401 |
| P5-03 | `GET /companies` scheme `Basic` | 401 | Không có Bearer = không có key |
| P5-04 | `GET /companies` `Bearer` rỗng | 401 | Như P5-03 |
| P5-05 | `POST /companies` không key | 401 | Như P5-01, với thao tác ghi |
| P5-06 | `GET /open-api/core` không key | Quan sát | Endpoint công khai, không key chỉ trả khung schema |

Khi có key chỉ đọc (`TWENTY_API_KEY_LIMITED`) bổ sung P5-07 (đọc → 200) và P5-08 (ghi → 403).

## 6. Triển khai ở Sprint 3–4

1. Viết bộ test, chạy SC1 sau khi seed lại dữ liệu và chặn ghi hàng loạt; chạy hai lần để kiểm tra tái lập.
2. Chạy RED để chứng minh bộ test bắt được lỗi.
3. Chạy SC2 trên 5 đối tượng, điền cột "Kết quả".
4. Tạo key chỉ đọc, chạy SC5 và các ca P5.
