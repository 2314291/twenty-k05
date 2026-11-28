# hooks/

Hook Schemathesis của bộ K05. `scripts/run_k05.py` tự nạp `k05_hooks.py` qua biến `SCHEMATHESIS_HOOKS`
(tắt bằng `--no-hooks`). Tên hook, chữ ký và phase áp dụng đã đối chiếu với mã nguồn Schemathesis 4.31.1.

| Hook | Phase | Việc | Tắt bằng |
|---|---|---|---|
| `before_call` | mọi phase (kể cả examples và ca "phương thức không khai báo" của `unsupported_method`) | Mọi request Twenty hiểu thành ghi hàng loạt theo filter: `DELETE`, `PATCH`, `PUT` tới `/{đối tượng}`, `/batch/{đối tượng}`, `/{đối tượng}/groupBy`, `/{đối tượng}/duplicates`, `/{đối tượng}/merge` (trừ `PATCH …/merge`, route gộp riêng). Filter bị bọc thành `and(<filter gốc>,createdAt[gte]:"<K05_RUN_START>")` (thêm mới nếu thiếu), chỉ chạm bản ghi tạo trong lần chạy | `--no-protect` (`K05_PROTECT_DATA=0`) |
| `before_call` | mọi phase | `DELETE /{đối tượng}/{id}` và `PATCH /{đối tượng}/merge` trỏ tới id seed: đổi sang UUID không tồn tại (tất định), để bản ghi seed không bị xoá hay gộp mất | `--no-protect` |
| `map_case` | coverage, fuzzing, stateful | Ca dương có `{id}` là UUID hợp lệ (trừ `DELETE`): thay bằng id trong `reports/seed-manifest.json`, ánh xạ tất định | `--no-real-ids` (`K05_REAL_IDS=0`) |

Vì sao cần: ca ví dụ `filter` của schema kèm `soft_delete=false` đã xoá vĩnh viễn 209 công ty ở lần SC1 ngày 16/10; SC2 ngày 26/11 còn mất 6/30 task seed vì đồng hồ container Docker đi trước Windows; SC1 ngày 27/11 check `unsupported_method` gửi `DELETE /{đối tượng}/groupBy` kèm `filter=createdAt[gte]:"2023-01-01"`, Twenty bỏ qua chữ `groupBy` với mọi phương thức (`parse-core-path.utils.ts:42-47`, lỗi D-11) nên xoá cứng sạch cả 5 object, trong khi bản hook cũ chỉ khớp đúng `/{đối tượng}`. Danh sách đường dẫn và phương thức ở trên lấy từ mã nguồn Twenty v2.45.6 (`parse-core-path.utils.ts:34-48`, `rest-api-core.controller.ts`, `rest-api-core.service.ts:56-94`). Vì vậy `run_k05.py` đặt `K05_RUN_START` = max(giờ máy + 1 giây, `createdAt` mới nhất trong DB + 1 ms) và ghi nguồn mốc vào `run-config.json`. Chi tiết: `docs/dac-ta-sc1-sc2-red.md` mục 2.
Request sau khi hook sửa là request thật sự được gửi, nên reproducer trong `reports/` chạy lại được mà không cần hook.

Chạy tay với `st`:

```bash
SCHEMATHESIS_HOOKS=hooks/k05_hooks.py K05_RUN_START=2026-10-19T14:00:00.000Z st run schema/core.openapi.json --url http://localhost:3001/rest ...
```

Kiểm tra logic hook (không cần Schemathesis hay Twenty): `python scripts/selftest/test_hooks.py`.

Lưới an toàn thứ hai: sau mỗi lần chạy, `run_k05.py` đếm lại bản ghi seed (`GET /{đối tượng}?filter=id[in]:[…]`) và ghi `seed_after`, `seed_lost` vào `run-config.json`. Mất seed thì in cảnh báo lớn và `thong_ke.py` loại lần chạy đó khỏi thống kê.
