#!/usr/bin/env python3
"""Chạy lại các ca SC3, SC4, SC6 đã kiểm thử tay ngày 02/11/2026 (Trung), để người khác ra cùng kết quả.

    python scripts/kiem_thu_sc3_sc4_sc6.py                 # chạy cả ba, khoảng 12 phút
    python scripts/kiem_thu_sc3_sc4_sc6.py --only sc6      # chỉ SC6 trên Companies, khoảng 1 phút
    python scripts/kiem_thu_sc3_sc4_sc6.py --only sc6 --objects all   # SC6 trên cả 5 object, khoảng 5 phút

Yêu cầu: Twenty v2.45.6 chạy ở localhost, TWENTY_API_KEY (role Admin) trong .env.
Mỗi ca in: mã trả về, kết luận so với kỳ vọng (ĐẠT / LỆCH / QUAN SÁT) và so với lần chạy tay 02/11 (GIỐNG / KHÁC).
Kỳ vọng và mã lỗi G-xx lấy từ docs/dac-ta-sc3-sc4.md và docs/du-lieu-sc5-sc6.md.

- Đi chậm 1 request mỗi giây vì Twenty giới hạn 100 request mỗi 60 giây cho mỗi khoá (G-01); gặp 429 thì chờ rồi gửi lại.
- Mọi bản ghi tạo ra có tên bắt đầu bằng K05-CB- và được xoá vĩnh viễn ở cuối, kể cả khi có ca lỗi.
- Kết quả ghi vào reports/kiem-thu-tay/<thời điểm>.md và .json; khoá API được che.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from urllib.parse import quote

import k05_common as c

PREFIX = "K05-CB-"
MISSING = "00000000-0000-4000-8000-000000000000"
DELAY = 1.0
OBJECTS = ("companies", "people", "opportunities", "notes", "tasks")
CLEANUP_ORDER = ("tasks", "notes", "opportunities", "people", "companies")  # bản ghi phụ thuộc xoá trước
OUT_DIR = c.ROOT / "reports" / "kiem-thu-tay"


class Runner:
    def __init__(self, key: str, delay: float):
        self.key, self.delay, self.rows, self._last = key, delay, [], 0.0
        self.ids: dict[str, list[str]] = {o: [] for o in OBJECTS}

    # ---- gửi request ------------------------------------------------------------------
    def http(self, method: str, path: str, body=None, raw: bytes | None = None):
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

    # ---- ghi kết quả -----------------------------------------------------------------
    def check(self, cid: str, sc: str, desc: str, method: str, path: str, status: int, expect, manual,
              ok_extra: bool = True, note: str = "", bug: str = ""):
        if expect is None:
            verdict = "QUAN SÁT"
        else:
            verdict = "ĐẠT" if status in expect and ok_extra else "LỆCH"
        same = "" if manual is None else ("GIỐNG" if status == manual else "KHÁC")
        self.rows.append({"id": cid, "sc": sc, "desc": desc, "request": f"{method} {path[:90]}", "status": status,
                          "expect": sorted(expect) if expect else None, "verdict": verdict, "manual_0211": manual,
                          "same_as_manual": same, "note": note, "bug": bug})
        tail = f"  [{bug}]" if bug else ""
        print(f"{cid:<8} {status:<4} {verdict:<9} {same:<6} {desc}{(' | ' + note) if note else ''}{tail}")

    def created(self, parsed, kind: str):
        rec = c.first_record(parsed)
        recs = rec if isinstance(rec, list) else [rec]
        ids = [r["id"] for r in recs if isinstance(r, dict) and "id" in r]
        self.ids[kind].extend(ids)
        return ids


def batch_body(n: int, tag: str) -> list[dict]:
    return [{"name": f"{PREFIX}{tag}-{i}"} for i in range(n)]


def count_of(parsed, plural: str) -> int:
    data = parsed.get("data") if isinstance(parsed, dict) else None
    return len(data.get(plural) or []) if isinstance(data, dict) else -1


# ---- SC4 ---------------------------------------------------------------------------------
def sc4(r: Runner) -> None:
    print("\n== SC4: batch POST /batch/companies")
    for cid, n, expect, manual, bug in [
        ("P4-01", 0, None, 201, "G-03"), ("P4-02", 1, {200, 201}, 201, ""), ("B-03", 2, {200, 201}, 201, ""),
        ("P4-05", 61, {200, 201}, 201, ""), ("B-05", 199, {200, 201}, 201, ""), ("P4-03", 200, {200, 201}, 201, ""),
    ]:
        s, p = r.http("POST", "/batch/companies", batch_body(n, f"B{n}"))
        ids = r.created(p, "companies") if s in (200, 201) else []
        r.check(cid, "SC4", f"batch {n} bản ghi", "POST", "/batch/companies", s, expect, manual,
                ok_extra=(len(ids) == n), note=f"tạo {len(ids)} bản ghi", bug=bug)
    s, p = r.http("POST", "/batch/companies", batch_body(201, "B201"))
    ids = r.created(p, "companies") if s in (200, 201) else []
    msg = json.dumps(p, ensure_ascii=False) if p is not None else ""
    r.check("P4-04", "SC4", "batch 201 bản ghi", "POST", "/batch/companies", s, {400, 413, 422}, 400,
            ok_extra=("Maximum number of records to upsert is 200" in msg and not ids), note=f"tạo {len(ids)} bản ghi")
    for cid, raw, desc, manual, bug in [
        ("P4-06", b'{"name":"x"}', "object thay vì mảng", 400, "G-05"),
        ("P4-07", b'[{"name":123},null,"x"]', "mảng có phần tử null và chuỗi", 400, "G-05"),
        ("P4-08", b"{khong phai json", "JSON hỏng", 400, ""),
    ]:
        s, p = r.http("POST", "/batch/companies", raw=raw)
        err = p.get("error") if isinstance(p, dict) else None
        r.check(cid, "SC4", desc, "POST", "/batch/companies", s, {400, 422}, manual,
                ok_extra=(err != "TypeError"), note=f"error={err}", bug=bug)


# ---- SC3 ---------------------------------------------------------------------------------
def sc3(r: Runner) -> None:
    print("\n== SC3: GET /companies (phân trang, lọc, sắp xếp)")
    s, p = r.http("GET", "/companies?limit=200")
    if count_of(p, "companies") < 200:  # cần hơn 200 công ty để kiểm biên 200
        for tag, n in (("S3A", 200), ("S3B", 10)):
            s2, p2 = r.http("POST", "/batch/companies", batch_body(n, tag))
            if s2 in (200, 201):
                r.created(p2, "companies")
    for cid, q, expect, n_expect, manual, bug in [
        ("P3-01", "limit=0", None, None, 200, ""), ("P3-02", "limit=1", {200}, 1, 200, ""),
        ("P3-03", "limit=60", {200}, 60, 200, ""), ("P3-04", "limit=200", {200}, 200, 200, ""),
        ("P3-05", "limit=201", {400}, None, 200, "G-04"), ("P3-06", "limit=100000", {400}, None, 200, "G-04"),
        ("P3-07", "limit=-1", {400}, None, 400, ""), ("P3-08", "limit=abc", {400}, None, 400, ""),
        ("P3-09", "limit=1.5", None, None, 400, ""), ("P3-10", "limit=", None, None, 200, ""),
        ("P3-11", "starting_after=khong-phai-cursor", None, None, 400, ""),
        ("P3-12", "ending_before=%00", None, None, 400, ""), ("P3-13", "order_by=khongtontai", None, None, 400, ""),
        ("P3-14", "filter=name%5Beq", None, None, 400, ""), ("P3-15", "depth=99", None, None, 400, ""),
    ]:
        path = f"/companies?{q}"
        s, p = r.http("GET", path)
        n = count_of(p, "companies") if s == 200 else None
        r.check(cid, "SC3", q, "GET", path, s, expect, manual,
                ok_extra=(n_expect is None or n == n_expect), note=(f"trả {n} bản ghi" if n is not None else ""), bug=bug)
    for cid, path, expect, manual in [("P3-16", "/companies/not-a-uuid", None, 400),
                                      ("P3-17", f"/companies/{MISSING}", {404}, 404)]:
        s, _ = r.http("GET", path)
        r.check(cid, "SC3", path, "GET", path, s, expect, manual)


# ---- SC6 ---------------------------------------------------------------------------------
def _get(rec, path: str):
    for k in path.split("."):
        rec = rec.get(k) if isinstance(rec, dict) else None
    return rec


# Mỗi object: tên số ít trong phản hồi, body tạo, body sửa, trường được sửa và giá trị mới,
# trường phải giữ nguyên sau khi sửa. Body giống lần chạy tay ngày 12/11/2026 (E-13), tiền tố K05-CB-.
SC6_CFG = {
    "companies": dict(one="company", create={"name": f"{PREFIX}SC6", "domainName": {"primaryLinkUrl": "https://k05-sc6.example.com"}},
                      edit={"name": f"{PREFIX}SC6-sua"}, changed=("name", f"{PREFIX}SC6-sua"), keep="domainName.primaryLinkUrl"),
    "people": dict(one="person", create={"name": {"firstName": f"{PREFIX}SC6", "lastName": "Nguoi"},
                                          "emails": {"primaryEmail": "k05.cb.sc6@example.com"}},
                   edit={"name": {"firstName": f"{PREFIX}SC6-sua", "lastName": "Nguoi"}},
                   changed=("name.firstName", f"{PREFIX}SC6-sua"), keep="emails.primaryEmail"),
    "opportunities": dict(one="opportunity", create={"name": f"{PREFIX}SC6-Opp", "stage": "NEW",
                                                      "amount": {"amountMicros": 1000000, "currencyCode": "USD"}},
                          edit={"stage": "MEETING"}, changed=("stage", "MEETING"), keep="amount.amountMicros"),
    "notes": dict(one="note", create={"title": f"{PREFIX}SC6-Note", "bodyV2": {"markdown": "Noi dung K05"}},
                  edit={"title": f"{PREFIX}SC6-Note-sua"}, changed=("title", f"{PREFIX}SC6-Note-sua"), keep="bodyV2.markdown"),
    "tasks": dict(one="task", create={"title": f"{PREFIX}SC6-Task", "status": "TODO", "dueAt": "2026-12-31T00:00:00.000Z"},
                  edit={"status": "DONE"}, changed=("status", "DONE"), keep="title"),
}


def sc6(r: Runner, obj: str = "companies") -> None:
    cfg = SC6_CFG[obj]
    sc = "SC6" if obj == "companies" else f"SC6-{obj}"
    print(f"\n== SC6: vòng đời một bản ghi ({obj})")
    s, p = r.http("POST", f"/{obj}", cfg["create"])
    ids = r.created(p, obj) if s in (200, 201) else []
    r.check("S6-01", sc, "tạo bản ghi", "POST", f"/{obj}", s, {201}, 201, ok_extra=bool(ids))
    if not ids:
        print(f"   Không tạo được bản ghi {obj}, bỏ qua phần còn lại của SC6 trên object này.")
        return
    rid = ids[0]
    s, p = r.http("GET", f"/{obj}/{rid}")
    rec = c.first_record(p) or {}
    kept_before = _get(rec, cfg["keep"])
    note = f"{cfg['keep']} = {kept_before!r}"
    if obj == "companies":
        note += " (gửi kèm https://)"
    r.check("S6-02", sc, "đọc lại", "GET", f"/{obj}/{rid}", s, {200}, 200, ok_extra=kept_before is not None, note=note)
    s, _ = r.http("PATCH", f"/{obj}/{rid}", cfg["edit"])
    r.check("S6-03", sc, f"sửa {cfg['changed'][0]}", "PATCH", f"/{obj}/{rid}", s, {200}, 200)
    s, p = r.http("GET", f"/{obj}/{rid}")
    rec = c.first_record(p) or {}
    field, want = cfg["changed"]
    ok = _get(rec, field) == want and _get(rec, cfg["keep"]) == kept_before
    r.check("S6-04", sc, "đọc sau sửa", "GET", f"/{obj}/{rid}", s, {200}, 200, ok_extra=ok,
            note=f"{field} = {_get(rec, field)!r}, {cfg['keep']} giữ nguyên = {_get(rec, cfg['keep']) == kept_before}")
    path = f"/{obj}?filter=" + quote(f"id[eq]:{rid}", safe="")
    s, p = r.http("GET", path)
    r.check("S6-05", sc, "lọc theo id", "GET", path, s, {200}, 200, ok_extra=count_of(p, obj) == 1,
            note=f"trả {count_of(p, obj)} bản ghi")
    for cid_, m, pth, body, exp, desc in [
        ("S6-06", "DELETE", f"/{obj}/{rid}", None, {200}, "xoá (mặc định là xoá vĩnh viễn)"),
        ("S6-07", "GET", f"/{obj}/{rid}", None, {404}, "đọc sau xoá"),
        ("S6-08", "DELETE", f"/{obj}/{rid}", None, {404}, "xoá lần hai"),
        ("S6-09", "PATCH", f"/{obj}/{rid}", cfg["edit"], {404}, "sửa sau xoá"),
        ("S6-10", "PATCH", f"/{obj}/{rid}/restore", None, {404}, "khôi phục sau xoá vĩnh viễn"),
    ]:
        s, _ = r.http(m, pth, body)
        r.check(cid_, sc, desc, m, pth, s, exp, list(exp)[0])
    if obj == "companies":  # S6-11: xoá công ty đang có người (chỉ chạy trên Companies)
        s, p = r.http("POST", "/companies", {"name": f"{PREFIX}SC6-Rel"})
        rel = r.created(p, "companies")
        if rel:
            s, p = r.http("POST", "/people", {"name": {"firstName": "K05CB", "lastName": "Rel"}, "companyId": rel[0]})
            per = r.created(p, "people")
            s, _ = r.http("DELETE", f"/companies/{rel[0]}")
            if per:
                s, p = r.http("GET", f"/people/{per[0]}")
                rec = c.first_record(p) or {}
                r.check("S6-11", sc, "đọc người sau khi xoá công ty của họ", "GET", f"/people/{per[0]}", s, None, 200,
                        note=f"companyId = {rec.get('companyId') if isinstance(rec, dict) else None!r}")
    for cid_, m, body in [("S6-12a", "GET", None), ("S6-12b", "PATCH", cfg["edit"]), ("S6-12c", "DELETE", None)]:
        s, _ = r.http(m, f"/{obj}/{MISSING}", body)
        r.check(cid_, sc, f"{m} id không tồn tại", m, f"/{obj}/{MISSING}", s, {404}, 404)
    s, p = r.http("POST", f"/{obj}", cfg["create"])  # S6-13: xoá mềm rồi khôi phục
    soft = r.created(p, obj)
    if soft:
        sid = soft[0]
        for cid_, m, pth, exp, desc in [
            ("S6-13b", "DELETE", f"/{obj}/{sid}?soft_delete=true", {200}, "xoá mềm"),
            ("S6-13c", "GET", f"/{obj}/{sid}", {404}, "đọc sau xoá mềm"),
            ("S6-13d", "PATCH", f"/{obj}/{sid}/restore", {200}, "khôi phục"),
            ("S6-13e", "GET", f"/{obj}/{sid}", {200}, "đọc sau khôi phục"),
        ]:
            s, _ = r.http(m, pth)
            r.check(cid_, sc, desc, m, pth, s, exp, list(exp)[0])


# ---- dọn dẹp -------------------------------------------------------------------------------
def cleanup(r: Runner) -> None:
    print("\n== Dọn dữ liệu K05-CB-")
    done, left = {}, []
    for obj in CLEANUP_ORDER:
        n = 0
        for rid in dict.fromkeys(r.ids[obj]):
            s, _ = r.http("DELETE", f"/{obj}/{rid}")
            if s in (200, 404):
                n += 1
            else:
                left.append(f"{obj}/{rid}")
        if r.ids[obj]:
            done[obj] = n
    print("Đã xoá " + (", ".join(f"{n} {o}" for o, n in done.items()) or "0 bản ghi") + "." +
          (f" Còn {len(left)} bản ghi chưa xoá được: {left[:5]}" if left else ""))


def write_report(r: Runner, key: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    lines = ["# Chạy lại các ca SC3, SC4, SC6", "", f"Thời điểm: {stamp}. Môi trường: {c.base_url()}.", "",
             "| Mã | Kịch bản | Ca | Mã trả về | Kỳ vọng | Kết luận | So với 02/11 | Ghi chú | Lỗi |", "|---|---|---|---|---|---|---|---|---|"]
    for x in r.rows:
        lines.append(f"| {x['id']} | {x['sc']} | {x['desc']} | {x['status']} | {x['expect'] or 'quan sát'} | {x['verdict']} | "
                     f"{x['same_as_manual']} | {x['note']} | {x['bug']} |")
    md = c.redact_text("\n".join(lines) + "\n", [key])
    (OUT_DIR / f"{stamp}.md").write_text(md, encoding="utf-8")
    (OUT_DIR / f"{stamp}.json").write_text(c.redact_text(json.dumps(r.rows, ensure_ascii=False, indent=2), [key]), encoding="utf-8")
    print(f"\nĐã ghi reports/kiem-thu-tay/{stamp}.md")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--only", default="sc4,sc3,sc6", help="danh sách kịch bản, ví dụ sc6 hoặc sc3,sc4")
    ap.add_argument("--objects", default="companies",
                    help="object cho SC6: companies (mặc định), danh sách như people,tasks, hoặc all; SC3, SC4 luôn chạy trên companies")
    ap.add_argument("--delay", type=float, default=DELAY, help="số giây giữa hai request (mặc định 1)")
    args = ap.parse_args()
    c.load_env()
    c.assert_localhost(c.base_url())
    key = c.api_key()
    r = Runner(key, args.delay)
    only = [x.strip().lower() for x in args.only.split(",") if x.strip()]
    print(f"{'Mã':<8} {'Mã':<4} {'Kết luận':<9} {'Tay':<6} Ca")
    try:
        objs = list(OBJECTS) if args.objects.strip().lower() == "all" else \
            [o.strip().lower() for o in args.objects.split(",") if o.strip()]
        bad = [o for o in objs if o not in OBJECTS]
        if bad:
            raise SystemExit(f"Object không hợp lệ: {bad}. Chọn trong {list(OBJECTS)} hoặc all.")
        if "sc4" in only:  # SC4 trước để SC3 có sẵn hơn 200 công ty
            sc4(r)
        if "sc3" in only:
            sc3(r)
        if "sc6" in only:
            for obj in objs:
                sc6(r, obj)
    finally:
        cleanup(r)
    write_report(r, key)
    n = {v: sum(1 for x in r.rows if x["verdict"] == v) for v in ("ĐẠT", "LỆCH", "QUAN SÁT")}
    khac = sum(1 for x in r.rows if x["same_as_manual"] == "KHÁC")
    print(f"Tổng {len(r.rows)} ca: ĐẠT {n['ĐẠT']}, LỆCH {n['LỆCH']}, QUAN SÁT {n['QUAN SÁT']}. Khác lần chạy tay (02/11, 12/11): {khac}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
