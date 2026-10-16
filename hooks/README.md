# hooks/

Chỗ dành cho hook Schemathesis (ví dụ gắn id có thật vào request phụ thuộc dữ liệu, cho SC6). Mốc giữa kỳ chưa cần hook:
xác thực được truyền bằng `-H "Authorization: Bearer ..."` trong `scripts/run_k05.py`. Hook sẽ thêm ở sprint cuối kỳ, kiểm tra với `st run --help`/tài liệu bản 4.31.1.
