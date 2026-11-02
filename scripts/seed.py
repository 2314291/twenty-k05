#!/usr/bin/env python3
"""Nạp dữ liệu mẫu có tiền tố K05- vào Twenty qua REST (chỉ localhost).

Tạo: N công ty, N người (gắn công ty), N cơ hội (gắn công ty + người), N ghi chú, N việc cần làm,
ghi ID vào reports/seed-manifest.json để dọn lại bằng --cleanup. Chia lô <= 50 (giới hạn batch thật của
v2.45.6 là 200, xem docs/architecture.md mục 5). Đủ 5 đối tượng trong phạm vi K05.

    python scripts/seed.py --count 30
    python scripts/seed.py --cleanup

Tên trường đã đối chiếu với schema/core.openapi.json thật của v2.45.6 (Company, Person, Opportunity,
Note, Task). Company KHÔNG có trường `employees` trong bản này. Note có `title`, `bodyV2.markdown`;
Task có thêm `status` (TODO, IN_PROGRESS, DONE) và `dueAt`. Nếu API trả 400 hãy so lại với schema.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import k05_common as c

STAGES = ["NEW", "SCREENING", "MEETING", "PROPOSAL", "CUSTOMER"]
TASK_STATUSES = ["TODO", "IN_PROGRESS", "DONE"]
CITIES = ["Da Lat", "Ha Noi", "Ho Chi Minh", "Da Nang", "Hue"]
MANIFEST = c.ROOT / "reports" / "seed-manifest.json"
CHUNK = 50
MAX_RETRY = 10  # số lần thử lại khi bị giới hạn tốc độ (429)


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


def build_note(i: int) -> dict:
    return {
        "title": f"K05-Note-{i:03d}",
        "bodyV2": {"markdown": f"Ghi chú mẫu K05 số {i:03d}"},
    }


def build_task(i: int) -> dict:
    return {
        "title": f"K05-Task-{i:03d}",
        "bodyV2": {"markdown": f"Việc mẫu K05 số {i:03d}"},
        "status": TASK_STATUSES[i % len(TASK_STATUSES)],
        "dueAt": "2026-12-31T00:00:00.000Z",
    }


def ids_of(parsed) -> list[str]:
    recs = c.first_record(parsed)
    if isinstance(recs, dict):
        recs = [recs]
    return [r["id"] for r in (recs or []) if isinstance(r, dict) and "id" in r]


def call(method: str, path: str, body=None, key: str | None = None):
    """Gọi c.http, gặp 429 (mặc định Twenty cho 100 request/60 giây mỗi khoá) thì chờ rồi gửi lại."""
    for _ in range(MAX_RETRY):
        status, parsed, secs = c.http(method, path, body, key)
        if status != 429:
            return status, parsed, secs
        wait = parsed.get("retryAfterSeconds", 1) if isinstance(parsed, dict) else 1
        wait = max(1, min(int(wait or 1), 60))
        print(f"  {method} {path} bị giới hạn tốc độ (429), chờ {wait}s rồi thử lại")
        time.sleep(wait)
    return status, parsed, secs


def post_batch(plural: str, rows: list[dict], key: str) -> list[str]:
    ids: list[str] = []
    for i in range(0, len(rows), CHUNK):
        chunk = rows[i:i + CHUNK]
        status, parsed, _ = call("POST", f"/batch/{plural}", chunk, key)
        if status not in (200, 201):
            sys.exit(f"POST /batch/{plural} trả {status}: {json.dumps(parsed, ensure_ascii=False)[:400]}")
        ids += ids_of(parsed)
    return ids


def cleanup(key: str) -> None:
    if not MANIFEST.exists():
        sys.exit("Không có reports/seed-manifest.json, không có gì để dọn.")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    left: dict[str, list[str]] = {}
    for plural in ("tasks", "notes", "opportunities", "people", "companies"):  # xoá bản ghi phụ thuộc trước
        for rid in manifest.get(plural, []):
            status, _, _ = call("DELETE", f"/{plural}/{rid}", key=key)
            print(f"DELETE /{plural}/{rid} -> {status}")
            if status not in (200, 204, 404):  # 404: đã xoá từ trước
                left.setdefault(plural, []).append(rid)
    if left:
        MANIFEST.write_text(json.dumps(left, indent=2), encoding="utf-8")
        n = sum(len(v) for v in left.values())
        sys.exit(f"Còn {n} bản ghi chưa xoá được, đã giữ lại trong manifest. Chạy lại --cleanup sau.")
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
    note_ids = post_batch("notes", [build_note(i) for i in range(args.count)], key)
    task_ids = post_batch("tasks", [build_task(i) for i in range(args.count)], key)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(
            {"companies": comp_ids, "people": person_ids, "opportunities": opp_ids, "notes": note_ids, "tasks": task_ids},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"Đã tạo {len(comp_ids)} công ty, {len(person_ids)} người, {len(opp_ids)} cơ hội, "
        f"{len(note_ids)} ghi chú, {len(task_ids)} việc. Manifest: {MANIFEST.relative_to(c.ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
