#!/usr/bin/env python3
"""Kiểm tra mốc dữ liệu của run_k05.py khi đồng hồ máy chủ lệch với máy chạy test (không cần Twenty).

    python scripts/selftest/test_run_k05.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_k05 as r  # noqa: E402

failures = []


def check(name, cond):
    print(("ĐẠT  " if cond else "LỖI  ") + name)
    if not cond:
        failures.append(name)


def fake_http(newest_by_obj):
    def http(method, path, body=None, key=None, **kw):
        obj = path.split("?")[0].strip("/")
        stamp = newest_by_obj.get(obj)
        rows = [{"id": "x", "createdAt": stamp}] if stamp else []
        return 200, {"data": {obj: rows}}, 0.01
    return http


now = dt.datetime.now(dt.timezone.utc)
ahead = (now + dt.timedelta(seconds=7)).strftime("%Y-%m-%dT%H:%M:%S.123Z")
behind = (now - dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

r.c.http = fake_http({"companies": behind, "tasks": ahead})
mark, src = r.data_mark("k")
check("đồng hồ máy chủ đi trước 7 giây: mốc = createdAt mới nhất + 1 ms", mark.endswith(".124Z") and mark > ahead and "máy chủ" in src)

r.c.http = fake_http({"companies": behind})
mark, src = r.data_mark("k")
check("máy chủ không đi trước: mốc theo giờ máy chạy test, sau createdAt mới nhất", mark > behind and src == "giờ máy chạy test")

r.c.http = fake_http({})
mark, src = r.data_mark("k")
check("DB rỗng: vẫn có mốc", mark.endswith("Z") and src == "giờ máy chạy test")

mark, src = r.data_mark(None)
check("không có key: không gọi máy chủ, dùng giờ máy", src == "giờ máy chạy test")


def refused(*a, **k):
    raise SystemExit("Không kết nối được")


r.c.http = refused
mark, src = r.data_mark("k")
check("không kết nối được máy chủ: không dừng chương trình, dùng giờ máy", src == "giờ máy chạy test")

print(f"\n{'ĐẠT' if not failures else 'LỖI'}: {len(failures)} ca lỗi")
sys.exit(1 if failures else 0)
