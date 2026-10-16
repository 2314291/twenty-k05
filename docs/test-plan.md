# Kế hoạch kiểm thử K05 (Báo cáo Phần D)

Người phụ trách: Tiến. Bản đầy đủ các bảng nằm trong `SPEC.md` (mục 3 đến 5); tệp này là bản trình bày cho báo cáo giữa kỳ.

## D.1. Nguyên lý

Schemathesis đọc OpenAPI và dùng Hypothesis (kiểm thử dựa trên thuộc tính) để sinh request **hợp lệ** và **không hợp lệ** cho từng operation,
gửi tới instance thật rồi kiểm các invariant: không 5xx, status nằm trong danh sách khai báo, Content-Type và body đúng schema, dữ liệu sai bị từ chối,
thiếu key bị chặn. Khi gặp lỗi, công cụ thu nhỏ ca lỗi và in lệnh tái hiện. Bộ test của nhóm bọc công cụ này bằng
`scripts/run_k05.py` (cấu hình từng kịch bản, chốt localhost, redact key) và `scripts/summarize.py` (thống kê, reproducer `curl`).

## D.2. Vì sao chọn phạm vi này

- API của Twenty sinh tự động từ mô hình dữ liệu từng workspace → nhiều operation cùng khuôn, dễ lệch khỏi schema → hợp với quét tự động.
- Năm đối tượng chuẩn (Companies, People, Opportunities, Notes, Tasks) phủ kiểu trường phức hợp, quan hệ, phân trang, batch mà không ôm cả hệ thống.
- Đã đọc mã nguồn (xem `architecture.md`) để biết trước các giới hạn: `limit` tối đa 200 (cắt âm thầm), batch tối đa 200, merge tối đa 9.

## D.3. Giả định

Twenty chạy local ở tag đã ghim, workspace test riêng, reset được; một key đầy đủ quyền và một key role chỉ đọc; không pull `main`;
**schema là nguồn chân lý** (hành vi lệch schema ghi là defect loại "lệch schema").

## D.4. Rủi ro và giảm thiểu

| Rủi ro | Giảm thiểu |
|---|---|
| Tải schema không có key → schema rỗng | `fetch_schema.py` cảnh báo khi 0 đường dẫn |
| `servers` của schema là `.../rest/` nhưng đường dẫn không có `/rest` | Runner truyền `--url <base>/rest` |
| Giới hạn tốc độ (429) | `--rate-limit auto` theo `Retry-After`; `--workers 1` |
| Schema không khớp hành vi thật (nhiều báo động giả) | Phân loại "lệch schema", kiểm chứng tay bằng reproducer trước khi gọi là defect |
| Fuzz `DELETE` hàng loạt xoá dữ liệu seed | Seed lại trước mỗi lần chạy |
| Lỗi nội bộ hiện thành 400 (H3) | Đọc thông điệp lỗi, không chỉ mã |
| Lộ API key | `.env` trong `.gitignore`; mọi báo cáo bị redact; thu hồi key nếu lỡ lộ |
| Test nhầm hệ thống công khai | Mọi script `assert_localhost` |

## D.5. Tiêu chí pass/fail

| Check | Pass khi | Fail (ghi defect) khi |
|---|---|---|
| `not_a_server_error` | Không 5xx | Có 5xx |
| `status_code_conformance` | Status nằm trong khai báo | Status ngoài khai báo |
| `content_type_conformance` | Đúng Content-Type | Khác |
| `response_schema_conformance` | Body đúng schema | Thiếu/thừa/sai kiểu |
| `negative_data_rejection` | Dữ liệu sai bị 4xx | Dữ liệu sai nhận 2xx |
| `positive_data_acceptance` | Dữ liệu đúng được nhận | Dữ liệu đúng bị từ chối |
| `ignored_auth` | Thiếu/sai key bị 401/403 | Truy cập được không cần key |

**Giữa kỳ (20/10):** SC1 chạy xong trên Companies có thống kê + ít nhất 1 reproducer + 1 ca đỏ cố ý.
**Cuối kỳ:** ≥80% operation trong phạm vi được chạy; mỗi operation ≥50 test case; chạy hai lần cùng cấu hình cho cùng kết quả; mỗi lỗi có reproducer và RCA; nếu không có lỗi thì nộp bằng chứng coverage.

## D.6. Giới hạn của K05

Không hiểu nghiệp vụ (sai logic mà đúng schema thì không phát hiện); chất lượng phụ thuộc độ chính xác của OpenAPI; request phụ thuộc dữ liệu cần chế độ stateful (SC6).

## D.7. Kịch bản và lịch

Xem `scenarios.md` (SC1 đến SC5, SC6/SC7 mở rộng) và `PHAN_CONG.md` (lịch hai mốc).
