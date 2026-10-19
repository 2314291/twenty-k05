# Báo cáo giữa kỳ 20/10/2026 — R10 Twenty + K05 (Schemathesis)

Nhóm: Tiến (trưởng nhóm), Tuấn, Thuận, Trung, Quang. Môn Kiểm thử phần mềm, ĐH Đà Lạt, GV Nguyễn Thế Lâm.
Phiên bản: `twenty/v2.45.6`, SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`.

> Cách đọc tài liệu này: mỗi phần có **Trạng thái**. `XONG` = đã có nội dung hoàn chỉnh trong repo. `CHỜ CHẠY THẬT` = mã/tài liệu đã sẵn,
> còn thiếu số liệu hoặc ảnh phải lấy từ instance Twenty đang chạy; chỗ trống ghi `[ĐIỀN]`. Không điền số liệu khi chưa chạy.

## A. Hệ thống

Trạng thái: **XONG** (đọc từ mã nguồn v2.45.6). Mục tiêu, actor, use case, cây `packages/`, phụ thuộc và 5 data flow: `docs/architecture.md` (A.1–A.4, C).

## B. Kiến trúc

Trạng thái: **XONG**. Sơ đồ container (server, worker, PostgreSQL, Redis, volume) và sơ đồ component tầng REST; 5 module liên quan test: `docs/architecture.md` (A.4, B.1, B.2). Phát hiện đáng chú ý ảnh hưởng thiết kế test:

| Mã | Phát hiện |
|---|---|
| H1 | `limit` tối đa 200; lớn hơn bị cắt về 200 không báo lỗi |
| H2 | Batch tối đa **200** (ghi chú cũ của nhóm nói 60) |
| H3 | Lỗi không phải `HttpException` bị đổi thành 400 |
| H4 | Có `PUT *path` không được tài liệu hóa trong OpenAPI |
| H5 | API key là JWT; key thu hồi/hết hạn → 403 |

## C. Môi trường và 3 luồng nghiệp vụ

Trạng thái: tài liệu **XONG**; bằng chứng **CHỜ CHẠY THẬT**.

- Cài đặt, biến môi trường, lệnh, sự cố: `docs/SETUP.md`; ghim phiên bản: `env/VERSION.txt`; Compose: `env/docker-compose.yml` (cổng 3001).
- 3 luồng (tạo Company; tạo Person gắn Company; đổi stage Opportunity): `docs/business-flows.md`, chạy bằng `python scripts/business_flows.py`.

| Bằng chứng | File | Có chưa |
|---|---|---|
| Instance chạy (`docker compose ps`) | `evidence/01-*.png` | [ĐIỀN] |
| Đăng nhập Twenty ở :3001 | `evidence/02-*.png` | [ĐIỀN] |
| Kết quả 3 luồng | `evidence/business-flows-20261016-213042.json` | Có (cả 3 luồng đạt, 16/10) |
| Video dự phòng 1–2 phút | `evidence/demo.mp4` | [ĐIỀN] |

## D. Kỹ thuật K05

Trạng thái: **XONG**. Nguyên lý, lý do chọn phạm vi, giả định, rủi ro, tiêu chí pass/fail, giới hạn: `docs/test-plan.md` (chi tiết ở `docs/SPEC.md`).

## E. Kịch bản

Trạng thái: **XONG** (SC1–SC5 có cấu hình chạy được); SC6, SC7 là mở rộng cuối kỳ. Xem `docs/scenarios.md`. Dữ liệu test: `scripts/seed.py`.

## F. Harness (báo trước cho cuối kỳ)

Trạng thái: **XONG phần khung, đã tự kiểm tra trên máy chủ giả** (không phải Twenty).

| Thành phần | Vai trò |
|---|---|
| `scripts/fetch_schema.py` | Tải OpenAPI kèm key, báo khi schema rỗng |
| `scripts/list_operations.py` | Đếm operation → mẫu số cho độ phủ |
| `scripts/run_k05.py` | Chạy SC1–SC5, chốt localhost, redact key |
| `scripts/summarize.py` | Thống kê theo operation/mã/check, reproducer `curl`, so sánh hai lần chạy |
| `scripts/probe_boundaries.py` | Ca biên có chủ đích (limit, batch, xác thực) |
| `scripts/make_red_case.py` | Ca đỏ cố ý |
| `scripts/selftest/` | Tự kiểm tra bằng máy chủ giả |

## G. Kết quả chạy thử (SC1 trên Companies)

Trạng thái: **ĐÃ CHẠY** SC1 hai lần (300 giây mỗi lần) và ca đỏ ngày 16/10:

| Chỉ số | Giá trị |
|---|---|
| Operation Companies trong schema / đã test | 13 / 13 |
| Tổng test case | 1248 (mỗi operation từ 64 đến 177) |
| Lỗi 5xx | 0 |
| Nhóm lỗi duy nhất | 52 (63 lỗi); check đỏ chính: `status_code_conformance` 283, `positive_data_acceptance` 276, `response_schema_conformance` 72 |
| Reproducer | `reports/SC1/20261016-213452-seed20261020/reproducers/*.sh` (52 file) |
| Lỗi ứng viên chính | D-01 `limit` cắt âm thầm; D-02 thiếu key trả 403; D-03 trường null khai báo không-null; D-04 groupBy trả mảng trần; D-05 `order_by` của groupBy; xem `docs/defects.md` |
| Ca đỏ cố ý (`--label RED`) | ĐÃ CHẠY 16/10 (120 giây, 779 case, 48 nhóm lỗi). Bản sao schema đổi `CompanyForResponse.name` từ string sang integer. Harness báo `response_schema_conformance` đỏ: `"" is not of type "integer"` tại `/components/schemas/CompanyForResponse/properties/name`, ở 4 operation (GET /companies, POST /companies, PATCH /companies, PATCH /companies/restore). Lần chạy gốc không có lỗi kiểu này (0 lần), nên lỗi do ca đỏ gây ra. Thư mục: `reports/SC1/20261016-215144-seed20261020-RED/` |
| Tái lập (2 lần SC1: `213452` và `220101`) | 50/52 nhóm lỗi trùng (96%), lần 2 không có nhóm mới. Lần 1: 1248 case, 52 nhóm; lần 2: 1257 case, 50 nhóm. Hai nhóm chỉ có ở lần 1 đều thuộc `GET /companies` (`missing_required_header`, `status_code_conformance`); lần 2 `GET /companies` chỉ chạy 72 case so với 81, nhiều khả năng do cắt theo thời gian 300 giây. Số test case lệch nhẹ vì giới hạn thời gian và dữ liệu trong workspace thay đổi giữa hai lần. Cuối kỳ cần chạy không cắt thời gian để so sánh chặt hơn |
| Thăm dò biên (31 ca) | MATCH 11, DIFF 4, OBSERVE 16 (`reports/probes/20261016-213052.md`) |
| D-07 (5 ca `negative_data_rejection`) | Đã mở từng request: 3/5 là `null` ở trường schema không khai báo nullable (gộp RCA với D-03), 1/5 là D-01, 1/5 chờ chạy lại trên dữ liệu có thật (`docs/defects.md`) |
| Lưu ý tính hợp lệ (R-01) | Request thứ 34 của SC1 (ví dụ `filter` của chính schema, `soft_delete=false`) **xoá vĩnh viễn 209 công ty**, gồm dữ liệu seed; phần còn lại của cả hai lần chạy diễn ra trên bảng gần rỗng. Các lỗi lệch schema vẫn đúng, nhưng độ tái lập 96% một phần do cả hai lần cùng chạy trên bảng rỗng. Đã sửa bằng hook bảo vệ dữ liệu và `--reset` (`hooks/k05_hooks.py`), cần chạy lại SC1 để có số liệu mới |

## H. Cấu hình và chạy lại

Trạng thái: **XONG**. `env/VERSION.txt`, `requirements.txt` (Schemathesis 4.31.1), `.env.example`, `README.md` mục "Chạy lại trên máy mới".

## Kế hoạch tới cuối kỳ

Mục tiêu ≥80% operation, ≥50 case/operation, 2 lần chạy cùng kết quả, mọi lỗi có reproducer + RCA, thêm SC6/SC7 nếu kịp: `docs/PHAN_CONG.md` (Mốc 2).
