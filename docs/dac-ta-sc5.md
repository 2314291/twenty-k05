# Đặc tả và kết quả SC5: Xác thực và phân quyền (Tuấn)

Phần E của SC5, kèm nhật ký lỗi. Bổ sung cho `Phan_Cong_module/KICH_BAN_K05.md` (mục SC5) và `docs/dac-ta-sc1-sc2-red.md` (mục 5, ca P5).
Kỳ vọng đọc từ schema (`schema/core.openapi.json`) và chuẩn HTTP; nguyên nhân đọc từ mã nguồn Twenty v2.45.6 (SHA `6007ad5a7f6cb676fd8a9ff0c2a86a2e3d4c260e`).

## 1. Mục tiêu và phạm vi

| Mục | Nội dung |
|---|---|
| Mục tiêu | Không có quyền thì không đọc, không ghi được; key chỉ đọc đọc được nhưng không ghi được; mã lỗi đúng chuẩn và đúng schema |
| Bất biến | I1 (không 5xx), I2 (mã nằm trong schema), I6 (thiếu/sai key thì không truy cập được) |
| Phạm vi | 5 object (Companies, People, Opportunities, Notes, Tasks) × 13 operation × 4 loại key = **260 ca**, cộng 10 ca biên tay P5 |
| Ngoài phạm vi | GraphQL, đăng nhập bằng cookie của giao diện web, hết hạn key, thu hồi key |
| Kỹ thuật | Phân vùng tương đương trên đầu vào `Authorization` (4 vùng), giá trị biên về định dạng header (P5-03, P5-04), ca đối chứng |

## 2. Input: bốn loại key (bốn vùng tương đương)

| Loại | Cách có | Đọc (4 operation) | Ghi (9 operation) |
|---|---|---|---|
| `full` đủ quyền | Settings → APIs, `TWENTY_API_KEY` | 200 | 200/201 (đối chứng) |
| `limited` chỉ đọc | Role `K05 Chi doc` chỉ bật quyền xem 5 object; key gán role đó, `TWENTY_API_KEY_LIMITED` | 200 | **403** |
| `wrong` sai | `k05-sai-key-000000` | 401 | 401 |
| `none` không có | Không gửi `Authorization` | 401 | 401 |

Bốn thao tác đọc: `GET /{o}`, `GET /{o}/{id}`, `GET /{o}/groupBy`, `POST /{o}/duplicates`.
Chín thao tác ghi: `POST /{o}`, `POST /batch/{o}`, `PATCH /{o}/{id}`, `PATCH /{o}`, `PATCH /{o}/merge`, `PATCH /{o}/{id}/restore`, `PATCH /{o}/restore`, `DELETE /{o}/{id}`, `DELETE /{o}`.

## 3. Điều kiện đầu và dữ liệu test

| Hạng mục | Giá trị |
|---|---|
| Trạng thái ban đầu | `python scripts/reset_env.py` (khôi phục snapshot, seed 30 bản ghi mỗi object) |
| Key chỉ đọc | Đã tạo **trước khi chụp snapshot**, nếu không reset sẽ xoá mất (xem `SETUP.md` mục 8) |
| Bản ghi đích | Script tự tạo bằng key đủ quyền, mỗi object **2 bộ** × 7 bản ghi tiền tố `K05-SC5-` (1 để đọc/sửa, 2 để gộp, 2 đã xoá mềm để khôi phục, 2 để xoá). Bộ thứ nhất cho `none`/`wrong`/`limited`, bộ `dc-` riêng cho `full` (đối chứng), để nếu một key lẽ ra bị chặn mà ghi được thì đối chứng vẫn còn bản ghi; xoá vĩnh viễn ở cuối |
| Body | Tối thiểu hợp lệ, giống `seed.py`: `name` (Companies, Opportunities), `name.firstName/lastName` (People), `title` (Notes, Tasks) |
| Tham số đặc biệt | `group_by=[{"createdAt":{"granularity":"DAY","timeZone":"Asia/Ho_Chi_Minh"}}]` (thiếu `timeZone` sẽ 400); xoá/sửa/khôi phục hàng loạt luôn kèm `filter=id[eq]:<id>` |
| Nhịp gửi | 1 request/giây, gặp 429 thì chờ `retryAfterSeconds` (giới hạn G-01) |
| Lệnh | `python scripts/kiem_thu_sc5.py` (khoảng 7 phút) |

**Kiểm tra điều kiện đầu tự động** (rút ra từ hai lần chạy không hợp lệ, mục 6.3): script dừng nếu key đủ quyền không đọc được, nếu key chỉ đọc trống, ngắn hơn 100 ký tự, trùng key đủ quyền, không đọc được Companies, hoặc **ghi được** (`POST /companies` thành công nghĩa là key đang gán role có quyền ghi, thường là Admin; script xoá bản ghi vừa tạo rồi dừng).

## 4. Cách kết luận (3 cột độc lập)

| Cột | Câu hỏi | Giá trị |
|---|---|---|
| Chặn | Có chặn đúng không? (I6) | ĐẠT; **LỖI BẢO MẬT** (2xx ở chỗ phải chặn); CHẶN NHẦM (key chỉ đọc bị chặn khi đọc); ĐỐI CHỨNG HỎNG; KHÔNG KẾT LUẬN (đối chứng hỏng thì không biết request có hợp lệ không); KHÔNG ÁP DỤNG (object không hỗ trợ thao tác, ví dụ `merge` trên Opportunities, Notes, Tasks trả 400 "Merge is only available for objects with duplicate criteria", đúng thiết kế) |
| Mã | Mã có đúng kỳ vọng ở mục 2 không? | ĐÚNG / LỆCH |
| Schema | Mã có nằm trong danh sách schema khai báo không? (I2) | CÓ / KHÔNG |

Tách 3 cột vì một ca có thể **an toàn nhưng sai mã** (D-02), hoặc **đúng chuẩn HTTP nhưng không có trong schema** (key chỉ đọc ghi → 403, schema không khai báo 403; thuộc G-07).

Thứ tự trong một operation: `none` → `wrong` → `limited` → `full`. Ba loại đầu phải bị chặn nên không làm đổi dữ liệu; `full` chạy cuối vì có thể xoá hoặc gộp bản ghi đích.

## 5. Ca biên tay P5

| Mã ca | Request | Kỳ vọng | 25–26/11 (curl, máy Tuấn) | 28/11 (`kiem_thu_sc5.py`, 2 lần, máy Tuấn) |
|---|---|---|---|---|
| P5-00 | `GET /companies`, key đủ quyền | 200 | 200. MATCH | 200. MATCH |
| P5-01 | `GET /companies`, không key | 401 | 403. **DIFF → D-02** | 403 `Missing authentication token`. **DIFF → D-02** |
| P5-02 | `GET /companies`, key sai | 401 | 401. MATCH | 401 `Token invalid.` MATCH |
| P5-03 | scheme `Basic` | 401 | 403. **DIFF → D-02** | 403. **DIFF → D-02** |
| P5-04 | `Bearer` rỗng | 401 | 403. **DIFF → D-02** | 403. **DIFF → D-02** |
| P5-05 | `POST /companies`, không key | 401 | 403. **DIFF → D-02** | 403. **DIFF → D-02** |
| P5-06 | `GET /open-api/core` không key so với có key | quan sát | 200 cả hai. OBSERVE | 200 cả hai: không key 1 đường dẫn (5 157 ký tự), có key 322 đường dẫn (988 112 ký tự). OBSERVE (người lạ không thấy cấu trúc dữ liệu) |
| P5-07 | `GET`, key chỉ đọc | 200 | Lần chạy không hợp lệ (key trống) | 200. MATCH |
| P5-08 | `POST`, key chỉ đọc | 403 | Lần chạy không hợp lệ (key trống) | 400 `PERMISSION_DENIED`. **DIFF → D-12** (vẫn bị chặn, sai mã) |

Bằng chứng: `evidence/sc5-thu-cong-20261126.md` (25–26/11), `reports/sc5/20261128-010047-p5.json`, `reports/sc5/20261128-010929-p5.json` (28/11).

## 6. Kết quả ma trận 260 ca

### 6.1. Lần chạy chính thức

| Mục | Giá trị |
|---|---|
| Môi trường | Twenty `v2.45.6` (digest `sha256:dca6d829…51e53`), `http://localhost:3001`, máy Tuấn (Windows, Docker Desktop) |
| Key | `full` role Admin; `limited` role **K05 Chi doc** (chỉ bật `canReadObjectRecords` cho 5 object, không quyền cập nhật, xoá mềm, xoá cứng, cài đặt); `wrong` `k05-sai-key-000000`; `none` |
| Điều kiện đầu | Snapshot chụp lại 28/11 00:59 sau khi đã có role và key chỉ đọc (5/5/6/0/0 bản ghi); trước mỗi lần chạy `reset_env.py` (35/35/36/30/30) |
| Lần 1 | 28/11/2026 01:00, `reports/sc5/20261128-010047.md` |
| Lần 2 | 28/11/2026 01:09, `reports/sc5/20261128-010929.md` |
| **Tái lập** | `--compare`: 260 ca chung, **GIỐNG 260, KHÁC 0** |
| I1 (không 5xx) | Giữ ở cả 260 ca và 10 ca P5 |

| Cột | Kết quả (mỗi lần chạy) |
|---|---|
| Chặn (I6) | **ĐẠT 248**, LỖI BẢO MẬT 0, CHẶN NHẦM 0, ĐỐI CHỨNG HỎNG 0, KHÔNG ÁP DỤNG 6, KHÔNG KẾT LUẬN 6 |
| Mã đúng kỳ vọng | 147 / 260 (lệch: 65 ca `none` do D-02, 42 ca `limited` ghi do D-12; 6 ca không áp dụng) |
| Mã có trong schema (I2) | 190 / 260 (ngoài schema: 65 ca `none` trả 403, 5 ca `wrong` trên `groupBy` trả 401 trong khi schema `groupBy` chỉ khai 200 → D-03) |

KHÔNG ÁP DỤNG: `merge` trên Opportunities, Notes, Tasks với key `limited` và `full` (object không có tiêu chí trùng lặp).
KHÔNG KẾT LUẬN: `merge` trên 3 object đó với `none`, `wrong`; thông điệp cho thấy đã bị chặn ở bước xác thực (`Missing authentication token`, `Token invalid.`), nhưng không có đối chứng hợp lệ nên script không chấm.

### 6.2. Bảng mã trạng thái theo loại key (gộp 5 object, giống hệt ở cả 2 lần)

| Operation | Loại | none | wrong | limited | full |
|---|---|---|---|---|---|
| `GET /{o}` | đọc | 403×5 | 401×5 | 200×5 | 200×5 |
| `GET /{o}/{id}` | đọc | 403×5 | 401×5 | 200×5 | 200×5 |
| `GET /{o}/groupBy` | đọc | 403×5 | 401×5 | 200×5 | 200×5 |
| `POST /{o}/duplicates` | đọc | 403×5 | 401×5 | 200×5 | 200×5 |
| `POST /{o}` | ghi | 403×5 | 401×5 | 400×5 | 201×5 |
| `POST /batch/{o}` | ghi | 403×5 | 401×5 | 400×5 | 201×5 |
| `PATCH /{o}/{id}` | ghi | 403×5 | 401×5 | 400×5 | 200×5 |
| `PATCH /{o}` | ghi | 403×5 | 401×5 | 400×5 | 200×5 |
| `PATCH /{o}/merge` | ghi | 403×5 | 401×5 | 400×5 | 200×2 (Companies, People), 400×3 (không áp dụng) |
| `PATCH /{o}/{id}/restore` | ghi | 403×5 | 401×5 | 400×5 | 200×5 |
| `PATCH /{o}/restore` | ghi | 403×5 | 401×5 | 400×5 | 200×5 |
| `DELETE /{o}/{id}` | ghi | 403×5 | 401×5 | 400×5 | 200×5 |
| `DELETE /{o}` | ghi | 403×5 | 401×5 | 400×5 | 200×5 |

So với dự đoán trước khi chạy: cột `none` toàn 403 và cột `wrong` toàn 401 đúng như dự đoán; cột `limited` ghi ra **400** chứ không phải 403 như dự đoán (D-12).
Hành vi giống nhau ở cả 5 object, nên D-02 và D-12 là lỗi ở tầng xác thực/phân quyền dùng chung, không phải lỗi riêng một object.

### 6.3. Hai lần chạy không hợp lệ (không tính là lỗi, giữ làm bằng chứng)

| Lần | Hiện tượng | Nguyên nhân | Xử lý |
|---|---|---|---|
| 28/11 00:37 và 00:45 (`reports/sc5/khong-hop-le-20261128/`) | Key "chỉ đọc" ghi được ở mọi operation (35 ca LỖI BẢO MẬT); kéo theo 15 ca ĐỐI CHỨNG HỎNG vì key `limited` đã xoá/gộp mất bản ghi đích trước khi `full` chạy | Key tên "K05 Chi doc" được tạo với role **Admin** (xác nhận qua `getRoles`: role K05 Chi doc có `apiKeys: []`). Kiểm tra điều kiện đầu cũ chỉ thử đọc, mà key Admin cũng đọc được | Đổi role của key sang K05 Chi doc trong Settings → APIs (API key không tự đổi được: `assignRoleToApiKey` trả `FORBIDDEN` với caller là API key); thêm bước thử ghi vào kiểm tra điều kiện đầu; tách bộ bản ghi đích cho `full` |
| Cùng hai lần trên | `GET /{o}/groupBy` trả 400 ở cả key đủ quyền | Lỗi mã test: thiếu `timeZone` trong `group_by` | Thêm `"timeZone":"Asia/Ho_Chi_Minh"` |

Bài học: kiểm tra điều kiện đầu phải phân biệt được vùng tương đương cần kiểm (chỉ đọc) với vùng lân cận (đủ quyền); chỉ thử thao tác mà cả hai vùng đều làm được thì không phân biệt được.

## 7. Nhật ký lỗi SC5

### D-02. Thiếu thông tin xác thực trả 403 thay vì 401

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC5; cả 5 object × 13 operation (65 ca cột `none`, 28/11, 2 lần chạy), cộng ca tay P5-01, P5-03..P5-05 |
| Ca | P5-01, P5-03, P5-04, P5-05 (một nguyên nhân, **tính là một lỗi**) |
| Kỳ vọng | 401. Căn cứ: schema chỉ khai báo 200/400/401 cho `GET /companies`; RFC 9110: chưa xác thực là 401 |
| Thực tế | 403, body `{"statusCode":403,"messages":["Missing authentication token"],"error":"FORBIDDEN_EXCEPTION"}` |
| Đối chiếu | Key **sai** (P5-02) ra 401 đúng. Vậy server chỉ gắn sai mã khi **không có** token |
| Loại | Lệch schema (máy chủ vẫn chặn đúng) |
| Mức độ | Thấp: không lộ dữ liệu, không ghi được gì. Tác hại: client nhận 403 sẽ hiểu là "thiếu quyền", không biết cần gắn key |
| Người phát hiện | Tuấn (17/10 lần đầu, xác nhận lại 25–26/11 với 4 reproducer) |

**Reproducer** (PowerShell):

```powershell
curl.exe -s -w "`n=> HTTP %{http_code}`n" "http://localhost:3001/rest/companies?limit=1"
curl.exe -s -w "`n=> HTTP %{http_code}`n" -H "Authorization: Bearer " "http://localhost:3001/rest/companies?limit=1"
```

**Nguyên nhân (RCA)**, theo đường đi của request trong Twenty v2.45.6:

1. `engine/core-modules/auth/token/services/access-token.service.ts`, hàm `validateTokenByRequest` (dòng 195–221): tìm Bearer token; không có thì tìm cookie phiên; **không có cả hai** thì ném `AuthException('Missing authentication token', AuthExceptionCode.FORBIDDEN_EXCEPTION)` (dòng 217–220). Token có nhưng sai thì đi nhánh khác, mã `UNAUTHENTICATED`.
2. `engine/middlewares/middleware.service.ts`, `getStatus` (dòng 206–216): lỗi xác thực được đổi sang mã HTTP qua `getAuthExceptionRestStatus`.
3. `engine/core-modules/auth/utils/get-auth-exception-rest-status.util.ts`: `FORBIDDEN_EXCEPTION` → **403**, `UNAUTHENTICATED` → 401.

Kết luận: lỗi gắn nhãn ở bước 1. "Thiếu token" là chuyện xác thực nên phải là `UNAUTHENTICATED` (401). `Basic ...` và `Bearer ` rỗng không khớp mẫu `Bearer <chuỗi>` nên cũng bị coi là không có token.

**Đề xuất sửa** (chỉ để báo cáo, nhóm không sửa mã Twenty): đổi mã ở dòng 219 thành `UNAUTHENTICATED`; hoặc sửa schema, khai báo thêm 403 cho mọi operation.

### D-12. Key đã xác thực nhưng thiếu quyền ghi trả 400 thay vì 403

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC5; cả 5 object, cả 9 thao tác ghi (42 ca; 3 ca `merge` không áp dụng), cộng P5-08 |
| Kỳ vọng | **403**. Căn cứ: RFC 9110 mục 15.5.4 (đã xác thực nhưng không được phép); `kiem_thu_sc5.py` mục 2 |
| Thực tế | `400 {"statusCode":400,"error":"Error","messages":["Entity performing the request does not have permission"],"code":"PERMISSION_DENIED"}` |
| Đối chứng | Cùng request bằng key đủ quyền: 200/201 (request hợp lệ). Đọc bằng key chỉ đọc: 200 (key hợp lệ). Hai lần chạy giống nhau |
| Loại | Lỗi chức năng (sai mã trạng thái). Schema có khai báo 400 nên cột Schema vẫn "CÓ", nhưng 400 trong schema mang nghĩa dữ liệu sai |
| Mức độ | Thấp: thao tác ghi vẫn bị chặn, không lộ dữ liệu. Tác hại: client không phân biệt được "thiếu quyền" với "dữ liệu sai", dễ thử lại vô ích |
| Người phát hiện | Trung (27/11, máy Trung, 1 ca POST Companies); Tuấn xác nhận trên 5 object × 9 thao tác (28/11, 2 lần chạy) |

**Reproducer** (PowerShell, `$L` là key role chỉ đọc):

```powershell
'{"name":"K05-D12"}' | Out-File -Encoding ascii body.json
curl.exe -s -w "`n=> HTTP %{http_code}`n" -X POST -H "Authorization: Bearer $L" -H "Content-Type: application/json" --data-binary "@body.json" http://localhost:3001/rest/companies
```

**Nguyên nhân (giả thuyết, cần Thuận đối chiếu mã nguồn):** ngoại lệ phân quyền của tầng truy vấn (`PERMISSION_DENIED`) không được bộ lọc lỗi REST đổi sang 403 mà rơi vào nhánh mặc định 400.
Gợi ý chỗ đọc: `rest-api-exception.filter.ts` và tiện ích đổi mã của `PermissionsException` trong `engine/metadata-modules/permissions/`.

**Đề xuất sửa** (chỉ để báo cáo): ánh xạ `PermissionsExceptionCode.PERMISSION_DENIED` sang 403 ở tầng REST; khai báo 403 trong schema.

### Ghi nhận phụ (chưa thành lỗi, cần người phụ trách xác nhận)

- `GET /{o}/groupBy`: schema chỉ khai báo **200**, không có 400 và 401. Đã thấy thật ở 5 ca `wrong` (401 ngoài schema) ngày 28/11. Thuộc D-03 (schema thiếu mã lỗi), không mở mã mới.
- `PATCH /{o}/merge` chỉ dùng được cho Companies, People; 3 object còn lại trả 400 có thông điệp rõ ràng. Đúng thiết kế, nhưng schema vẫn khai `merge` cho cả 5 object mà không ghi điều kiện này (thuộc D-03/D-10, đề nghị Thuận xét).
