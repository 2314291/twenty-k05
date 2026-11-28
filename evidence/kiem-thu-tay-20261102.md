# Bằng chứng kiểm thử tay (Trung), ngày 02/11/2026 và 12/11/2026

Nguyên văn output terminal (PowerShell trong VS Code) khi chạy tay trên Twenty v2.45.6, Docker, `http://localhost:3001`, khoá API role Admin.
Khoá API không xuất hiện trong output. Mỗi khối có mã E-xx để `docs/test-case-trung.md` trỏ tới. Các id là id bản ghi tạm, đã bị xoá sau khi chạy.

## E-01. Nạp dữ liệu, dọn dữ liệu, ba luồng nghiệp vụ (14:56)

Lệnh (chạy liền một lượt): `python scripts/seed.py --count 5`, `python scripts/seed.py --cleanup`, `python scripts/business_flows.py`.

```
Đã tạo 5 công ty, 5 người, 5 cơ hội. Manifest: reports\seed-manifest.json
DELETE /opportunities/17bf385e-db8d-4b64-9c11-81bcedd381a5 -> 200
DELETE /opportunities/57c5bb3c-9ae4-455e-906c-067f12eaad3a -> 200
DELETE /opportunities/625771e6-406d-4bc1-9ef6-73ba321a04bf -> 200
DELETE /opportunities/9ccb7387-e0ca-448c-a2fb-5f7032d724e2 -> 200
DELETE /opportunities/ae75130e-022d-4a85-bb77-55345130d5ea -> 200
DELETE /people/bf8a5162-2e75-41b6-ab3b-c780c938eead -> 200
DELETE /people/063d8d3b-6d1e-4119-a6c2-325607a3a144 -> 200
DELETE /people/29bb29ac-2287-4d34-b0ac-d26e6fb3f1c2 -> 200
DELETE /people/6b8675c2-a79f-4d86-824d-75e8e55cf581 -> 200
DELETE /people/9a890de6-3635-4ca4-a499-4827a3f409ff -> 200
DELETE /companies/fba64671-4cee-49b8-972f-b82b5cee81eb -> 200
DELETE /companies/8d177237-592a-432d-9adf-1313666c0155 -> 200
DELETE /companies/b23901a4-ea58-42c0-9b3c-1a9639146cb9 -> 200
DELETE /companies/23b2e2f2-0a96-41bb-9371-6739a0495d12 -> 200
DELETE /companies/ee459b31-5ad5-44af-bc59-7304c9d8559f -> 200
Đã dọn xong.
[F1 tạo Company] POST /companies -> 201 (0.20s)
[F2 tạo Person gắn Company] POST /people -> 201 (0.07s)
[F2b đọc lại Person] GET /people/c6b7f2c2-319d-4570-aa81-a0605618fd72 -> 200 (0.05s)
[F3a tạo Opportunity (NEW)] POST /opportunities -> 201 (0.05s)
[F3b đổi stage -> MEETING] PATCH /opportunities/fb9d81e3-35d6-4c9d-9580-9b33f99904e1 -> 200 (0.07s)
[F3c đọc lại Opportunity] GET /opportunities/fb9d81e3-35d6-4c9d-9580-9b33f99904e1 -> 200 (0.07s)
    stage hiện tại = 'MEETING' (kỳ vọng 'MEETING')
[dọn opportunities] DELETE /opportunities/fb9d81e3-35d6-4c9d-9580-9b33f99904e1 -> 200 (0.07s)
[dọn people] DELETE /people/c6b7f2c2-319d-4570-aa81-a0605618fd72 -> 200 (0.07s)
[dọn companies] DELETE /companies/74c5b554-266d-4985-a939-1cc93b6fbc8e -> 200 (0.05s)

Kết quả: ĐẠT. Bằng chứng: evidence\business-flows-20261102-145619.json
```

## E-02. SC3, 17 ca khi có 125 công ty (14:59)

Lệnh: `python scripts/seed.py --count 120`, rồi vòng lặp `curl.exe` cho 17 ca, rồi `Invoke-RestMethod` đếm số bản ghi.

```
Đã tạo 120 công ty, 120 người, 120 cơ hội. Manifest: reports\seed-manifest.json
P3-01  200  /companies?limit=0
P3-02  200  /companies?limit=1
P3-03  200  /companies?limit=60
P3-04  200  /companies?limit=200
P3-05  200  /companies?limit=201
P3-06  200  /companies?limit=100000
P3-07  400  /companies?limit=-1
P3-08  400  /companies?limit=abc
P3-09  400  /companies?limit=1.5
P3-10  200  /companies?limit=
P3-11  400  /companies?starting_after=khong-phai-cursor
P3-12  400  /companies?ending_before=%00
P3-13  400  /companies?order_by=khongtontai
P3-14  400  /companies?filter=name[eq
P3-15  400  /companies?depth=99
P3-16  400  /companies/not-a-uuid
P3-17  404  /companies/00000000-0000-4000-8000-000000000000
limit=1 -> 1 bản ghi
limit=60 -> 60 bản ghi
limit=200 -> 125 bản ghi
limit=201 -> 125 bản ghi
limit=100000 -> 125 bản ghi
```

## E-03. Giới hạn tốc độ 429 (15:01)

Trích dòng đầu và dòng cuối của output khi chạy `seed.py --cleanup` (bản cũ) rồi `seed.py --count 210`, `seed.py --cleanup`:

```
POST /batch/companies trả 429: {"statusCode": 429, "error": "RATE_LIMITED", "messages": ["Rate limit exceeded for apiKey: 100 requests per 60s."], "limitKind": "speed", "exhaustedKind": "limit", "scope": {"spenderType": "apiKey", "spenderId": null, "operationType": "API_REQUEST"}, "limit": 100, "remaining": 0, "periodCount": 60, "periodUnit": "second", "retryAfterSeconds": 1}
...
Không có reports/seed-manifest.json, không có gì để dọn.
```

## E-04. Số bản ghi bị sót sau `seed.py --cleanup` bản cũ (15:13)

Đếm bằng cách liệt kê và xoá từng bản ghi có tên bắt đầu bằng `K05`:

```
opportunities: đã xoá 3
people: đã xoá 115
companies: đã xoá 115
5
```

## E-05. SC4, batch theo số bản ghi (15:17), và nguyên văn phản hồi của P4-04

```
P4-01  n=0  -> 201
P4-02  n=1  -> 201
B-03  n=2  -> 201
P4-05  n=61  -> 201
B-05  n=199  -> 201
P4-03  n=200  -> 201
P4-04  n=201  -> 400
PS D:\twenty-k05> Get-Content "$env:TEMP\k05r.json"
{"statusCode":400,"error":"BadRequestException","messages":["Maximum number of records to upsert is 200."]}
```

## E-06. SC3 chạy lại ba ca biên khi có 468 công ty (15:18)

```
limit=200 -> 200 bản ghi
limit=201 -> 200 bản ghi
limit=100000 -> 200 bản ghi
```

## E-07. SC4, body sai kiểu (15:25)

```
P4-06  -> 400  {"statusCode":400,"error":"TypeError","messages":["args.data.forEach is not a function"]}
P4-07  -> 400  {"statusCode":400,"error":"TypeError","messages":["Cannot read properties of null (reading 'position')"]}
P4-08  -> 400  {"message":"Expected property name or '}' in JSON at position 1 (line 1 column 2)","error":"Bad Request","statusCode":400}
```

## E-08. Dọn sau SC4: số công ty đã xoá và số còn lại (15:36)

```
companies: đã xoá 463
5
```

## E-09. SC6, vòng đời một công ty (19:14)

```
S6-01  POST /companies  -> 201
  id = d4174c8f-9938-4921-8de6-144a390e3dcc
S6-02  GET /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 200
  name=K05-SC6-Company  domain=k05-sc6.example.com
S6-03  PATCH /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 200
S6-04  GET /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 200
  name=K05-SC6-Company-sua  domain=k05-sc6.example.com
S6-05  GET /companies?filter=id[eq]:d4174c8f-9938-4921-8de6-144a390e3dcc  -> 200
  so ban ghi = 1
S6-06  DELETE /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 200
S6-07  GET /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 404
S6-08  DELETE /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 404
S6-09  PATCH /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 404
S6-10  PATCH /companies/d4174c8f-9938-4921-8de6-144a390e3dcc/restore  -> 404
S6-10b  GET /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 404
S6-11a  POST /companies  -> 201
S6-11b  POST /people  -> 201
S6-11c  DELETE /companies/3f293b0d-9c41-40df-b8ae-002abd50c278  -> 200
S6-11d  GET /people/5f56d1a7-6c67-479a-8c84-5bc4c53bc618  -> 200
  companyId = 
S6-12a  GET /companies/00000000-0000-4000-8000-000000000000  -> 404
S6-12b  PATCH /companies/00000000-0000-4000-8000-000000000000  -> 404
S6-12c  DELETE /companies/00000000-0000-4000-8000-000000000000  -> 404
don-1  DELETE /people/5f56d1a7-6c67-479a-8c84-5bc4c53bc618  -> 200
don-2  DELETE /companies/d4174c8f-9938-4921-8de6-144a390e3dcc  -> 404
PS D:\twenty-k05> $last
{"statusCode":404,"error":"NotFoundException","messages":["Record not found"]}
```

Body gửi ở S6-01: `{"name":"K05-SC6-Company","domainName":{"primaryLinkUrl":"https://k05-sc6.example.com"}}`.

## E-10. SC6, xoá mềm rồi khôi phục (19:20)

```
S6-13a  POST /companies  -> 201
S6-13b  DELETE /companies/d78191a5-db22-4ab2-9b2f-1dc5659900ff?soft_delete=true  -> 200
S6-13c  GET /companies/d78191a5-db22-4ab2-9b2f-1dc5659900ff  -> 404
S6-13d  PATCH /companies/d78191a5-db22-4ab2-9b2f-1dc5659900ff/restore  -> 200
S6-13e  GET /companies/d78191a5-db22-4ab2-9b2f-1dc5659900ff  -> 200
S6-13f  DELETE /companies/d78191a5-db22-4ab2-9b2f-1dc5659900ff  -> 200
```

## E-12. Nạp 5 đối tượng và dọn bằng `seed.py` bản đã sửa (19:37)

Chạy trên nhánh `feature/trung-seed-notes-tasks`. Output đầy đủ (150 dòng `DELETE` cùng các dòng chờ khi gặp 429) lưu ở `evidence/seed-20261102.txt`.

```
PS D:\twenty-k05> Get-Content -Encoding UTF8 evidence\seed-20261102.txt -TotalCount 1
Đã tạo 30 công ty, 30 người, 30 cơ hội, 30 ghi chú, 30 việc. Manifest: reports\seed-manifest.json
PS D:\twenty-k05> (Select-String -Path evidence\seed-20261102.txt -Pattern "429").Count
15
PS D:\twenty-k05> Get-Content -Encoding UTF8 evidence\seed-20261102.txt -Tail 1
Đã dọn xong.
```

## E-13. SC6 cho People, Opportunities, Notes, Tasks (12/11/2026, 19:20)

Cùng môi trường, chạy bằng hàm `Sc6` trong PowerShell (mỗi request cách 1 giây). Dữ liệu tạo và dữ liệu sửa:
People `{"name":{"firstName":"K05SC6","lastName":"Nguoi"},"emails":{"primaryEmail":"k05.sc6@example.com"}}`, sửa `firstName`;
Opportunities `{"name":"K05-SC6-Opp","stage":"NEW","amount":{"amountMicros":1000000,"currencyCode":"USD"}}`, sửa `stage` sang `MEETING`;
Notes `{"title":"K05-SC6-Note","bodyV2":{"markdown":"Noi dung K05"}}`, sửa `title`;
Tasks `{"title":"K05-SC6-Task","status":"TODO","dueAt":"2026-12-31T00:00:00.000Z"}`, sửa `status` sang `DONE`.

```
Person-01  POST /people  -> 201
  id = 07ab3056-2470-40a0-9059-8c3d20f50846
Person-02  GET /people/07ab3056-2470-40a0-9059-8c3d20f50846  -> 200
  ten=K05SC6  email=k05.sc6@example.com
Person-03  PATCH /people/07ab3056-2470-40a0-9059-8c3d20f50846  -> 200
Person-04  GET /people/07ab3056-2470-40a0-9059-8c3d20f50846  -> 200
  ten=K05SC6sua  email=k05.sc6@example.com
Person-05  GET /people?filter=id[eq]:07ab3056-2470-40a0-9059-8c3d20f50846  -> 200
  so ban ghi = 1
Person-06  DELETE /people/07ab3056-2470-40a0-9059-8c3d20f50846  -> 200
Person-07  GET /people/07ab3056-2470-40a0-9059-8c3d20f50846  -> 404
Person-08  DELETE /people/07ab3056-2470-40a0-9059-8c3d20f50846  -> 404
Person-09  PATCH /people/07ab3056-2470-40a0-9059-8c3d20f50846  -> 404
Person-10  PATCH /people/07ab3056-2470-40a0-9059-8c3d20f50846/restore  -> 404
Person-13a  POST /people  -> 201
Person-13b  DELETE /people/183bcf88-c07a-4cec-a07c-1f5b1f93f00a?soft_delete=true  -> 200
Person-13c  GET /people/183bcf88-c07a-4cec-a07c-1f5b1f93f00a  -> 404
Person-13d  PATCH /people/183bcf88-c07a-4cec-a07c-1f5b1f93f00a/restore  -> 200
Person-13e  GET /people/183bcf88-c07a-4cec-a07c-1f5b1f93f00a  -> 200
Person-13f  DELETE /people/183bcf88-c07a-4cec-a07c-1f5b1f93f00a  -> 200
Opportunity-01  POST /opportunities  -> 201
  id = 27502a79-81a4-496a-b3c2-2682188ae429
Opportunity-02  GET /opportunities/27502a79-81a4-496a-b3c2-2682188ae429  -> 200
  stage=NEW  amount=1000000
Opportunity-03  PATCH /opportunities/27502a79-81a4-496a-b3c2-2682188ae429  -> 200
Opportunity-04  GET /opportunities/27502a79-81a4-496a-b3c2-2682188ae429  -> 200
  stage=MEETING  amount=1000000
Opportunity-05  GET /opportunities?filter=id[eq]:27502a79-81a4-496a-b3c2-2682188ae429  -> 200
  so ban ghi = 1
Opportunity-06  DELETE /opportunities/27502a79-81a4-496a-b3c2-2682188ae429  -> 200
Opportunity-07  GET /opportunities/27502a79-81a4-496a-b3c2-2682188ae429  -> 404
Opportunity-08  DELETE /opportunities/27502a79-81a4-496a-b3c2-2682188ae429  -> 404
Opportunity-09  PATCH /opportunities/27502a79-81a4-496a-b3c2-2682188ae429  -> 404
Opportunity-10  PATCH /opportunities/27502a79-81a4-496a-b3c2-2682188ae429/restore  -> 404
Opportunity-13a  POST /opportunities  -> 201
Opportunity-13b  DELETE /opportunities/0ef9b4fc-d6ef-4ed7-ae6a-81bc7e0346a2?soft_delete=true  -> 200
Opportunity-13c  GET /opportunities/0ef9b4fc-d6ef-4ed7-ae6a-81bc7e0346a2  -> 404
Opportunity-13d  PATCH /opportunities/0ef9b4fc-d6ef-4ed7-ae6a-81bc7e0346a2/restore  -> 200
Opportunity-13e  GET /opportunities/0ef9b4fc-d6ef-4ed7-ae6a-81bc7e0346a2  -> 200
Opportunity-13f  DELETE /opportunities/0ef9b4fc-d6ef-4ed7-ae6a-81bc7e0346a2  -> 200
Note-01  POST /notes  -> 201
  id = d2fe3545-d63b-43d7-aeb1-353eb8e9706a
Note-02  GET /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 200
  title=K05-SC6-Note  body=Noi dung K05
Note-03  PATCH /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 200
Note-04  GET /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 200
  title=K05-SC6-Note-sua  body=Noi dung K05
Note-05  GET /notes?filter=id[eq]:d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 200
  so ban ghi = 1
Note-06  DELETE /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 200
Note-07  GET /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 404
Note-08  DELETE /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 404
Note-09  PATCH /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a  -> 404
Note-10  PATCH /notes/d2fe3545-d63b-43d7-aeb1-353eb8e9706a/restore  -> 404
Note-13a  POST /notes  -> 201
Note-13b  DELETE /notes/c2bb17b5-4626-4f11-99e8-3fc4ed738ac6?soft_delete=true  -> 200
Note-13c  GET /notes/c2bb17b5-4626-4f11-99e8-3fc4ed738ac6  -> 404
Note-13d  PATCH /notes/c2bb17b5-4626-4f11-99e8-3fc4ed738ac6/restore  -> 200
Note-13e  GET /notes/c2bb17b5-4626-4f11-99e8-3fc4ed738ac6  -> 200
Note-13f  DELETE /notes/c2bb17b5-4626-4f11-99e8-3fc4ed738ac6  -> 200
Task-01  POST /tasks  -> 201
  id = 6279f522-35da-45aa-90d0-b92a3c2cd5bc
Task-02  GET /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 200
  title=K05-SC6-Task  status=TODO
Task-03  PATCH /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 200
Task-04  GET /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 200
  title=K05-SC6-Task  status=DONE
Task-05  GET /tasks?filter=id[eq]:6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 200
  so ban ghi = 1
Task-06  DELETE /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 200
Task-07  GET /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 404
Task-08  DELETE /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 404
Task-09  PATCH /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc  -> 404
Task-10  PATCH /tasks/6279f522-35da-45aa-90d0-b92a3c2cd5bc/restore  -> 404
Task-13a  POST /tasks  -> 201
Task-13b  DELETE /tasks/0e86fd47-c182-42c9-95fb-076e5720d68d?soft_delete=true  -> 200
Task-13c  GET /tasks/0e86fd47-c182-42c9-95fb-076e5720d68d  -> 404
Task-13d  PATCH /tasks/0e86fd47-c182-42c9-95fb-076e5720d68d/restore  -> 200
Task-13e  GET /tasks/0e86fd47-c182-42c9-95fb-076e5720d68d  -> 200
Task-13f  DELETE /tasks/0e86fd47-c182-42c9-95fb-076e5720d68d  -> 200
```

## E-11. Căn cứ đối chiếu trích từ `schema/core.openapi.json` (bản của nhóm, Twenty v2.45.6)

```
components.parameters.limit:
  {"name": "limit", "in": "query", "schema": {"type": "integer", "minimum": 0, "maximum": 200, "default": 60}}
components.parameters.softDelete:
  {"name": "soft_delete", "in": "query", "schema": {"type": "boolean", "default": false},
   "description": "If true, soft deletes the objects. If false, objects are permanently deleted."}
paths./batch/companies.post.requestBody: {"type": "array", "items": {"$ref": "#/components/schemas/Company"}}
paths./batch/companies.post.responses: 201, 400, 401
paths./companies/{id}.get.responses: 200, 400, 401
paths./companies/{id}.patch.responses: 200, 400, 401
paths./companies/{id}.delete.responses: 200, 400, 401
paths./companies/{id}/restore.patch.responses: 200, 400, 401
components.schemas.Company.properties.domainName.properties.primaryLinkUrl: {"type": "string"}
```
