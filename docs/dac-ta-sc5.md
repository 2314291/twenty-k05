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
| Bản ghi đích | Script tự tạo bằng key đủ quyền, mỗi object 7 bản ghi tiền tố `K05-SC5-` (1 để đọc/sửa, 2 để gộp, 2 đã xoá mềm để khôi phục, 2 để xoá); xoá vĩnh viễn ở cuối |
| Body | Tối thiểu hợp lệ, giống `seed.py`: `name` (Companies, Opportunities), `name.firstName/lastName` (People), `title` (Notes, Tasks) |
| Tham số đặc biệt | `group_by=[{"createdAt":{"granularity":"DAY"}}]`; xoá/sửa/khôi phục hàng loạt luôn kèm `filter=id[eq]:<id>` |
| Nhịp gửi | 1 request/giây, gặp 429 thì chờ `retryAfterSeconds` (giới hạn G-01) |
| Lệnh | `python scripts/kiem_thu_sc5.py` (khoảng 7 phút) |

**Kiểm tra điều kiện đầu tự động** (rút ra từ lần chạy P5-07/08 không hợp lệ): script dừng nếu key đủ quyền không đọc được, nếu key chỉ đọc trống, ngắn hơn 100 ký tự, trùng key đủ quyền, hoặc không đọc được Companies.

## 4. Cách kết luận (3 cột độc lập)

| Cột | Câu hỏi | Giá trị |
|---|---|---|
| Chặn | Có chặn đúng không? (I6) | ĐẠT; **LỖI BẢO MẬT** (2xx ở chỗ phải chặn); CHẶN NHẦM (key chỉ đọc bị chặn khi đọc); ĐỐI CHỨNG HỎNG; KHÔNG KẾT LUẬN (đối chứng hỏng thì không biết request có hợp lệ không) |
| Mã | Mã có đúng kỳ vọng ở mục 2 không? | ĐÚNG / LỆCH |
| Schema | Mã có nằm trong danh sách schema khai báo không? (I2) | CÓ / KHÔNG |

Tách 3 cột vì một ca có thể **an toàn nhưng sai mã** (D-02), hoặc **đúng chuẩn HTTP nhưng không có trong schema** (key chỉ đọc ghi → 403, schema không khai báo 403; thuộc G-07).

Thứ tự trong một operation: `none` → `wrong` → `limited` → `full`. Ba loại đầu phải bị chặn nên không làm đổi dữ liệu; `full` chạy cuối vì có thể xoá hoặc gộp bản ghi đích.

## 5. Ca biên tay P5

| Mã ca | Request | Kỳ vọng | Kết quả 25–26/11 (curl, máy Tuấn) |
|---|---|---|---|
| P5-00 | `GET /companies`, key đủ quyền | 200 | 200. MATCH |
| P5-01 | `GET /companies`, không key | 401 | 403. **DIFF → D-02** |
| P5-02 | `GET /companies`, key sai | 401 | 401. MATCH |
| P5-03 | scheme `Basic` | 401 | 403 `Missing authentication token`. **DIFF → D-02** |
| P5-04 | `Bearer` rỗng | 401 | 403 `Missing authentication token`. **DIFF → D-02** |
| P5-05 | `POST /companies`, không key | 401 | 403 `Missing authentication token`. **DIFF → D-02** |
| P5-06 | `GET /open-api/core` không key so với có key | quan sát | 200 cả hai; không key chỉ có khung, có key có đủ đường dẫn của workspace. OBSERVE (hành vi tốt: người lạ không thấy cấu trúc dữ liệu) |
| P5-07 | `GET`, key chỉ đọc | 200 | Chưa có kết quả hợp lệ (lần chạy 26/11 thiếu key, xem `evidence/sc5-thu-cong-20261126.md`) |
| P5-08 | `POST`, key chỉ đọc | 403 | Chưa có kết quả hợp lệ |

Bằng chứng: `evidence/sc5-thu-cong-20261126.md`.

## 6. Kết quả ma trận 260 ca

Chưa chạy trên instance thật. Sau khi chạy, dán bảng "Bảng mã trạng thái theo loại key" từ `reports/sc5/<thời điểm>.md` vào đây,
rồi chạy lần 2 và so: `python scripts/kiem_thu_sc5.py --compare reports/sc5/<lần1>.json reports/sc5/<lần2>.json` (tiêu chí tái lập: KHÁC 0).

Dự đoán trước khi chạy (để đối chiếu, không phải kết quả): cột `none` toàn 403 (D-02); cột `wrong` toàn 401, riêng `groupBy` ra 401 nhưng schema của `groupBy` chỉ khai báo 200; cột `limited` đọc 200, ghi 403 (không có trong schema, thuộc G-07).

## 7. Nhật ký lỗi SC5

### D-02. Thiếu thông tin xác thực trả 403 thay vì 401

| Mục | Nội dung |
|---|---|
| Kịch bản, object | SC5; Companies (ca tay). Ma trận 260 ca sẽ cho biết có lặp lại ở cả 5 object không |
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

### Ghi nhận phụ (chưa thành lỗi, cần người phụ trách xác nhận)

- `GET /{o}/groupBy`: schema chỉ khai báo **200**, không có 400 và 401. Mọi ca thiếu/sai key trên `groupBy` sẽ lệch schema. Đề nghị Thuận gộp vào G-07 (schema thiếu mã lỗi).
