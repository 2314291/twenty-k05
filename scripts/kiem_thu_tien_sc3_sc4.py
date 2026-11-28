#!/usr/bin/env python3
"""SC3 (phân trang, lọc, sắp xếp) và SC4 (batch) trên các object được giao cho Tiến.

    python scripts/kiem_thu_tien_sc3_sc4.py                          # SC3 trên notes, tasks; SC4 trên people, notes
    python scripts/kiem_thu_tien_sc3_sc4.py --only sc3 --objects notes
    python scripts/kiem_thu_tien_sc3_sc4.py --only sc4 --objects people

Cùng bộ ca P3-01..P3-17 và P4-01..P4-08 với script Companies của Trung (`kiem_thu_sc3_sc4_sc6.py`),
chỉ đổi object và body tạo bản ghi. Kỳ vọng lấy từ `docs/dac-ta-sc3-sc4.md`.

Yêu cầu: Twenty v2.45.6 chạy ở localhost, TWENTY_API_KEY (role Admin) trong .env.

- Đi chậm 1 request mỗi giây (giới hạn 100 request mỗi 60 giây mỗi khoá); gặp 429 thì chờ rồi gửi lại.
- Bản ghi tạo ra có tiền tố K05-TIEN- và bị xoá vĩnh viễn ở cuối, kể cả khi có ca lỗi.
- Kết quả ghi vào reports/kiem-thu-tien/<thời điểm>.md và .json, kèm lệnh curl tái hiện cho mọi ca LỆCH
  và QUAN SÁT; khoá API được che.
- Cột "Companies" cho biết mã trả về lần chạy tay của Trung trên Companies (02/11), để so hành vi giữa các object.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import time

import k05_common as c

PREFIX = "K05-TIEN-"
MISSING = "00000000-0000-4000-8000-000000000000"
DELAY = 1.0
OUT_DIR = c.ROOT / "reports" / "kiem-thu-tien"

DEFAULT_PLAN = {"sc3": ["notes", "tasks"], "sc4": ["people", "notes"]}
OBJECTS = ("companies", "people", "opportunities", "notes", "tasks")
TITLE_FIELD = {"notes": "title", "tasks": "title", "people": "name", "companies": "name", "opportunities": "name"}


def build(obj: str, tag: str, i: int) -> dict:
    """Body tối thiểu hợp lệ để tạo một bản ghi của object (theo seed.py)."""
    name = f"{PREFIX}{tag}-{i}"
    if obj == "people":
        return {"name": {"firstName": f"{PREFIX}{tag}", "lastName": str(i)}}
    if obj in ("notes", "tasks"):
        return {"title": name}
    return {"name": name}


class Runner:
    def __init__(self, key: str, delay: float):
        self.key, self.delay, self._last = key, delay, 0.0
        self.rows: list[dict] = []
        self.created_ids: dict[str, list[str]] = {o: [] for o in OBJECTS}

    def http(self, method: str, path: str, body=None, raw: bytes | None = None):
        status, parsed = 0, None
        for _ in range(10):
            wait = self.delay - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            status, parsed, _ = c.http(method, path, body, self.key, raw_body=raw)
            self._last = time.monotonic()
            if status != 429:
                return status, parsed
            sec = parsed.get("retryAfterSeconds", 1) if isinstance(parsed, dict) else 1
            time.sleep(max(1, min(int(sec or 1), 60)))
        return status, parsed

    def remember(self, obj: str, parsed) -> list[str]:
        rec = c.first_record(parsed)
        recs = rec if isinstance(rec, list) else [rec]
        ids = [r["id"] for r in recs if isinstance(r, dict) and "id" in r]
        self.created_ids[obj].extend(ids)
        return ids

    def check(self, cid: str, sc: str, obj: str, desc: str, method: str, path: str, status: int, expect,
              companies, ok_extra: bool = True, note: str = "", bug: str = "", body=None, raw: bytes | None = None):
        if expect is None:
            verdict = "QUAN SÁT"
        else:
            verdict = "ĐẠT" if status in expect and ok_extra else "LỆCH"
        same = "" if companies is None else ("GIỐNG" if status == companies else "KHÁC")
        self.rows.append({
            "id": cid, "sc": sc, "object": obj, "desc": desc, "method": method, "path": path, "status": status,
            "expect": sorted(expect) if expect else None, "verdict": verdict, "companies_0211": companies,
            "same_as_companies": same, "note": note, "bug": bug,
            "curl": curl_cmd(method, path, body, raw),
        })
        tail = f"  [{bug}]" if bug else ""
        print(f"{cid:<6} {obj:<7} {status:<4} {verdict:<9} {same:<6} {desc}{(' | ' + note) if note else ''}{tail}")


def curl_cmd(method: str, path: str, body=None, raw: bytes | None = None) -> str:
    url = c.rest_url() + path
    parts = [f'curl -s -X {method} "{url}"', '-H "Authorization: Bearer $TWENTY_API_KEY"']
    data = None
    if raw is not None:
        data = raw.decode("utf-8", "replace")
    elif body is not None:
        data = json.dumps(body, ensure_ascii=False)
        if len(data) > 300:  # batch lớn: ghi bằng lệnh python sinh body thay vì dán cả mảng
            data = None
            n = len(body) if isinstance(body, list) else 0
            parts.append('-H "Content-Type: application/json"')
            parts.append(f"--data-binary @body-{n}.json  # tạo body bằng hàm build() trong script, {n} phần tử")
            return " ".join(parts)
    if data is not None:
        parts.append('-H "Content-Type: application/json"')
        parts.append("-d '" + data.replace("'", "'\\''") + "'")
    return " ".join(parts)


def count_of(parsed, plural: str) -> int:
    data = parsed.get("data") if isinstance(parsed, dict) else None
    return len(data.get(plural) or []) if isinstance(data, dict) else -1


# ---- SC4: batch --------------------------------------------------------------------------
def sc4(r: Runner, obj: str) -> None:
    print(f"\n== SC4: POST /batch/{obj}")
    path = f"/batch/{obj}"
    # (mã ca, số phần tử, kỳ vọng, mã Companies 02/11, lỗi đã thấy trên Companies)
    for cid, n, expect, comp, bug in [
        ("P4-01", 0, None, 201, "G-03"), ("P4-02", 1, {200, 201}, 201, ""), ("P4-05", 61, {200, 201}, 201, ""),
        ("P4-03", 200, {200, 201}, 201, ""),
    ]:
        body = [build(obj, f"B{n}", i) for i in range(n)]
        s, p = r.http("POST", path, body)
        ids = r.remember(obj, p) if s in (200, 201) else []
        r.check(cid, "SC4", obj, f"batch {n} bản ghi", "POST", path, s, expect, comp,
                ok_extra=(len(ids) == n), note=f"tạo {len(ids)} bản ghi", bug=bug, body=body)
    body = [build(obj, "B201", i) for i in range(201)]
    s, p = r.http("POST", path, body)
    ids = r.remember(obj, p) if s in (200, 201) else []
    msg = json.dumps(p, ensure_ascii=False) if p is not None else ""
    r.check("P4-04", "SC4", obj, "batch 201 bản ghi", "POST", path, s, {400, 413, 422}, 400,
            ok_extra=("Maximum number of records to upsert is 200" in msg and not ids),
            note=f"tạo {len(ids)} bản ghi", body=body)
    f = TITLE_FIELD[obj]
    for cid, raw, desc, comp, bug in [
        ("P4-06", f'{{"{f}":"x"}}'.encode(), "object thay vì mảng", 400, "G-05"),
        ("P4-07", f'[{{"{f}":123}},null,"x"]'.encode(), f"mảng có phần tử sai kiểu ({f}=123), null và chuỗi", 400, "G-05"),
        ("P4-08", b"{khong phai json", "JSON hỏng", 400, ""),
    ]:
        s, p = r.http("POST", path, raw=raw)
        err = p.get("error") if isinstance(p, dict) else None
        r.check(cid, "SC4", obj, desc, "POST", path, s, {400, 422}, comp,
                ok_extra=(err != "TypeError"), note=f"error={err}", bug=bug, raw=raw)


# ---- SC3: phân trang, lọc, sắp xếp -------------------------------------------------------
def sc3(r: Runner, obj: str) -> None:
    print(f"\n== SC3: GET /{obj} (phân trang, lọc, sắp xếp)")
    s, p = r.http("GET", f"/{obj}?limit=200")
    have = count_of(p, obj)
    if have < 200:  # cần hơn 200 bản ghi để kiểm biên 200
        need = 210 - max(have, 0)
        for start in range(0, need, 200):
            n = min(200, need - start)
            body = [build(obj, f"S3{start}", i) for i in range(n)]
            s2, p2 = r.http("POST", f"/batch/{obj}", body)
            if s2 in (200, 201):
                r.remember(obj, p2)
            else:
                print(f"   Không tạo đủ dữ liệu cho SC3 ({s2}); các ca biên 200 có thể LỆCH vì thiếu bản ghi.")
    field = TITLE_FIELD[obj]
    for cid, q, expect, n_expect, comp, bug in [
        ("P3-01", "limit=0", None, None, 200, ""), ("P3-02", "limit=1", {200}, 1, 200, ""),
        ("P3-03", "limit=60", {200}, 60, 200, ""), ("P3-04", "limit=200", {200}, 200, 200, ""),
        ("P3-05", "limit=201", {400}, None, 200, "G-04"), ("P3-06", "limit=100000", {400}, None, 200, "G-04"),
        ("P3-07", "limit=-1", {400}, None, 400, ""), ("P3-08", "limit=abc", {400}, None, 400, ""),
        ("P3-09", "limit=1.5", None, None, 400, ""), ("P3-10", "limit=", None, None, 200, ""),
        ("P3-11", "starting_after=khong-phai-cursor", None, None, 400, ""),
        ("P3-12", "ending_before=%00", None, None, 400, ""), ("P3-13", "order_by=khongtontai", None, None, 400, ""),
        ("P3-14", f"filter={field}%5Beq", None, None, 400, ""), ("P3-15", "depth=99", None, None, 400, ""),
    ]:
        path = f"/{obj}?{q}"
        s, p = r.http("GET", path)
        n = count_of(p, obj) if s == 200 else None
        r.check(cid, "SC3", obj, q, "GET", path, s, expect, comp,
                ok_extra=(n_expect is None or n == n_expect),
                note=(f"trả {n} bản ghi" if n is not None else ""), bug=bug)
    for cid, path, expect, comp in [("P3-16", f"/{obj}/not-a-uuid", None, 400),
                                    ("P3-17", f"/{obj}/{MISSING}", {404}, 404)]:
        s, _ = r.http("GET", path)
        r.check(cid, "SC3", obj, path, "GET", path, s, expect, comp)


# ---- dọn dẹp và báo cáo ------------------------------------------------------------------
def cleanup(r: Runner) -> None:
    print("\n== Dọn dữ liệu K05-TIEN-")
    for obj, ids in r.created_ids.items():
        left = []
        for rid in dict.fromkeys(ids):
            s, _ = r.http("DELETE", f"/{obj}/{rid}")
            if s not in (200, 404):
                left.append(rid)
        if ids:
            print(f"{obj}: đã xoá {len(set(ids)) - len(left)}" + (f", còn {len(left)} chưa xoá: {left[:5]}" if left else ""))


def write_report(r: Runner, key: str, stamp: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Kết quả SC3, SC4 phần Tiến", "", f"Thời điểm: {stamp}. Môi trường: {c.base_url()}.", "",
             "| Mã | Kịch bản | Object | Ca | Mã trả về | Kỳ vọng | Kết luận | Companies 02/11 | So với Companies | Ghi chú | Lỗi |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in r.rows:
        lines.append(f"| {x['id']} | {x['sc']} | {x['object']} | {x['desc']} | {x['status']} | {x['expect'] or 'quan sát'} | "
                     f"{x['verdict']} | {x['companies_0211']} | {x['same_as_companies']} | {x['note']} | {x['bug']} |")
    repro = [x for x in r.rows if x["verdict"] != "ĐẠT"]
    if repro:
        lines += ["", "## Lệnh tái hiện (ca LỆCH và QUAN SÁT)", "",
                  "Đặt khoá trước: PowerShell `$env:TWENTY_API_KEY=\"...\"` (dùng `curl.exe`), bash `export TWENTY_API_KEY=...`.", ""]
        for x in repro:
            lines += [f"**{x['id']} {x['object']}** ({x['verdict']}, trả {x['status']}): {x['desc']}", "",
                      "```bash", x["curl"], "```", ""]
    md = c.redact_text("\n".join(lines) + "\n", [key])
    (OUT_DIR / f"{stamp}.md").write_text(md, encoding="utf-8")
    (OUT_DIR / f"{stamp}.json").write_text(
        c.redact_text(json.dumps(r.rows, ensure_ascii=False, indent=2), [key]), encoding="utf-8")
    print(f"\nĐã ghi reports/kiem-thu-tien/{stamp}.md")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--only", default="sc4,sc3", help="sc3, sc4 hoặc sc3,sc4")
    ap.add_argument("--objects", default="", help="ghi đè object, ví dụ notes hoặc people,notes "
                                                    "(mặc định: SC3 notes,tasks; SC4 people,notes)")
    ap.add_argument("--delay", type=float, default=DELAY, help="số giây giữa hai request (mặc định 1)")
    args = ap.parse_args()
    only = [x.strip().lower() for x in args.only.split(",") if x.strip()]
    override = [x.strip().lower() for x in args.objects.split(",") if x.strip()]
    bad = [o for o in override if o not in OBJECTS]
    if bad:
        raise SystemExit(f"Object không hợp lệ: {bad}. Chọn trong {OBJECTS}.")
    c.load_env()
    c.assert_localhost(c.base_url())
    key = c.api_key()
    r = Runner(key, args.delay)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    print(f"{'Mã':<6} {'Object':<7} {'Mã':<4} {'Kết luận':<9} {'Comp.':<6} Ca")
    try:
        for name, fn in (("sc4", sc4), ("sc3", sc3)):  # SC4 trước: lỗi ở batch được thấy sớm
            if name in only:
                for obj in (override or DEFAULT_PLAN[name]):
                    fn(r, obj)
    finally:
        cleanup(r)
    write_report(r, key, stamp)
    n = {v: sum(1 for x in r.rows if x["verdict"] == v) for v in ("ĐẠT", "LỆCH", "QUAN SÁT")}
    print(f"Tổng {len(r.rows)} ca: ĐẠT {n['ĐẠT']}, LỆCH {n['LỆCH']}, QUAN SÁT {n['QUAN SÁT']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
