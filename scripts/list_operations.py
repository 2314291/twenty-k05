#!/usr/bin/env python3
"""Liệt kê operation trong schema và sinh bảng Markdown (cho báo cáo mục E / mẫu số 80%).

    python scripts/list_operations.py [schema/core.openapi.json] [--md docs/operations.md]
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import k05_common as c

METHODS = ["get", "post", "put", "patch", "delete"]


def object_of(path: str) -> str:
    parts = [p for p in path.strip("/").split("/") if p]
    if parts and parts[0] == "batch":
        parts = parts[1:]
    return parts[0] if parts else "(root)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("schema", nargs="?", default=str(c.ROOT / "schema/core.openapi.json"))
    ap.add_argument("--md", help="Ghi bảng Markdown ra file này")
    args = ap.parse_args()

    doc = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    ops = []
    for path, item in doc.get("paths", {}).items():
        for m in METHODS:
            if m in item:
                ops.append((object_of(path), m.upper(), path, item[m].get("operationId", ""), item[m].get("summary", "")))
    ops.sort()
    by_obj = defaultdict(int)
    for o in ops:
        by_obj[o[0]] += 1

    lines = ["| # | Đối tượng | Method | Đường dẫn | operationId |", "|---|---|---|---|---|"]
    for i, (obj, m, path, opid, _s) in enumerate(ops, 1):
        lines.append(f"| {i} | {obj} | {m} | `{path}` | {opid} |")
    table = "\n".join(lines)
    summary = f"\nTổng: {len(ops)} operation, {len(by_obj)} đối tượng.\n"
    print(table + summary)
    print("Đếm theo đối tượng:", dict(sorted(by_obj.items(), key=lambda kv: -kv[1])))
    if args.md:
        Path(args.md).write_text(f"# Danh sách operation\n\nNguồn: `{args.schema}`\n\n{table}\n{summary}", encoding="utf-8")
        print(f"Đã ghi {args.md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
