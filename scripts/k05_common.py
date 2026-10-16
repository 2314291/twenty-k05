"""Tiện ích dùng chung cho các script K05. Chỉ dùng thư viện chuẩn."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

for _stream in (sys.stdout, sys.stderr):      # Windows: tránh lỗi mã hóa khi in tiếng Việt/emoji
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def load_env(path: Path | None = None) -> None:
    """Nạp .env (KEY=VALUE) vào os.environ nếu biến chưa có. Không in giá trị."""
    path = path or ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def base_url() -> str:
    return os.environ.get("TWENTY_BASE_URL", "http://localhost:3001").rstrip("/")


def rest_url() -> str:
    return base_url() + "/rest"


def assert_localhost(url: str) -> None:
    """Chốt an toàn: chỉ cho phép test trên máy local (SPEC mục 5, rủi ro R-04)."""
    host = urlparse(url).hostname
    if host not in LOCAL_HOSTS:
        sys.exit(
            f"TỪ CHỐI: '{host}' không phải localhost. Bộ test K05 chỉ được chạy trên "
            "instance Twenty cục bộ của nhóm."
        )


def api_key(name: str = "TWENTY_API_KEY", required: bool = True) -> str:
    value = os.environ.get(name, "").strip()
    if required and not value:
        sys.exit(f"Thiếu {name}. Điền vào file .env (xem .env.example).")
    return value


def redact_text(text: str, secrets: list[str]) -> str:
    """Thay mọi API key bằng <REDACTED> để file báo cáo commit được an toàn."""
    for s in secrets:
        if s:
            text = text.replace(s, "<REDACTED>")
    return text


def redact_tree(directory: Path, secrets: list[str]) -> int:
    """Redact đệ quy các file văn bản trong thư mục. Trả về số file đã sửa."""
    changed = 0
    for p in directory.rglob("*"):
        if not p.is_file():
            continue
        try:
            raw = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = redact_text(raw, secrets)
        if new != raw:
            p.write_text(new, encoding="utf-8")
            changed += 1
    return changed


# ---------- HTTP helper (stdlib) ----------
import json as _json
import time as _time
import urllib.error as _uerr
import urllib.request as _ureq


def http(method: str, path: str, body=None, key: str | None = None, raw_body: bytes | None = None,
         headers: dict | None = None, timeout: float = 30.0):
    """Gọi REST của Twenty. `path` bắt đầu bằng '/' (vd '/companies'), tự thêm '/rest' (trừ '/open-api/...').

    Trả về (status, json_hoặc_text, giây). Không bao giờ ném lỗi HTTP: status 4xx/5xx trả về bình thường.
    """
    url = (base_url() if path.startswith("/open-api") else rest_url()) + path
    assert_localhost(url)
    data = raw_body if raw_body is not None else (None if body is None else _json.dumps(body).encode())
    h = {"Accept": "application/json"}
    if data is not None:
        h["Content-Type"] = "application/json"
    if key:
        h["Authorization"] = f"Bearer {key}"
    h.update(headers or {})
    req = _ureq.Request(url, data=data, method=method, headers=h)
    t0 = _time.perf_counter()
    try:
        with _ureq.urlopen(req, timeout=timeout) as resp:
            status, payload = resp.status, resp.read()
    except _uerr.HTTPError as e:
        status, payload = e.code, e.read()
    except _uerr.URLError as e:
        raise SystemExit(f"Không kết nối được {url}: {e.reason}. Twenty đã chạy chưa?")
    dt = _time.perf_counter() - t0
    try:
        parsed = _json.loads(payload) if payload else None
    except ValueError:
        parsed = payload.decode("utf-8", "replace")
    return status, parsed, dt


def first_record(parsed):
    """Lấy bản ghi đầu tiên (hoặc danh sách) từ phong bì {"data": {"<op>": ...}}."""
    if not isinstance(parsed, dict):
        return None
    data = parsed.get("data")
    if isinstance(data, dict) and data:
        return next(iter(data.values()))
    return data
