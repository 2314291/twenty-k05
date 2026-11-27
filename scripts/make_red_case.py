#!/usr/bin/env python3
"""Tạo ca đỏ cố ý (red case) để chứng minh bộ test BẮT được lỗi: sửa kiểu của một trường trong
bản sao của schema (schema/core.red.openapi.json). Mặc định đổi `CompanyForResponse.name` từ string sang integer:
server vẫn trả chuỗi nên check response_schema_conformance phải ĐỎ.

    python scripts/make_red_case.py [--schema schema/core.openapi.json] [--component Company] [--field employees]
    python scripts/run_k05.py SC1 --schema schema/core.red.openapi.json --label RED

Không sửa file gốc. Nếu không chỉ định, script tự tìm một trường kiểu integer/number trong thành phần
có tên bắt đầu bằng 'Company' và in rõ nó đã đổi gì (ghi vào báo cáo).
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

import k05_common as c


def find_target(doc: dict, component: str | None, field: str | None):
    """Chọn (thành phần, trường) để đổi kiểu. Ưu tiên schema PHẢN HỒI (`...ForResponse`) vì check
    response_schema_conformance so sánh phản hồi thật với schema phản hồi. Trường `name` luôn có trong phản hồi."""
    schemas = doc.get("components", {}).get("schemas", {})
    if component:
        names = [component] if component in schemas else []
    else:
        names = sorted([n for n in schemas if re.match(r"^Company", n)],
                       key=lambda n: (not n.endswith("ForResponse"), " " in n, len(n)))
    for n in names:
        props = schemas[n].get("properties", {})
        cands = [field] if field else ["name", "position"] + list(props)
        for k in cands:
            if k in props and props[k].get("type") in ("string", "integer", "number"):
                return n, k
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--schema", default="schema/core.openapi.json")
    ap.add_argument("--out", default="schema/core.red.openapi.json")
    ap.add_argument("--component")
    ap.add_argument("--field")
    args = ap.parse_args()
    src = c.ROOT / args.schema
    doc = json.loads(src.read_text(encoding="utf-8"))
    hit = find_target(doc, args.component, args.field)
    if not hit:
        sys.exit("Không tìm được trường để đổi kiểu. Chỉ định --component và --field "
                 "(xem components.schemas trong file schema).")
    comp, field = hit
    red = copy.deepcopy(doc)
    old = red["components"]["schemas"][comp]["properties"][field]
    new_type = "integer" if old.get("type") == "string" else "string"
    red["components"]["schemas"][comp]["properties"][field] = {"type": new_type, "x-k05-red-case": f"was {json.dumps(old)}"}
    out = c.ROOT / args.out
    out.write_text(json.dumps(red, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Ca đỏ: components.schemas['{comp}'].properties['{field}']  {json.dumps(old)} -> {{'type': '{new_type}'}}")
    print(f"Đã ghi {out.relative_to(c.ROOT)}. Chạy: python scripts/run_k05.py SC1 --schema {args.out} --label RED")
    print("Kỳ vọng: response_schema_conformance ĐỎ (kiểu trong phản hồi thật khác kiểu schema khai báo).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
