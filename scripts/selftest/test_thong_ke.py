#!/usr/bin/env python3
"""Kiểm tra scripts/thong_ke.py trên dữ liệu giả (không cần Schemathesis hay Twenty).

    python scripts/selftest/test_thong_ke.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import thong_ke as t  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="k05-thongke-"))
failures = []


def check(name, cond):
    print(("ĐẠT  " if cond else "LỖI  ") + name)
    if not cond:
        failures.append(name)


def make_run(sc, name, obj, fails, cases=60, variant="valid", schema="schema/core.openapi.json"):
    d = TMP / sc / name
    d.mkdir(parents=True)
    (d / "run-config.json").write_text(json.dumps({"scenario": sc, "object": obj, "variant": variant, "schema": schema}))
    ops = [f"GET /{obj}", f"POST /{obj}", f"GET /{obj}/{{id}}"]
    (d / "summary.json").write_text(json.dumps({
        "tested": ops, "schema_operations": 13, "test_cases": cases * 3, "ops_ge_50": 3, "five_xx": 0,
        "checks": {"not_a_server_error": {"success": cases * 3, "failure": 0},
                   "status_code_conformance": {"success": cases * 3 - len(fails), "failure": len(fails)}},
        "failures": [{"operation": op.replace("{obj}", obj), "check": "status_code_conformance", "type": "UndefinedStatusCode", "count": 4}
                     for op in fails]}))


make_run("SC1", "20261127-100000-seed20261020-companies", "companies", ["GET /{obj}/{id}", "POST /{obj}"])
make_run("SC1", "20261127-110000-seed20261020-companies", "companies", ["GET /{obj}/{id}"])
make_run("SC1", "20261127-120000-seed20261020-people", "people", ["GET /{obj}/{id}"])
make_run("SC1", "20261127-130000-seed20261020-companies-RED", "companies", ["GET /{obj}"], schema="schema/core.red.openapi.json")
make_run("SC5", "20261127-140000-seed20261020-tasks-none", "tasks", [], variant="none")

runs = t.collect(TMP)
check("gom đúng 4 nhóm (SC1 companies, SC1 people, SC1 RED companies, SC5 none tasks)", len(runs) == 4)
text = t.render(runs)
check("lấy lần chạy mới nhất của SC1 companies", "20261127-110000-seed20261020-companies" in text)
check("tái lập = 50% (1 nhóm chung / 2 nhóm hợp)", "50% (20261127-100000-seed20261020-companies)" in text)
check("lần chạy đơn: ghi chưa chạy lần 2", "chưa chạy lần 2" in text)
check("ca đỏ tách riêng thành kịch bản SC1 RED", "| SC1 RED | companies |" in text)
check("SC5 ghi biến thể key", "SC5 (none)" in text)
check("bảng check có tên bất biến", "I2 mã trạng thái" in text and "1/180" in text)
check("gộp xuyên object: GET /{obj}/{id} gặp ở 2 object", "| SC1 | `GET /{obj}/{id}` | I2 mã trạng thái | UndefinedStatusCode | 2 | companies, people | 8 |" in text)
check("generic_op giữ /batch/", t.generic_op("POST /batch/notes") == "POST /batch/{obj}")
check("thư mục rỗng không lỗi", "Chưa có lần chạy" in t.render(t.collect(TMP / "khong-co")))

print(f"\n{'ĐẠT' if not failures else 'LỖI'}: {len(failures)} ca lỗi")
sys.exit(1 if failures else 0)
