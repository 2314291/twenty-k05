#!/usr/bin/env python3
"""SC5 - Xác thực và phân quyền (phần của Tuấn): 5 object × 13 operation × 4 loại key.

    python scripts/kiem_thu_sc5.py                         # chạy đủ 4 loại key trên 5 object (khoảng 6-7 phút)
    python scripts/kiem_thu_sc5.py --objects companies     # chỉ một object (khoảng 1,5 phút)
    python scripts/kiem_thu_sc5.py --variants none,wrong,full   # khi chưa có key chỉ đọc
    python scripts/kiem_thu_sc5.py --compare reports/sc5/A.json reports/sc5/B.json   # so 2 lần chạy
    python scripts/kiem_thu_sc5.py --no-p5                 # bỏ 10 ca biên tay P5-00..P5-08 (mặc định có chạy)

Bốn loại key (vùng tương đương của đầu vào "Authorization"):
  full     TWENTY_API_KEY          (đối chứng: phải thành công, nếu không thì ca đó KHÔNG KẾT LUẬN)
  limited  TWENTY_API_KEY_LIMITED  (role chỉ đọc: đọc -> 200, ghi -> 403)
  wrong    chuỗi bất kỳ            (-> 401)
  none     không gửi Authorization (-> 401 theo schema; Twenty trả 403, lỗi D-02)

Mỗi ô được chấm theo 3 cột độc lập:
  Chặn       có chặn đúng không (bất biến I6). 2xx ở chỗ phải chặn là LỖI BẢO MẬT.
  Mã         mã có đúng mã kỳ vọng không (401 / 403 / 2xx).
  Schema     mã có nằm trong danh sách schema khai báo không (bất biến I2).

Trình tự trong một operation: none -> wrong -> limited -> full. Ba loại đầu phải bị chặn nên không làm
thay đổi dữ liệu; full chạy cuối vì có thể xoá hoặc gộp bản ghi đích.
Bản ghi tạo ra có tiền tố K05-SC5- và bị xoá vĩnh viễn ở cuối. Đi chậm 1 request/giây (giới hạn 100/60s).
Kết quả: reports/sc5/<thời điểm>.md và .json, có lệnh curl tái hiện; key được che bằng <REDACTED>.
Yêu cầu: Twenty v2.45.6 ở localhost, đã chạy `python scripts/reset_env.py` (có ≥ 1 bản ghi mỗi object).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path
from urllib.parse import quote

import k05_common as c

PREFIX = "K05-SC5-"
DELAY = 1.0
OUT_DIR = c.ROOT / "reports" / "sc5"
SCHEMA = c.ROOT / "schema" / "core.openapi.json"
OBJECTS = ("companies", "people", "opportunities", "notes", "tasks")
VARIANTS = ("none", "wrong", "limited", "full")
WRONG_KEY = "k05-sai-key-000000"
GROUP_BY = '[{"createdAt":{"granularity":"DAY"}}]'


# ---------------------------------------------------------------- dữ liệu
def body_for(obj: str, label: str) -> dict:
    """Body tối thiểu hợp lệ để tạo/sửa một bản ghi (giống seed.py)."""
    name = f"{PREFIX}{label}"
    if obj == "people":
        return {"name": {"firstName": name, "lastName": "SC5"}}
    if obj in ("notes", "tasks"):
        return {"title": name}
    return {"name": name}


def flt(rid: str) -> str:
    return "filter=" + quote(f"id[eq]:{rid}", safe="")


def operations(obj: str, fx: dict) -> list[dict]:
    """13 operation của một object, theo đúng phạm vi KICH_BAN_K05 mục 2.

    write=False nghĩa là thao tác đọc (key chỉ đọc phải được phép). Chỉ đường dẫn đã có filter mới được xoá hàng loạt.
    """
    return [
        dict(op="GET /{o}", m="GET", p=f"/{obj}?limit=1", b=None, write=False),
        dict(op="GET /{o}/{id}", m="GET", p=f"/{obj}/{fx['read']}", b=None, write=False),
        dict(op="GET /{o}/groupBy", m="GET", p=f"/{obj}/groupBy?group_by=" + quote(GROUP_BY, safe=""), b=None, write=False),
        dict(op="POST /{o}/duplicates", m="POST", p=f"/{obj}/duplicates", b={"ids": [fx["read"]]}, write=False),
        dict(op="POST /{o}", m="POST", p=f"/{obj}", b=body_for(obj, "tao"), write=True),
        dict(op="POST /batch/{o}", m="POST", p=f"/batch/{obj}", b=[body_for(obj, "batch")], write=True),
        dict(op="PATCH /{o}/{id}", m="PATCH", p=f"/{obj}/{fx['read']}", b=body_for(obj, "sua"), write=True),
        dict(op="PATCH /{o}", m="PATCH", p=f"/{obj}?{flt(fx['read'])}", b=body_for(obj, "sua-loat"), write=True),
        dict(op="PATCH /{o}/merge", m="PATCH", p=f"/{obj}/merge",
             b={"ids": [fx["merge1"], fx["merge2"]], "conflictPriorityIndex": 0}, write=True),
        dict(op="PATCH /{o}/{id}/restore", m="PATCH", p=f"/{obj}/{fx['soft1']}/restore", b=None, write=True),
        dict(op="PATCH /{o}/restore", m="PATCH", p=f"/{obj}/restore?{flt(fx['soft2'])}", b=None, write=True),
        dict(op="DELETE /{o}/{id}", m="DELETE", p=f"/{obj}/{fx['del1']}", b=None, write=True),
        dict(op="DELETE /{o}", m="DELETE", p=f"/{obj}?{flt(fx['del2'])}", b=None, write=True),
    ]


def schema_path(op: str, obj: str) -> tuple[str, str]:
    method, tmpl = op.split(" ", 1)
    return method.lower(), tmpl.replace("{o}", obj)


def load_declared() -> dict:
    s = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return {(p, m): sorted(int(k) for k in op.get("responses", {}) if k.isdigit())
            for p, ops in s["paths"].items() for m, op in ops.items() if isinstance(op, dict)}


def expected(variant: str, write: bool, ok_code: int) -> int:
    if variant == "full":
        return ok_code
    if variant == "limited":
        return 403 if write else ok_code
    return 401                                     # none, wrong: chưa xác thực -> 401


# ---------------------------------------------------------------- HTTP
class Runner:
    def __init__(self, keys: dict, delay: float):
        self.keys, self.delay, self._last = keys, delay, 0.0
        self.rows: list[dict] = []
        self.created: dict[str, list[str]] = {o: [] for o in OBJECTS}

    def http(self, variant: str, method: str, path: str, body=None):
        key = self.keys.get(variant)               # none -> None: không gửi Authorization
        status, parsed = 0, None
        for _ in range(10):
            wait = self.delay - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            status, parsed, _ = c.http(method, path, body, key)
            self._last = time.monotonic()
            if status != 429:
                return status, parsed
            sec = parsed.get("retryAfterSeconds", 5) if isinstance(parsed, dict) else 5
            time.sleep(max(1, min(int(sec or 5), 60)))
        return status, parsed

    def create(self, obj: str, label: str, soft: bool = False) -> str | None:
        s, p = self.http("full", "POST", f"/{obj}", body_for(obj, label))
        rec = c.first_record(p)
        rid = rec.get("id") if isinstance(rec, dict) else None
        if s not in (200, 201) or not rid:
            return None
        self.created[obj].append(rid)
        if soft:
            s, _ = self.http("full", "DELETE", f"/{obj}/{rid}?soft_delete=true")
            if s != 200:
                return None
        return rid

    def remember(self, obj: str, parsed) -> None:
        rec = c.first_record(parsed)
        for r in (rec if isinstance(rec, list) else [rec]):
            if isinstance(r, dict) and r.get("id"):
                self.created[obj].append(r["id"])


def message(parsed) -> str:
    if isinstance(parsed, dict):
        msgs = parsed.get("messages") or parsed.get("message") or ""
        if isinstance(msgs, list):
            msgs = "; ".join(str(x) for x in msgs)
        err = parsed.get("error") or ""
        return f"{err}: {msgs}".strip(": ")[:120] if (err or msgs) else ""
    return str(parsed or "")[:120]


def curl_cmd(variant: str, method: str, path: str, body=None) -> str:
    url = c.rest_url() + path
    parts = ["curl.exe", "-s", "-w", '"%{http_code}"', "-X", method]
    if variant in ("full", "limited"):
        parts += ["-H", f'"Authorization: Bearer $env:{"K" if variant == "full" else "L"}"']
    elif variant == "wrong":
        parts += ["-H", f'"Authorization: Bearer {WRONG_KEY}"']
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).replace('"', '\\"')
        parts += ["-H", '"Content-Type: application/json"', "-d", f'"{data}"']
    parts.append(f'"{url}"')
    return " ".join(parts)


# ---------------------------------------------------------------- ca biên tay P5 (dac-ta-sc1-sc2-red.md mục 5)
P5_CASES = [
    # mã, mô tả, method, path, (variant, header Authorization ghi đè), body, kỳ vọng (None = quan sát)
    ("P5-00", "GET, key đủ quyền (đối chứng)", "GET", "/companies?limit=1", ("full", None), None, 200),
    ("P5-01", "GET, không key", "GET", "/companies?limit=1", ("none", None), None, 401),
    ("P5-02", "GET, key sai", "GET", "/companies?limit=1", ("wrong", None), None, 401),
    ("P5-03", "GET, scheme Basic", "GET", "/companies?limit=1", ("none", "Basic {full}"), None, 401),
    ("P5-04", "GET, Bearer rỗng", "GET", "/companies?limit=1", ("none", "Bearer "), None, 401),
    ("P5-05", "POST, không key", "POST", "/companies", ("none", None), {"name": f"{PREFIX}P5-05"}, 401),
    ("P5-06a", "GET /open-api/core, không key", "GET", "/open-api/core", ("none", None), None, None),
    ("P5-06b", "GET /open-api/core, có key", "GET", "/open-api/core", ("full", None), None, None),
    ("P5-07", "GET, key chỉ đọc", "GET", "/companies?limit=1", ("limited", None), None, 200),
    ("P5-08", "POST, key chỉ đọc", "POST", "/companies", ("limited", None), {"name": f"{PREFIX}P5-08"}, 403),
]


def run_p5(r: Runner, variants: list[str]) -> list[dict]:
    print("\n== Ca biên tay P5-00..P5-08")
    rows = []
    for cid, desc, m, path, (v, hdr), body, exp in P5_CASES:
        if v == "limited" and "limited" not in variants:
            rows.append(dict(id=cid, desc=desc, status="-", expect=exp, verdict="CHƯA CHẠY", msg="chưa có key chỉ đọc", size=""))
            continue
        headers = {"Authorization": hdr.format(full=r.keys["full"])} if hdr else None
        wait = r.delay - (time.monotonic() - r._last)
        if wait > 0:
            time.sleep(wait)
        s, p, _ = c.http(m, path, body, r.keys.get(v) if not hdr else None, headers=headers)
        r._last = time.monotonic()
        if 200 <= s < 300 and m == "POST":
            r.remember("companies", p)
        size = len(json.dumps(p, ensure_ascii=False)) if path.startswith("/open-api") else ""
        verdict = "OBSERVE" if exp is None else ("MATCH" if s == exp else "DIFF")
        msg = message(p) if not path.startswith("/open-api") else f"{len((p or {}).get('paths', {})) if isinstance(p, dict) else 0} đường dẫn"
        rows.append(dict(id=cid, desc=desc, status=s, expect=exp, verdict=verdict, msg=msg, size=size))
        print(f"   {cid:<7} {desc:<34} {s}  {verdict:<8} {msg}")
    return rows


# ---------------------------------------------------------------- chạy
def judge(variant: str, write: bool, status: int, ok_code: int, control_ok: bool | None) -> tuple[str, str]:
    """Trả về (Chặn, Mã)."""
    must_block = variant in ("none", "wrong") or (variant == "limited" and write)
    is_2xx = 200 <= status < 300
    if variant == "full":
        block = "ĐẠT" if is_2xx else "ĐỐI CHỨNG HỎNG"
    elif must_block:
        block = "LỖI BẢO MẬT" if is_2xx else "ĐẠT"
    else:                                           # limited đọc: phải được phép
        block = "ĐẠT" if is_2xx else "CHẶN NHẦM"
    if control_ok is False and variant != "full":
        block = "KHÔNG KẾT LUẬN"                    # đối chứng không chạy được thì không biết request có hợp lệ không
    code = "ĐÚNG" if status == expected(variant, write, ok_code) else "LỆCH"
    return block, code


def run_object(r: Runner, obj: str, variants: list[str], declared: dict) -> None:
    print(f"\n== {obj}: chuẩn bị bản ghi đích (key đủ quyền)")
    fx = {
        "read": r.create(obj, "doc"),
        "merge1": r.create(obj, "gop-1"), "merge2": r.create(obj, "gop-2"),
        "soft1": r.create(obj, "khoi-phuc-1", soft=True), "soft2": r.create(obj, "khoi-phuc-2", soft=True),
        "del1": r.create(obj, "xoa-1"), "del2": r.create(obj, "xoa-2"),
    }
    if not all(fx.values()):
        missing = [k for k, v in fx.items() if not v]
        print(f"   Không tạo đủ bản ghi đích ({', '.join(missing)}), bỏ qua {obj}.")
        r.rows.append(dict(obj=obj, op="(chuẩn bị)", variant="full", status=0, note=f"thiếu {missing}",
                           block="KHÔNG KẾT LUẬN", code="", schema="", expect="", declared=[], msg="", curl=""))
        return
    for o in operations(obj, fx):
        m_lower, spath = schema_path(o["op"], obj)
        decl = declared.get((spath, m_lower), [])
        ok_code = next((x for x in decl if 200 <= x < 300), 200)
        results = {}
        for v in variants:
            s, p = r.http(v, o["m"], o["p"], o["b"])
            if 200 <= s < 300 and o["m"] == "POST" and o["write"]:
                r.remember(obj, p)                 # dọn cả bản ghi tạo nhầm (nếu key không được phép mà vẫn tạo)
            results[v] = (s, p)
        control_ok = (200 <= results["full"][0] < 300) if "full" in results else None
        line = []
        for v in variants:
            s, p = results[v]
            block, code = judge(v, o["write"], s, ok_code, control_ok)
            schema = "CÓ" if s in decl else "KHÔNG"
            msg = message(p)
            if v == "limited" and "Missing authentication token" in msg:
                block = "ĐIỀU KIỆN ĐẦU SAI"       # key chỉ đọc không được gửi: biến rỗng hoặc dán sai
            r.rows.append(dict(obj=obj, op=o["op"].replace("{o}", obj), op_tmpl=o["op"], variant=v,
                               write=o["write"], status=s, expect=expected(v, o["write"], ok_code), declared=decl,
                               block=block, code=code, schema=schema, msg=msg,
                               curl=curl_cmd(v, o["m"], o["p"], o["b"]) if (block != "ĐẠT" or code != "ĐÚNG" or schema != "CÓ") else ""))
            line.append(f"{v}={s}")
        print(f"   {o['op'].replace('{o}', obj):<32} " + "  ".join(line))


def cleanup(r: Runner) -> None:
    print("\n== Dọn bản ghi K05-SC5- (xoá vĩnh viễn)")
    left = 0
    for obj, ids in r.created.items():
        for rid in dict.fromkeys(ids):
            s, _ = r.http("full", "DELETE", f"/{obj}/{rid}")
            if s == 404:                            # có thể đang bị xoá mềm: khôi phục rồi xoá vĩnh viễn
                s2, _ = r.http("full", "PATCH", f"/{obj}/{rid}/restore")
                if s2 == 200:
                    s, _ = r.http("full", "DELETE", f"/{obj}/{rid}")
            if s not in (200, 404):
                left += 1
    total = sum(len(set(v)) for v in r.created.values())
    print(f"   Đã xử lý {total} bản ghi" + (f", còn {left} chưa xoá được." if left else "."))


# ---------------------------------------------------------------- báo cáo
def matrix(rows: list[dict], variants: list[str]) -> list[str]:
    """Bảng mã trạng thái theo loại key: mỗi ô gộp mã của 5 object, vd '403×5' hoặc '200×4, 400×1'."""
    out = ["| Operation | Loại | " + " | ".join(variants) + " |", "|---|---|" + "---|" * len(variants)]
    tmpls = list(dict.fromkeys(x["op_tmpl"] for x in rows if "op_tmpl" in x))
    for t in tmpls:
        kind = next(x for x in rows if x.get("op_tmpl") == t)["write"]
        cells = []
        for v in variants:
            codes = [x["status"] for x in rows if x.get("op_tmpl") == t and x["variant"] == v]
            cnt = {k: codes.count(k) for k in dict.fromkeys(codes)}
            cells.append(", ".join(f"{k}×{n}" for k, n in cnt.items()) or "-")
        out.append(f"| `{t}` | {'ghi' if kind else 'đọc'} | " + " | ".join(cells) + " |")
    return out


def summary(rows: list[dict]) -> list[str]:
    real = [x for x in rows if x["op"] != "(chuẩn bị)"]
    def n(k, val): return sum(1 for x in real if x[k] == val)
    return [
        f"- Tổng số ca: **{len(real)}**",
        f"- Chặn: ĐẠT {n('block', 'ĐẠT')}, LỖI BẢO MẬT {n('block', 'LỖI BẢO MẬT')}, CHẶN NHẦM {n('block', 'CHẶN NHẦM')}, "
        f"ĐỐI CHỨNG HỎNG {n('block', 'ĐỐI CHỨNG HỎNG')}, KHÔNG KẾT LUẬN {n('block', 'KHÔNG KẾT LUẬN')}, "
        f"ĐIỀU KIỆN ĐẦU SAI {n('block', 'ĐIỀU KIỆN ĐẦU SAI')}",
        f"- Mã đúng kỳ vọng: {n('code', 'ĐÚNG')} / {len(real)}",
        f"- Mã nằm trong schema: {n('schema', 'CÓ')} / {len(real)}",
    ]


def write_report(rows: list[dict], keys: dict, variants: list[str], stamp: str, p5: list[dict] | None = None) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md = ["# Kết quả SC5 - Xác thực và phân quyền (Tuấn)", "",
          f"Thời điểm: {stamp}. Môi trường: {c.base_url()}. Loại key: {', '.join(variants)}.", "",
          "## Tóm tắt", "", *summary(rows), "",
          "## Bảng mã trạng thái theo loại key (gộp các object đã chạy)", "", *matrix(rows, variants), "",
          *(["## Ca biên tay P5", "", "| Mã ca | Ca | Mã trả về | Kỳ vọng | Kết luận | Thông điệp / kích thước |",
              "|---|---|---|---|---|---|"] + [f"| {x['id']} | {x['desc']} | {x['status']} | {x['expect'] or 'quan sát'} | "
              f"{x['verdict']} | {x['msg']}{(' (' + str(x['size']) + ' ký tự)') if x['size'] else ''} |" for x in (p5 or [])] + [""]
             if p5 else []),
          "## Chi tiết từng ca", "",
          "| Object | Operation | Key | Mã | Kỳ vọng | Schema khai báo | Chặn | Mã | Schema | Thông điệp |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for x in rows:
        md.append(f"| {x['obj']} | `{x['op']}` | {x['variant']} | {x['status']} | {x['expect']} | "
                  f"{','.join(map(str, x['declared']))} | {x['block']} | {x['code']} | {x['schema']} | {x['msg']} |")
    repro = [x for x in rows if x.get("curl")]
    if repro:
        md += ["", "## Lệnh tái hiện (PowerShell; đặt trước `$env:K` và `$env:L`)", ""]
        seen = set()
        for x in repro:
            k = (x["op_tmpl"] if "op_tmpl" in x else x["op"], x["variant"], x["status"])
            if k in seen:
                continue                            # mỗi kiểu lệch chỉ cần một reproducer
            seen.add(k)
            md += [f"- {x['obj']} `{x['op']}` key={x['variant']} -> {x['status']}", "", f"  ```\n  {x['curl']}\n  ```"]
    secrets = [v for v in keys.values() if v and v != WRONG_KEY]
    (OUT_DIR / f"{stamp}.md").write_text(c.redact_text("\n".join(md) + "\n", secrets), encoding="utf-8")
    (OUT_DIR / f"{stamp}.json").write_text(
        c.redact_text(json.dumps(rows, ensure_ascii=False, indent=2), secrets), encoding="utf-8")
    if p5:
        (OUT_DIR / f"{stamp}-p5.json").write_text(
            c.redact_text(json.dumps(p5, ensure_ascii=False, indent=2), secrets), encoding="utf-8")
    return OUT_DIR / f"{stamp}.md"


def compare(a: str, b: str) -> int:
    """Kiểm tra tái lập: cùng (object, operation, key) phải ra cùng mã trạng thái."""
    ra = {(x["obj"], x["op"], x["variant"]): x["status"] for x in json.loads(Path(a).read_text(encoding="utf-8"))}
    rb = {(x["obj"], x["op"], x["variant"]): x["status"] for x in json.loads(Path(b).read_text(encoding="utf-8"))}
    common = sorted(set(ra) & set(rb))
    diff = [k for k in common if ra[k] != rb[k]]
    print(f"So {len(common)} ca chung: GIỐNG {len(common) - len(diff)}, KHÁC {len(diff)}")
    for k in diff:
        print(f"  KHÁC  {k[0]:<14} {k[1]:<36} {k[2]:<8} {ra[k]} -> {rb[k]}")
    only = set(ra) ^ set(rb)
    if only:
        print(f"  ({len(only)} ca chỉ có ở một trong hai lần chạy)")
    return 1 if diff else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--objects", default=",".join(OBJECTS))
    ap.add_argument("--variants", default=",".join(VARIANTS))
    ap.add_argument("--delay", type=float, default=DELAY)
    ap.add_argument("--compare", nargs=2, metavar=("A.json", "B.json"))
    ap.add_argument("--no-p5", action="store_true", help="bỏ qua 10 ca biên tay P5")
    args = ap.parse_args()
    if args.compare:
        return compare(*args.compare)

    objects = [o.strip() for o in args.objects.split(",") if o.strip()]
    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    bad = [o for o in objects if o not in OBJECTS] + [v for v in variants if v not in VARIANTS]
    if bad:
        sys.exit(f"Giá trị không hợp lệ: {bad}")
    if "full" not in variants:
        variants.append("full")                     # luôn có đối chứng
    variants = [v for v in VARIANTS if v in variants]

    c.load_env()
    c.assert_localhost(c.base_url())
    keys = {"none": None, "wrong": WRONG_KEY, "full": c.api_key("TWENTY_API_KEY"),
            "limited": c.api_key("TWENTY_API_KEY_LIMITED", required=False)}

    # ---- kiểm tra điều kiện đầu: chạy khi điều kiện đầu sai thì kết quả vô nghĩa
    r = Runner(keys, args.delay)
    s, _ = r.http("full", "GET", "/companies?limit=1")
    if s != 200:
        sys.exit(f"Key đủ quyền không dùng được (trả {s}). Kiểm tra TWENTY_API_KEY trong .env.")
    if "limited" in variants:
        if len(keys["limited"] or "") < 100:
            sys.exit("TWENTY_API_KEY_LIMITED trống hoặc quá ngắn (cần khoảng 440 ký tự). Tạo key chỉ đọc theo "
                     "SETUP.md mục 8, hoặc chạy tạm với --variants none,wrong,full.")
        if keys["limited"] == keys["full"]:
            sys.exit("TWENTY_API_KEY_LIMITED trùng với TWENTY_API_KEY: đây không phải key chỉ đọc.")
        s, p = r.http("limited", "GET", "/companies?limit=1")
        if s != 200:
            sys.exit(f"Key chỉ đọc không đọc được Companies (trả {s}, {message(p)}). Kiểm tra role đã bật quyền xem.")
    print("Điều kiện đầu: ĐẠT (key đủ quyền đọc được" + (", key chỉ đọc đọc được" if "limited" in variants else "") + ")")

    declared = load_declared()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    p5 = None
    try:
        if not args.no_p5:
            p5 = run_p5(r, variants)
        for obj in objects:
            run_object(r, obj, variants, declared)
    finally:
        cleanup(r)
    out = write_report(r.rows, keys, variants, stamp, p5)
    print("\n" + "\n".join(summary(r.rows)))
    print(f"\nĐã ghi {out.relative_to(c.ROOT)} và .json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
