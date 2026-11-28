"""Hook Schemathesis cho bộ test K05 (Twenty v2.45.6). Người viết: Quang.

`scripts/run_k05.py` tự nạp file này qua biến `SCHEMATHESIS_HOOKS` (tắt bằng `--no-hooks`).
Chạy tay: `SCHEMATHESIS_HOOKS=hooks/k05_hooks.py st run ...`

Hai việc, bật/tắt bằng biến môi trường (run_k05.py tự đặt):

1. Bảo vệ dữ liệu (`K05_PROTECT_DATA=1`, mặc định bật). Hook `before_call` chạy ở MỌI phase, kể cả
   examples, và với cả ca "phương thức không khai báo" của check `unsupported_method` (phase coverage sinh
   chúng như ca thường, gửi qua `Case.call`). Mọi request mà Twenty sẽ hiểu thành ghi hàng loạt theo filter
   (xem `is_bulk_write`) bị bọc filter thành `and(<filter gốc>,createdAt[gte]:"<K05_RUN_START>")`, nên chỉ
   chạm được bản ghi tạo ra TRONG lần chạy này. Lý do:
   - SC1 16/10: ca ví dụ `DELETE /companies?filter=or(...,not(id[is]:NULL))&soft_delete=false` (lấy từ
     `examples` của schema) xoá vĩnh viễn 209 công ty, gồm cả seed (docs/defects.md, mục R-01).
   - SC1 27/11 (D-11, Thuận phát hiện): `unsupported_method` gửi `DELETE /{đối tượng}/groupBy` kèm
     `filter=createdAt[gte]:"2023-01-01"`. Twenty bỏ qua chữ `groupBy` với mọi phương thức
     (`parse-core-path.utils.ts:42-47`) nên chạy xoá cứng hàng loạt, xoá sạch cả 5 object. Bản cũ của
     hook chỉ khớp đúng `/{đối tượng}` nên không chặn.

   Thêm vào đó (cũng trong `before_call`): `DELETE /{đối tượng}/{id}` và `PATCH /{đối tượng}/merge` mà
   trỏ tới id của bản ghi seed thì id đó được đổi sang một UUID không tồn tại (cùng giá trị -> cùng UUID), nên
   bản ghi seed không bao giờ bị xoá hay gộp mất giữa lần chạy. Mốc `K05_RUN_START` do run_k05.py lấy theo
   đồng hồ của máy chủ (createdAt mới nhất trong DB), để đồng hồ Docker lệch với Windows không làm lọt bản ghi seed.

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
import uuid
from pathlib import Path

try:  # cho phép chạy unit test (scripts/selftest/test_hooks.py) khi chưa cài schemathesis
    import schemathesis

    hook = schemathesis.hook
except ImportError:  # pragma: no cover
    def hook(func):
        return func

ROOT = Path(__file__).resolve().parent.parent
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
# Đường dẫn mà Twenty v2.45.6 đọc thành "đối tượng, không có id" với MỌI phương thức
# (packages/twenty-server/src/engine/api/rest/input-request-parsers/path-parser-utils/parse-core-path.utils.ts:34-48):
# /companies, /batch/companies, /companies/groupBy, /companies/duplicates, /companies/merge.
BULK_PATH_RE = re.compile(r"^/(?:batch/)?([A-Za-z]+)(?:/(?:groupBy|duplicates|merge))?$")
ID_PATH_RE = re.compile(r"^/([A-Za-z]+)/\{id\}(/restore)?$")  # /companies/{id}, /companies/{id}/restore
# Không có id thì (core/services/rest-api-core.service.ts:56-94): DELETE -> xoá hàng loạt theo filter
# (xoá cứng nếu thiếu soft_delete=true); PATCH, PUT (bí danh PATCH, controller dòng 164) -> cập nhật hàng loạt
# theo filter, KHÔNG bắt buộc filter (rest-api-update-many.handler.ts). POST không xoá/sửa bản ghi cũ nên bỏ qua.
BULK_METHODS = {"DELETE", "PATCH", "PUT"}
DELETE_ID_RE = re.compile(r"^/([A-Za-z]+)/\{id\}$")            # DELETE /companies/{id}
MERGE_RE = re.compile(r"^/([A-Za-z]+)/merge$")                  # PATCH /companies/merge


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


def seed_ids(obj: str) -> set[str]:
    return {i.lower() for i in load_manifest().get(obj, []) if isinstance(i, str)}


def decoy_id(value: str) -> str:
    """UUID không tồn tại, tất định theo giá trị gốc (chạy lại vẫn ra cùng request)."""
    return str(uuid.UUID(hashlib.sha256(("k05-decoy:" + value).encode()).hexdigest()[:32]))


def shield_seed_ids(case) -> None:
    """Không để request xoá theo id hoặc gộp bản ghi chạm vào bản ghi seed."""
    method, path = str(case.method).upper(), case.path or ""
    m = DELETE_ID_RE.match(path)
    if method == "DELETE" and m:
        params = case.path_parameters if isinstance(case.path_parameters, dict) else None
        value = params.get("id") if params else None
        if isinstance(value, str) and value.lower() in seed_ids(m.group(1)):
            params["id"] = decoy_id(value)
        return
    m = MERGE_RE.match(path)
    if method == "PATCH" and m and isinstance(case.body, dict) and isinstance(case.body.get("ids"), list):
        protected = seed_ids(m.group(1))
        ids = case.body["ids"]
        for i, v in enumerate(ids):
            if isinstance(v, str) and v.lower() in protected:
                ids[i] = decoy_id(v)


def is_negative(case) -> bool:
    meta = getattr(case, "meta", None)
    mode = getattr(getattr(getattr(meta, "generation", None), "mode", None), "value", None)
    return mode == "negative"


def is_bulk_write(method: str, path: str) -> bool:
    """Request mà Twenty xử lý thành xoá/cập nhật hàng loạt theo filter (đã đối chiếu mã nguồn, xem trên)."""
    if method not in BULK_METHODS or not BULK_PATH_RE.match(path):
        return False
    # Ngoại lệ duy nhất: PATCH /{đối tượng}/merge có route riêng (@Patch('*path/merge')), gộp theo body["ids"],
    # không theo filter; seed được che bằng shield_seed_ids.
    return not (method == "PATCH" and path.endswith("/merge"))


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
    shield_seed_ids(case)
    if not is_bulk_write(str(case.method).upper(), case.path or ""):
        return
    if not isinstance(case.query, dict):
        case.query = {}
    # sửa tại chỗ: Schemathesis băm lại container sau before_call để cập nhật metadata của ca
    case.query["filter"] = guard_filter(case.query.get("filter"))
