# Phân công: mỗi người làm kịch bản (SC) nào, trên module (object) nào

Cập nhật: 25/11/2026. Đề tài R10 Twenty + K05 Schema-Based API / Fuzz. 5 module (object): Companies, People, Opportunities, Notes, Tasks.

## 1. Mỗi người làm gì

| Người | Kịch bản (SC) | Module (object) | Hỗ trợ |
|---|---|---|---|
| **Quang** | **SC1** quét 13 operation, dữ liệu hợp lệ; ca đỏ RED | Companies, People, Opportunities, Notes, Tasks | Khôi phục harness `run_k05.py`; hỗ trợ Thuận, Tuấn chạy bằng harness |
| **Thuận** | **SC2** dữ liệu sai | Companies, People, Opportunities, Notes, Tasks | Gộp bảng lỗi của cả nhóm |
| **Trung** | **SC3** phân trang, lọc, sắp xếp | Companies (đã xong), People, Opportunities | |
| | **SC4** batch 0/1/61/200/201 | Companies (đã xong), Opportunities, Tasks | Giao script `--object` cho Tiến |
| | **SC6** chuỗi vòng đời | Companies, People, Opportunities, Notes, Tasks (đã xong tay; còn mở rộng script) | |
| **Tiến** | **SC3** phân trang, lọc, sắp xếp | Notes, Tasks | Dùng script của Trung |
| | **SC4** batch | People, Notes | Dùng script của Trung |
| **Tuấn** | **SC5** xác thực 4 loại key | Companies, People, Opportunities, Notes, Tasks | Trung cấp key chỉ đọc và dữ liệu |

Mỗi người tự tái hiện lỗi mình tìm được bằng `curl`, phân loại "lệch schema" hoặc "lỗi chức năng", viết nguyên nhân, rồi gửi Thuận gộp.

## 2. Đã có trên git

| Kịch bản | Có trên git | Ở đâu |
|---|---|---|
| SC1, SC2, ca đỏ | Đặc tả (Quang); harness và kết quả SC1 trên Companies | Đặc tả trên main; harness còn trong lịch sử git |
| SC3 | Đặc tả; chạy tay và script trên Companies (Trung) | Đặc tả trên main; kết quả ở PR #8, #9, #12 |
| SC4 | Đặc tả; chạy tay và script trên Companies (Trung) | Đặc tả trên main; kết quả ở PR #8, #9, #12 |
| SC5 | Ca P5 (Quang); dữ liệu SC5 (Trung); ảnh xác thực tay 08 (Tuấn). Chưa chạy | Main, PR #11 |
| SC6 | Đặc tả S6-01 đến S6-13; chạy tay trên 5 object; script chỉ Companies (Trung) | PR #9, #11, #12 |

## 3. Tài liệu liên quan

- `KE_HOACH_PHAN_CONG_V2.md`: kế hoạch công việc, phần báo cáo của từng người, đối chiếu yêu cầu của thầy, review chéo, rủi ro.
- `CHECKLIST_THANH_VIEN.md`: việc cụ thể của từng người.
- `KICH_BAN_K05.md`: mô tả chi tiết từng kịch bản SC1 đến SC6.
