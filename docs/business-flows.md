# Ba luồng nghiệp vụ và dữ liệu mẫu (Báo cáo Phần C, E)

Người phụ trách: Trung. Cách nhanh: `python scripts/business_flows.py` chạy cả ba luồng, lưu bằng chứng vào `evidence/business-flows-*.json`
(key đã redact). Phần dưới là bản làm tay bằng giao diện và `curl` để chụp ảnh cho báo cáo.

| Luồng | Làm trên giao diện | Tương đương REST | Kỳ vọng |
|---|---|---|---|
| F1 Tạo Company | Companies → New → nhập tên → lưu | `POST /rest/companies {"name":"..."}` | 201, có `id` |
| F2 Tạo Person gắn Company | People → New → chọn Company | `POST /rest/people {"name":{"firstName":"..","lastName":".."},"companyId":"<id>"}` | 201, `GET /rest/people/{id}` trả `companyId` đúng |
| F3 Đổi stage Opportunity | Opportunities → kéo thẻ sang cột MEETING | `PATCH /rest/opportunities/{id} {"stage":"MEETING"}` | 200, đọc lại thấy `stage` = `MEETING` |

```bash
# PowerShell dùng curl.exe; đặt khóa: $env:TWENTY_API_KEY="..."
curl -s -X POST http://localhost:3001/rest/companies -H "Authorization: Bearer $TWENTY_API_KEY" -H "Content-Type: application/json" -d '{"name":"Demo Co"}'
```

## Dữ liệu mẫu cho K05 (`scripts/seed.py`)

Tạo N công ty, N người (gắn công ty luân phiên), N cơ hội (stage lần lượt NEW, SCREENING, MEETING, PROPOSAL, CUSTOMER). Chia lô 50 (giới hạn batch thật là 200).
Tên trường lấy từ hằng seed của Twenty rồi đổi từ dạng cột phẳng sang dạng lồng của REST:

| Đối tượng | Trường gửi | Ghi chú |
|---|---|---|
| Company | `name`, `domainName.primaryLinkUrl`, `address.addressCity`, `annualRevenue.{amountMicros,currencyCode}` | Cột seed: `domainNamePrimaryLinkUrl`, `addressAddressCity` |
| Person | `name.firstName`, `name.lastName`, `emails.primaryEmail`, `jobTitle`, `companyId` | |
| Opportunity | `name`, `amount.amountMicros`, `amount.currencyCode`, `stage`, `closeDate`, `companyId`, `pointOfContactId` | |

Tên trường đã đối chiếu với `schema/core.openapi.json` thật (Company không có `employees` ở v2.45.6). Nếu API vẫn trả 400, so lại với schema rồi sửa hàm `build_*` trong `seed.py`.

## Danh sách operation (chốt phạm vi)

`python scripts/list_operations.py --md docs/operations.md` sinh bảng đầy đủ từ schema thật. Với mỗi đối tượng trong phạm vi
(companies, people, opportunities, notes, tasks) kỳ vọng 8 đường dẫn (xem `architecture.md` B.2), tổng số operation sẽ do script đếm.
Mẫu số cho tiêu chí "≥80% operation" lấy từ file này.

## Key giới hạn role (SC5)

1. Settings → Roles → tạo role mới, chỉ bật quyền **đọc** trên Companies/People/Opportunities/Notes/Tasks, tắt tạo/sửa/xoá. (Tên menu cần xác nhận trên v2.45.6.)
2. Settings → API → tạo key thứ hai, gán role vừa tạo.
3. Dán vào `.env`: `TWENTY_API_KEY_LIMITED=...`. Key này dùng cho SC5 ở Sprint 3–4 (ca P5-07 đọc → 200, P5-08 ghi → 403).
