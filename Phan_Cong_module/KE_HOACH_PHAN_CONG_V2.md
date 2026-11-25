# Kế hoạch phân công công việc cho 5 người (R10 Twenty + K05 Schema-Based API / Fuzz)

Cập nhật: 25/11/2026. Mô tả từng kịch bản ở `KICH_BAN_K05.md`; việc cụ thể của từng người ở `CHECKLIST_THANH_VIEN.md`.
 Twenty `v2.45.6` (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`), API `http://localhost:3001`, công cụ Schemathesis.
5 module (object): Companies, People, Opportunities, Notes, Tasks. Mỗi object có 13 operation, tổng 65.

Ngày bảo vệ (T) chưa biết. Hạn nộp báo cáo và mã là **T−7**.

## 1. Ai làm gì (tóm tắt)

| Người | Kiểm thử (kịch bản, module) | Phần báo cáo | Việc chung |
|---|---|---|---|
| **Quang** | SC1 (5 object), ca đỏ RED; khôi phục harness `run_k05.py`, chạy harness cho SC2 cùng Thuận | F (mã, README), G (số liệu, thống kê); E và RCA của SC1 | Giữ harness Schemathesis |
| **Thuận** | SC2 (5 object) | D (lý thuyết, phạm vi, tiêu chí pass/fail); E và RCA của SC2; gộp RCA xuyên module | Review và merge PR; gộp bảng lỗi |
| **Trung** (`hqt7105`) | SC3 (Companies đã xong, People, Opportunities); SC4 (Companies đã xong, Opportunities, Tasks); SC6 (5 object, đã chạy tay, còn mở rộng script) | E và RCA của SC3, SC4, SC6; ghép Phần E | Cấp key, seed, script chung |
| **Tiến** | SC3 (Notes, Tasks); SC4 (People, Notes), dùng script của Trung | A (hệ thống, actor, luồng dữ liệu), B (rà lại sơ đồ có sẵn); E và RCA phần mình chạy | Bảng Jira/Trello, hỏi thầy ngày T, ghép báo cáo, slide |
| **Tuấn** | SC5 (5 object, 4 loại key) | C (môi trường, 3 luồng nghiệp vụ F1 đến F3 chạy được), H (pin phiên bản, chạy lại trên máy mới); E và RCA của SC5 | `reset-env.sh`, video demo dự phòng |

Trung đã làm trên git: đặc tả SC3/SC4 và kết quả chạy trên Companies, chạy tay SC6 trên 5 object, dữ liệu SC5/SC6, 109 ca kiểm thử (PR #7 đến #12). Vì vậy Trung làm tiếp các phần đó.

So với bản trước:
- SC3 trên Notes và Tasks chuyển từ Trung sang Tiến, vì Trung đang gánh nhiều nhất và Tiến nhẹ nhất ở phần kiểm thử.
- Phần E và RCA do mỗi người viết cho kịch bản mình chạy; Trung ghép Phần E, Thuận gộp RCA.
- Phần A và B ở Tiến (đã chuyển từ Thuận ở bản trước).

## 2. Kế hoạch công việc

| Ai | Việc | Kết quả cần có |
|---|---|---|
| Cả nhóm | Chạy được Twenty `v2.45.6` trên máy mình, lấy được `GET /open-api/core` | Ảnh chụp hoặc log chạy thành công |
| Tiến | Hỏi thầy ngày T; lập bảng Jira/Trello/GitHub Projects theo mục 1 | Ngày T; bảng công việc |
| Thuận | Review rồi merge PR theo thứ tự #7, #10, #9, #8, #11, #12 | Nhánh chung có script, dữ liệu, ca kiểm thử của Trung |
| Quang | Khôi phục harness `run_k05.py` từ lịch sử git (trước commit `c5be360`) lên nhánh chung; mở rộng đặc tả SC1 từ Companies ra 5 object | `run_k05.py SC1` đến `SC5` chạy được |
| Trung | Tạo key role chỉ đọc; thêm tham số `--object` cho `kiem_thu_sc3_sc4_sc6.py`; hướng dẫn Tiến | Đủ 4 loại key cho Tuấn; script chạy từng object |
| Tuấn | Viết `reset-env.sh` (reset DB, seed bằng `scripts/seed.py`) | Một lệnh đưa DB về trạng thái ban đầu |
| Quang | SC1 trên 5 object; ca đỏ RED (đổi kiểu `CompanyForResponse.name` trong bản sao schema) | Kết quả, reproducer; I3 đỏ đúng chỗ |
| Thuận | SC2 trên 5 object (Quang hỗ trợ chạy harness) | Kết quả, reproducer |
| Trung | SC3 trên People, Opportunities; SC4 trên Opportunities, Tasks | Kết quả, reproducer |
| Tiến | SC3 trên Notes, Tasks; SC4 trên People, Notes | Kết quả, reproducer |
| Tuấn | SC5 với 4 loại key (đủ quyền, chỉ đọc, sai, không key) | Bảng mã trạng thái theo từng loại key |
| Cả nhóm | Chạy lại cùng seed để kiểm tra tái lập; đo số operation phủ được và số ca mỗi operation | Mỗi kịch bản đạt ngưỡng ở mục 3 |
| Trung | Mở rộng script SC6 cho 5 object | Script SC6 chạy 5 object |
| Mỗi người | Tái hiện từng lỗi bằng `curl`; phân loại "lệch schema" hoặc "lỗi chức năng"; viết RCA lỗi của kịch bản mình | Mỗi lỗi có reproducer và nguyên nhân |
| Thuận | Gộp lỗi thành một bảng, viết RCA xuyên module | Bảng lỗi; RCA tổng |
| Quang | Phần F, Phần G | F, G |
| Thuận | Phần D | D |
| Mỗi người | Phần E cho kịch bản mình chạy: input, điều kiện trước, kết quả mong đợi, dữ liệu test | E của từng kịch bản |
| Trung | Ghép các phần E thành Phần E hoàn chỉnh | E |
| Tiến | Phần A; Phần B (rà lại sơ đồ component và container có sẵn trong `docs/images/` cho khớp phần kiểm thử) | A, B |
| Tuấn | Phần C (tài liệu môi trường, chạy được 3 luồng F1 Tạo Company, F2 Tạo Person gắn Company, F3 Đổi stage Opportunity); Phần H; dựng lại thử trên máy sạch | C, H |
| Tiến | Ghép A đến H; kiểm tra tên, số liệu, tag, SHA khớp nhau | Báo cáo bản đầy đủ |
| Cả nhóm | Review chéo (mục 5); sửa theo góp ý | Báo cáo bản sửa |
| Tiến, Tuấn | Làm slide; Tuấn quay video demo dự phòng | Slide; video |
| Tiến | Hạn T−7: nộp báo cáo và mã | Đã nộp |
| Cả nhóm | Ngày T−3: tổng duyệt; tập demo chạy script bằng một lệnh | Demo chạy trơn tru |
| Cả nhóm | Ngày T: bảo vệ; mỗi người trình bày phần của mình; đánh giá chéo thành viên | Buổi bảo vệ |

Họp ngắn 15 phút (chat hoặc gọi): họp khởi động, rồi họp giữa mỗi giai đoạn và một buổi tổng duyệt trước T−3.

## 3. Đối chiếu yêu cầu của thầy

| Yêu cầu trong hướng dẫn | Ai lo | Ở đâu |
|---|---|---|
| Phần A: mục tiêu, actor, cây module, dependency, luồng dữ liệu | Tiến | `docs/architecture.md` |
| Phần B: ≥ 1 sơ đồ component/container, giải thích 3 đến 5 module | Tiến | `docs/images/` |
| Phần C: môi trường, lệnh build/run, seed, ≥ 3 luồng nghiệp vụ chạy được | Tuấn | `docs/SETUP.md`, `docs/business-flows.md` |
| Phần D: nguyên lý, phạm vi, giả định, rủi ro, tiêu chí pass/fail | Thuận | `docs/test-plan.md` |
| Phần E: kịch bản, input, điều kiện đầu, kỳ vọng/bất biến, dữ liệu test | Mỗi người, Trung ghép | `KICH_BAN_K05.md` |
| Phần F: mã test chạy lại tự động, README lệnh chạy và dependency | Quang | `scripts/`, `README.md` |
| Phần G: log, metrics, danh sách lỗi, RCA | Quang (số liệu), Thuận (lỗi, RCA) | `reports/` |
| Phần H: pin tag/SHA, cấu hình test, cách chạy lại trên máy mới | Tuấn | `env/VERSION.txt` |
| K05: chạy schema tests, lưu reproducer, thống kê lỗi | Cả nhóm | SC1 đến SC6 |
| Quản lý task (Jira/Trello/GitHub Projects) | Tiến | Bảng công việc |
| Dùng Git, commit đều (lịch sử commit được chấm) | Cả nhóm | Mục 7 |
| Nộp báo cáo trước bảo vệ 1 tuần (T−7) | Tiến | |
| Demo chạy script automation khi bảo vệ | Quang | |
| Đánh giá chéo (peer-review) | Cả nhóm | Mục 5 |

## 4. Khi nào coi một kịch bản là xong

- Mỗi object phủ ≥ 11/13 operation; mỗi operation ≥ 50 test case. Hai ngưỡng này do nhóm tự đặt trong `SPEC.md`, thầy không quy định.
- Có seed cố định và một lệnh chạy lại được cho kết quả tương tự.
- Mỗi lỗi có reproducer (`curl` hoặc ca Schemathesis), được phân loại, có nguyên nhân và ghi vào bảng lỗi.
- Kết quả đã commit lên nhánh của mình, PR được người khác review.

## 5. Review chéo

| Người review | Đọc phần của |
|---|---|
| Thuận | SC1 (Quang) |
| Trung | SC2 (Thuận) |
| Quang | SC3 (Trung, Tiến) |
| Tuấn | SC4 (Trung, Tiến) và SC6 (Trung) |
| Tiến | SC5 (Tuấn) |

Người review phải là người không chạy kịch bản đó.

## 6. Ai chờ ai

| Việc | Cần có trước | Do ai |
|---|---|---|
| Tuấn chạy SC5 | Key chỉ đọc, dữ liệu SC5 | Trung |
| Tiến chạy SC3, SC4 | Script có `--object` | Trung |
| Quang, Thuận, Tuấn chạy SC1, SC2, SC5 | Harness `run_k05.py` trên nhánh chung | Quang |
| Cả nhóm | PR #7 đến #12 đã merge | Thuận |
| Bảng lỗi và RCA tổng | Kết quả và RCA SC1 đến SC6 | Từng người |
| Ghép Phần E | E của từng kịch bản | Từng người |
| Ghép báo cáo | Phần A đến H | Từng người |

## 7. Quy tắc làm việc

- Mỗi người commit bằng đúng tài khoản git của mình, commit nhỏ và đều mỗi ngày (thầy chấm lịch sử commit).
- Không push thẳng `main`. Tên nhánh: `feat/<kịch bản>-<object>-<tên>`, ví dụ `feat/sc4-people-tien`.
- Mỗi PR cần ít nhất 1 người khác review rồi mới merge.
- Không commit key thật hay file `.env`.
- Giới hạn tốc độ là 100 request mỗi 60 giây cho mỗi key. Mỗi người dùng key riêng; nếu dùng chung một Twenty thì không chạy cùng lúc.
- Reset DB và seed lại trước mỗi lần chạy chính thức.
- Lỗi đánh một mã duy nhất: giữ D-xx, ghi mã G-xx cũ ở cột "mã cũ" (hiện D-01/G-04 là cùng một lỗi).

## 8. Rủi ro và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Trung vẫn quá tải (SC3, SC4, SC6, key, script, Phần E) | Sau lượt chạy đầu, nếu SC6 script chưa xong thì Tuấn (xong SC5) hoặc Quang (xong SC1) nhận SC6 trên Notes và Tasks |
| T đến sớm hơn dự kiến | Giữ SC1 đến SC3 trước, rồi SC4, SC5; cắt SC6 sau cùng |
| Tuấn bị chặn vì chưa có key | Trung cấp key trước khi bắt đầu chạy |
| Tiến bị chặn vì script chưa có `--object` | Trung làm `--object` đầu tiên, trước các việc khác |
| Harness của Quang chạy lỗi | Dùng tạm script của Trung cho Companies, sửa harness song song |
| Demo hỏng khi bảo vệ | Tuấn quay video dự phòng trước T−3 |
| Có người trễ hạn | Báo nhóm ngay trong ngày; Tiến chia lại việc |

## 9. Ai trình bày khi bảo vệ (đề xuất)

Tiến mở đầu và kiến trúc; Trung kịch bản và dữ liệu; Quang demo chạy script; Thuận lỗi và RCA; Tuấn môi trường và xác thực.
