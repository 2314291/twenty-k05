#!/usr/bin/env python3
"""Chạy 3 luồng nghiệp vụ mẫu qua REST và lưu bằng chứng (key đã redact) vào evidence/.

  F1  Tạo Company
  F2  Tạo Person gắn Company
  F3  Đổi stage của Opportunity (NEW -> MEETING)

    python scripts/business_flows.py

Mỗi bước ghi: request, status, thời gian, phần thân phản hồi rút gọn. Dùng làm bằng chứng mục C/E
của báo cáo. Dọn dữ liệu: các bản ghi tạo ra có tên 'K05-FLOW-*' và được xoá cuối script
(dùng --keep để giữ lại).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json

import k05_common as c


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--keep", action="store_true", help="không xoá dữ liệu sau khi chạy")
    args = ap.parse_args()
    c.load_env()
    c.assert_localhost(c.base_url())
    key = c.api_key()

    log: list[dict] = []

    def step(name, method, path, body=None):
        status, parsed, secs = c.http(method, path, body, key)
        log.append({"step": name, "request": f"{method} /rest{path}", "body": body, "status": status,
                    "seconds": round(secs, 3), "response": parsed})
        print(f"[{name}] {method} {path} -> {status} ({secs:.2f}s)")
        return status, parsed

    ok = True
    # F1
    s, p = step("F1 tạo Company", "POST", "/companies", {"name": "K05-FLOW-Company",
                "domainName": {"primaryLinkUrl": "https://k05-flow.example.com"}})
    company = c.first_record(p) or {}
    cid = company.get("id") if isinstance(company, dict) else None
    ok &= s in (200, 201) and bool(cid)
    # F2
    pid = None
    if cid:
        s, p = step("F2 tạo Person gắn Company", "POST", "/people", {
            "name": {"firstName": "K05", "lastName": "FLOW"}, "emails": {"primaryEmail": "k05.flow@example.com"},
            "companyId": cid})
        person = c.first_record(p) or {}
        pid = person.get("id") if isinstance(person, dict) else None
        ok &= s in (200, 201) and bool(pid)
        s, p = step("F2b đọc lại Person", "GET", f"/people/{pid}") if pid else (0, None)
    # F3
    oid = None
    if cid:
        s, p = step("F3a tạo Opportunity (NEW)", "POST", "/opportunities", {
            "name": "K05-FLOW-Opportunity", "stage": "NEW", "companyId": cid, **({"pointOfContactId": pid} if pid else {})})
        opp = c.first_record(p) or {}
        oid = opp.get("id") if isinstance(opp, dict) else None
        ok &= s in (200, 201) and bool(oid)
    if oid:
        s, p = step("F3b đổi stage -> MEETING", "PATCH", f"/opportunities/{oid}", {"stage": "MEETING"})
        ok &= s == 200
        s, p = step("F3c đọc lại Opportunity", "GET", f"/opportunities/{oid}")
        rec = c.first_record(p)
        stage = rec.get("stage") if isinstance(rec, dict) else None
        print(f"    stage hiện tại = {stage!r} (kỳ vọng 'MEETING')")
        ok &= stage == "MEETING"

    if not args.keep:
        for plural, rid in (("opportunities", oid), ("people", pid), ("companies", cid)):
            if rid:
                step(f"dọn {plural}", "DELETE", f"/{plural}/{rid}")

    out = c.ROOT / "evidence" / f"business-flows-{dt.datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(c.redact_text(json.dumps(log, ensure_ascii=False, indent=2), [key]), encoding="utf-8")
    print(f"\nKết quả: {'ĐẠT' if ok else 'CÓ BƯỚC LỖI'}. Bằng chứng: {out.relative_to(c.ROOT)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
