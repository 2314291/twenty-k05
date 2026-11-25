#!/usr/bin/env python3
"""Đưa Twenty về trạng thái ban đầu cố định trước mỗi lần chạy test (việc reset-env của Tuấn).

Cách làm: khôi phục DB từ một bản chụp (snapshot) rồi seed lại bằng scripts/seed.py.
Không dùng `docker compose down -v`, vì sau lệnh đó phải tạo lại tài khoản, workspace và API key bằng tay.

    python scripts/reset_env.py --snapshot   # MỘT LẦN: sau khi đã tạo workspace + API key, chụp DB "sạch"
    python scripts/reset_env.py              # trước mỗi lần chạy test: khôi phục snapshot + seed 30 bản ghi/object
    python scripts/reset_env.py --no-seed    # chỉ khôi phục, không seed
    python scripts/reset_env.py --count 50   # seed 50 bản ghi/object

Snapshot nằm ở env/snapshot/ và KHÔNG được commit (chứa dữ liệu workspace và API key).
Yêu cầu: Docker Desktop đang chạy, đã `docker compose up -d` trong env/, .env ở gốc repo có TWENTY_API_KEY.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

import k05_common as c

ENV_DIR = c.ROOT / "env"
SNAP_DIR = ENV_DIR / "snapshot"
SNAP_FILE = SNAP_DIR / "k05-clean.dump"
SNAP_IN_DB = "/tmp/k05-clean.dump"          # đường dẫn bên trong container db
OBJECTS = ["companies", "people", "opportunities", "notes", "tasks"]
MANIFEST = c.ROOT / "reports" / "seed-manifest.json"


def compose(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Chạy `docker compose ...` trong thư mục env/ (nơi có docker-compose.yml và .env của Twenty)."""
    print("  $ docker compose " + " ".join(args))
    r = subprocess.run(["docker", "compose", *args], cwd=ENV_DIR, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        sys.exit(f"Lỗi khi chạy docker compose {' '.join(args)}:\n{r.stderr.strip()[-800:]}")
    return r


def pg() -> tuple[str, str]:
    """Tên user và database Postgres, lấy từ env/.env (mặc định giống docker-compose.yml)."""
    c.load_env(ENV_DIR / ".env")
    return os.environ.get("PG_DATABASE_USER", "postgres"), os.environ.get("PG_DATABASE_NAME", "default")


def check_running() -> None:
    r = compose("ps", "--status", "running", "--services", check=False)
    if r.returncode != 0:
        sys.exit("Không gọi được Docker. Mở Docker Desktop, chờ 'Engine running' rồi chạy lại.")
    running = set(r.stdout.split())
    missing = {"db", "redis"} - running
    if missing:
        sys.exit(f"Service chưa chạy: {', '.join(sorted(missing))}. Chạy `docker compose up -d` trong env/ trước.")


# ---------------------------------------------------------------- chụp snapshot (làm một lần)
def snapshot() -> None:
    user, db = pg()
    check_running()
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    # -Fc: định dạng nén của Postgres, pg_restore đọc lại được. Ghi bên trong container rồi chép ra,
    # không dùng `>` vì PowerShell làm hỏng file nhị phân.
    compose("exec", "-T", "db", "pg_dump", "-U", user, "-d", db, "-Fc", "-f", SNAP_IN_DB)
    compose("cp", f"db:{SNAP_IN_DB}", str(SNAP_FILE))
    tag = os.environ.get("TAG", "?")
    (SNAP_DIR / "info.txt").write_text(
        f"Chụp lúc: {dt.datetime.now().isoformat(timespec='seconds')}\nTwenty TAG: {tag}\nDatabase: {db}\n",
        encoding="utf-8",
    )
    print(f"Đã chụp snapshot: {SNAP_FILE.relative_to(c.ROOT)} ({SNAP_FILE.stat().st_size // 1024} KB)")


# ---------------------------------------------------------------- reset (mỗi lần chạy test)
def wait_healthy(timeout: int = 180) -> None:
    url = c.base_url() + "/healthz"
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                if r.status == 200:
                    print(f"  Twenty sẵn sàng sau {time.time() - t0:.0f}s")
                    return
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(3)
    sys.exit(f"Quá {timeout}s mà {url} chưa trả 200. Xem log: docker compose logs --tail 50 server")


def total_count(obj: str, key: str):
    status, parsed, _ = c.http("GET", f"/{obj}?limit=1", key=key)
    if status != 200:
        return f"lỗi {status}"
    return parsed.get("totalCount", "?") if isinstance(parsed, dict) else "?"


def reset(seed: bool, count: int) -> None:
    if not SNAP_FILE.exists():
        sys.exit("Chưa có snapshot. Dựng Twenty, tạo workspace và API key, rồi chạy: "
                 "python scripts/reset_env.py --snapshot")
    user, db = pg()
    c.load_env()                       # .env ở gốc repo: TWENTY_BASE_URL, TWENTY_API_KEY
    c.assert_localhost(c.base_url())
    key = c.api_key()
    check_running()

    print("1/5 Dừng server và worker (để không còn ai giữ kết nối tới DB)")
    compose("stop", "server", "worker")

    print("2/5 Xoá DB và khôi phục từ snapshot")
    compose("cp", str(SNAP_FILE), f"db:{SNAP_IN_DB}")
    compose("exec", "-T", "db", "dropdb", "-U", user, "--force", "--if-exists", db)
    compose("exec", "-T", "db", "createdb", "-U", user, db)
    r = compose("exec", "-T", "db", "pg_restore", "-U", user, "-d", db, "--no-owner", SNAP_IN_DB, check=False)
    if r.returncode != 0:
        # pg_restore trả mã khác 0 cả khi chỉ có cảnh báo; in ra để người chạy tự đánh giá.
        print("  Cảnh báo từ pg_restore (kiểm tra bước 4 để biết có sao không):\n  " + r.stderr.strip()[-600:])

    print("3/5 Xoá cache Redis (cache metadata cũ sẽ không khớp với DB vừa khôi phục)")
    compose("exec", "-T", "redis", "redis-cli", "FLUSHALL")

    print("4/5 Bật lại server, worker và chờ sẵn sàng")
    compose("start", "server", "worker")
    wait_healthy()
    status, _, _ = c.http("GET", "/companies?limit=1", key=key)
    if status != 200:
        sys.exit(f"API key trong .env không dùng được sau khi khôi phục (trả {status}). "
                 "Snapshot có được chụp SAU khi tạo key này không?")
    print("  API key vẫn dùng được")

    if seed:
        print(f"5/5 Seed {count} bản ghi mỗi object")
        if MANIFEST.exists():
            MANIFEST.unlink()          # manifest cũ trỏ tới id đã mất cùng DB cũ
        r = subprocess.run([sys.executable, str(c.ROOT / "scripts" / "seed.py"), "--count", str(count)])
        if r.returncode != 0:
            sys.exit("seed.py lỗi, xem thông báo ở trên.")
    else:
        print("5/5 Bỏ qua seed (--no-seed)")

    print("\nSố bản ghi sau reset (chạy reset lần nữa phải ra đúng các số này):")
    for obj in OBJECTS:
        print(f"  {obj:<14} {total_count(obj, key)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--snapshot", action="store_true", help="chụp DB hiện tại làm trạng thái ban đầu")
    ap.add_argument("--no-seed", action="store_true", help="chỉ khôi phục, không seed")
    ap.add_argument("--count", type=int, default=30, help="số bản ghi mỗi object khi seed (mặc định 30)")
    args = ap.parse_args()
    if args.snapshot:
        snapshot()
    else:
        reset(seed=not args.no_seed, count=args.count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
