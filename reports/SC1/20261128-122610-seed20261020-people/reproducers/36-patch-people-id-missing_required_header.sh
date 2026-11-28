#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 36-patch-people-id-missing_required_header.sh
# Operation : PATCH /people/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 200 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X PATCH \
  'http://localhost:3001/rest/people/a25319c3-8651-4789-8388-f0f61cf66831?depth=0&fields=id%2Cname' \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary '{"name": {"firstName": "", "lastName": ""}, "emails": {"primaryEmail": "", "additionalEmails": []}, "linkedinLink": {"primaryLinkLabel": "", "primaryLinkUrl": "", "secondaryLinks": []}, "jobTitle": "", "phones": {"additionalPhones": [], "primaryPhoneCountryCode": "", "primaryPhoneCallingCode": "", "primaryPhoneNumber": ""}, "avatarUrl": "", "avatarFile": [], "position": 0, "createdBy": {"source": "EMAIL"}, "updatedBy": {"source": "EMAIL"}, "companyId": "bd7b1b6e-1d4a-4787-a191-fda42d4e47b5"}'
