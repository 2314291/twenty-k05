# Kịch bản K05 chi tiết (Báo cáo Phần E)

Người phụ trách: Quang (kèm Trung về dữ liệu). Bảng tổng quan nằm ở `SPEC.md` mục 4; tệp này mô tả cách mỗi kịch bản được
cấu hình và chạy. Mọi lệnh chạy qua `python scripts/run_k05.py <SC>`; tham số `st run` đã đối chiếu với Schemathesis 4.31.1.

## Quy ước

- Base: `--url http://localhost:3001/rest` (các đường dẫn trong schema không có `/rest`).
- Xác thực: `Authorization: Bearer $TWENTY_API_KEY` (đọc từ `.env`, bị redact khỏi mọi file trong `reports/`).
- Mỗi lần chạy sinh thư mục `reports/<SC>/<thời-điểm>-seed<N>[-nhãn]/` gồm `st-output.txt`, `json-*.json`, `ndjson-*.ndjson`,
  `junit-*.xml`, `html-*/`, **`summary.md`**, `summary.json`, `REPRODUCERS.md`, `reproducers/*.sh`.
- Tái lập: `--generation-deterministic` (loại bỏ ngẫu nhiên); kiểm tra bằng `python scripts/summarize.py --compare <A> <B>`.
  (Ở chế độ này Schemathesis in "Seed: not used"; vẫn truyền `--seed` để ghi lại.)
- Trước mỗi lần chạy: thêm `--reset` (runner tự gọi `seed.py --cleanup` rồi `seed.py --count 30`) để dữ liệu giống nhau.
- Hook `hooks/k05_hooks.py` được nạp mặc định (biến `SCHEMATHESIS_HOOKS`):
  - **Bảo vệ dữ liệu:** `DELETE`/`PATCH /{đối tượng}` (ghi hàng loạt theo filter) bị bọc filter thành
    `and(<filter gốc>,createdAt[gte]:"<mốc bắt đầu>")`, chỉ chạm bản ghi tạo trong lần chạy. Lý do: lần SC1 16/10 tự xoá sạch Companies (`docs/defects.md` R-01). Tắt: `--no-protect`.
  - **Id có thật:** ca dương của `GET`/`PATCH /{đối tượng}/{id}` và `.../{id}/restore` dùng id trong `reports/seed-manifest.json` thay vì UUID ngẫu nhiên (giảm 404). `DELETE .../{id}` và ca âm giữ nguyên. Tắt: `--no-real-ids`. Tắt cả hai: `--no-hooks`.
- Mỗi thư mục kết quả có thêm `run-config.json` (kịch bản, đối tượng, regex, seed, mốc thời gian, số bản ghi seed, hook bật/tắt) để báo cáo Phần H và để so sánh hai lần chạy.
- Chia nhỏ theo đối tượng (tránh 429, dễ so sánh): `--object companies|people|opportunities|notes|tasks` dùng được cho mọi kịch bản.

## SC1 — Quét Companies với dữ liệu theo schema (PoC giữa kỳ)

| Mục | Nội dung |
|---|---|
| Lệnh | `python scripts/run_k05.py SC1 --reset` (Companies); đối tượng khác: `--object people` (tương tự opportunities, notes, tasks) |
| Phạm vi | Đường dẫn khớp `^/(batch/)?<đối tượng>(/\|$)`: list, create, get, update, delete, batch, duplicates, restore, merge, groupBy (13 operation mỗi đối tượng) |
| Precondition | Instance chạy; key đầy đủ quyền; đã seed |
| Check | `all` (gồm 7 check của SPEC mục 5.4 và các check phụ) |
| Phase / mode | `examples,coverage,fuzzing` / `all` (cả dữ liệu đúng và sai) / 50 ví dụ mỗi operation |
| Invariant | Không 5xx; status và body đúng schema; dữ liệu sai bị 4xx |
| Đầu ra | `summary.md` (số operation, số request, lỗi theo check và theo operation), reproducer `.sh` cho từng lỗi |
| Giới hạn | Hook chỉ gắn id có thật ở phase coverage/fuzzing (phase examples dùng nguyên ví dụ của schema); `notes`, `tasks` chưa có trong `seed.py` nên vẫn 404 nhiều → SC6 hoặc mở rộng seed (Trung) |
| Sprint 3 (chạy trên 5 đối tượng) | `for o in companies people opportunities notes tasks; do python scripts/run_k05.py SC1 --object $o --reset; done` |

**Ca đỏ cố ý (chứng minh công cụ bắt được lỗi):**
```bash
python scripts/make_red_case.py          # đổi CompanyForResponse.name từ string sang integer, ghi schema/core.red.openapi.json
python scripts/run_k05.py SC1 --schema schema/core.red.openapi.json --label RED
```
Kỳ vọng: `response_schema_conformance` đỏ (phản hồi thật trả chuỗi, schema nói số nguyên). Không sửa file schema gốc. Ghi trong báo cáo: trường đã đổi, check bị đỏ, đường dẫn reproducer.

## SC2 — Dữ liệu sai (negative)

Lệnh `python scripts/run_k05.py SC2`. Phạm vi 5 đối tượng (companies, people, opportunities, notes, tasks). Chế độ `negative`, phase
`coverage,fuzzing`. Check: `negative_data_rejection`, `not_a_server_error`, `status_code_conformance`, `response_schema_conformance`.
Invariant: input sai schema → 4xx, không 2xx, không 5xx. Lưu ý H3: lỗi nội bộ có thể hiện thành 400, nên với mỗi 400 khả nghi hãy đọc `message`.

## SC3 — Phân trang / lọc / sắp xếp

Lệnh: `python scripts/run_k05.py SC3` (chỉ GET danh sách) **và** `python scripts/probe_boundaries.py --only sc3`.
Probe gọi trực tiếp các biên mà Schemathesis không chắc chạm: `limit` = 0, 1, 60, 200, 201, 100000, −1, `abc`, 1.5, rỗng;
`starting_after`/`ending_before` rác; `order_by`/`filter` sai; `depth=99`; id không phải UUID; UUID không tồn tại.
Kỳ vọng rút ra từ mã nguồn: −1 và `abc` → 400; 201 → bị cắt về 200 không lỗi (H1, ghi là OBSERVE).

## SC4 — Batch

Lệnh: `python scripts/run_k05.py SC4` **và** `python scripts/probe_boundaries.py --only sc4`.
Probe: mảng 0, 1, 200, 201 phần tử, 61 (đối chiếu ghi chú "60"), body là object, phần tử sai, JSON hỏng.
Kỳ vọng: 200 nhận; 201 → 4xx với thông điệp "Maximum number of records to upsert is 200". Probe tự xoá bản ghi tạo ra.

## SC5 — Xác thực

Lệnh:
```bash
python scripts/run_k05.py SC5 --variant none      # không gửi key
python scripts/run_k05.py SC5 --variant wrong     # key sai
python scripts/run_k05.py SC5 --variant limited   # key role chỉ đọc (cần TWENTY_API_KEY_LIMITED)
python scripts/probe_boundaries.py --only sc5
```
Check: `ignored_auth`, `not_a_server_error`, `status_code_conformance`. Invariant: thiếu/sai key → 401 (key thu hồi/hết hạn → 403, H5);
key chỉ đọc không ghi được (403). Chú ý: với `none`/`wrong` gần như mọi phản hồi là 401, Schemathesis sẽ cảnh báo "Authentication failed" — **đó là kết quả mong đợi**, không phải lỗi môi trường.

## SC6, SC7 (mở rộng, cuối kỳ nếu kịp)

SC6 chuỗi create → get → update → delete → get(404) bằng chế độ stateful (`--phases stateful`, cần các link trong schema) hoặc script chuỗi.
SC7 GraphQL: lấy schema từ instance đang chạy rồi chạy `st run <url>/graphql`. Chưa có mã trong mốc 1.
