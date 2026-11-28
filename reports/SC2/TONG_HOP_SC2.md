# Tổng hợp SC2 (dữ liệu sai) trên 5 object: chạy thử 26/11/2026 và chạy chính thức 28/11/2026

Người chạy: Thuận (máy Thuận). Harness: `run_k05.py` nhánh `backup/quang-harness-hooks` (commit `d26d813`, trước khi harness lên `develop` ở PR #20), Schemathesis 4.31.1, seed 20261020,
`--mode negative --phases coverage,fuzzing --max-examples 50`, `--reset` trước mỗi object.
Các vấn đề A–F đã kiểm chứng tay bằng `curl` (file `KIEM_CHUNG_*.md` trong thư mục này) và đã có mã trong `reports/bang-loi.md`.
Thư mục kết quả không kèm file `.ndjson` (bản ghi thô, khoảng 53 MB) để repo nhẹ; báo cáo HTML, JSON, JUnit, `summary.md` và reproducer vẫn đủ.

## Số liệu

| Object | Operation | Test case | 5xx | Operation < 50 ca | Thư mục |
|---|---|---|---|---|---|
| Companies | 13/13 | 1801 | 0 | `DELETE /{id}` (17) | `20261126-105625-seed20261020-companies` |
| People | 13/13 | 1862 | 0 | `DELETE /{id}` (18) | `20261126-110828-seed20261020-people` |
| Opportunities | 13/13 | 1338 | 0 | `DELETE /{id}` (14) | `20261126-111239-seed20261020-opportunities` |
| Notes | 13/13 | 1195 | 0 | `DELETE /{id}` (21) | `20261126-111735-seed20261020-notes` |
| Tasks | 13/13 | 1282 | 0 | `DELETE /{id}` (18) | `20261126-112206-seed20261020-tasks` |
| **Tổng** | **65/65** | **7478** | **0** | 5 operation | |

## Ứng viên lỗi (gom theo nguyên nhân)

| # | Vấn đề | Check | Object bị | Phân loại | Module code | Mã lỗi | Kiểm chứng |
|---|---|---|---|---|---|---|---|
| A | Tham số boolean `soft_delete`, `upsert` nhận số/chuỗi/null mà không báo lỗi (2xx thay vì 400) | negative_data_rejection | cả 5 | Lỗi chức năng | `input-request-parsers` | D-07 | `KIEM_CHUNG_A.md` |
| B | `limit` > 200 được chấp nhận (H1: cắt âm thầm về 200) | negative_data_rejection | cả 5 | Lệch schema (schema ghi `maximum 200`) | `input-request-parsers` | D-01; kèm D-08 (`limit` thập phân) | `KIEM_CHUNG_B.md` |
| C | Response có `null` ở trường schema khai báo không-null (vd `addressLat`, `avatarFile`) | response_schema_conformance | cả 5 | Lệch schema (thiếu `nullable`) | `open-api` (sinh schema) | D-09 | `KIEM_CHUNG_C.md` |
| D | Thiếu key → 403 `Missing authentication token`, schema chỉ khai 401 | status_code_conformance | cả 5, mọi operation | Lệch schema (trùng phạm vi SC5) | `auth` / `open-api` | D-02 | SC5 (Tuấn), `docs/dac-ta-sc5.md` |
| E | `groupBy`: trả 400 không khai báo (schema chỉ có 200); body 200 là mảng, schema khai object | status_code + response_schema | cả 5 | Lệch schema | `open-api` | D-10 | `KIEM_CHUNG_E_F.md` |
| F | Operation theo `{id}` trả 404 không khai báo (schema chỉ 200/400/401) | status_code_conformance | cả 5 | Lệch schema | `open-api` | D-03 (G-07) | `KIEM_CHUNG_E_F.md` |

## Tái lập (lần 2, cùng seed 20261020, `--reset` trước mỗi object)

`python scripts/summarize.py --compare <lần 1> <lần 2>` (cần `PYTHONUTF8=1` trên Windows):

| Object | Test case lần 1 / lần 2 | Nhóm lỗi lần 1 / lần 2 | Trùng | Thư mục lần 2 |
|---|---|---|---|---|
| Companies | 1801 / 1801 | 22 / 22 | 100% | `20261126-195126-seed20261020-companies` |
| People | 1862 / 1862 | 23 / 23 | 100% | `20261126-195519-seed20261020-people` |
| Opportunities | 1338 / 1338 | 19 / 19 | 100% | `20261126-200024-seed20261020-opportunities` |
| Notes | 1195 / 1195 | 26 / 26 | 100% | `20261126-200521-seed20261020-notes` |
| Tasks | 1282 / 1282 | 26 / 26 | 100% | `20261126-200951-seed20261020-tasks` |

Kết luận: **tái lập được** ở cả 5 object. Riêng People, dòng "unique failures" của Schemathesis là 52 (lần 1) và 54 (lần 2), do khác biệt nhỏ trong nội dung thông điệp; các nhóm lỗi (operation × check × loại) vẫn trùng 100%.

## Lần chạy chính thức 28/11/2026 (harness trên `develop`)

Người chạy: Thuận (máy Thuận). Nhánh `feat/sc2-ket-qua-thuan` = `develop` (`426dc69`, có harness PR #20: hook chặn ghi qua `/groupBy`, `/duplicates`, `/merge`, không để xoá hay gộp bản ghi seed) + commit tài liệu.
Lệnh: `python scripts/run_k05.py SC2 --object all --reset`, chạy 2 lần liên tiếp (lần 1 từ 19:42, lần 2 từ 20:06). Cấu hình giống lần 26/11.

| Object | Operation | Test case lần 1 / lần 2 | 5xx | Nhóm lỗi lần 1 / lần 2 | Trùng | `DELETE /{id}` lần 1 / lần 2 | Thư mục lần 1 · lần 2 |
|---|---|---|---|---|---|---|---|
| Companies | 13/13 | 1845 / 1817 | 0 | 22 / 22 | 100% | 61 / 33 | `20261128-194232-…` · `20261128-200642-…` |
| People | 13/13 | 1871 / 1871 | 0 | 22 / 22 | 100% | 27 / 27 | `20261128-194709-…` · `20261128-201139-…` |
| Opportunities | 13/13 | 1385 / 1385 | 0 | 19 / 19 | 100% | 61 / 61 | `20261128-195210-…` · `20261128-201647-…` |
| Notes | 13/13 | 1197 / 1201 | 0 | 24 / 24 | 100% | 23 / 27 | `20261128-195715-…` · `20261128-202148-…` |
| Tasks | 13/13 | 1325 / 1325 | 0 | 24 / 24 | 100% | 61 / 61 | `20261128-200146-…` · `20261128-202623-…` |
| **Tổng** | **65/65** | **7623 / 7599** | **0** | **111 / 111** | **100%** | | |

- **Tái lập:** `summarize.py --compare` cho trùng 100% nhóm lỗi ở cả 5 object. 12/13 operation mỗi object có số ca giống hệt giữa hai lần và giống lần 26/11.
- **Chỉ `DELETE /{id}` đổi số ca.** Ở phase fuzzing, Schemathesis dùng lại id xuất hiện trong response trước đó; hook mới cho `GET /{id}` đọc bản ghi seed thật, nên `DELETE /{id}` có thêm id seed để thử. Hook đổi các id seed này thành id giả trước khi gửi (Tasks lần 2: 23/50 ca fuzzing nhắm id seed, đều bị đổi, trả 400/404). Id seed đổi sau mỗi `--reset`, nên số ca của operation này thay đổi giữa các lần (23–61). Các operation còn lại không phụ thuộc vào đó.
- **Ngưỡng 50 ca:** `DELETE /{id}` đạt ≥ 50 ở Opportunities, Tasks (cả hai lần) và Companies lần 1; People (27), Notes (23, 27), Companies lần 2 (33) vẫn dưới 50: vẫn áp dụng ngoại lệ (bằng chứng `delete-id-max-examples/`).
- **Dữ liệu seed:** sau lần chạy, kiểm lại 5 object còn đủ 30/30 bản ghi seed. Hook mới bảo vệ được dữ liệu.
- **So với 26/11:** 111/116 nhóm lỗi giống nhau. 5 nhóm chỉ có ở 26/11 đều do hook cũ để request chạm bản ghi seed, không phải Twenty đã sửa:
  `DELETE /{people,notes,tasks}/{id}` × `negative_data_rejection` (lần trước `soft_delete` sai xoá trúng bản ghi seed nên trả 200, D-07; nay id seed bị đổi nên trả 404; D-07 vẫn thấy ở `DELETE /{obj}` cả 5 object) và
  `PATCH /{notes,tasks}` × `response_schema_conformance` (lần trước sửa trúng bản ghi seed nên body có `null`, D-09; nay filter của hook không khớp bản ghi nào; D-09 vẫn thấy ở `GET` cả 5 object).
- **Mã lỗi:** không có nhóm lỗi mới; A–F vẫn ứng với D-07, D-01 (+ D-08), D-09, D-02, D-10, D-03 như bảng trên.

## Việc còn lại

- ~~Kiểm chứng tay A–F bằng `curl`, đọc `messages` (bẫy H3), rồi mới đánh mã D-xx.~~ Xong (xem cột Mã lỗi).
- ~~`DELETE /{id}` < 50 ca ở cả 5 object.~~ Đã ghi là ngoại lệ, bằng chứng ở `delete-id-max-examples/`.
- ~~D trùng SC5 (Tuấn), C/E/F có thể trùng SC1 (Quang).~~ Đã gộp vào `reports/bang-loi.md`.
- ~~Chạy lại lần 2 cùng seed để kiểm tra tái lập.~~ Xong (xem mục Tái lập).
- ~~Báo Quang: `summarize.py --compare` lỗi `UnicodeEncodeError`.~~ Quang đã sửa (PR #20).
- ~~Chạy lại SC2 trên harness của `develop` để có lần chạy chính thức.~~ Xong 28/11 (xem mục Lần chạy chính thức).
