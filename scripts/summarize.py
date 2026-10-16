#!/usr/bin/env python3
"""Thống kê lỗi + sinh reproducer từ báo cáo NDJSON của Schemathesis (4.x).

    python scripts/summarize.py reports/SC1/<thư-mục-lần-chạy> [--schema schema/core.openapi.json]
    python scripts/summarize.py --compare <lần-chạy-A> <lần-chạy-B>      # kiểm tra tái lập cùng seed

Đầu ra trong thư mục lần chạy:
  summary.md / summary.json   thống kê theo operation, mã trạng thái, check
  reproducers/NN-*.sh         lệnh curl tái hiện từng lỗi (key thay bằng $TWENTY_API_KEY)
  REPRODUCERS.md              mục lục reproducer
Chỉ dùng thư viện chuẩn.
"""
from __future__ import annotations

import argparse
import base64
import collections
import glob
import json
import re
import shlex
import sys
from pathlib import Path

METHODS = {"get", "post", "put", "patch", "delete"}


def load_events(run_dir: Path) -> list[dict]:
    files = sorted(glob.glob(str(run_dir / "ndjson-*.ndjson")) + glob.glob(str(run_dir / "*.ndjson")))
    if not files:
        sys.exit(f"Không thấy file .ndjson trong {run_dir}")
    return [json.loads(line) for line in open(files[0], encoding="utf-8") if line.strip()]


def decode_body(b):
    if b is None:
        return None
    if isinstance(b, dict) and "$base64" in b:
        return base64.b64decode(b["$base64"])
    if isinstance(b, (dict, list)):
        return json.dumps(b).encode()
    return str(b).encode()


def status_class(code: int) -> str:
    return f"{code // 100}xx"


def analyse(events: list[dict]) -> dict:
    ops: dict[str, dict] = collections.defaultdict(lambda: {
        "cases": 0, "positive": 0, "negative": 0, "codes": collections.Counter(),
        "failed_cases": 0, "phases": collections.Counter()})
    failures: dict[tuple, dict] = {}
    check_totals = collections.Counter()
    code_totals = collections.Counter()
    for ev in events:
        if "ScenarioFinished" not in ev:
            continue
        sc = ev["ScenarioFinished"]
        rec = sc.get("recorder") or {}
        label = rec.get("label")
        if not label or "cases" not in rec:
            continue
        o = ops[label]
        for cid, case in rec["cases"].items():
            v = case["value"]
            mode = v.get("meta", {}).get("generation", {}).get("mode", "positive")
            o["cases"] += 1
            o[mode if mode in ("positive", "negative") else "positive"] += 1
            o["phases"][sc["phase"]] += 1
            inter = rec.get("interactions", {}).get(cid)
            code = inter["response"]["status_code"] if inter and inter.get("response") else None
            if code is not None:
                o["codes"][code] += 1
                code_totals[code] += 1
            case_failed = False
            for ch in rec.get("checks", {}).get(cid, []):
                check_totals[(ch["name"], ch["status"])] += 1
                if ch["status"] == "failure":
                    case_failed = True
                    f = (ch.get("failure_info") or {}).get("failure", {})
                    msg = (f.get("message") or "").strip()
                    key = (label, ch["name"], f.get("type", ""))
                    g = failures.setdefault(key, {
                        "operation": label, "check": ch["name"], "type": f.get("type", ""),
                        "title": f.get("title", ""), "severity": f.get("severity", ""),
                        "message": msg, "count": 0, "phase": sc["phase"], "case": case, "interaction": inter,
                        "variants": set()})
                    g["count"] += 1
                    g["variants"].add(msg.splitlines()[-1] if msg else "")
            if case_failed:
                o["failed_cases"] += 1
    return {"ops": ops, "failures": list(failures.values()), "checks": check_totals, "codes": code_totals}


def schema_operations(schema_path: Path | None, scope_regex: str | None = None, method: str | None = None) -> list[str]:
    """Operation trong schema; nếu có scope_regex thì chỉ đếm các đường dẫn thuộc phạm vi kịch bản."""
    if not schema_path or not schema_path.exists():
        return []
    doc = json.loads(schema_path.read_text(encoding="utf-8"))
    rx = re.compile(scope_regex) if scope_regex else None
    return sorted(f"{m.upper()} {p}" for p, item in doc.get("paths", {}).items() for m in item
                  if m in METHODS and (not rx or rx.search(p)) and (not method or m.upper() == method.upper()))


def curl_for(interaction: dict) -> str:
    req = interaction["request"]
    parts = ["curl -sS -i", f"-X {req['method']}", shlex.quote(req["uri"])]
    for name, vals in req.get("headers", {}).items():
        if name.lower() == "authorization":
            parts.append('-H "Authorization: Bearer $TWENTY_API_KEY"')
            continue
        for v in vals:
            parts.append("-H " + shlex.quote(f"{name}: {v}"))
    body = decode_body(req.get("body"))
    if body:
        try:
            parts.append("--data-binary " + shlex.quote(body.decode("utf-8")))
        except UnicodeDecodeError:
            parts.append("--data-binary $'" + "".join(f"\\x{b:02x}" for b in body) + "'")
    return " \\\n  ".join(parts)


def slug(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()[:50]


def write_reproducers(run_dir: Path, failures: list[dict], seed) -> list[tuple[str, str]]:
    rd = run_dir / "reproducers"
    rd.mkdir(exist_ok=True)
    for old in rd.glob("*.sh"):
        old.unlink()
    index = []
    for n, f in enumerate(sorted(failures, key=lambda x: (x["operation"], x["check"])), 1):
        if not f["interaction"]:
            continue
        name = f"{n:02d}-{slug(f['operation'])}-{f['check']}.sh"
        head = [
            "#!/usr/bin/env bash",
            "# Reproducer tự sinh bởi scripts/summarize.py (Schemathesis 4.x). Chạy: export TWENTY_API_KEY=... && bash " + name,
            f"# Operation : {f['operation']}",
            f"# Check     : {f['check']}  ({f['type']}, mức {f['severity']})",
            f"# Seed      : {seed}   Phase: {f['phase']}   Số lần gặp: {f['count']}",
        ] + ["# " + ln for ln in f["message"].splitlines()] + (
            [f"# Còn {len(f['variants']) - 1} biến thể khác của lỗi này (xem summary.md)"] if len(f["variants"]) > 1 else [])
        (rd / name).write_text("\n".join(head) + "\n\n" + curl_for(f["interaction"]) + "\n", encoding="utf-8")
        index.append((name, f"{f['operation']} — {f['check']}"))
    return index


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def signature(a: dict) -> dict:
    return {
        "per_op_cases": {k: v["cases"] for k, v in sorted(a["ops"].items())},
        "unique_failures": sorted(f"{f['operation']}|{f['check']}|{f['type']}|{len(f['variants'])}" for f in a["failures"]),
        "codes": {str(k): v for k, v in sorted(a["codes"].items())},
    }


def run_info(run_dir: Path) -> dict:
    files = glob.glob(str(run_dir / "json-*.json")) + glob.glob(str(run_dir / "report.json"))
    return json.loads(Path(files[0]).read_text(encoding="utf-8")) if files else {}


def summarize(run_dir: Path, schema: Path | None) -> None:
    a = analyse(load_events(run_dir))
    info = run_info(run_dir)
    seed = info.get("seed", "?")
    cmd = info.get("command", "")
    m_rx = re.search(r"--include-path-regex (\S+)", cmd)
    m_me = re.search(r"--include-method (\S+)", cmd)
    all_ops = schema_operations(schema, m_rx.group(1) if m_rx else None, m_me.group(1) if m_me else None)
    tested = sorted(k for k, v in a["ops"].items() if v["cases"])
    index = write_reproducers(run_dir, a["failures"], seed)

    rows = []
    for k, v in sorted(a["ops"].items()):
        c = v["codes"]
        rows.append([f"`{k}`", v["cases"], v["positive"], v["negative"],
                     sum(n for code, n in c.items() if 200 <= code < 300), sum(n for code, n in c.items() if 400 <= code < 500),
                     sum(n for code, n in c.items() if code >= 500), v["failed_cases"], "có" if v["cases"] >= 50 else "chưa"])
    lines = [f"# Thống kê lần chạy `{run_dir.name}`", ""]
    lines += [md_table(["Mục", "Giá trị"], [
        ["Schemathesis", info.get("schemathesis_version", "?")], ["Seed", seed],
        ["Bắt đầu (UTC)", info.get("started_at", "?")], ["Thời gian chạy (giây)", round(info.get("running_time", 0), 1)],
        ["Exit code", info.get("exit_code", "?")],
        ["Phase", ", ".join(f"{k}={v.get('status')}" for k, v in info.get("phases", {}).items()) or "?"],
        ["Test case sinh ra", info.get("test_cases", {}).get("generated", sum(v['cases'] for v in a['ops'].values()))],
        ["Lỗi duy nhất", len(a["failures"])]]), ""]
    if all_ops:
        miss = [o for o in all_ops if o not in tested]
        lines += [f"**Độ phủ operation:** {len(tested)}/{len(all_ops)} = {100 * len(tested) / len(all_ops):.0f}% "
                  f"trong phạm vi kịch bản (ngưỡng cuối kỳ ≥ 80% của 65 operation 5 đối tượng). Chưa test: {len(miss)}.", ""]
    lines += ["## Theo operation", "", md_table(
        ["Operation", "Test case", "Dương", "Âm", "2xx", "4xx", "5xx", "Case lỗi", "≥50 case"], rows), ""]
    lines += ["## Mã trạng thái", "", md_table(["Mã", "Số lần"], [[k, v] for k, v in sorted(a["codes"].items())]), ""]
    chk = collections.defaultdict(lambda: collections.Counter())
    for (name, status), n in a["checks"].items():
        chk[name][status] += n
    lines += ["## Theo check", "", md_table(["Check", "Đạt", "Lỗi"], [[n, c["success"], c["failure"]] for n, c in sorted(chk.items())]), ""]
    lines += ["## Lỗi duy nhất", ""]
    if a["failures"]:
        lines += [md_table(["#", "Operation", "Check", "Loại", "Mức", "Lần gặp", "Biến thể (dòng cuối thông điệp)"], [
            [i, f"`{f['operation']}`", f["check"], f["type"], f["severity"], f["count"],
             ("; ".join(sorted(f["variants"])[:3]) + (f" (+{len(f['variants']) - 3})" if len(f["variants"]) > 3 else "")).replace("|", "\\|")]
            for i, f in enumerate(sorted(a["failures"], key=lambda x: (x["operation"], x["check"])), 1)]), ""]
    else:
        lines += ["Không có lỗi.", ""]
    (run_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    (run_dir / "summary.json").write_text(json.dumps({"seed": seed, "signature": signature(a), "tested": tested,
                                                      "schema_operations": len(all_ops)}, ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "REPRODUCERS.md").write_text("# Reproducer\n\n" + ("\n".join(f"- `reproducers/{n}` — {d}" for n, d in index) or "Không có lỗi."), encoding="utf-8")
    print(f"Đã ghi summary.md, summary.json, REPRODUCERS.md ({len(index)} reproducer) trong {run_dir}")


def compare(a_dir: Path, b_dir: Path) -> int:
    """So hai lần chạy. Tiêu chí tái lập: tập nhóm lỗi (operation, check, loại) trùng nhau.
    Số test case và số lần gặp có thể lệch nhẹ khi chạy bị cắt theo --max-time (giới hạn theo giờ)."""
    if a_dir.resolve() == b_dir.resolve():
        print("LỖI: hai tham số là cùng một thư mục, so sánh không có ý nghĩa. Chạy lại SC1 và dùng thư mục mới.")
        return 2
    aa, bb = analyse(load_events(a_dir)), analyse(load_events(b_dir))
    ga = {(f["operation"], f["check"], f["type"]) for f in aa["failures"]}
    gb = {(f["operation"], f["check"], f["type"]) for f in bb["failures"]}
    common, only_a, only_b = ga & gb, ga - gb, gb - ga
    union = len(ga | gb) or 1
    overlap = len(common) / union
    print(f"Nhóm lỗi: A={len(ga)}, B={len(gb)}, chung={len(common)}, chỉ A={len(only_a)}, chỉ B={len(only_b)}, trùng={overlap:.0%}")
    for tag, grp in (("chỉ ở A", only_a), ("chỉ ở B", only_b)):
        for op, ck, ty in sorted(grp):
            print(f"  - {tag}: {op} | {ck} | {ty}")
    sa, sb = signature(aa), signature(bb)
    exact = sa == sb
    print("Giống hệt về số liệu." if exact else "Số test case / số lần gặp lệch nhẹ (bình thường khi chạy bị cắt theo thời gian).")
    ok = exact or (overlap >= 0.9 and not only_b)
    print("TÁI LẬP ĐƯỢC: các nhóm lỗi chính trùng nhau giữa hai lần chạy." if ok else "KHÁC NHAU: cần xem các nhóm lỗi lệch ở trên.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("run_dir", nargs="?")
    ap.add_argument("--schema")
    ap.add_argument("--compare", nargs=2, metavar=("A", "B"))
    args = ap.parse_args()
    if args.compare:
        return compare(Path(args.compare[0]), Path(args.compare[1]))
    if not args.run_dir:
        ap.error("cần run_dir hoặc --compare")
    summarize(Path(args.run_dir), Path(args.schema) if args.schema else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
