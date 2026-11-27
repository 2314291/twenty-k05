#!/usr/bin/env python3
"""Thống kê gộp mọi lần chạy Schemathesis trong reports/ (số liệu cho báo cáo Phần G). Người viết: Quang.

Đọc reports/<SCx>/<lần chạy>/summary.json (do summarize.py ghi) và run-config.json (do run_k05.py ghi), rồi ghi
reports/thong-ke.md gồm:
  1. Tổng quan theo kịch bản và object: operation đã test, test case, operation đủ 50 ca, 5xx, nhóm lỗi, tái lập.
  2. Lỗi theo loại kiểm tra (check) và object, cho từng kịch bản.
  3. Nhóm lỗi gộp xuyên object (cùng operation, check, loại lỗi): giúp gộp bảng lỗi và RCA xuyên module.

Mỗi (kịch bản, nhãn, biến thể, object) lấy lần chạy MỚI NHẤT; nếu có lần trước đó thì so tập nhóm lỗi để đo tái lập.

    python scripts/thong_ke.py
    python scripts/thong_ke.py --reports reports --out reports/thong-ke.md
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):  # console Windows không in được tiếng Việt
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent
OBJECTS = ["companies", "people", "opportunities", "notes", "tasks"]
ALL = "5 object"
CHECK_LABEL = {  # mã bất biến theo Phan_Cong_module/KICH_BAN_K05.md
    "not_a_server_error": "I1 không 5xx",
    "status_code_conformance": "I2 mã trạng thái",
    "response_schema_conformance": "I3 body đúng schema",
    "negative_data_rejection": "I4 từ chối dữ liệu sai",
    "positive_data_acceptance": "I5 nhận dữ liệu đúng",
    "ignored_auth": "I6 xác thực (ignored_auth)",
    "missing_required_header": "I6 xác thực (thiếu header)",
    "content_type_conformance": "I7 Content-Type",
}


def run_meta(run_dir: Path) -> dict:
    cfg_file = run_dir / "run-config.json"
    cfg = json.loads(cfg_file.read_text(encoding="utf-8")) if cfg_file.exists() else {}
    name = run_dir.name
    obj = cfg.get("object") or next((o for o in OBJECTS if f"-{o}" in name), None)
    scenario = cfg.get("scenario") or run_dir.parent.name
    if not obj:
        obj = "companies" if scenario == "SC1" else ALL
    variant = cfg.get("variant") or next((v for v in ("none", "wrong", "limited") if f"-{v}" in name), "valid")
    label = "RED" if "-RED" in name or ".red." in str(cfg.get("schema", "")) else ""
    return {"scenario": scenario, "object": obj, "variant": variant, "label": label, "dir": run_dir}


def groups(summary: dict) -> set[tuple]:
    if "failures" in summary:
        return {(f["operation"], f["check"], f["type"]) for f in summary["failures"]}
    out = set()  # summary.json cũ: chỉ có chuỗi "op|check|type|n"
    for s in summary.get("signature", {}).get("unique_failures", []):
        parts = s.split("|")
        if len(parts) >= 3:
            out.add(tuple(parts[:3]))
    return out


def generic_op(op: str) -> str:
    return re.sub(r"/(?:batch/)?(" + "|".join(OBJECTS) + r")(?=/|$)", lambda m: m.group(0).replace(m.group(1), "{obj}"), op)


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def scenario_name(m: dict) -> str:
    s = m["scenario"] + (f" {m['label']}" if m["label"] else "")
    return s + (f" ({m['variant']})" if m["variant"] != "valid" else "")


def collect(reports: Path) -> dict:
    runs = collections.defaultdict(list)
    for sj in sorted(reports.glob("SC*/*/summary.json")):
        m = run_meta(sj.parent)
        m["summary"] = json.loads(sj.read_text(encoding="utf-8"))
        runs[(m["scenario"], m["label"], m["variant"], m["object"])].append(m)
    for v in runs.values():
        v.sort(key=lambda m: m["dir"].name)
    return runs


def obj_order(o: str) -> int:
    return OBJECTS.index(o) if o in OBJECTS else len(OBJECTS)


def render(runs: dict) -> str:
    lines = ["# Thống kê kết quả K05 (Phần G)", "",
             "Tạo bởi `python scripts/thong_ke.py` từ `reports/*/*/summary.json`. Mỗi dòng là lần chạy mới nhất; "
             "cột tái lập so tập nhóm lỗi (operation, check, loại) với lần chạy trước đó của cùng kịch bản và object.", ""]
    if not runs:
        return "\n".join(lines + ["Chưa có lần chạy nào có `summary.json`."])

    rows, latest = [], {}
    for key in sorted(runs, key=lambda k: (k[0], k[1], k[2], obj_order(k[3]))):
        hist = runs[key]
        cur = hist[-1]
        latest[key] = cur
        s = cur["summary"]
        g = groups(s)
        if len(hist) > 1:
            prev = groups(hist[-2]["summary"])
            union = len(g | prev) or 1
            rep = f"{len(g & prev) / union:.0%} ({hist[-2]['dir'].name})"
        else:
            rep = "chưa chạy lần 2"
        tested = len(s.get("tested", []))
        total = s.get("schema_operations") or "?"
        cases = s.get("test_cases", sum(s.get("signature", {}).get("per_op_cases", {}).values()))
        ge50 = s.get("ops_ge_50", sum(1 for n in s.get("signature", {}).get("per_op_cases", {}).values() if n >= 50))
        fxx = s.get("five_xx", sum(n for code, n in s.get("signature", {}).get("codes", {}).items() if int(code) >= 500))
        rows.append([scenario_name(cur), cur["object"], f"`{cur['dir'].name}`", f"{tested}/{total}", cases,
                     f"{ge50}/{tested}", fxx, len(g), rep])
    lines += ["## 1. Tổng quan theo kịch bản và object", "", md_table(
        ["Kịch bản", "Object", "Lần chạy", "Operation đã test", "Test case", "Operation ≥ 50 ca", "5xx", "Nhóm lỗi", "Tái lập"],
        rows), ""]

    lines += ["## 2. Lỗi theo loại kiểm tra và object", "",
              "Mỗi ô: số lần check báo lỗi / số lần check được chạy.", ""]
    by_sc = collections.defaultdict(list)
    for key, m in latest.items():
        by_sc[scenario_name(m)].append(m)
    for sc in sorted(by_sc):
        ms = sorted(by_sc[sc], key=lambda m: obj_order(m["object"]))
        names = sorted({n for m in ms for n in m["summary"].get("checks", {})},
                       key=lambda n: list(CHECK_LABEL).index(n) if n in CHECK_LABEL else 99)
        lines += [f"### {sc}", ""]
        if not names:
            lines += ["(`summary.json` cũ, không có số theo check; chạy lại `python scripts/summarize.py <thư mục>`.)", ""]
            continue
        trs = []
        for n in names:
            cells = []
            for m in ms:
                c = m["summary"].get("checks", {}).get(n)
                cells.append(f"{c['failure']}/{c['failure'] + c['success']}" if c else "—")
            trs.append([CHECK_LABEL.get(n, n), *cells])
        lines += [md_table(["Check", *[m["object"] for m in ms]], trs), ""]

    lines += ["## 3. Nhóm lỗi gộp xuyên object", "",
              "Cùng một operation (đổi tên object thành `{obj}`), cùng check và loại lỗi được gộp một dòng.", ""]
    merged = collections.defaultdict(lambda: {"objects": set(), "count": 0})
    for key, m in latest.items():
        s = m["summary"]
        counts = {(f["operation"], f["check"], f["type"]): f["count"] for f in s.get("failures", [])}
        for op, ck, ty in groups(s):
            g = merged[(scenario_name(m), generic_op(op), ck, ty)]
            g["objects"].add(m["object"])
            g["count"] += counts.get((op, ck, ty), 0)
    trs = [[sc, f"`{op}`", CHECK_LABEL.get(ck, ck), ty or "—", len(v["objects"]),
            ", ".join(sorted(v["objects"], key=obj_order)), v["count"] or "—"]
           for (sc, op, ck, ty), v in sorted(merged.items(), key=lambda kv: (kv[0][0], -len(kv[1]["objects"]), kv[0][1], kv[0][2]))]
    lines += [md_table(["Kịch bản", "Operation", "Check", "Loại lỗi", "Số object", "Object", "Lần gặp"], trs) if trs
              else "Không có nhóm lỗi.", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--reports", default=str(ROOT / "reports"))
    ap.add_argument("--out", help="mặc định <reports>/thong-ke.md")
    args = ap.parse_args()
    reports = Path(args.reports)
    out = Path(args.out) if args.out else reports / "thong-ke.md"
    text = render(collect(reports))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\nĐã ghi {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
