# Kịch bản demo giữa kỳ 20/10 (khoảng 10–12 phút)

| Phút | Người nói | Nội dung | Chuẩn bị |
|---|---|---|---|
| 0–1 | Tiến | Giới thiệu nhóm, đề tài R10 + K05, phiên bản ghim | Slide 1–2 |
| 1–3 | Tuấn | Môi trường: `docker compose ps`, đăng nhập `http://localhost:3001` | Instance đang chạy, video dự phòng |
| 3–6 | Thuận | Kiến trúc: sơ đồ container/component, 2 phát hiện (limit 200, batch 200) | Slide 4–6 |
| 6–8 | Trung | 3 luồng nghiệp vụ + lấy OpenAPI kèm key (`fetch_schema.py`) | `business_flows.py` đã chạy thử |
| 8–11 | Quang | Thiết kế kịch bản: SC1–SC5, ca đỏ, bảng bất biến I1–I7, 31 ca biên | Slide đặc tả, `docs/dac-ta-*.md` |
| 11–12 | Tiến | Kế hoạch cuối kỳ, tiêu chí, câu hỏi | Slide cuối |

Dự phòng: instance sập → phát video.
Trước giờ demo: chạy lại `business_flows.py` một lần để chắc chắn hệ thống còn chạy; không hiển thị API key trên màn hình.
