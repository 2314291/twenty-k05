"""Hook Schemathesis cho bộ test K05 (Twenty v2.45.6). Người viết: Quang.

`scripts/run_k05.py` tự nạp file này qua biến `SCHEMATHESIS_HOOKS` (tắt bằng `--no-hooks`).
Chạy tay: `SCHEMATHESIS_HOOKS=hooks/k05_hooks.py st run ...`

Hai việc, bật/tắt bằng biến môi trường (run_k05.py tự đặt):

1. Bảo vệ dữ liệu (`K05_PROTECT_DATA=1`, mặc định bật). Hook `before_call` chạy ở MỌI phase, kể cả
   examples. Với các operation ghi hàng loạt theo filter (`DELETE /{đối tượng}` và `PATCH /{đối tượng}`),
   filter bị bọc thành `and(<filter gốc>,createdAt[gte]:"<K05_RUN_START>")` nên chỉ chạm được bản ghi
   tạo ra TRONG lần chạy này. Lý do: lần SC1 ngày 16/10, ca ví dụ `filter=or(...,not(id[is]:NULL))`
   + `soft_delete=false` (lấy từ `examples` của schema) đã xoá vĩnh viễn 209 công ty, gồm cả dữ liệu
   seed, và phần còn lại của lần chạy diễn ra trên bảng gần như rỗng (xem docs/defects.md, mục R-01).

2. Id có thật (`K05_REAL_IDS=1`, mặc định bật). Hook `map_case` (phase coverage, fuzzing, stateful)
   thay `{id}` là UUID hợp lệ của ca DƯƠNG bằng một id trong `reports/seed-manifest.json`, để
   GET/PATCH/restore theo id chạm bản ghi thật thay vì 404. Không áp dụng cho `DELETE /{đối tượng}/{id}`
   (giữ id ngẫu nhiên, không xoá dữ liệu seed) và không đụng ca âm (id sai định dạng được giữ nguyên).
   Cùng một id sinh ra luôn được ánh xạ tới cùng vị trí trong manifest, nên chạy lại cho cùng kết quả.

Tên hook, chữ ký và phase đã đối chiếu với mã nguồn Schemathesis 4.31.1
(`hook_specs.py`, `generation/drivers.py`, `docs/reference/hooks.md`).
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
from pathlib import Path

try:  # cho phép chạy unit test (scripts/selftest/test_hooks.py) khi chưa cài schemathesis
    import schemathesis

    hook = schemathesis.hook
except ImportError:  # pragma: no cover
    def hook(func):
        return func

ROOT = Path(__file__).resolve().parent.parent
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
BULK_PATH_RE = re.compile(r"^/([A-Za-z]+)$")                 # /companies
ID_PATH_RE = re.compile(r"^/([A-Za-z]+)/\{id\}(/restore)?$")  # /companies/{id}, /companies/{id}/restore
BULK_METHODS = {"DELETE", "PATCH"}


def _flag(name: str, default: str = "1") -> bool:
    return os.environ.get(name, default).strip().lower() not in ("0", "false", "no", "off", "")


def _now_iso() -> str:
    """Giây kế tiếp (làm tròn lên), cùng cách tính với run_k05.py."""
    now = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0) + _dt.timedelta(seconds=1)
    return now.strftime("%Y-%m-%dT%H:%M:%S.000Z")


RUN_START = os.environ.get("K05_RUN_START") or _now_iso()
_manifest_cache: dict | None = None


def load_manifest() -> dict:
    global _manifest_cache
    if _manifest_cache is None:
        path = Path(os.environ.get("K05_SEED_MANIFEST", ROOT / "reports" / "seed-manifest.json"))
        try:
            _manifest_cache = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _manifest_cache = {}
    return _manifest_cache


def pick_real_id(obj: str, generated: str) -> str | None:
    """Ánh xạ tất định: cùng giá trị sinh ra -> cùng vị trí trong danh sách id của manifest."""
    ids = [i for i in load_manifest().get(obj, []) if isinstance(i, str)]
    if not ids:
        return None
    return ids[int(hashlib.sha256(generated.encode()).hexdigest(), 16) % len(ids)]


def is_negative(case) -> bool:
    meta = getattr(case, "meta", None)
    mode = getattr(getattr(getattr(meta, "generation", None), "mode", None), "value", None)
    return mode == "negative"


def guard_filter(value):
    """Bọc filter để ghi hàng loạt chỉ chạm bản ghi tạo sau RUN_START."""
    guard = f'createdAt[gte]:"{RUN_START}"'
    if value is None or value == "":
        return guard
    if isinstance(value, str):
        return f"and({value},{guard})"
    if isinstance(value, list):
        return [guard_filter(v) if isinstance(v, str) or v is None else v for v in value] or [guard]
    return value  # kiểu lạ của ca âm: server từ chối bằng 400, để nguyên


@hook
def map_case(ctx, case):
    if not _flag("K05_REAL_IDS"):
        return case
    m = ID_PATH_RE.match(case.path or "")
    if not m or str(case.method).upper() == "DELETE" or is_negative(case):
        return case
    params = case.path_parameters or {}
    value = params.get("id")
    if not isinstance(value, str) or not UUID_RE.match(value):
        return case
    real = pick_real_id(m.group(1), value)
    if real:
        params["id"] = real
        case.path_parameters = params
    return case


@hook
def before_call(ctx, case, kwargs):
    if not _flag("K05_PROTECT_DATA"):
        return
    if str(case.method).upper() not in BULK_METHODS or not BULK_PATH_RE.match(case.path or ""):
        return
    if not isinstance(case.query, dict):
        case.query = {}
    # sửa tại chỗ: Schemathesis băm lại container sau before_call để cập nhật metadata của ca
    case.query["filter"] = guard_filter(case.query.get("filter"))
