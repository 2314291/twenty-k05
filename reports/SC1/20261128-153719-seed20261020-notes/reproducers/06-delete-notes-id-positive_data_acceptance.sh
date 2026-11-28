#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 06-delete-notes-id-positive_data_acceptance.sh
# Operation : DELETE /notes/{id}
# Check     : positive_data_acceptance  (RejectedPositiveData, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 49
# Valid data should have been accepted
# Expected: 2xx, 3xx, 401, 403, 404, 409, 429, 5xx

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/notes/333f7cec-8cb4-d2bd-c744-7cd8c4656e45?soft_delete=false' \
  -H "Authorization: Bearer $TWENTY_API_KEY"
