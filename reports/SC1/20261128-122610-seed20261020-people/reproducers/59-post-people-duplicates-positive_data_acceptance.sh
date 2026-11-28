#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 59-post-people-duplicates-positive_data_acceptance.sh
# Operation : POST /people/duplicates
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 89
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx
# Còn 4 biến thể khác của lỗi này (xem summary.md)

curl -sS -i \
  -X POST \
  'http://localhost:3001/rest/people/duplicates?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"ids": ["67b5b1e6-88ad-46c2-aab4-529cdb984145"], "data": [{"name": {"firstName": "", "lastName": ""}, "emails": {"primaryEmail": "", "additionalEmails": []}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "jobTitle": "", "phones": {"additionalPhones": [], "primaryPhoneCountryCode": "", "primaryPhoneCallingCode": "", "primaryPhoneNumber": ""}, "avatarUrl": "", "avatarFile": [], "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "WEBHOOK"}, "companyId": "e3e70682-c209-1cac-a29f-6fbed82c07cd"}]}'
