#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 47-post-batch-people-negative_data_rejection.sh
# Operation : POST /batch/people
# Check     : negative_data_rejection  (AcceptedNegativeData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 3
# Invalid data should have been rejected
# Expected: 400, 401, 403, 404, 405, 406, 409, 415, 422, 428, 429, 5xx
# Invalid component: in body - array with invalid items: companyId: Incorrect type
# Còn 1 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/batch/people?depth=0&fields=id%2Cname&upsert=true' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '[{"name": {"firstName": "", "lastName": ""}, "emails": {"primaryEmail": "", "additionalEmails": []}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "jobTitle": "", "phones": {"additionalPhones": [], "primaryPhoneCountryCode": "", "primaryPhoneCallingCode": "", "primaryPhoneNumber": ""}, "avatarUrl": "", "avatarFile": [], "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": null}]'
