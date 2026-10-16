#!/usr/bin/env python3
"""Tự kiểm tra bộ script K05 trên MÁY CHỦ GIẢ (mock). Chạy trong thư mục tạm, không đụng reports/.

    python scripts/selftest/run_selftest.py

Kết quả KHÔNG phải kết quả của Twenty. Mục đích: bảo đảm runner, thống kê, reproducer, so sánh seed,
make_red_case chạy đúng trước khi nối vào Twenty thật.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PORT = "3099"


def sh(cmd, **kw):
    print("$", " ".join(cmd))
    return subprocess.run(cmd, text=True, **kw)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="k05-selftest-"))
    work = tmp / "repo"
    shutil.copytree(ROOT / "scripts", work / "scripts", ignore=shutil.ignore_patterns("__pycache__", "selftest"))
    (work / "schema").mkdir()
    (work / "reports").mkdir()
    shutil.copy(HERE / "mock_schema.json", work / "schema" / "core.openapi.json")
    env = dict(os.environ, TWENTY_BASE_URL=f"http://localhost:{PORT}", TWENTY_API_KEY="mock-key-123")
    srv = subprocess.Popen([sys.executable, str(HERE / "mock_server.py"), PORT])
    time.sleep(1)
    rc = 0
    try:
        py = sys.executable
        r1 = sh([py, str(work / "scripts/run_k05.py"), "SC1", "--seed", "7", "--max-examples", "20"], env=env)
        r2 = sh([py, str(work / "scripts/run_k05.py"), "SC1", "--seed", "7", "--max-examples", "20"], env=env)
        runs = sorted((work / "reports" / "SC1").iterdir())
        assert len(runs) == 2, runs
        assert (runs[0] / "summary.md").exists() and (runs[0] / "REPRODUCERS.md").exists()
        leaked = [p for p in runs[0].rglob("*") if p.is_file() and b"mock-key-123" in p.read_bytes()]
        assert not leaked, f"key rò rỉ trong {leaked}"
        cmp_ = sh([py, str(work / "scripts/summarize.py"), "--compare", str(runs[0]), str(runs[1])])
        red = sh([py, str(work / "scripts/make_red_case.py")], env=env)
        assert red.returncode == 0 and (work / "schema" / "core.red.openapi.json").exists()
        print("\nSELFTEST:", "ĐẠT" if cmp_.returncode == 0 else "so sánh seed KHÁC NHAU (xem trên)")
        print("Thư mục tạm:", tmp)
        rc = 0 if cmp_.returncode == 0 else 1
    finally:
        srv.terminate()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
