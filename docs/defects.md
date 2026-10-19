# Danh sách lỗi và quan sát (Báo cáo Phần G)

Nguồn: `reports/probes/20261016-213052.md` (thăm dò biên), `reports/SC1/20261016-213452-seed20261020/` (SC1 trên Companies, 300 giây) — cả hai chạy ngày 16/10/2026 trên instance local `twenty/v2.45.6` — và đọc mã nguồn.
Trạng thái "đã tái hiện" = đã thấy trên instance thật bằng reproducer bên dưới. Phân loại theo SPEC mục 3.5: **lệch schema** (hành vi khác OpenAPI khai báo) hoặc **lỗi chức năng**.
Cập nhật bảng này sau khi chạy SC1 đến SC5.

## Lỗi ứng viên

### D-01. `limit` lớn hơn 200 được chấp nhận và bị cắt âm thầm (lệch schema, mức thấp)

| Mục | Nội dung |
|---|---|
| Schema khai báo | `limit`: integer, `minimum 0`, `maximum 200`, `default 60` (`GET /companies`) |
| Thực tế | `limit=201` và `limit=100000` trả **200 OK**; `limit=-1`, `limit=abc` trả 400 (đúng) |
| Check dự kiến báo | `negative_data_rejection` (dữ liệu vi phạm `maximum` vẫn được chấp nhận) |
| Reproducer | `curl -i -H "Authorization: Bearer $TWENTY_API_KEY" "http://localhost:3001/rest/companies?limit=201"` |
| RCA (đọc mã) | `parseLimitRestRequest` chỉ từ chối giá trị âm hoặc không phải số, còn lại trả `Math.min(limit, QUERY_MAX_RECORDS)` với `QUERY_MAX_RECORDS = 200` (`rest/input-request-parsers/limit-parser-utils/parse-limit-rest-request.util.ts`) |
| Ghi chú | Có thể là chủ ý thiết kế (cắt trần thay vì lỗi). Báo cáo ghi là lệch giữa schema và hành vi, không khẳng định là bug chức năng |
| Trạng thái | Đã tái hiện (P3-05, P3-06) |

### D-02. Thiếu hoặc sai dạng thông tin xác thực trả 403, schema chỉ khai báo 401 (lệch schema, mức trung bình)

| Mục | Nội dung |
|---|---|
| Schema khai báo | Mọi operation chỉ khai báo `200/201`, `400`, `401`; không có `403` |
| Thực tế | Không gửi `Authorization`, scheme `Basic`, `Bearer ` rỗng, và `POST` không key đều trả **403**. Key sai (`Bearer k05-sai-key-000000`) trả **401** |
| Check dự kiến báo | `status_code_conformance` (403 không khai báo); `ignored_auth` vẫn đạt vì không truy cập được dữ liệu |
| Reproducer | `curl -i "http://localhost:3001/rest/companies"` (không header) |
| RCA (một phần) | `JwtAuthGuard.canActivate` trả `false` khi không xác thực được (không token, token hỏng) (`engine/guards/jwt-auth.guard.ts`); Nest đổi `false` của guard thành `ForbiddenException` = 403. Việc key sai nhưng có mặt trả 401 do một tầng khác (chưa xác định, cần Thuận đọc `validateTokenByRequest` và middleware REST) |
| Hệ quả | Theo ngữ nghĩa HTTP, thiếu thông tin xác thực nên là 401 (kèm `WWW-Authenticate`); client không phân biệt được "chưa đăng nhập" với "không đủ quyền" |
| Bằng chứng SC1 | Check `missing_required_header` đỏ ở **13/13** operation của Companies: "Got 403 when missing required 'Authorization' header, expected 401". Thân phản hồi: `{"statusCode":403,"messages":["Missing authentication token"],"error":"FORBIDDEN_EXCEPTION"}` |
| Trạng thái | Đã tái hiện (P5-01, P5-03, P5-04, P5-05; SC1 reproducers `*-missing_required_header.sh`). RCA đầy đủ: còn việc |

### D-03. Schema phản hồi khai báo trường không-null nhưng server trả `null` (lệch schema, mức cao)

| Mục | Nội dung |
|---|---|
| Thực tế | Bản ghi mới tạo có `"deletedAt": null`; schema `CompanyForResponse.deletedAt` là `{"type":"string","format":"date-time"}` (không cho null). Cùng lỗi ở `accountOwnerId`, `accountOwner` (object), `createdBy.workspaceMemberId`, `updatedBy.workspaceMemberId`, `annualRevenue.currencyCode` |
| Check báo | `response_schema_conformance`: **72 lần**, 62 ở `GET /companies`, 10 ở `GET /companies/groupBy`; thông điệp `null is not of type "string"` |
| Reproducer | Tạo một Company rồi `curl -H "Authorization: Bearer $TWENTY_API_KEY" "http://localhost:3001/rest/companies?depth=0&limit=1"`, so `deletedAt` với schema. Tự sinh: `reports/SC1/.../reproducers/09-get-companies-response_schema_conformance.sh` |
| Ảnh hưởng | Mọi client sinh từ OpenAPI và kiểm phản hồi nghiêm ngặt (TypeScript client, validator) sẽ báo lỗi với dữ liệu hợp lệ; OpenAPI 3.1 cần `"type": ["string","null"]` |
| RCA | Cần Thuận: đọc bộ sinh schema (`core-modules/open-api/utils/`, các hàm `compute*` và ánh xạ field → schema) xem có bỏ qua `isNullable` của metadata field không |
| Trạng thái | Đã tái hiện |

### D-04. `GET /{đối tượng}/groupBy` trả mảng trần, schema khai báo object bọc `data` (lệch schema, mức cao)

| Mục | Nội dung |
|---|---|
| Thực tế | Phản hồi: `[{"countNotEmptyId":"1","groupByDimensionValues":["..."],"records":[]}]` (JSON array) |
| Schema khai báo | `{"type":"object","properties":{"data":{"properties":{"companiesGroupBy":{"type":"array"...}}}}}` |
| Check báo | `response_schema_conformance`: 10 lần, `... is not of type "object"` |
| Reproducer | `reproducers/13-get-companies-groupby-response_schema_conformance.sh` |
| RCA | Handler `RestApiGroupByHandler` trả `CommonGroupByOutputItem[]` (kiểu trả về của `handle`) trong khi các handler khác trả `{data: ...}` (`rest-api-base.handler.ts`); schema do `open-api` dựng theo mẫu bọc `data` |
| Trạng thái | Đã tái hiện; RCA có căn cứ trong mã, cần xác nhận khi đọc `rest-api-group-by.handler.ts` |

### D-05. Tham số của `groupBy` mô tả khác với server chấp nhận (lệch schema, mức trung bình)

| Mục | Nội dung |
|---|---|
| Thực tế | Request hợp lệ theo schema (`order_by=createdAt`, kiểu string) bị **400**: `Invalid order_by query parameter - should be a valid array of objects - ex: [{"firstField": "AscNullsFirst"}...]`. Schema khai báo `groupBy` trả 200 (và 400 không được khai báo ở operation này) |
| Check báo | `positive_data_acceptance` 65 lần; `status_code_conformance` 117 lần (400 không khai báo) |
| Reproducer | `reproducers/12-get-companies-groupby-positive_data_acceptance.sh`, `.../14-...status_code_conformance.sh` |
| Ghi chú | Danh sách `order_by` kiểu `field[Direction]` ở trang mô tả OpenAPI dành cho list; groupBy đòi mảng JSON |
| Trạng thái | Đã tái hiện; cần xác minh tay một request chuẩn để chắc chắn chỉ `order_by` gây lỗi |

### D-06. Phương thức không hỗ trợ trả 404 thay vì 405 (mức thấp)

`unsupported_method`: 39 lần (ví dụ `TRACE /companies/merge` → `404 {"message":"Cannot TRACE /rest/companies/merge...","error":"Not Found"}`, không có `Allow`). Hành vi mặc định của Express/Nest; ghi để đối chiếu RFC 9110 (405). Reproducer: `reproducers/15-*unsupported_method.sh` (và 19, 27, 31, 38, 42, 47, 52).

### D-07. Server chấp nhận dữ liệu "sai kiểu": thực chất là `null` mà schema không khai báo (lệch schema, mức thấp)

`negative_data_rejection`, 5 lần, giống hệt nhau ở cả hai lần chạy `213452` và `220101`. Quang đã mở từng request/response trong `ndjson-*.ndjson` (cách làm ở cuối mục):

| Operation | Giá trị "sai" Schemathesis gửi | Schema khai báo | Phản hồi | Kết luận |
|---|---|---|---|---|
| `POST /companies` | `"accountOwnerId": null` | `{"type":"string","format":"uuid"}`, không cho `null` | **201**, tạo bản ghi | Không có chủ sở hữu là trạng thái hợp lệ (bản ghi trả về cũng có `accountOwnerId: null`, xem D-03). Lỗi nằm ở schema: thiếu `"type": ["string","null"]`. **Cùng nguyên nhân gốc với D-03** |
| `PATCH /companies?filter=createdAt[gte]:"2023-01-01"` | `"accountOwnerId": null` | như trên | 200 `{"data":{"updateCompanies":[]}}` | Như dòng trên. Lưu ý: cập nhật **0 bản ghi** vì bảng đã bị xoá sạch (R-01), nên không biết server có thật sự ghi `null` hay không |
| `PATCH /companies?filter=...` | `"updatedBy": {"source": null}` | `source` là chuỗi trong enum 9 giá trị | 200, 0 bản ghi | **Chưa kết luận được**: không có bản ghi nào để cập nhật. `updatedBy` là trường actor do hệ thống ghi, có thể bị bỏ qua. Cần xác minh lại bằng `PATCH /companies/{id có thật}` sau khi seed |
| `POST /companies/duplicates` | `{"ids": [null]}` | `ids`: mảng UUID | 200 `{"data":[]}` | Server bỏ qua phần tử `null` thay vì trả 400. Lệch schema nhẹ, không gây hại |
| `GET /companies?limit=201` | `limit=201` | `maximum 200` | 200 | Là D-01 |

Phân loại: 3/5 là "schema không biểu đạt `nullable`" (gộp RCA với D-03), 1/5 là D-01, 1/5 chờ chạy lại.
Reproducer: `reproducers/44-*`, `21-*`, `49-*`, `07-*`. Việc tiếp: Trung xác minh tay dòng `updatedBy.source` trên một bản ghi có thật.

Cách lấy request/response từ log (để kiểm tra lại): đọc `ndjson-*.ndjson`, sự kiện `ScenarioFinished` → `recorder.checks[<case id>]` có `name == "negative_data_rejection"` và `status == "failure"` → `recorder.interactions[<case id>]` chứa `request` và `response` (body mã hóa base64; hàm `decode_body` trong `scripts/summarize.py`).

## R-01. Lần chạy SC1 ngày 16/10 tự xoá sạch Companies ngay từ ca thứ 34 (ảnh hưởng tính hợp lệ của kết quả)

Đây không phải lỗi của Twenty mà là **lỗi thiết kế của bộ test**, phát hiện khi đọc lại log để phân tích D-07 (Quang, 19/10).

| Mục | Nội dung |
|---|---|
| Ca gây ra | Phase `examples`, `DELETE /companies?soft_delete=false&filter=or(createdAt[gte]:"2024-01-01",createdAt[lte]:"2023-01-01",not(id[is]:NULL))` |
| Nguồn của giá trị | Ví dụ `complex` của tham số `filter` trong chính schema (`components.parameters.filter.examples`). Schemathesis dùng nguyên văn ví dụ của schema ở phase `examples` |
| Hệ quả | Điều kiện `not(id[is]:NULL)` khớp mọi bản ghi; `soft_delete=false` (cũng là mặc định của schema) là **xoá vĩnh viễn**. Phản hồi 200 liệt kê **209 bản ghi đã xoá**, tức toàn bộ Companies của workspace, gồm 30 công ty seed |
| Phạm vi ảnh hưởng | Đó là request thứ 34/1248. Sau đó bảng chỉ còn bản ghi do fuzz tạo ra: `GET /companies?limit=201` trả 1 dòng; mọi `PATCH /companies` hàng loạt cập nhật 0 dòng. Lần chạy `220101` bắt đầu từ bảng gần rỗng (cùng ca đó chỉ xoá được 1 bản ghi) |
| Hệ quả cho báo cáo | Số liệu lỗi của SC1 ngày 16/10 vẫn đúng (các lỗi lệch schema D-01 đến D-06 không phụ thuộc dữ liệu), nhưng: (1) 161/173 lần 404 thuộc các operation theo `{id}` với UUID ngẫu nhiên, vốn 404 dù bảng có dữ liệu hay không; hook `map_case` mới thay bằng id seed để các ca này chạm bản ghi thật; (2) hai lần chạy giống nhau 96% một phần vì **cả hai cùng chạy trên bảng rỗng**; (3) các ca ghi hàng loạt không kiểm tra được hành vi trên dữ liệu thật. Khi demo nên nói rõ điểm này |
| Biện pháp (đã làm, nhánh `feature/quang-harness-hooks`) | `hooks/k05_hooks.py` hook `before_call` (chạy ở mọi phase, kể cả `examples`) bọc filter của `DELETE`/`PATCH /{đối tượng}` thành `and(<filter gốc>,createdAt[gte]:"<mốc bắt đầu>")`, chỉ chạm bản ghi tạo trong lần chạy. `run_k05.py --reset` dọn và seed lại trước mỗi lần chạy; `run-config.json` ghi mốc thời gian và số bản ghi seed. `reports/seed-manifest.json` hiện có trong repo trỏ tới 30 công ty **đã bị xoá** trong lần chạy này, nên lần chạy tới phải dùng `--reset` |
| Còn phải kiểm chứng trên instance | Twenty chấp nhận `and(...)` lồng `or(...)` và so sánh `createdAt` với chuỗi ISO có giờ (cú pháp lấy từ phần mô tả filter trong schema, chưa chạy thật). Lệnh thử: `curl -H "Authorization: Bearer $TWENTY_API_KEY" 'http://localhost:3001/rest/companies?filter=and(not(id%5Bis%5D:NULL),createdAt%5Bgte%5D:%222026-10-19T00:00:00.000Z%22)'` phải trả 200 và chỉ các bản ghi tạo sau mốc |

## Nhóm "báo động giả do schema thiếu ràng buộc" (không tính là lỗi của Twenty)

| Nhóm | Số lần | Giải thích |
|---|---|---|
| `positive_data_acceptance` với `fields=id,name,emails,company` | nhiều | Schema khai báo `fields` là chuỗi tự do; server từ chối tên trường không tồn tại ở Company (`Unknown or unreadable fields on 'company': emails, company`). Đúng với hành vi hợp lý; schema không biểu đạt được |
| `positive_data_acceptance` với `filter=emails.primaryEmail[eq]:...` trên Companies | nhiều | Company không có trường `emails` (đó là của Person). Cùng lý do |
| `positive_data_acceptance` do thuộc tính thừa (`additionalProperties`) | hàng chục | Schema không cấm thuộc tính lạ, nhưng server trả 400 khi body có trường không tồn tại. Nên khai báo `additionalProperties: false` |
| `status_code_conformance` với **404** | 173 lần | Id không tồn tại trả 404 mà schema không khai báo 404 (O-5). Hành vi đúng; thiếu trong schema |

## Thống kê SC1 (Companies, 13 operation, chạy 300 giây)

| Chỉ số | Giá trị |
|---|---|
| Operation đã test | 13/13 operation của Companies (65 operation cho 5 đối tượng) |
| Test case sinh ra | 1248; mỗi operation từ 64 đến 177 (đều ≥ 50) |
| Mã trạng thái | 400: 881, 404: 173, 200: 134, 403: 21, 201: 23, 204: 8, 401: 8; **5xx: 0** |
| Nhóm lỗi duy nhất | 52 (63 lỗi theo Schemathesis) |
| `not_a_server_error` | 0 lỗi trên 1232 ca: không có 5xx |
| Check đỏ nhiều nhất | `status_code_conformance` 283; `positive_data_acceptance` 276; `response_schema_conformance` 72 |
| Lưu ý | Chạy bị cắt ở 300 giây (`--max-time`); coverage đầy đủ cần chạy dài hơn hoặc từng operation |


## Quan sát (không phải lỗi)

| # | Quan sát | Bằng chứng | Ý nghĩa |
|---|---|---|---|
| O-1 | Batch nhận **200** bản ghi, từ chối **201** bằng 400; batch 61 vẫn được nhận | P4-03, P4-04, P4-05 | Con số 60 trong ghi chú cũ là sai; đã sửa SC4 |
| O-2 | Batch rỗng `[]` trả 201 | P4-01 | Hành vi chấp nhận được; ghi để đối chiếu schema |
| O-3 | Cursor rác, `order_by` sai, `filter` sai cú pháp, `depth=99`, id không phải UUID đều trả 400 (không 5xx) | P3-11 đến P3-16 | Tốt: đầu vào sai bị từ chối rõ ràng |
| O-4 | `limit=` rỗng trả 200, `limit=0` trả 200 | P3-01, P3-10 | Ghi nhận |
| O-5 | Id UUID hợp lệ nhưng không tồn tại trả 404, trong khi schema không khai báo 404 | P3-17 | Sẽ bị `status_code_conformance` báo (cùng loại lệch schema với D-02) |
| O-6 | `GET /open-api/core` không key trả 200 với schema khung (1 đường dẫn) | P5-06 | Đúng như mã nguồn (`PublicEndpointGuard`) |
| O-7 | 3 luồng nghiệp vụ (tạo Company; tạo Person gắn Company; đổi stage Opportunity NEW sang MEETING) chạy đúng: 201, 201, 200 và đọc lại thấy `stage` đúng | `evidence/business-flows-20261016-213042.json` | Bằng chứng mục C |

## Việc còn lại

- Chạy SC2 đến SC5 và bổ sung lỗi mới vào đây (mỗi lỗi: reproducer, check, RCA).
- RCA đầy đủ cho D-02, D-03 (gộp cả D-07), D-04 (Thuận); xác minh tay D-05 và dòng `updatedBy.source` của D-07 (Trung).
- Đã chạy ca đỏ và lần SC1 thứ hai (50/52 nhóm lỗi trùng). Còn lại: chạy lại SC1 có hook bảo vệ dữ liệu và `--reset` (R-01), không cắt thời gian, rồi so sánh hai lần bằng `summarize.py --compare`.
- Quyết định với thầy: phân loại "lệch schema" có tính là defect không (xem `email-hoi-thay.md`, bổ sung câu hỏi).
