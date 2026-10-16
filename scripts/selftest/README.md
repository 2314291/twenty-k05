# selftest — CHỈ ĐỂ KIỂM TRA SCRIPT, KHÔNG PHẢI KẾT QUẢ TWENTY

`mock_server.py` là máy chủ **giả** mô phỏng vài endpoint kiểu Twenty (`/rest/companies`...). Nó có một lỗi
cố ý (limit quá lớn → 500) để kiểm tra đường ống reproducer/thống kê.
Kết quả chạy trên mock **không** được đưa vào báo cáo như kết quả của Twenty và không được lưu trong `reports/`.

    python scripts/selftest/run_selftest.py
