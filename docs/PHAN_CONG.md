# Phân công công việc nhóm R10 Twenty + K05

Cập nhật: 16/10/2026. Người lập: Tiến (nhóm trưởng). Chi tiết kỹ thuật xem `SPEC.md` cùng thư mục.

Có hai mốc:

| | Mốc 1: Báo cáo giữa kỳ | Mốc 2: Bảo vệ cuối kỳ |
|---|---|---|
| Ngày | **Thứ Ba 20/10/2026** | Chưa có lịch (thường tháng 12). Hạn nộp báo cáo và mã test: **trước ngày bảo vệ 1 tuần**. Tiến điền ngày khi thầy công bố: `__/__/2026` |
| Giai đoạn làm việc | 16/10 đến 20/10 | 21/10 đến ngày nộp |
| Cần đạt | Demo Twenty chạy; sơ đồ kiến trúc; tài liệu on-boarding; kế hoạch K05 (phạm vi, giả định, tiêu chí) | Thuyết trình toàn bộ; demo chạy script automation; nộp mã test và báo cáo tổng kết A đến H; peer-review |

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Đề tài | R10 twentyhq/twenty + K05 Schema-Based API / Fuzz (Schemathesis) |
| Phiên bản pin | Tag `twenty/v2.45.6`, SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e` |
| Địa chỉ chạy local | `http://localhost:3001` |
| Nguồn schema | `GET /open-api/core` kèm Bearer API key |

## 2. Thành viên và vai trò

| Thành viên | Vai trò | Phụ trách chính | Phần báo cáo |
|---|---|---|---|
| **Tiến** | Nhóm trưởng, QA Lead | Board, điều phối, chốt phạm vi K05, ghép báo cáo và slide, rà checklist | D, tổng hợp |
| **Tuấn** | Kỹ sư môi trường | Docker Compose ở bản pin, `.env`, `SETUP.md`, reset môi trường, chạy lại trên máy mới | C, H |
| **Thuận** | Phân tích hệ thống | Cây module, sơ đồ kiến trúc, data flow, phân tích nguyên nhân gốc (RCA) trong mã nguồn | A, B, G (RCA) |
| **Trung** | API và dữ liệu | API key, OpenAPI, dữ liệu mẫu, 3 luồng nghiệp vụ, xác minh thủ công lỗi nghi ngờ | C (luồng), E (dữ liệu) |
| **Quang** | Harness K05 | Repo test, Schemathesis, scenario SC1 đến SC7, chạy test, thống kê và reproducer | E, F, G |

Trung và Quang làm cặp: Trung cấp schema và dữ liệu, Quang chạy test và đối chiếu lỗi.

---

# MỐC 1: BÁO CÁO GIỮA KỲ (thứ Ba 20/10)

## 3. Thứ tự phụ thuộc

```
Tuấn: instance chạy (17/10 12:00)
   └─> Trung: tạo API key, tải OpenAPI (18/10 12:00)
          └─> Quang: chạy thử Schemathesis trên schema thật (19/10 18:00)
Thuận: đọc mã, vẽ sơ đồ (độc lập, chỉ cần repo ở đúng SHA)
Tiến: board, Phần D, ghép báo cáo (độc lập, nhận sản phẩm của 4 người)
```

Trong lúc chờ instance, Quang học và thử Schemathesis trên schema mẫu; Thuận làm sơ đồ; Tiến lập board và viết Phần D. Không ai đứng chờ.

## 4. Chi tiết từng người (giữa kỳ)

### Tiến (nhóm trưởng)

- [ ] 16/10 tối: tạo board Trello/Jira, giao thẻ cho 4 người, gửi `SPEC.md` và file này vào nhóm chat
- [ ] 16/10 tối: tạo repo nhóm `twenty-k05`, mời đủ thành viên, bật bảo vệ nhánh `main`
- [ ] 17/10: viết Phần D (nguyên lý, phạm vi, giả định, rủi ro, tiêu chí pass/fail) từ `SPEC.md` mục 3 và 5
- [ ] 17/10: kiểm tra nội bộ lần 1 (instance chạy chưa, ai đang vướng)
- [ ] 17/10: xác nhận tag và SHA khớp với bản nhóm đã đăng ký với thầy hạn 18/9
- [ ] Hỏi thầy: chỉ làm REST có được chấp nhận không, có yêu cầu thêm GraphQL không
- [ ] 18/10: nhận sản phẩm của Tuấn, Thuận, Trung; ghép báo cáo A đến E
- [ ] 19/10: slide nháp xong trước 20:00 (10-12 trang), phân người nói từng phần
- [ ] 19/10: kiểm tra nội bộ lần 2, rà checklist Milestone 2, tổng duyệt
- [ ] 20/10: điều phối buổi demo

**Xong khi:** board đủ thẻ và có lịch sử; báo cáo A đến E ghép xong; slide đã tập một lần; checklist ở mục 7 tick hết.

### Tuấn (môi trường)

- [ ] 16/10 tối: chốt máy chuẩn, chuẩn hóa `.env` (`TAG=v2.45.6`, `SERVER_URL=http://localhost:3001`, `ENCRYPTION_KEY` ngẫu nhiên)
- [ ] **17/10 trước 12:00: instance chạy** trên máy chuẩn, đăng nhập được, báo vào nhóm chat
- [ ] 17/10: viết `docs/SETUP.md` (runtime, Docker, biến môi trường, cổng, lệnh chạy, sự cố thường gặp)
- [ ] 17/10: giúp từng người cài lại trên máy của họ; ghi lại lỗi gặp phải
- [ ] 18/10 trước 12:00: nộp Phần C và H cho Tiến; lưu `VERSION.txt` (tag + SHA), `.env.example`, `docker-compose.yml` vào `env/`
- [ ] 18/10: chụp ảnh bằng chứng (`docker compose ps`, đăng nhập, 3 luồng) cùng Trung
- [ ] 19/10: quay video màn hình bản demo làm phương án dự phòng

**Xong khi:** một người khác dựng lại được từ `SETUP.md` mà không cần hỏi thêm; không có API key nào nằm trong Git.

### Thuận (phân tích hệ thống)

- [ ] 16/10: clone Twenty ở SHA đã pin, kiểm tra `git rev-parse HEAD`, lập cây thư mục `packages/`
- [ ] 17/10: đọc `packages/twenty-server/src/engine/core-modules/open-api`, `.../api/rest/core`, `.../api/rest/metadata`, `.../api/graphql`
- [ ] 17/10: đối chiếu nốt module xác thực và role trong mã nguồn
- [ ] **18/10 trước 18:00: sơ đồ kiến trúc nháp** (mức component/container) và data flow của 3-5 nghiệp vụ
- [ ] 19/10: dựng lại hệ thống từ máy sạch theo `SETUP.md` của Tuấn, ghi lỗi gặp phải
- [ ] 19/10 trước 12:00: nộp bản cuối Phần A và B cho Tiến

**Xong khi:** sơ đồ có giải thích 3-5 module liên quan K05; README dựng lại được trên máy sạch.

### Trung (API và dữ liệu)

- [ ] 16/10: đọc cách tạo API key và lấy OpenAPI (xem `SPEC.md` mục 3.1 và 9)
- [ ] Sau khi instance chạy (17/10): tạo workspace, tạo API key (Settings, mục MCP & APIs), lưu vào biến môi trường, không commit
- [ ] **18/10 trước 12:00: tải `schema/core.openapi.json`** kèm key, kiểm tra có đủ Companies, People, Opportunities, Notes, Tasks; ghi lại trường `servers`
- [ ] 18/10: chốt danh sách operation trong phạm vi (gồm `duplicates`, `restore`, `merge`, `groupBy`)
- [ ] 19/10 trước 12:00: viết `scripts/seed.py` tạo dữ liệu mẫu (chia lô 50 bản ghi; giới hạn batch thật trong mã nguồn là 200)
- [ ] 19/10: chạy 3 luồng nghiệp vụ qua UI và API (tạo Company, tạo Person gắn Company, đổi stage Opportunity), chụp bằng chứng
- [ ] Tạo thêm một API key giới hạn role để Quang chạy SC5

**Xong khi:** Quang chạy được Schemathesis trên schema của Trung; `seed.py` chạy lại được trên DB trống; 3 luồng có ảnh hoặc video.

### Quang (harness K05)

- [ ] 16/10 đến 17/10: cài Schemathesis, thử trên schema mẫu, đọc `st run --help` ghi lại tên check và tham số của bản đã cài
- [ ] 17/10: dựng repo `twenty-k05` theo cấu trúc ở `SPEC.md` mục 8, viết `README.md` khung
- [ ] 17/10: viết SC1 (quét operation, dữ liệu hợp lệ)
- [ ] 18/10: viết SC2 đến SC5 (dữ liệu sai, phân trang biên, batch 0/1/200/201, xác thực)
- [ ] 18/10 sau khi có schema: chạy thử SC1 trên Companies, lưu log
- [ ] **19/10 trước 18:00: kết quả chạy thử** có thống kê (số operation, số request, số lỗi theo check) và ít nhất 1 reproducer
- [ ] 19/10: làm 1 ca đỏ cố ý (chạy trên schema sửa tay, đổi kiểu một field) để chứng minh công cụ bắt được lỗi
- [ ] Chỉ chạy trên `localhost`; script từ chối URL khác

**Xong khi:** `scripts/run_k05.py` (có bọc `run_k05.sh`) chạy lại từ đầu ra cùng kết quả hai lần; `reports/` có log, thống kê, reproducer.

## 5. Lịch theo ngày (giữa kỳ)

| Ngày | Tiến | Tuấn | Thuận | Trung | Quang |
|---|---|---|---|---|---|
| T6 16/10 | Board, repo, giao thẻ | Chuẩn hóa `.env`, chốt máy chuẩn | Clone ở SHA, cây `packages/` | Đọc cách tạo key, OpenAPI | Cài Schemathesis, thử schema mẫu |
| T7 17/10 | Phần D; kiểm tra lần 1; xác nhận SHA | **12:00 instance chạy**; `SETUP.md` | Đọc mã `open-api`, `rest`, `graphql` | Tạo key, bắt đầu tải schema | Repo `twenty-k05`, SC1 |
| CN 18/10 | Ghép báo cáo | **12:00 nộp C, H**; chụp bằng chứng | **18:00 sơ đồ nháp** | **12:00 có `core.openapi.json`**; chốt operation | SC2 đến SC5; chạy thử Companies |
| T2 19/10 | **20:00 slide nháp**; kiểm tra lần 2; tổng duyệt | Video dự phòng; hỗ trợ demo | **12:00 nộp A, B**; dựng lại máy sạch | **12:00 `seed.py`**; 3 luồng, bằng chứng | **18:00 kết quả chạy thử** |
| T3 20/10 | Điều phối demo | Demo môi trường | Trình bày kiến trúc | Demo 3 luồng | Demo chạy K05 |

## 6. Phân người nói khi demo 20/10

| Phần | Người nói |
|---|---|
| Giới thiệu đề tài, K05 là gì, phạm vi, tiêu chí pass/fail | Tiến |
| Môi trường và cài đặt, demo Twenty chạy | Tuấn |
| Kiến trúc và data flow | Thuận |
| 3 luồng nghiệp vụ, nguồn schema, dữ liệu mẫu | Trung |
| Demo chạy Schemathesis, kết quả sơ bộ, reproducer | Quang |

## 7. Checklist demo giữa kỳ (Tiến rà tối 19/10)

- [ ] Twenty chạy từ `docker compose up -d`, đăng nhập được (Tuấn)
- [ ] 3 luồng nghiệp vụ chạy được, có ảnh hoặc video (Trung)
- [ ] Sơ đồ component/container và data flow (Thuận)
- [ ] `docs/SETUP.md`, `VERSION.txt` (tag + SHA), đã có người dựng lại thử (Tuấn, Thuận)
- [ ] Kế hoạch K05: phạm vi, giả định, rủi ro, tiêu chí pass/fail (Tiến)
- [ ] `schema/core.openapi.json` đủ 5 object (Trung)
- [ ] Một lượt chạy Schemathesis có thống kê, 1 reproducer, 1 ca đỏ cố ý (Quang)
- [ ] Board có lịch sử thẻ; Git có commit của cả 5 người (Tiến)
- [ ] Slide 10-12 trang, đã tổng duyệt (cả nhóm)

## 8. Dự phòng (giữa kỳ)

| Tình huống | Cách xử lý |
|---|---|
| 17/10 12:00 instance chưa chạy | Tiến cử người dựng song song trên máy khác; Quang tiếp tục thử trên schema mẫu |
| Không tải được OpenAPI kèm key | Thử `/rest/open-api/core`, kiểm tra role của key, hoặc lấy schema từ API Playground trong Settings |
| Schema trỏ sai cổng | Đặt `SERVER_URL=http://localhost:3001`, hoặc truyền `--url` rõ ràng |
| Một thành viên không kịp hạn | Báo Tiến sớm; Tiến chia lại việc, ưu tiên phần demo giữa kỳ |
| GraphQL (SC7) chưa kịp | Demo chỉ REST, đưa GraphQL vào kế hoạch cuối kỳ |
| Mạng hoặc Docker lỗi lúc demo | Chiếu video dự phòng của Tuấn |

---

# MỐC 2: BẢO VỆ CUỐI KỲ

Ngày bảo vệ chưa có. Kế hoạch dưới đây chia theo tuần kể từ sau giữa kỳ, và theo mốc tương đối so với ngày bảo vệ (gọi là **T**). Khi biết ngày, Tiến điền vào bảng ở đầu file và dời các sprint nếu cần; nếu T đến sớm hơn dự kiến thì nén Sprint 6 và 7.

## 9. Mục tiêu cuối kỳ (theo `SPEC.md` mục 5.4)

- Chạy đầy đủ SC1 đến SC5 trên 5 object (SC6, SC7 nếu kịp).
- Ít nhất 80% operation trong phạm vi được chạy ít nhất một lần; mỗi operation tối thiểu 50 test case.
- Mỗi lỗi có reproducer trong `reports/` và có phân tích nguyên nhân gốc (RCA).
- Chạy lại hai lần với cùng seed cho kết quả lỗi giống nhau.
- Nếu không tìm thấy lỗi: nộp bằng chứng coverage theo các ngưỡng trên.
- Báo cáo đủ Phần A đến H; mã test chạy lại được từ máy sạch theo README.

## 10. Mốc tương đối theo ngày bảo vệ (T)

| Mốc | Việc | Người chịu trách nhiệm |
|---|---|---|
| T−14 | Đóng băng mã test; chạy bản chính thức lần cuối | Quang, Tuấn |
| T−10 | Báo cáo nháp đủ A đến H | Tiến ghép; mỗi người nộp phần của mình |
| T−8 | Review chéo báo cáo và mã (mỗi phần có một người khác đọc) | Cả nhóm |
| **T−7** | **Nộp báo cáo và mã test** | Tiến |
| T−3 | Tổng duyệt thuyết trình và demo script automation | Cả nhóm |
| T | Bảo vệ, peer-review | Cả nhóm |

## 11. Các sprint sau giữa kỳ (ngày dự kiến, chỉnh khi biết T)

| Sprint | Thời gian | Mục tiêu | Cổng kiểm tra cuối sprint |
|---|---|---|---|
| 3 | 21/10 đến 27/10 | Nền tảng ổn định: script reset môi trường, schema chốt, SC1 đến SC3 chạy đủ 5 object | Chạy từ DB sạch ra kết quả lặp lại được |
| 4 | 28/10 đến 3/11 | Thêm SC4 (batch), SC5 (xác thực); chạy toàn bộ lần 1; gom defect và phân loại | Có danh sách defect đợt 1 (thật hay lệch schema) |
| 5 | 4/11 đến 10/11 | RCA từng defect; SC6 (chuỗi create, get, update, delete); xác minh thủ công; SC7 GraphQL nếu kịp | Mỗi defect có reproducer và nguyên nhân |
| 6 | 11/11 đến 17/11 | Chạy chính thức 3 lần để kiểm tra tái lập; chốt số liệu coverage; báo cáo nháp A đến H | Số liệu đạt ngưỡng ở mục 9 hoặc có kế hoạch bù |
| 7 | 18/11 đến 24/11 | Hoàn thiện báo cáo, slide, README; dựng lại trên máy sạch; tổng duyệt; đệm dự phòng | Báo cáo và mã sẵn sàng nộp trước T−7 |

## 12. Chi tiết từng người (cuối kỳ)

### Tiến (nhóm trưởng)

- [ ] Sau 20/10: ghi nhận góp ý của thầy ở buổi giữa kỳ, đưa vào board thành thẻ cụ thể
- [ ] Hỏi thầy ngày bảo vệ và hạn nộp chính xác; điền vào bảng đầu file, dời sprint nếu cần
- [ ] Chốt phạm vi cuối (có làm GraphQL, SC6, SC7 hay không) trước hết Sprint 3
- [ ] Mỗi tuần: rà board, kiểm tra mỗi người có commit; nhắc ai chưa có commit
- [ ] Review phân loại defect cùng Thuận và Trung (lỗi thật hay lệch schema)
- [ ] T−10: ghép báo cáo A đến H, kiểm tra các phần khớp nhau (tên, số liệu, tag, SHA)
- [ ] Làm slide cuối kỳ, phân người nói, tổ chức tổng duyệt T−3
- [ ] Chuẩn bị peer-review: tổng hợp đóng góp từng người từ board và lịch sử Git
- [ ] **T−7: nộp báo cáo và mã**

**Xong khi:** báo cáo A đến H nhất quán; đã nộp đúng hạn; slide đã tập ít nhất hai lần.

### Tuấn (môi trường)

- [ ] Sprint 3: viết `scripts/reset-env.sh` (xóa dữ liệu, dựng lại workspace sạch, seed lại) để mỗi lần chạy test bắt đầu từ trạng thái giống nhau
- [ ] Sprint 3: xác định máy demo chính và máy dự phòng; ghi cấu hình tối thiểu cần có
- [ ] Sprint 4 đến 6: hỗ trợ Quang khi cần môi trường riêng (ví dụ reset giữa các scenario, chạy SC6 stateful)
- [ ] Sprint 6: viết Phần H hoàn chỉnh: pin tag/SHA, lưu cấu hình test, mô tả cách chạy lại trên máy mới
- [ ] Sprint 7: dựng lại toàn bộ từ máy sạch theo README một lần nữa, sửa tài liệu theo lỗi gặp
- [ ] Sprint 7: quay video demo cuối kỳ làm phương án dự phòng
- [ ] Giữ `.env` ngoài Git; kiểm tra lịch sử Git không lộ key

**Xong khi:** từ máy sạch, theo README, chạy được từ cài đặt đến ra báo cáo test; không lộ key trong Git.

### Thuận (phân tích hệ thống)

- [ ] Sprint 3: hoàn thiện Phần A và B nếu giữa kỳ cần sửa theo góp ý của thầy
- [ ] Sprint 4: đọc mã xử lý xác thực, phân quyền, validation của các endpoint trong phạm vi để hiểu cách server từ chối request sai (phục vụ SC2, SC5)
- [ ] Sprint 5: **RCA cho từng defect**: lần theo request lỗi vào mã server, chỉ ra tầng gây lỗi (validation, xử lý tham số, truy vấn, schema sinh), ghi vào Phần G
- [ ] Sprint 5: cùng Trung phân biệt lỗi thật của server và lệch schema (schema sinh sai so với hành vi)
- [ ] Sprint 5 đến 6: nếu làm SC7, hỗ trợ tìm cách lấy schema GraphQL của instance
- [ ] Sprint 6: viết phần phân tích nguyên nhân tổng hợp (nhóm lỗi, tần suất, tầng gây lỗi)
- [ ] Sprint 7: kiểm tra sơ đồ kiến trúc còn khớp với phần test thực tế

**Xong khi:** mỗi defect có nguyên nhân gốc trỏ đến tầng hoặc module cụ thể; Phần G có bảng nhóm lỗi.

### Trung (API và dữ liệu)

- [ ] Sprint 3: giữ `schema/core.openapi.json` ổn định; ghi lại mỗi lần schema đổi (khi thêm object hoặc field tùy biến)
- [ ] Sprint 3: mở rộng `seed.py` đủ cho SC3 (phân trang cần nhiều bản ghi) và SC4 (batch)
- [ ] Sprint 4: tạo key giới hạn role và chuẩn bị dữ liệu cho SC5 (key đủ quyền, key giới hạn, key sai, không key)
- [ ] Sprint 5: viết SC6: chuỗi create, get, update, delete trên cùng bản ghi (script hoặc chế độ stateful của Schemathesis)
- [ ] Sprint 5: **xác minh thủ công** các lỗi nghi ngờ bằng `curl` hoặc Postman trước khi Quang ghi thành defect
- [ ] Sprint 5 đến 6: nếu làm SC7, lấy schema GraphQL từ `/graphql` và đưa vào `schema/`
- [ ] Sprint 6: viết Phần E phần dữ liệu test (mỗi scenario dùng dữ liệu nào, sinh thế nào)

**Xong khi:** mỗi defect trong báo cáo đã được xác minh bằng request tay; dữ liệu seed tạo lại được từ DB trống.

### Quang (harness K05)

- [ ] Sprint 3: chạy SC1 đến SC3 trên cả 5 object; sửa cấu hình để kết quả lặp lại (cùng seed)
- [ ] Sprint 4: hoàn thiện SC4 (batch 0/1/200/201) và SC5 (xác thực); chạy toàn bộ lần 1; xuất thống kê (số operation, số request, lỗi theo check và theo endpoint)
- [ ] Sprint 4: lưu reproducer (`curl` hoặc cassette) cho mọi lỗi vào `reports/`
- [ ] Sprint 5: làm SC6 cùng Trung; làm SC7 nếu có schema GraphQL
- [ ] Sprint 6: chạy chính thức 3 lần để kiểm tra tái lập; tính coverage theo ngưỡng (80% operation, 50 case mỗi operation)
- [ ] Sprint 6: viết `scripts/run_k05.py` (có bọc `run_k05.sh`) chạy một lệnh từ DB sạch ra báo cáo; dọn mã cho gọn
- [ ] Sprint 7: hoàn thiện `README.md` (lệnh chạy, dependency, cách đọc báo cáo); viết Phần F và thống kê Phần G
- [ ] T−14: đóng băng mã test

**Xong khi:** một lệnh chạy lại được toàn bộ và ra cùng kết quả; `reports/` có log, thống kê, reproducer; số liệu đạt ngưỡng hoặc có giải thích.

## 13. Ma trận việc theo sprint (cuối kỳ)

| Sprint | Tiến | Tuấn | Thuận | Trung | Quang |
|---|---|---|---|---|---|
| 3 (21/10 đến 27/10) | Ghi góp ý giữa kỳ; hỏi ngày bảo vệ; chốt phạm vi | `reset-env.sh`; chọn máy demo | Sửa A, B theo góp ý | Schema ổn định; mở rộng `seed.py` | SC1 đến SC3 trên 5 object |
| 4 (28/10 đến 3/11) | Rà board, nhắc commit | Hỗ trợ môi trường | Đọc mã xác thực, validation | Key giới hạn role; dữ liệu SC5 | SC4, SC5; chạy lần 1; reproducer |
| 5 (4/11 đến 10/11) | Review phân loại defect | Hỗ trợ SC6 | **RCA từng defect** | SC6; xác minh thủ công | SC6, SC7 nếu kịp |
| 6 (11/11 đến 17/11) | Báo cáo nháp A đến H | Phần H hoàn chỉnh | Phân tích nguyên nhân tổng hợp | Phần E (dữ liệu test) | Chạy chính thức 3 lần; `run_k05.sh` |
| 7 (18/11 đến 24/11) | Slide; tổng duyệt; nộp T−7 | Dựng lại máy sạch; video dự phòng | Kiểm tra sơ đồ khớp | Rà dữ liệu và schema cuối | README; Phần F, G; đóng băng mã |

## 14. Phân người nói khi bảo vệ (đề xuất)

| Phần | Người nói |
|---|---|
| Mục tiêu, K05, phạm vi, tiêu chí pass/fail, kết luận | Tiến |
| Môi trường, cách chạy lại, pin phiên bản | Tuấn |
| Kiến trúc, phân tích nguyên nhân lỗi | Thuận |
| Schema, dữ liệu test, xác minh lỗi | Trung |
| Demo script automation, kết quả, thống kê, reproducer | Quang |

## 15. Dự phòng (cuối kỳ)

| Tình huống | Cách xử lý |
|---|---|
| Không tìm thấy lỗi nào | Nộp bằng chứng coverage: số operation đã chạy, số request, check đã bật, kết quả lặp lại |
| Quá nhiều lỗi giả do schema lệch hành vi | Phân loại riêng "lệch schema", ghi vào báo cáo như một phát hiện, không tính là lỗi server |
| Kết quả hai lần chạy khác nhau | Kiểm tra seed, reset DB, thứ tự chạy; ghi rõ nguồn không ổn định |
| Chạy chậm hoặc nhận 429 | Giảm tốc độ bằng `--rate-limit`; chia chạy theo object |
| Ngày bảo vệ đến sớm hơn dự kiến | Nén Sprint 6 và 7; bỏ SC6, SC7; giữ SC1 đến SC5 |
| Một thành viên vắng kéo dài | Báo Tiến; chia lại phần việc theo ma trận mục 13, ưu tiên phần có trong báo cáo A đến H |
| Lỗi môi trường khi demo | Chiếu video dự phòng của Tuấn |

---

## 16. Quy tắc làm việc (áp dụng cả hai mốc)

- Họp nhanh 15 phút mỗi tối lúc 21:00 qua nhóm chat trong tuần nước rút (16/10 đến 20/10). Sau giữa kỳ, họp nhóm mỗi tuần một lần và check-in ngắn qua chat các ngày còn lại.
- Vướng quá 1 giờ thì báo ngay vào nhóm chat, không chờ đến buổi họp.
- Mỗi người ít nhất 3 commit trước 20/10, sau đó giữ nhịp commit đều mỗi tuần (đề bài chấm lịch sử commit và sự tham gia đều; peer-review cuối kỳ dựa vào đây).
- Một thẻ chuyển cột mỗi ngày làm việc.
- Nhánh: `main` được bảo vệ; mỗi task một nhánh `feature/<ten>-<task>`; PR cần 1 người review.
- Commit: `feat(harness): ...`, `feat(scenario): ...`, `docs(setup): ...`, `fix: ...`.
- Hạn nộp là hạn riêng của từng người ở các mục trên. Trễ hạn thì báo Tiến trước khi hết hạn.
- Không `git pull` bản mới của Twenty; chỉ dùng `twenty/v2.45.6`.
- **Bảo mật:** `.env` nằm trong `.gitignore`, chỉ commit `.env.example`. Không gửi API key qua chat. Chỉ test trên `localhost`, không bắn vào hệ thống công khai.
