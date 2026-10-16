# SPEC: Kiểm thử API dựa trên schema (K05 Schema-Based API / Fuzz) cho Twenty CRM (R10)

Môn: Kiểm thử phần mềm, Khoa CNTT, Trường ĐH Đà Lạt. Giảng viên: Nguyễn Thế Lâm.
Nguồn: (1) "Hướng dẫn thực hiện đề tài môn Kiểm thử phần mềm" của giảng viên; (2) kết quả kiểm tra repo Twenty trên máy nhóm ngày 16/10/2026.

---

## 1. Thông tin đề tài

| Mục | Nội dung |
|---|---|
| Tổ hợp | R10 twentyhq/twenty + K05 Schema-Based API / Fuzz |
| Công cụ | Schemathesis (chính); Postman (phụ, nếu cần xem tay một request) |
| Quy mô nhóm | 5 thành viên: Tiến (trưởng nhóm), Tuấn, Thuận, Trung, Quang |
| Hệ thống bị test (SUT) | Twenty CRM: Nx monorepo, TypeScript, NestJS, React, PostgreSQL, Redis |
| Repo gốc | https://github.com/twentyhq/twenty (chỉ clone và chạy, không sửa mã) |
| Repo nhóm | `twenty-k05` (chỉ chứa tài liệu và mã test) |

### Phiên bản đã pin (Phần H)

| Mục | Giá trị | Đã kiểm tra |
|---|---|---|
| Tag | `twenty/v2.45.6` | Có trong `.git/packed-refs` của repo trên máy |
| Commit SHA | `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e` | `HEAD` và tag trỏ cùng SHA này |
| Image Docker | `twentycrm/twenty:v2.45.6` | `TAG=v2.45.6` trong `packages/twenty-docker/.env` |
| Node / yarn (chạy từ source) | 24.16.0 / yarn 4.13.0 | `.nvmrc`, `package.json` |
| Base URL khi chạy local | `http://localhost:3001` | `docker-compose.yml` map `3001:3000`, `SERVER_URL=http://localhost:3001` |

Nếu nhóm đã đăng ký một SHA khác với giảng viên trước hạn 18/9, cần đối chiếu và thống nhất lại.

---

## 2. Yêu cầu của giảng viên

### 2.1. Hai phần bắt buộc

**Phần 1: Phân tích hệ thống và thiết lập môi trường**
- Đọc hiểu cấu trúc mã nguồn, nhận diện module và dependency chính.
- Vẽ kiến trúc và data flow của 3-5 nghiệp vụ trọng tâm.
- Cài đặt chạy thành công (local hoặc Docker).
- Lập tài liệu cài đặt (môi trường, runtime, biến môi trường, lệnh build/run, seed data).

**Phần 2: Ứng dụng kỹ thuật kiểm thử nâng cao**
- Nghiên cứu cơ sở lý thuyết, giới hạn và tiêu chí áp dụng.
- Thiết kế kịch bản kiểm thử tập trung vào luồng cốt lõi hoặc module rủi ro.
- Viết mã kiểm thử tự động.
- Chạy, thu log/metrics, phát hiện lỗi hoặc chứng minh coverage/score, rồi phân tích nguyên nhân gốc (RCA).

### 2.2. Yêu cầu riêng của K05 (Phụ lục 2 và 3)

- Ý tưởng: dùng OpenAPI/GraphQL để sinh request hợp lệ và lỗi, rồi kiểm tra invariant và status code.
- Đầu ra: **chạy schema tests; lưu reproducer; thống kê lỗi.** Đề bài không đặt số lượng tối thiểu, nên nhóm tự đặt ngưỡng ở mục 5.4.
- Điều kiện áp dụng: dự án có sẵn OpenAPI/GraphQL hoặc trích được schema. Twenty đạt: server có endpoint sinh OpenAPI (mục 3.1). Không phù hợp nếu không có API.
- Công cụ gợi ý: Schemathesis, Postman. Độ khó ★★◦.

### 2.3. Cấu trúc báo cáo bắt buộc (Phần A-H)

| Phần | Nội dung |
|---|---|
| A | Mục tiêu hệ thống, actor/use case, cây thư mục/module, dependency, data flow |
| B | Ít nhất 1 sơ đồ kiến trúc mức component/container; giải thích 3-5 module liên quan test |
| C | Môi trường, phiên bản, lệnh build/run, DB/service, seed data; bằng chứng chạy được và **ít nhất 3 luồng nghiệp vụ** |
| D | Nguyên lý, lý do chọn phạm vi, giả định, rủi ro, tiêu chí pass/fail |
| E | Scenario/case hoặc artefact tương đương: input, precondition, expected/invariant, dữ liệu test |
| F | Mã test/harness chạy lại tự động; README có lệnh chạy và dependency |
| G | Log/report/metrics, danh sách defect, phân tích nguyên nhân (nếu không có lỗi: chứng minh coverage/score đạt ngưỡng) |
| H | Pin commit/tag, lưu cấu hình test, cách chạy lại trên máy mới |

### 2.4. Mốc thời gian

| Mốc | Sự kiện | Cần đạt |
|---|---|---|
| 18/9 | Hạn đăng ký đề tài (đã qua) | Chốt thành viên, repo, kỹ thuật, commit SHA/tag, công cụ quản lý dự án |
| **20/10** | Báo cáo giữa kỳ (Milestone 2) | Demo hệ thống chạy; sơ đồ kiến trúc, tài liệu on-boarding; kế hoạch áp dụng kỹ thuật (phạm vi, giả định, tiêu chí) |
| Thi cuối kỳ (thường tháng 12) | Bảo vệ cuối kỳ | Thuyết trình, demo automation, nộp code test và báo cáo (**nộp trước 1 tuần**), peer-review |

### 2.5. Tiêu chí chấm

1. **Chuyên môn và mã nguồn:** vẽ lại được data flow; hướng dẫn cài đặt dựng lại được (khuyến khích Docker); hiểu và vận dụng đúng kỹ thuật; kịch bản mô tả cụ thể; code test gọn, chạy tự động; giải thích được kết quả và lỗi.
2. **Quản trị dự án và thuyết trình:** lịch sử commit Git đều của các thành viên; slide gọn; trả lời đúng trọng tâm.
3. **Đóng góp cá nhân:** peer evaluation, điểm cá nhân có thể chênh so với điểm nhóm.

---

## 3. Phạm vi kiểm thử

### 3.1. Nguồn schema (đã đọc trong mã nguồn ở tag `twenty/v2.45.6`)

- `OpenApiController` phục vụ `GET /open-api/core` và `GET /rest/open-api/core`; tương tự `.../metadata` cho Metadata API. File: `packages/twenty-server/src/engine/core-modules/open-api/`.
- **Không có Bearer key hợp lệ**, server chỉ trả schema khung, không có endpoint của object nào. Phải tải schema kèm key.
- Có key, `OpenApiService` sinh schema theo workspace, mỗi object (theo tên số nhiều) có các đường dẫn: `/{namePlural}`, `/batch/{namePlural}`, `/{namePlural}/{id}`, `/{namePlural}/duplicates`, `/{namePlural}/{id}/restore`, `/{namePlural}/restore`, `/{namePlural}/merge`, `/{namePlural}/groupBy`.
- Địa chỉ trong trường `servers` của schema là `${SERVER_URL}/rest/` (đọc từ `utils/base-schema.utils.ts`), nên `SERVER_URL` phải là `http://localhost:3001` và khi chạy Schemathesis với file schema phải truyền `--url http://localhost:3001/rest` (các đường dẫn trong schema là `/companies`..., không có tiền tố `/rest`).
- Schema đổi khi workspace thêm object/field (Metadata API), nên lưu bản chụp `schema/core.openapi.json` kèm commit để chạy lại cho ổn định.

### 3.2. Trong phạm vi

REST Core API của Companies, People, Opportunities, Notes, Tasks: list, get, create, update, delete, batch, và các endpoint `duplicates`, `restore`, `merge`, `groupBy` mà schema sinh cho mỗi object. Xác thực bằng `Authorization: Bearer <API key>`.

### 3.3. Mở rộng nếu còn thời gian

GraphQL `/graphql` (cần lấy schema từ instance đang chạy) và Metadata API (`/rest/metadata`, `/metadata`).

### 3.4. Ngoài phạm vi

Giao diện web, workflow, AI chat, email và lịch, job của worker, kiểm thử hiệu năng, và mọi hệ thống công khai (chỉ chạy trên instance local của nhóm).

### 3.5. Giả định

- Twenty chạy local bằng Docker ở tag đã pin, workspace test riêng, có thể reset bất kỳ lúc nào.
- Một API key quyền đầy đủ để chạy chính; thêm một key giới hạn role để kiểm thử phân quyền. Mỗi máy tự tạo key riêng (key chỉ có hiệu lực trên DB của máy đó).
- Không pull `main`; mọi thành viên dùng đúng tag và SHA ở mục 1.
- Schema là nguồn chân lý: hành vi lệch schema được ghi là defect loại "lệch schema", kể cả khi tính năng vẫn dùng được.

### 3.6. Phát hiện từ mã nguồn v2.45.6 (đã đọc, chưa chạy thật)

| # | Phát hiện | Nguồn | Hệ quả cho test |
|---|---|---|---|
| H1 | `limit` mặc định 60, tối đa 200. Giá trị lớn hơn 200 **bị cắt về 200 âm thầm**, không báo lỗi; chỉ `limit` âm hoặc không phải số mới bị từ chối | `twenty-shared/constants/QueryDefaultLimitRecords.ts`, `QueryMaxRecords.ts`; `rest/input-request-parsers/limit-parser-utils/parse-limit-rest-request.util.ts` | Nếu schema khai báo `maximum`, `negative_data_rejection` sẽ báo "chấp nhận `limit=201`". Cần phân loại: lệch schema hay thiết kế |
| H2 | Batch tối đa **200** bản ghi/lần (`Maximum number of records to upsert is 200`), không phải 60 | `common-create-many-query-runner.service.ts` | Sửa SC4 thành 0/1/200/201 |
| H3 | `RestApiExceptionFilter` đổi mọi lỗi không phải `HttpException` thành **400** (chú thích trong mã: đáng ra là 500) | `rest/rest-api-exception.filter.ts` | `not_a_server_error` ít khi đỏ vì lỗi nội bộ có thể hiện thành 400; nên đối chiếu thông điệp lỗi, không chỉ mã trạng thái |
| H4 | Controller có thêm `PUT *path` làm bí danh không được tài liệu hóa trong OpenAPI | `rest-api-core.controller.ts` | Check `unsupported_method` hoặc `status_code_conformance` có thể báo; ghi nhận là quan sát |
| H5 | API key là JWT; key bị thu hồi/hết hạn ném `AuthException FORBIDDEN_EXCEPTION`, key sai chữ ký bị passport từ chối | `auth/strategies/jwt.auth.strategy.ts` | SC5 chấp nhận cả 401 và 403 tùy trường hợp, ghi rõ từng ca |
| H6 | Quyền theo role: handler lấy `objectsPermissions` từ role của API key hoặc user | `rest/core/handlers/rest-api-base.handler.ts` | Key role giới hạn là cách duy nhất để kiểm thử phân quyền (SC5) |
| H7 | `MUTATION_MAX_MERGE_RECORDS = 9`; `QUERY_MAX_RECORDS_FROM_RELATION = 60` (con số 60 trong ghi chú nhóm có thể đến từ đây) | `twenty-shared/constants` | Ca biên cho `/merge`; giải thích nguồn gốc nhầm lẫn 60 |

### 3.7. Quan sát từ schema thật (tải ngày 16/10/2026 từ instance local, kèm Bearer key)

| Quan sát | Giá trị | Hệ quả |
|---|---|---|
| Phiên bản OpenAPI | 3.1.1; `servers[0].url` = `http://localhost:3001/rest/` | Chạy với `--url http://localhost:3001/rest` |
| Quy mô | 322 đường dẫn, **522 operation**, 41 đối tượng | Mẫu số "80% operation" tính trên **phạm vi 5 đối tượng = 65 operation** (13 mỗi đối tượng), không tính 522 |
| `limit` khai báo | `integer`, `minimum 0`, `maximum 200`, `default 60` | Khớp mã nguồn; `limit=201` được chấp nhận (H1) sẽ bị `negative_data_rejection` báo: lệch schema |
| Status khai báo | Chỉ `200/201`, `400`, `401` | Mọi `404`, `403`, `429` thật sự trả về sẽ bị `status_code_conformance` báo (lệch schema, không phải lỗi chức năng) |
| Schema phản hồi | `CompanyForResponse`, `CompanyForUpdate`, `Company` (body tạo) | Ca đỏ đổi kiểu `CompanyForResponse.name` |
| Company không có `employees` | Có `annualRevenue`, `position`... | `seed.py` dùng `annualRevenue` |


---

## 4. Danh sách scenario

SC1 là PoC cho Milestone 2; SC6, SC7 làm nếu kịp. K05 khai báo invariant, Schemathesis sinh input, nên mỗi scenario ghi invariant thay vì giá trị cụ thể.

| ID | Scenario | Precondition | Invariant / expected | Dữ liệu | Mốc |
|---|---|---|---|---|---|
| SC1 | Quét các operation trong phạm vi với dữ liệu hợp lệ theo schema | Instance chạy, key đầy đủ quyền | Không 5xx; status và body đúng schema | Sinh tự động; seed 20 Companies, 20 People | M2 (PoC trên Companies) |
| SC2 | Dữ liệu sai: thiếu field bắt buộc, sai kiểu, chuỗi rất dài, Unicode lạ, `null` | Như SC1 | Trả 4xx, không 2xx, không 5xx | Sinh tự động (chế độ negative) | Cuối kỳ |
| SC3 | List với tham số phân trang, lọc, sắp xếp ở giá trị biên | Có ít nhất 20 bản ghi | Không 5xx; cấu trúc phân trang nhất quán | Giá trị biên sinh tự động | Cuối kỳ |
| SC4 | Batch ở ngưỡng 0, 1, 200, 201 bản ghi (thêm ca đối chứng 61 vì ghi chú nhóm nói ngưỡng 60) | Như SC1 | 200 được nhận; 201 bị từ chối rõ ràng bằng 4xx, không 5xx. Ngưỡng 200 đọc từ mã nguồn (`QUERY_MAX_RECORDS`, mục 3.6); cần xác nhận trên instance | Mảng bản ghi sinh tự động | Cuối kỳ |
| SC5 | Xác thực: không key, key sai, key giới hạn role | Có thêm key role hạn chế | Thiếu/sai key bị 401 hoặc 403; role hạn chế không ghi được ngoài quyền | 3 loại key | Cuối kỳ |
| SC6 (mở rộng) | Chuỗi create, get, update, delete trên cùng bản ghi | Như SC1 | Get sau delete trả 404; không rò dữ liệu | Script chuỗi hoặc chế độ stateful | Nếu kịp |
| SC7 (mở rộng) | Cùng invariant trên GraphQL | Có endpoint `/graphql` | Không 5xx; lỗi đúng dạng GraphQL | Schema lấy từ instance | Nếu kịp |

### Ghi chú shape của response list (từ response thật của v2.45.6, theo ghi chú nhóm)

- Có `totalCount` (số nguyên) và `pageInfo` (`startCursor`, `endCursor`, `hasNextPage`, `hasPreviousPage`).
- Mỗi company có: `id` (UUID), `name`, `createdAt`, `updatedAt`, `deletedAt`, `domainName`, `address`, `annualRevenue`, `position`, `createdBy`, `updatedBy`, `accountOwnerId`.
- Dùng để đối chiếu schema với response thật khi phân loại "lệch schema".

---

## 5. Kỹ thuật kiểm thử (Phần D)

### 5.1. Nguyên lý

1. Schemathesis đọc OpenAPI, sinh request hợp lệ và không hợp lệ theo từng operation (dựa trên Hypothesis, property-based).
2. Gửi vào instance thật, rồi kiểm tra các check: không 5xx, status trong danh sách schema khai báo, Content-Type và body đúng schema, input sai bị từ chối, thiếu key bị chặn.
3. Khi gặp lỗi, công cụ tự thu nhỏ ca lỗi và in lệnh `curl` tái hiện. Nhóm lưu reproducer và thống kê (số operation, số request, số lỗi theo check và theo endpoint) vào `reports/`.

### 5.2. Lý do chọn phạm vi

- API của Twenty sinh tự động từ data model từng workspace, nên có nhiều operation giống nhau về cấu trúc và dễ lệch khỏi schema; phù hợp để quét tự động.
- Năm object chuẩn đủ phủ kiểu field phức hợp, quan hệ, phân trang, batch mà không ôm cả hệ thống.

### 5.3. Rủi ro

| Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|
| Tải schema không kèm key | Schema rỗng, test không có gì để chạy | Luôn gửi Bearer key; lưu bản chụp vào `schema/` |
| `SERVER_URL` sai | `servers` trong schema trỏ nhầm cổng | Đặt `SERVER_URL=http://localhost:3001`; hoặc truyền `--url` rõ ràng |
| Giới hạn tốc độ làm test nhận 429 | Kết quả nhiễu | Runner dùng `--rate-limit auto` (theo `Retry-After`); đo giới hạn thật của instance (tài liệu ghi 100 call/phút, chưa kiểm chứng) |
| Fuzz `DELETE /{đối tượng}` (xoá hàng loạt theo filter) làm mất dữ liệu seed | Các lần chạy sau thiếu dữ liệu, kết quả khác nhau | Workspace test riêng; chạy `scripts/seed.py` trước mỗi lần chạy |
| Schema không khớp hành vi thật | Nhiều báo lỗi giả | Phân loại riêng "lệch schema", kiểm chứng thủ công trước khi gọi là defect |
| Dữ liệu đổi giữa các lần chạy | Không lặp lại được | Reset DB và dùng cùng seed trước mỗi lần chạy |
| Lộ API key | Rủi ro bảo mật | Key trong `.env`, không commit; thu hồi nếu lỡ lộ |
| Vô tình test hệ thống công khai | Vi phạm quy định đề bài | Script chỉ cho phép `localhost` |
| `main` thay đổi | Test vỡ giữa kỳ | Pin tag, không pull `main` |
| Cổng 3000 bị chiếm (đã gặp) | Server không khởi động | Dùng `"3001:3000"` và `SERVER_URL=http://localhost:3001` |

### 5.4. Tiêu chí pass/fail

Tên check theo Schemathesis, đối chiếu lại bằng `st run --help` ở bản nhóm cài.

| Check | Pass khi | Fail (ghi thành defect) khi |
|---|---|---|
| `not_a_server_error` | Không có response 5xx | Có 5xx với bất kỳ input nào |
| `status_code_conformance` | Status nằm trong danh sách schema khai báo | Trả status schema không khai báo |
| `content_type_conformance` | Content-Type đúng khai báo | Khác khai báo |
| `response_schema_conformance` | Body đúng cấu trúc và kiểu | Thiếu/thừa field, sai kiểu |
| `negative_data_rejection` | Input sai schema bị 4xx | Input sai vẫn nhận 2xx |
| `positive_data_acceptance` | Input đúng schema được chấp nhận | Input đúng bị từ chối |
| `ignored_auth` | Thiếu/sai key bị 401 hoặc 403 | Truy cập được khi không có key hợp lệ |

Mỗi defect ghi kèm reproducer (`curl` hoặc cassette), endpoint, check bị vi phạm, và phân tích nguyên nhân (RCA).

**Ngưỡng Milestone 2:** SC1 chạy xong trên Companies, có thống kê (số operation, số request, số lỗi theo check) và ít nhất 1 reproducer. Thêm 1 ca đỏ cố ý để chứng minh công cụ bắt được lỗi, ví dụ chạy trên bản schema sửa tay (đổi kiểu một field) để `response_schema_conformance` báo lỗi.

**Ngưỡng cuối kỳ (đề xuất):**
- Ít nhất 80% operation trong phạm vi được chạy ít nhất một lần.
- Mỗi operation chạy tối thiểu 50 test case; tổng số request được thống kê.
- Mỗi lỗi có reproducer trong `reports/`.
- Chạy lại hai lần với cùng seed cho kết quả lỗi giống nhau.
- Nếu không tìm thấy lỗi: nộp bằng chứng coverage theo các ngưỡng trên.

### 5.5. Giới hạn của K05 (nêu khi báo cáo)

- Không hiểu nghiệp vụ: sai logic mà vẫn đúng schema thì không phát hiện.
- Chất lượng phụ thuộc độ chính xác của OpenAPI.
- Request phụ thuộc dữ liệu (tạo A rồi mới gọi B) cần cấu hình thêm hoặc chế độ stateful (SC6).

---

## 6. Phân vai

| Thành viên | Vai | Trách nhiệm chính | Phần báo cáo |
|---|---|---|---|
| Tiến | Trưởng nhóm / QA Lead | Board, điều phối, chốt phạm vi K05, ghép báo cáo và slide | D, tổng hợp |
| Tuấn | Kỹ sư môi trường | Chuẩn hóa `.env` và Docker Compose ở bản pin, `SETUP.md`, hướng dẫn cả nhóm cài | C, H |
| Thuận | Phân tích hệ thống | Cây module, sơ đồ component/container, data flow 3-5 nghiệp vụ, dựng lại từ máy sạch để kiểm README | A, B |
| Trung | API và dữ liệu | Tạo API key, lấy OpenAPI, script seed, chạy 3 luồng nghiệp vụ, chốt danh sách operation | C (luồng), E (dữ liệu) |
| Quang | Harness K05 | Dựng repo test, cấu hình Schemathesis, viết SC1 đến SC5, chạy thử, thống kê và reproducer | E, F, G |

Trung và Quang làm cặp: Trung cấp schema và dữ liệu, Quang chạy test và đối chiếu lỗi.

---

## 7. Lịch 16/10 đến 20/10

| Ngày | Tiến | Tuấn | Thuận | Trung | Quang |
|---|---|---|---|---|---|
| T6 16/10 | Tạo board, giao card, gửi SPEC cho nhóm | Chuẩn hóa `.env`, chốt máy chuẩn | Clone ở SHA đã pin, lập cây `packages/` | Chờ instance; đọc cách tạo key và OpenAPI | Cài Schemathesis, thử trên schema mẫu |
| T7 17/10 | Kiểm tra nội bộ lần 1; viết Phần D | **12:00 instance chạy** trên máy chuẩn; `SETUP.md` | Đọc mã `open-api`, `rest/core`; vẽ sơ đồ | Tạo key, tải OpenAPI | Dựng repo `twenty-k05`, viết SC1 |
| CN 18/10 | Ghép báo cáo | Nộp mục C, H (12:00); hỗ trợ ảnh, log | **18:00 sơ đồ nháp** | **12:00 có `core.openapi.json`**; viết `seed.py` | Viết SC2 đến SC5, chạy thử trên Companies |
| T2 19/10 | Slide nháp 20:00; rà checklist; kiểm tra nội bộ lần 2 | Hỗ trợ demo | Dựng lại từ máy sạch theo README | Chạy 3 luồng nghiệp vụ, chụp bằng chứng | **18:00 kết quả chạy thử** có thống kê |
| T3 20/10 | **Demo giữa kỳ** | Demo môi trường | Trình bày kiến trúc | Demo 3 luồng | Demo chạy K05 |

Dự phòng:
- Đến 12:00 ngày 17/10 instance chưa chạy: Tiến cử người dựng song song trên máy khác; các máy còn lại chạy thử Schemathesis trên schema mẫu.
- Không tải được OpenAPI kèm key: thử `/rest/open-api/core`, kiểm tra role của key, rồi lấy schema từ API Playground trong Settings.
- GraphQL (SC7) chưa kịp: demo chỉ REST, đưa GraphQL vào kế hoạch cuối kỳ.

---

## 8. Quy trình làm việc

- Cấu trúc repo `twenty-k05`: `docs/` (SPEC, SETUP, architecture, test-plan), `env/` (docker-compose.yml, `.env.example`, `VERSION.txt` ghi tag và SHA), `schema/` (`core.openapi.json`), `scripts/` (`fetch_schema.sh`, `seed.py`, `run_k05.sh`), `hooks/` (hook Schemathesis cho xác thực), `reports/` (log, kết quả, reproducer, `summary.md`), `README.md` (SHA của Twenty ở đầu).
- Nhánh: `main` được bảo vệ; mỗi task một nhánh `feature/<ten>-<task>`; PR cần 1 người review.
- Commit: `feat(harness): ...`, `feat(scenario): ...`, `docs(setup): ...`, `fix: ...`.
- Mỗi người tối thiểu 3 commit trước 20/10 (phục vụ peer-review).
- Check-in hằng ngày 21:00: đã làm, sẽ làm, đang vướng.
- Kiểm tra nội bộ: 17/10 và 19/10. Hạn nộp phần cá nhân cho Tiến theo từng người, ghi ở `PHAN_CONG.md`.
- **Bảo mật:** `.env` luôn nằm trong `.gitignore`; chỉ commit `.env.example`. Không gửi API key qua chat.

---

## 9. Hướng dẫn chạy môi trường (tóm tắt, chi tiết ở `docs/SETUP.md`)

1. Windows: `git config --global core.longpaths true`; clone vào thư mục đường dẫn ngắn.
2. `git clone https://github.com/twentyhq/twenty.git` rồi `git checkout twenty/v2.45.6`; đối chiếu `git rev-parse HEAD` với SHA ở mục 1.
3. Tạo `packages/twenty-docker/.env` từ `.env.example` với: `TAG=v2.45.6`, `PG_DATABASE_*`, `REDIS_URL`, `SERVER_URL=http://localhost:3001`, `ENCRYPTION_KEY` (ngẫu nhiên, `openssl rand -base64 32`), `STORAGE_TYPE=local`.
4. Nếu cổng 3000 bị chiếm: đổi `"3000:3000"` thành `"3001:3000"` trong `docker-compose.yml`.
5. `docker compose pull`, `docker compose up -d`; lần đầu server mất vài phút migration (trạng thái `unhealthy` ban đầu là bình thường).
6. Mở `http://localhost:3001`, tạo tài khoản và workspace; bước "Install apps" chọn Skip.
7. Tạo API key: Settings, mục **MCP & APIs** (tên menu theo ghi chú nhóm). Lưu vào biến môi trường `TWENTY_API_KEY`, không commit.
8. Tải schema: `python scripts/fetch_schema.py` (hoặc `curl.exe -H "Authorization: Bearer <KEY>" http://localhost:3001/open-api/core -o schema/core.openapi.json`).
9. Chạy thử (tên tham số kiểm tra bằng `st run --help` ở bản đã cài):
   `python scripts/run_k05.py SC1` (bên trong gọi `st run schema/core.openapi.json --url http://localhost:3001/rest -H "Authorization: Bearer <KEY>" --checks all --max-examples 50 ...`; xem `st run --help`, đã đối chiếu với Schemathesis 4.31.1)

Sự cố đã gặp và cách xử lý:

| Sự cố | Cách xử lý |
|---|---|
| `Filename too long` khi clone trên Windows | Bật `core.longpaths`, `git restore --source=HEAD :/`, clone vào đường dẫn ngắn |
| `port is already allocated` ở cổng 3000 | Đổi sang `3001:3000` |
| Server báo `could not translate host name "db"` | `docker compose down` rồi `up -d` để tạo lại mạng; nếu vẫn lỗi, restart Docker Desktop |
| `docker ps` không kết nối được | Mở Docker Desktop, chờ "Engine running" |
| Schema tải về không có endpoint của object | Gửi kèm Bearer key hợp lệ (không key chỉ ra schema khung) |

---

## 10. Checklist Milestone 2 (tick tối 19/10)

- [ ] Demo: Twenty chạy local, đăng nhập được, 3 luồng (tạo Company, tạo Person gắn Company, đổi stage Opportunity)
- [ ] Sơ đồ component/container và data flow 3-5 nghiệp vụ (A, B)
- [ ] `docs/SETUP.md` và SHA ghi trong `README.md` (C, H)
- [ ] Kế hoạch K05: phạm vi, giả định, rủi ro, tiêu chí pass/fail (D)
- [ ] `schema/core.openapi.json` đã tải kèm key và có đủ 5 object
- [ ] PoC Schemathesis: SC1 chạy trên Companies có thống kê, ít nhất 1 reproducer, và 1 ca đỏ cố ý
- [ ] Board có lịch sử thẻ; Git có commit của cả 5 người
- [ ] Slide 10-12 trang, tổng duyệt 19/10

---

## 11. Điểm cần xác minh trên máy thật

- [ ] Tag/SHA khớp với bản đã đăng ký với thầy hạn 18/9 (trong repo, tag và SHA đã khớp nhau).
- [ ] `GET /open-api/core` kèm key trả đủ object. (Mã nguồn cho thấy `servers[0].url` = `${SERVER_URL}/rest/`; xác nhận trên instance.)
- [ ] Giới hạn 100 call/phút có áp dụng trên instance self-host. (Ngưỡng batch: mã nguồn nói 200, không phải 60; `scripts/probe_boundaries.py` ca P4-03/04/05 xác nhận.)
- [ ] Tên menu tạo API key ("MCP & APIs") đúng với bản v2.45.6.
- [ ] Đường dẫn và cách lấy schema GraphQL nếu làm SC7.
- [ ] Hỏi giảng viên: phạm vi chỉ REST có được chấp nhận không, có yêu cầu thêm GraphQL không.

---

## 12. Tài liệu tham khảo

- https://github.com/twentyhq/twenty và https://github.com/twentyhq/twenty/releases
- https://docs.twenty.com/developers/extend/capabilities/apis
- https://docs.twenty.com/developers/self-host/capabilities/docker-compose
- https://schemathesis.github.io/schemathesis/
