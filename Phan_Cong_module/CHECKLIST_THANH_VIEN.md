# Checklist công việc từng thành viên (R10 Twenty + K05 Schema-Based API / Fuzz)

Cập nhật: 25/11/2026. Dựa trên `KE_HOACH_PHAN_CONG_V2.md`; chi tiết từng kịch bản ở `KICH_BAN_K05.md`. Tick `[x]` khi xong. Ngày bảo vệ (T) chưa biết, hạn nộp báo cáo và mã là T−7.

## Chung cho cả nhóm

- [ ] Chạy được Twenty `v2.45.6` trên máy mình (`http://localhost:3001`) và lấy được `GET /open-api/core`
- [ ] Commit bằng đúng tài khoản git của mình, commit nhỏ và đều mỗi ngày
- [ ] Không push thẳng `main`; nhánh đặt tên `feat/<kịch bản>-<object>-<tên>`
- [ ] Mỗi PR có ít nhất 1 người khác review rồi mới merge
- [ ] Không commit key thật hay file `.env`
- [ ] Reset DB và seed lại trước mỗi lần chạy chính thức
- [ ] Mỗi lỗi: có reproducer (`curl` hoặc ca Schemathesis), được phân loại "lệch schema" hoặc "lỗi chức năng", có nguyên nhân

**Một kịch bản coi là xong khi:** mỗi object phủ ≥ 11/13 operation, mỗi operation ≥ 50 ca (ngưỡng nhóm tự đặt, thầy không quy định); có seed cố định và lệnh chạy lại được; kết quả đã commit và PR được người khác review.

---

## Trung (`hqt7105`): SC3, SC4, SC6, Phần E

Làm hai việc đầu trước vì đang chặn người khác.

- [ ] Tạo key role chỉ đọc, đưa cho Tuấn cùng dữ liệu SC5
- [ ] Thêm tham số `--object` cho `kiem_thu_sc3_sc4_sc6.py`, hướng dẫn Tiến chạy
- [ ] SC3 (phân trang, lọc, sắp xếp) trên People
- [ ] SC3 trên Opportunities
- [ ] SC4 (batch 0/1/61/200/201) trên Opportunities
- [ ] SC4 trên Tasks
- [ ] Nhờ merge PR #11 để đặc tả SC6 (ca S6-01 đến S6-13) lên main
- [ ] Mở rộng script SC6 (chuỗi vòng đời tạo, đọc, sửa, xóa, khôi phục) cho cả 5 object
- [ ] Chạy lại cùng seed, kiểm tra kết quả giống nhau và đủ ngưỡng
- [ ] Viết reproducer, phân loại, nguyên nhân lỗi của SC3, SC4, SC6
- [ ] Viết Phần E cho SC3, SC4, SC6 (input, điều kiện trước, kết quả mong đợi, dữ liệu test)
- [ ] Ghép Phần E của mọi người thành một phần hoàn chỉnh
- [ ] Review chéo: đọc SC2 của Thuận
- [ ] Nhắc Thuận review và merge PR #7 đến #12
- [ ] Bảo vệ: trình bày kịch bản và dữ liệu

## Quang: SC1, Phần F, Phần G

- [ ] Khôi phục harness `run_k05.py` từ lịch sử git (trước commit `c5be360`) lên nhánh chung; chạy được `SC1`, `SC2`, `SC5` (việc này chặn Thuận và Tuấn, làm đầu tiên)
- [ ] Mở rộng đặc tả SC1 trong `dac-ta-sc1-sc2-red.md` từ Companies ra 5 object
- [ ] SC1 (quét 13 operation, dữ liệu hợp lệ) trên Companies
- [ ] SC1 trên People
- [ ] SC1 trên Opportunities
- [ ] SC1 trên Notes
- [ ] SC1 trên Tasks
- [ ] Ca đỏ RED: bản sao schema đổi `CompanyForResponse.name` sang `integer`, chạy SC1, I3 phải đỏ đúng chỗ
- [ ] Hỗ trợ Thuận chạy SC2 bằng harness
- [ ] Chạy lại cùng seed, kiểm tra kết quả giống nhau và đủ ngưỡng
- [ ] Viết reproducer, phân loại, nguyên nhân lỗi của SC1
- [ ] Viết Phần E cho SC1
- [ ] Phần F: mã test và harness chạy lại tự động; README ghi lệnh chạy và dependency
- [ ] Phần G: log, số liệu, danh sách lỗi; thống kê theo loại kiểm tra và theo object
- [ ] Review chéo: đọc SC3 của Trung và Tiến
- [ ] Bảo vệ: demo chạy script

## Thuận: SC2, Phần D, bảng lỗi và RCA

- [ ] Review rồi merge PR theo thứ tự #7, #10, #9, #8, #11, #12
- [ ] Nhận harness `run_k05.py` từ Quang
- [ ] SC2 (dữ liệu sai) trên Companies
- [ ] SC2 trên People
- [ ] SC2 trên Opportunities
- [ ] SC2 trên Notes
- [ ] SC2 trên Tasks
- [ ] Chạy lại cùng seed, kiểm tra kết quả giống nhau và đủ ngưỡng
- [ ] Viết reproducer, phân loại, nguyên nhân lỗi của SC2
- [ ] Viết Phần E cho SC2
- [ ] Gộp lỗi của mọi người thành một bảng: mỗi lỗi một mã D-xx, ghi mã G-xx cũ ở cột "mã cũ"
- [ ] Viết RCA xuyên module
- [ ] Phần D: nguyên lý kỹ thuật, lý do chọn phạm vi, giả định, rủi ro, tiêu chí pass/fail
- [ ] Review chéo: đọc SC1 của Quang
- [ ] Bảo vệ: trình bày lỗi và RCA

## Tiến: SC3 (Notes, Tasks), SC4 (People, Notes), Phần A, B, ghép báo cáo

- [ ] Hỏi thầy ngày bảo vệ (T), báo cho nhóm
- [ ] Lập bảng Jira/Trello/GitHub Projects theo bảng phân công
- [ ] Nhận hướng dẫn `--object` từ Trung
- [ ] SC3 trên Notes
- [ ] SC3 trên Tasks
- [ ] SC4 trên People
- [ ] SC4 trên Notes
- [ ] Chạy lại cùng seed, kiểm tra kết quả giống nhau và đủ ngưỡng
- [ ] Viết reproducer, phân loại, nguyên nhân lỗi phần mình chạy
- [ ] Viết Phần E cho phần mình chạy, gửi Trung ghép
- [ ] Phần A: mục tiêu hệ thống, actor và use case, cây thư mục và module, dependency, luồng dữ liệu
- [ ] Phần B: rà lại sơ đồ component và container có sẵn trong `docs/images/` cho khớp phần kiểm thử; giải thích 3 đến 5 module liên quan
- [ ] Ghép Phần A đến H; kiểm tra tên, số liệu, tag, SHA khớp nhau
- [ ] Làm slide (cùng Tuấn)
- [ ] Nộp báo cáo và mã đúng hạn T−7
- [ ] Review chéo: đọc SC5 của Tuấn
- [ ] Bảo vệ: mở đầu và trình bày kiến trúc

## Tuấn: SC5, Phần C, Phần H

- [ ] Viết `reset-env.sh`: một lệnh reset DB và seed bằng `scripts/seed.py`
- [ ] Nhận key role chỉ đọc và dữ liệu SC5 từ Trung; nhận harness `run_k05.py` từ Quang
- [ ] SC5 (xác thực, 4 loại key: đủ quyền, chỉ đọc, sai, không key) trên Companies
- [ ] SC5 trên People
- [ ] SC5 trên Opportunities
- [ ] SC5 trên Notes
- [ ] SC5 trên Tasks
- [ ] Chạy ca biên tay P5-01 đến P5-08
- [ ] Lập bảng mã trạng thái theo từng loại key
- [ ] Chạy lại cùng seed, kiểm tra kết quả giống nhau và đủ ngưỡng
- [ ] Viết reproducer, phân loại, nguyên nhân lỗi của SC5
- [ ] Viết Phần E cho SC5
- [ ] Phần C: tài liệu môi trường, phiên bản, lệnh build và run, DB và service, seed data
- [ ] Phần C: chạy được 3 luồng F1 (tạo Company), F2 (tạo Person gắn Company), F3 (đổi stage Opportunity), có bằng chứng
- [ ] Phần H: ghi cố định tag và SHA, lưu cấu hình test, mô tả cách chạy lại
- [ ] Dựng lại thử toàn bộ trên máy sạch
- [ ] Làm slide (cùng Tiến)
- [ ] Quay video demo dự phòng trước ngày tổng duyệt (T−3)
- [ ] Review chéo: đọc SC4 và SC6
- [ ] Bảo vệ: trình bày môi trường và xác thực

---

## Mốc chung

- [ ] PR #7 đến #12 đã merge vào main
- [ ] Kết quả SC1 đến SC6 đã có, bảng lỗi và RCA tổng đã xong
- [ ] Phần A đến H đã ghép, đã review chéo và sửa
- [ ] Đã nộp báo cáo và mã (T−7)
- [ ] Đã tổng duyệt, demo chạy script bằng một lệnh (T−3)
- [ ] Đã bảo vệ và đánh giá chéo thành viên (T)
