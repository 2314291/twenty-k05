#!/usr/bin/env python3
"""Kiểm tra logic của hooks/k05_hooks.py bằng đối tượng giả (không cần Schemathesis, không cần Twenty).

    python scripts/selftest/test_hooks.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent.parent
TMP = Path(tempfile.mkdtemp(prefix="k05-hooks-"))
MANIFEST = TMP / "seed-manifest.json"
SEED_IDS = [f"00000000-0000-4000-8000-00000000000{i}" for i in range(1, 4)]
MANIFEST.write_text(json.dumps({"companies": SEED_IDS, "people": []}), encoding="utf-8")
os.environ.update(K05_SEED_MANIFEST=str(MANIFEST), K05_RUN_START="2026-10-19T14:00:00.000Z")


def load_hooks():
    spec = importlib.util.spec_from_file_location("k05_hooks_under_test", ROOT / "hooks" / "k05_hooks.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def case(method, path, path_parameters=None, query=None, mode="positive"):
    meta = SimpleNamespace(generation=SimpleNamespace(mode=SimpleNamespace(value=mode)))
    return SimpleNamespace(method=method, path=path, path_parameters=path_parameters, query=query, meta=meta)


h = load_hooks()
GUARD = 'createdAt[gte]:"2026-10-19T14:00:00.000Z"'
RANDOM_UUID = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
failures = []


def check(name, cond):
    print(("ĐẠT  " if cond else "LỖI  ") + name)
    if not cond:
        failures.append(name)


# --- before_call: bảo vệ dữ liệu ---
c = case("DELETE", "/companies", query={"soft_delete": "false", "filter": 'or(createdAt[gte]:"2024-01-01",not(id[is]:NULL))'})
h.before_call(None, c, {})
check("DELETE hàng loạt: filter bị bọc and(...)", c.query["filter"] == f'and(or(createdAt[gte]:"2024-01-01",not(id[is]:NULL)),{GUARD})')
check("DELETE hàng loạt: giữ nguyên tham số khác", c.query["soft_delete"] == "false")

c = case("DELETE", "/companies", query={})
h.before_call(None, c, {})
check("DELETE hàng loạt không filter: thêm filter chặn", c.query["filter"] == GUARD)

c = case("PATCH", "/people", query=None)
h.before_call(None, c, {})
check("PATCH hàng loạt (query None): thêm filter chặn", c.query == {"filter": GUARD})

c = case("PATCH", "/companies", query={"filter": ["a[eq]:1", 5]})
h.before_call(None, c, {})
check("filter dạng mảng (ca âm): bọc phần tử chuỗi, giữ phần tử lạ", c.query["filter"] == [f"and(a[eq]:1,{GUARD})", 5])

for method, path in [("GET", "/companies"), ("POST", "/companies"), ("PATCH", "/companies/restore"),
                     ("PATCH", "/companies/{id}"), ("DELETE", "/companies/{id}"), ("POST", "/batch/companies")]:
    c = case(method, path, query={"filter": "x[eq]:1"})
    h.before_call(None, c, {})
    check(f"không đụng {method} {path}", c.query == {"filter": "x[eq]:1"})

os.environ["K05_PROTECT_DATA"] = "0"
c = case("DELETE", "/companies", query={"filter": "x[eq]:1"})
h.before_call(None, c, {})
check("K05_PROTECT_DATA=0 tắt bảo vệ", c.query == {"filter": "x[eq]:1"})
os.environ["K05_PROTECT_DATA"] = "1"

# --- map_case: id có thật ---
c = h.map_case(None, case("GET", "/companies/{id}", {"id": RANDOM_UUID}))
check("GET theo id: UUID ngẫu nhiên -> id trong manifest", c.path_parameters["id"] in SEED_IDS)
first = c.path_parameters["id"]
c = h.map_case(None, case("PATCH", "/companies/{id}/restore", {"id": RANDOM_UUID}))
check("ánh xạ tất định (cùng UUID -> cùng id)", c.path_parameters["id"] == first)

c = h.map_case(None, case("DELETE", "/companies/{id}", {"id": RANDOM_UUID}))
check("DELETE theo id: giữ id ngẫu nhiên", c.path_parameters["id"] == RANDOM_UUID)
c = h.map_case(None, case("GET", "/companies/{id}", {"id": RANDOM_UUID}, mode="negative"))
check("ca âm: giữ nguyên", c.path_parameters["id"] == RANDOM_UUID)
c = h.map_case(None, case("GET", "/companies/{id}", {"id": "khong-phai-uuid"}))
check("id sai định dạng: giữ nguyên", c.path_parameters["id"] == "khong-phai-uuid")
c = h.map_case(None, case("GET", "/people/{id}", {"id": RANDOM_UUID}))
check("đối tượng không có id seed: giữ nguyên", c.path_parameters["id"] == RANDOM_UUID)
c = h.map_case(None, case("GET", "/notes/{id}", {"id": RANDOM_UUID}))
check("đối tượng vắng trong manifest: giữ nguyên", c.path_parameters["id"] == RANDOM_UUID)
c = h.map_case(None, case("GET", "/companies", None))
check("operation không có {id}: không lỗi", c.path_parameters is None)

os.environ["K05_REAL_IDS"] = "0"
c = h.map_case(None, case("GET", "/companies/{id}", {"id": RANDOM_UUID}))
check("K05_REAL_IDS=0 tắt thay id", c.path_parameters["id"] == RANDOM_UUID)

print(f"\n{'ĐẠT' if not failures else 'LỖI'}: {len(failures)} ca lỗi")
sys.exit(1 if failures else 0)
