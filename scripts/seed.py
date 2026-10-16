#!/usr/bin/env python3
"""Nạp dữ liệu mẫu có tiền tố K05- vào Twenty qua REST (chỉ localhost).

Tạo: N công ty, N người (gắn công ty), N cơ hội (gắn công ty + người), ghi ID vào
reports/seed-manifest.json để dọn lại bằng --cleanup. Chia lô <= 50 (giới hạn batch thật của
v2.45.6 là 200, xem docs/architecture.md mục 5).

    python scripts/seed.py --count 30
    python scripts/seed.py --cleanup

Tên trường đã đối chiếu với schema/core.openapi.json thật của v2.45.6 (Company, Person, Opportunity).
Lưu ý Company KHÔNG có trường `employees` trong bản này. Nếu API trả 400 hãy so lại với schema.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import k05_common as c

STAGES = ["NEW", "SCREENING", "MEETING", "PROPOSAL", "CUSTOMER"]
CITIES = ["Da Lat", "Ha Noi", "Ho Chi Minh", "Da Nang", "Hue"]
MANIFEST = c.ROOT / "reports" / "seed-manifest.json"
CHUNK = 50


def build_company(i: int, rnd: random.Random) -> dict:
    return {
        "name": f"K05-Company-{i:03d}",
        "domainName": {"primaryLinkUrl": f"https://k05-company-{i:03d}.example.com"},
        "address": {"addressCity": rnd.choice(CITIES)},
        "annualRevenue": {"amountMicros": rnd.randint(1, 900) * 1_000_000, "currencyCode": "USD"},
    }


def build_person(i: int, company_id: str) -> dict:
    return {
        "name": {"firstName": f"K05Ho{i:03d}", "lastName": f"K05Ten{i:03d}"},
        "emails": {"primaryEmail": f"k05.person{i:03d}@example.com"},
        "jobTitle": "Tester",
        "companyId": company_id,
    }


def build_opportunity(i: int, company_id: str, person_id: str, rnd: random.Random) -> dict:
    return {
        "name": f"K05-Opportunity-{i:03d}",
        "amount": {"amountMicros": rnd.randint(1, 500) * 1_000_000, "currencyCode": "USD"},
        "stage": STAGES[i % len(STAGES)],
        "closeDate": "2026-12-31T00:00:00.000Z",
        "companyId": company_id,
        "pointOfContactId": person_id,
    }


def ids_of(parsed) -> list[str]:
    recs = c.first_record(parsed)
    if isinstance(recs, dict):
        recs = [recs]
    return [r["id"] for r in (recs or []) if isinstance(r, dict) and "id" in r]


def post_batch(plural: str, rows: list[dict], key: str) -> list[str]:
    ids: list[str] = []
    for i in range(0, len(rows), CHUNK):
        chunk = rows[i:i + CHUNK]
        status, parsed, _ = c.http("POST", f"/batch/{plural}", chunk, key)
        if status not in (200, 201):
            sys.exit(f"POST /batch/{plural} trả {status}: {json.dumps(parsed, ensure_ascii=False)[:400]}")
        ids += ids_of(parsed)
    return ids


def cleanup(key: str) -> None:
    if not MANIFEST.exists():
        sys.exit("Không có reports/seed-manifest.json, không có gì để dọn.")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for plural in ("opportunities", "people", "companies"):  # xoá bản ghi phụ thuộc trước
        for rid in manifest.get(plural, []):
            status, _, _ = c.http("DELETE", f"/{plural}/{rid}", key=key)
            print(f"DELETE /{plural}/{rid} -> {status}")
    MANIFEST.unlink()
    print("Đã dọn xong.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--count", type=int, default=30, help="số bản ghi mỗi loại (mặc định 30)")
    ap.add_argument("--seed", type=int, default=20261020)
    ap.add_argument("--cleanup", action="store_true")
    args = ap.parse_args()

    c.load_env()
    c.assert_localhost(c.base_url())
    key = c.api_key()
    if args.cleanup:
        cleanup(key)
        return 0

    rnd = random.Random(args.seed)
    comp_ids = post_batch("companies", [build_company(i, rnd) for i in range(args.count)], key)
    person_ids = post_batch("people", [build_person(i, comp_ids[i % len(comp_ids)]) for i in range(args.count)], key)
    opp_ids = post_batch(
        "opportunities",
        [build_opportunity(i, comp_ids[i % len(comp_ids)], person_ids[i % len(person_ids)], rnd) for i in range(args.count)],
        key,
    )
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"companies": comp_ids, "people": person_ids, "opportunities": opp_ids}, indent=2), encoding="utf-8")
    print(f"Đã tạo {len(comp_ids)} công ty, {len(person_ids)} người, {len(opp_ids)} cơ hội. Manifest: {MANIFEST.relative_to(c.ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
