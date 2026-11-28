# Bằng chứng ngoại lệ ngưỡng 50 ca: `DELETE /companies/{id}`

Người chạy: Thuận, 26/11/2026. Twenty v2.45.6 local, Schemathesis 4.31.1, cùng cấu hình SC2
(`--mode negative --phases coverage,fuzzing --seed 20261020 --workers 1 --rate-limit auto`),
chỉ chọn một operation bằng `--include-name 'DELETE /companies/{id}'`.

| Thư mục | Thay đổi so với SC2 | Test case sinh ra |
|---|---|---|
| `max50/` | `--max-examples 50` (như SC2) | 17 |
| `max150/` | `--max-examples 150` | 17 |
| `max500/` | `--max-examples 500` | 17 |
| `nondet-1/` | `--max-examples 50`, bỏ `--generation-deterministic` | 17 |
| `nondet-2/` | như `nondet-1/`, chạy lần 2 | 18 |

Mỗi thư mục có `out.txt` (output của `st run`, dòng cuối ghi số ca "generated") và báo cáo JSON.

Kết luận: tăng `--max-examples` không làm tăng số ca. Operation chỉ có 2 đầu vào (`id`, `soft_delete`), nên số ca **khác nhau**
bị cạn sớm và Schemathesis bỏ ca trùng. Đây là giới hạn của không gian input. Ngoại lệ này được ghi ở
`Phan_Cong_module/KICH_BAN_K05.md` (mục SC2) và `docs/test-plan.md` (D.5).
