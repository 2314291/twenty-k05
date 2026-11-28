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

# --- seed_check: đếm bản ghi seed còn sau lần chạy (phát hiện lần chạy bị lệch như D-11 ngày 27/11) ---
import json as _json  # noqa: E402
import tempfile as _tf  # noqa: E402
from urllib.parse import parse_qs, urlparse  # noqa: E402

SEED = {"companies": [f"00000000-0000-4000-8000-0000000000{i:02d}" for i in range(3)],
        "people": [f"00000000-0000-4000-8000-0000000001{i:02d}" for i in range(2)], "notes": []}
r.MANIFEST = Path(_tf.mkdtemp()) / "seed-manifest.json"
r.MANIFEST.write_text(_json.dumps(SEED), encoding="utf-8")
seen = []


def fake_db(alive, status=200):
    def http(method, path, body=None, key=None, **kw):
        u = urlparse(path)
        obj = u.path.strip("/")
        flt = parse_qs(u.query).get("filter", [""])[0]
        seen.append((method, obj, flt))
        asked = _json.loads(flt[len("id[in]:"):]) if flt.startswith("id[in]:") else []
        return status, {"data": {obj: [{"id": i} for i in asked if i in alive]}}, 0.01
    return http


r.c.http = fake_db(set(SEED["companies"]) | set(SEED["people"]))
check("seed còn đủ: [còn, tổng] theo từng object có seed", r.seed_check("k") == {"companies": [3, 3], "people": [2, 2]})
check("seed_check chỉ GET, lọc id[in] đúng danh sách seed",
      all(m == "GET" for m, _, _ in seen) and seen[0][2] == "id[in]:" + _json.dumps(SEED["companies"], separators=(",", ":")))
r.c.http = fake_db({SEED["people"][0]})
check("mất seed (D-11): companies 0/3, people 1/2", r.seed_check("k") == {"companies": [0, 3], "people": [1, 2]})
r.c.http = fake_db(set(), status=500)
check("máy chủ lỗi: bỏ qua object đó, không báo mất seed nhầm", r.seed_check("k") == {})
check("không có key: không kiểm", r.seed_check(None) == {})
r.c.http = refused
check("không kết nối được: không dừng chương trình", r.seed_check("k") == {})

print(f"\n{'ĐẠT' if not failures else 'LỖI'}: {len(failures)} ca lỗi")
sys.exit(1 if failures else 0)
