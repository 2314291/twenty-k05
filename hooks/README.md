# hooks/

Hook Schemathesis của bộ K05. `scripts/run_k05.py` tự nạp `k05_hooks.py` qua biến `SCHEMATHESIS_HOOKS`
(tắt bằng `--no-hooks`). Tên hook, chữ ký và phase áp dụng đã đối chiếu với mã nguồn Schemathesis 4.31.1.

| Hook | Phase | Việc | Tắt bằng |
|---|---|---|---|
| `before_call` | mọi phase (kể cả examples) | `DELETE`/`PATCH /{đối tượng}`: bọc filter thành `and(<filter gốc>,createdAt[gte]:"<K05_RUN_START>")`, chỉ chạm bản ghi tạo trong lần chạy | `--no-protect` (`K05_PROTECT_DATA=0`) |
| `map_case` | coverage, fuzzing, stateful | Ca dương có `{id}` là UUID hợp lệ (trừ `DELETE`): thay bằng id trong `reports/seed-manifest.json`, ánh xạ tất định | `--no-real-ids` (`K05_REAL_IDS=0`) |

Vì sao cần: `docs/defects.md` mục R-01 (ca ví dụ của schema xoá vĩnh viễn 209 công ty ở lần SC1 ngày 16/10).
Request sau khi hook sửa là request thật sự được gửi, nên reproducer trong `reports/` chạy lại được mà không cần hook.

Chạy tay với `st`:

```bash
SCHEMATHESIS_HOOKS=hooks/k05_hooks.py K05_RUN_START=2026-10-19T14:00:00.000Z st run schema/core.openapi.json --url http://localhost:3001/rest ...
```

Kiểm tra logic hook (không cần Schemathesis hay Twenty): `python scripts/selftest/test_hooks.py`.
