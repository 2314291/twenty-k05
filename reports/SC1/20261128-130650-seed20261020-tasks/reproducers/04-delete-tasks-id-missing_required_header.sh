#!/usr/bin/env bash
# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash 04-delete-tasks-id-missing_required_header.sh
# Operation : DELETE /tasks/{id}
# Check     : missing_required_header  (MissingHeaderNotRejected, mức medium)
# Seed      : 20261020   Phase: coverage   Số lần gặp: 1
# Got 403 when missing required 'Authorization' header, expected 401

curl -sS -i \
  -X DELETE \
  'http://localhost:3001/rest/tasks/d8ce1ef0-dd5f-c5f1-2c52-c16613f9b8e1?soft_delete=true'
