#!/usr/bin/env python3
"""Tải OpenAPI schema của Twenty (Core hoặc Metadata) về schema/.

Cần Bearer API key, nếu không schema chỉ có phần khung, không có đường dẫn đối tượng.
Chỉ chạy được với localhost.

    python scripts/fetch_schema.py                 # -> schema/core.openapi.json
    python scripts/fetch_schema.py --which metadata
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request

import k05_common as c


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--which", choices=["core", "metadata"], default="core")
    ap.add_argument("--out", help="Đường dẫn file đầu ra (mặc định schema/<which>.openapi.json)")
    args = ap.parse_args()

    c.load_env()
    url = f"{c.base_url()}/open-api/{args.which}"
    c.assert_localhost(url)
    key = c.api_key()

    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} khi gọi {url}. Kiểm tra API key và trạng thái instance.")
    except urllib.error.URLError as e:
        sys.exit(f"Không kết nối được {url}: {e.reason}. Twenty đã chạy chưa (docker compose up -d)?")

    doc = json.loads(body)
    paths = doc.get("paths", {})
    out = c.ROOT / (args.out or f"schema/{args.which}.openapi.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")

    sha = hashlib.sha256(body).hexdigest()
    print(f"Đã lưu {out.relative_to(c.ROOT)}  ({len(body):,} byte, sha256 {sha[:16]}...)")
    print(f"openapi={doc.get('openapi')}  số đường dẫn={len(paths)}  servers={[s.get('url') for s in doc.get('servers', [])]}")
    if not paths:
        print("CẢNH BÁO: schema không có đường dẫn nào. Thường do thiếu/sai API key hoặc workspace chưa có đối tượng.")
        return 2
    n_ops = sum(1 for p in paths.values() for m in p if m in {"get", "post", "put", "patch", "delete"})
    print(f"Tổng số operation: {n_ops}. Chạy: python scripts/list_operations.py để lập danh sách.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
