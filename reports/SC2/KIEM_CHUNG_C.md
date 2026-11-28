# Kiểm chứng tay vấn đề C: response trả `null` ở trường schema không cho `null`

Ngày: 26/11/2026. Twenty v2.45.6 local. Người kiểm: Thuận. Chỉ đọc (GET), không sửa dữ liệu.
Cách làm: lấy tối đa 30 bản ghi mỗi object (`GET /{object}?limit=30&depth=0`), so từng trường với `{Object}ForResponse` trong schema.

## Trường trả `null` trái schema

| Object | Trường | Tỉ lệ null | Schema khai |
|---|---|---|---|
| cả 5 | `deletedAt` | 100% | `string`, `date-time` |
| cả 5 | `createdBy.workspaceMemberId`, `updatedBy.workspaceMemberId` | 100% | `string`, `uuid` |
| Companies | `address.addressLat`, `address.addressLng` | 30/30 | `number` |
| Companies | `accountOwnerId` | 30/30 | `string`, `uuid` |
| Companies | `annualRevenue.amountMicros`, `.currencyCode` | 5/30 | `number` / `string` |
| People | `avatarFile` | 30/30 | `array` |
| People | `companyId` | 1/30 | `string`, `uuid` |
| Opportunities | `ownerId` | 25/30 | `string`, `uuid` |
| Notes | `bodyV2.blocknote` | 1/30 | `string` |
| Tasks | `assigneeId` | 24/24 | `string`, `uuid` |

## Nguyên nhân

Toàn bộ `components` trong schema có **0 lần** `nullable` và **0 lần** kiểu `"null"`. Tức là bộ sinh OpenAPI của Twenty
**không bao giờ đánh dấu trường nào được phép `null`**, trong khi database cho phép `null` ở các trường tùy chọn.

Các giá trị `null` ở đây **đúng nghiệp vụ**:
- `deletedAt: null` = bản ghi chưa bị xóa.
- `accountOwnerId`, `ownerId`, `assigneeId: null` = chưa gán người phụ trách.
- `createdBy.workspaceMemberId: null` = bản ghi tạo qua API key, không phải bởi một thành viên.
- `addressLat/Lng: null` = chưa có tọa độ.

Server trả đúng; **tài liệu sai**.

## Kết luận

- **Phân loại:** lệch schema (lỗi của tài liệu OpenAPI, không phải lỗi xử lý dữ liệu).
- **Mức độ:** trung bình. Không mất dữ liệu, nhưng client sinh code từ schema (SDK kiểu chặt, TypeScript, Java…) sẽ khai các trường này là không-null và có thể lỗi khi gặp `null`. Đây cũng là nguồn của phần lớn báo động trong `response_schema_conformance` (~800 lần ở SC2).
- **Phạm vi:** cả 5 object, mọi operation trả về bản ghi (GET, PATCH, restore, batch…).
- **Module nghi ngờ:** `engine/core-modules/open-api/` (sinh schema từ metadata: không chuyển cờ `isNullable` của field sang `nullable` / `type: [..., "null"]`). Cần đọc mã nguồn v2.45.6 để xác nhận.
- **Ảnh hưởng tới các kịch bản khác:** SC1, SC3, SC4 cũng sẽ gặp cùng báo động này. Nên ghi **một** mã lỗi D-xx dùng chung, không ghi lặp.

## Reproducer

```bash
curl -s -H 'Authorization: Bearer <KEY>' 'http://localhost:3001/rest/companies?limit=1&depth=0'
# -> "deletedAt": null, "accountOwnerId": null, "address": {... "addressLat": null, "addressLng": null}
# Schema (CompanyForResponse.properties.deletedAt): {"type": "string", "format": "date-time"}  — không có "null"
```

## Ghi chú phụ

Tasks chỉ còn 24/30 bản ghi seed: lần chạy SC2 đã xóa 6 task qua `DELETE /tasks/{id}` (hook chỉ chặn xóa hàng loạt, không chặn xóa theo id). Cần `--reset` trước mỗi lần chạy chính thức.
