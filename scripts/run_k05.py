#!/usr/bin/env python3
"""Chạy một kịch bản K05 bằng Schemathesis rồi tự thống kê + sinh reproducer.

    python scripts/run_k05.py SC1                       # PoC giữa kỳ: Companies
    python scripts/run_k05.py SC1 --schema schema/core.red.openapi.json --label RED   # ca đỏ cố ý
    python scripts/run_k05.py SC5 --variant none        # không gửi key
    python scripts/run_k05.py SC2 --max-examples 100 --seed 7
    python scripts/run_k05.py SC1 --dry-run             # chỉ in lệnh

Bảo vệ: chỉ chạy với localhost; key đọc từ .env/biến môi trường và được redact khỏi mọi file trong reports/.
Tên tham số `st run` đã đối chiếu với Schemathesis 4.31.1 (`st run --help`).
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
import subprocess
import sys
from pathlib import Path

import k05_common as c

OBJ = "companies|people|opportunities|notes|tasks"

SCENARIOS = {
    "SC1": dict(
        desc="PoC giữa kỳ: toàn bộ operation của Companies, mọi check",
        path_regex=r"^/(batch/)?companies(/|$)",
        checks="all", mode="all", phases="examples,coverage,fuzzing", max_examples=50),
    "SC2": dict(
        desc="Dữ liệu sai (negative) trên 5 đối tượng phạm vi",
        path_regex=rf"^/(batch/)?({OBJ})(/|$)",
        checks="negative_data_rejection,not_a_server_error,status_code_conformance,response_schema_conformance",
        mode="negative", phases="coverage,fuzzing", max_examples=50),
    "SC3": dict(
        desc="Phân trang / lọc / sắp xếp: GET danh sách (kèm scripts/probe_boundaries.py cho biên cụ thể)",
        path_regex=rf"^/({OBJ})$", include_method="GET",
        checks="not_a_server_error,status_code_conformance,response_schema_conformance,positive_data_acceptance",
        mode="all", phases="coverage,fuzzing", max_examples=50),
    "SC4": dict(
        desc="Batch /batch/{đối tượng} (kèm probe_boundaries.py cho 0/1/200/201 bản ghi)",
        path_regex=rf"^/batch/({OBJ})$",
        checks="not_a_server_error,status_code_conformance,response_schema_conformance,negative_data_rejection",
        mode="all", phases="coverage,fuzzing", max_examples=30),
    "SC5": dict(
        desc="Xác thực: không key / key sai / key role giới hạn (--variant none|wrong|limited|valid)",
        path_regex=rf"^/(batch/)?({OBJ})(/|$)",
        checks="ignored_auth,not_a_server_error,status_code_conformance",
        mode="positive", phases="fuzzing", max_examples=10),
}


def find_st() -> list[str]:
    """Tìm lệnh `st`. Trên Windows nó nằm trong thư mục Scripts, thường KHÔNG có trong PATH."""
    import sysconfig
    dirs = [Path(sys.executable).parent, Path(sys.executable).parent / "Scripts", Path(sys.executable).parent / "bin"]
    for scheme in (None, f"{os.name}_user"):
        try:
            dirs.append(Path(sysconfig.get_path("scripts", scheme) if scheme else sysconfig.get_path("scripts")))
        except Exception:
            pass
    for d in dirs:
        for name in ("st.exe", "st"):
            if (d / name).is_file():
                return [str(d / name)]
    exe = shutil.which("st") or shutil.which("schemathesis")
    if exe:
        return [exe]
    sys.exit("Không tìm thấy lệnh `st`. Chạy: pip install -r requirements.txt (xem thư mục Scripts của Python).")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("scenario", choices=sorted(SCENARIOS))
    ap.add_argument("--schema", default="schema/core.openapi.json")
    ap.add_argument("--url", help="mặc định <TWENTY_BASE_URL>/rest")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--max-examples", type=int)
    ap.add_argument("--variant", choices=["valid", "none", "wrong", "limited"], default="valid")
    ap.add_argument("--label", default="", help="nhãn thêm vào tên thư mục (vd RED)")
    ap.add_argument("--rate-limit", default="auto", help="vd 100/m hoặc auto (mặc định, theo Retry-After khi 429)")
    ap.add_argument("--max-time", type=int, help="giới hạn thời gian tổng (giây)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    c.load_env()
    sc = SCENARIOS[args.scenario]
    url = args.url or c.rest_url()
    c.assert_localhost(url)
    seed = args.seed if args.seed is not None else int(os.environ.get("K05_SEED", "20261020"))
    schema = Path(args.schema)
    if not schema.is_absolute():
        schema = c.ROOT / schema
    if not schema.exists():
        sys.exit(f"Không thấy {schema}. Chạy trước: python scripts/fetch_schema.py")

    secrets = [os.environ.get("TWENTY_API_KEY", ""), os.environ.get("TWENTY_API_KEY_LIMITED", "")]
    header = []
    if args.variant == "valid":
        header = ["-H", f"Authorization: Bearer {c.api_key()}"]
    elif args.variant == "limited":
        header = ["-H", f"Authorization: Bearer {c.api_key('TWENTY_API_KEY_LIMITED')}"]
    elif args.variant == "wrong":
        header = ["-H", "Authorization: Bearer k05-sai-key-000000"]

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f"{stamp}-seed{seed}" + (f"-{args.variant}" if args.scenario == "SC5" or args.variant != "valid" else "") + (f"-{args.label}" if args.label else "")
    out = c.ROOT / "reports" / args.scenario / name
    k = 1
    while out.exists():          # hai lần chạy trong cùng một giây
        k += 1
        out = c.ROOT / "reports" / args.scenario / f"{name}-{k}"
    cmd = find_st() + [
        "run", str(schema), "--url", url, *header,
        "--checks", sc["checks"], "--mode", sc["mode"], "--phases", sc["phases"],
        "--max-examples", str(args.max_examples or sc["max_examples"]),
        "--seed", str(seed), "--generation-deterministic",
        "--include-path-regex", sc["path_regex"],
        "--workers", "1", "--rate-limit", args.rate_limit, "--request-timeout", "20",
        "--continue-on-failure", "--no-color",
        "--report", "json,ndjson,junit,html", "--report-dir", str(out),
    ]
    if "include_method" in sc:
        cmd += ["--include-method", sc["include_method"]]
    if args.max_time:
        cmd += ["--max-time", str(args.max_time)]

    shown = " ".join(("'Authorization: Bearer <KEY>'" if a.startswith("Authorization: Bearer") else a) for a in cmd)
    print(f"[{args.scenario}] {sc['desc']}\n$ {shown}\n")
    if args.dry_run:
        return 0

    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env=env)
    text = c.redact_text(proc.stdout, secrets)
    (out / "st-output.txt").write_text(text, encoding="utf-8")
    print(text[-3500:])
    n = c.redact_tree(out, secrets)
    print(f"\nExit code của st: {proc.returncode} (0 = không lỗi, 1 = có lỗi test). Đã redact key trong {n} file.")

    try:
        import summarize
        summarize.summarize(out, schema)
    except SystemExit as e:
        print(f"Không thống kê được: {e}")
    print(f"Kết quả: {out.relative_to(c.ROOT)}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
