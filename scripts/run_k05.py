#!/usr/bin/env python3
"""Chạy một kịch bản K05 bằng Schemathesis rồi tự thống kê + sinh reproducer.

    python scripts/run_k05.py SC1                       # PoC giữa kỳ: Companies
    python scripts/run_k05.py SC1 --schema schema/core.red.openapi.json --label RED   # ca đỏ cố ý
    python scripts/run_k05.py SC5 --variant none        # không gửi key
    python scripts/run_k05.py SC2 --max-examples 100 --seed 7
    python scripts/run_k05.py SC1 --dry-run             # chỉ in lệnh
    python scripts/run_k05.py SC1 --object people --reset   # SC1 trên People, seed lại trước khi chạy

Bảo vệ: chỉ chạy với localhost; key đọc từ .env/biến môi trường và được redact khỏi mọi file trong reports/.
Mặc định nạp hooks/k05_hooks.py: chặn DELETE/PATCH hàng loạt chạm dữ liệu có sẵn, gắn id seed vào ca dương
(tắt bằng --no-protect, --no-real-ids, --no-hooks). Cấu hình mỗi lần chạy ghi ở run-config.json.
Tên tham số `st run` đã đối chiếu với Schemathesis 4.31.1 (`st run --help`).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import k05_common as c

OBJECTS = ["companies", "people", "opportunities", "notes", "tasks"]
OBJ = "|".join(OBJECTS)
HOOKS_FILE = c.ROOT / "hooks" / "k05_hooks.py"
MANIFEST = c.ROOT / "reports" / "seed-manifest.json"

SCENARIOS = {
    "SC1": dict(
        desc="Toàn bộ operation của một đối tượng (mặc định Companies, đổi bằng --object), mọi check",
        path_regex=r"^/(batch/)?{obj}(/|$)", default_object="companies",
        checks="all", mode="all", phases="examples,coverage,fuzzing", max_examples=50),
    "SC2": dict(
        desc="Dữ liệu sai (negative) trên 5 đối tượng phạm vi",
        path_regex=r"^/(batch/)?({obj})(/|$)",
        checks="negative_data_rejection,not_a_server_error,status_code_conformance,response_schema_conformance",
        mode="negative", phases="coverage,fuzzing", max_examples=50),
    "SC3": dict(
        desc="Phân trang / lọc / sắp xếp: GET danh sách (kèm scripts/probe_boundaries.py cho biên cụ thể)",
        path_regex=r"^/({obj})$", include_method="GET",
        checks="not_a_server_error,status_code_conformance,response_schema_conformance,positive_data_acceptance",
        mode="all", phases="coverage,fuzzing", max_examples=50),
    "SC4": dict(
        desc="Batch /batch/{đối tượng} (kèm probe_boundaries.py cho 0/1/200/201 bản ghi)",
        path_regex=r"^/batch/({obj})$",
        checks="not_a_server_error,status_code_conformance,response_schema_conformance,negative_data_rejection",
        mode="all", phases="coverage,fuzzing", max_examples=30),
    "SC5": dict(
        desc="Xác thực: không key / key sai / key role giới hạn (--variant none|wrong|limited|valid)",
        path_regex=r"^/(batch/)?({obj})(/|$)",
        checks="ignored_auth,not_a_server_error,status_code_conformance",
        mode="positive", phases="fuzzing", max_examples=10),
}


def path_regex(sc: dict, obj: str | None) -> str:
    """Thay {obj} trong mẫu bằng đối tượng được chọn (hoặc cả 5 đối tượng phạm vi)."""
    return sc["path_regex"].replace("{obj}", obj or sc.get("default_object", OBJ))


def reset_seed(count: int, dry_run: bool) -> None:
    """Dọn bản ghi seed cũ rồi seed lại, để mọi lần chạy bắt đầu từ cùng một tập dữ liệu K05."""
    seed = [sys.executable, str(c.ROOT / "scripts" / "seed.py")]
    steps = ([seed + ["--cleanup"]] if MANIFEST.exists() else []) + [seed + ["--count", str(count)]]
    for cmd in steps:
        print("$ python", " ".join([str(Path(cmd[1]).relative_to(c.ROOT)), *cmd[2:]]))
        if not dry_run and subprocess.run(cmd).returncode != 0:
            sys.exit("Seed lại thất bại, dừng để không chạy trên dữ liệu lệch. Xem lỗi ở trên.")


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
    ap.add_argument("--object", choices=OBJECTS, help="chỉ chạy trên một đối tượng (SC1 mặc định companies, SC2-SC5 mặc định cả 5)")
    ap.add_argument("--reset", action="store_true", help="dọn và seed lại dữ liệu K05 trước khi chạy (scripts/seed.py)")
    ap.add_argument("--seed-count", type=int, default=int(os.environ.get("K05_SEED_COUNT", "30")), help="số bản ghi mỗi loại khi --reset")
    ap.add_argument("--no-hooks", action="store_true", help="không nạp hooks/k05_hooks.py")
    ap.add_argument("--no-protect", action="store_true", help="tắt chặn DELETE/PATCH hàng loạt (có thể XOÁ dữ liệu có sẵn)")
    ap.add_argument("--no-real-ids", action="store_true", help="không thay {id} bằng id seed")
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

    regex = path_regex(sc, args.object)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f"{stamp}-seed{seed}" + (f"-{args.object}" if args.object else "") + (f"-{args.variant}" if args.scenario == "SC5" or args.variant != "valid" else "") + (f"-{args.label}" if args.label else "")
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
        "--include-path-regex", regex,
        "--workers", "1", "--rate-limit", args.rate_limit, "--request-timeout", "20",
        "--continue-on-failure", "--no-color",
        "--report", "json,ndjson,junit,html", "--report-dir", str(out),
    ]
    if "include_method" in sc:
        cmd += ["--include-method", sc["include_method"]]
    if args.max_time:
        cmd += ["--max-time", str(args.max_time)]

    shown = " ".join(("'Authorization: Bearer <KEY>'" if a.startswith("Authorization: Bearer") else a) for a in cmd)
    print(f"[{args.scenario}] {sc['desc']}")
    if args.reset:
        reset_seed(args.seed_count, args.dry_run)

    # Mốc thời gian sau khi seed (làm tròn LÊN giây kế tiếp để bản ghi seed tạo trong cùng giây vẫn nằm trước mốc):
    # hook chỉ cho DELETE/PATCH hàng loạt chạm bản ghi tạo sau mốc này.
    run_start = (dt.datetime.now(dt.timezone.utc).replace(microsecond=0) + dt.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    use_hooks = not args.no_hooks and HOOKS_FILE.exists()
    hook_env = {"K05_RUN_START": run_start, "K05_SEED_MANIFEST": str(MANIFEST),
                "K05_PROTECT_DATA": "0" if args.no_protect else "1", "K05_REAL_IDS": "0" if args.no_real_ids else "1"}
    if use_hooks:
        hook_env["SCHEMATHESIS_HOOKS"] = str(HOOKS_FILE)
    hooks_note = (f"hook {HOOKS_FILE.relative_to(c.ROOT)} (bảo vệ dữ liệu={hook_env['K05_PROTECT_DATA']}, id seed={hook_env['K05_REAL_IDS']})"
                  if use_hooks else "không dùng hook")
    print(f"$ {shown}\n[{hooks_note}; mốc dữ liệu {run_start}]\n")
    if use_hooks and not args.no_real_ids and not args.reset:
        print("Lưu ý: không có --reset, id lấy từ reports/seed-manifest.json có thể đã bị xoá ở lần chạy trước (ca theo id sẽ 404).\n")
    if args.no_hooks or args.no_protect:
        print("CẢNH BÁO: không chặn DELETE/PATCH hàng loạt. Ví dụ filter trong schema khớp mọi bản ghi và có thể xoá sạch dữ liệu.\n")
    if args.dry_run:
        return 0

    out.mkdir(parents=True, exist_ok=True)
    try:
        manifest_counts = {k: len(v) for k, v in json.loads(MANIFEST.read_text(encoding="utf-8")).items()}
    except (OSError, ValueError):
        manifest_counts = {}
    (out / "run-config.json").write_text(json.dumps({
        "scenario": args.scenario, "object": args.object, "path_regex": regex, "variant": args.variant,
        "seed": seed, "schema": str(schema.relative_to(c.ROOT)) if schema.is_relative_to(c.ROOT) else str(schema),
        "url": url, "reset": args.reset, "seed_count": args.seed_count if args.reset else None,
        "seed_manifest": manifest_counts, "run_start_utc": run_start, "hooks": use_hooks,
        "protect_data": use_hooks and not args.no_protect, "real_ids": use_hooks and not args.no_real_ids,
        "command": shown}, ensure_ascii=False, indent=2), encoding="utf-8")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", **hook_env)
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
