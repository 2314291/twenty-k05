#!/usr/bin/env python3
"""Thăm dò giá trị biên có chủ đích (SC3 phân trang, SC4 batch, SC5 xác thực) bằng HTTP thuần.

Schemathesis sinh dữ liệu theo schema nên không chắc chạm đúng các biên 0/1/200/201. Script này gọi trực
tiếp từng ca và so với kỳ vọng rút ra từ MÃ NGUỒN v2.45.6 (docs/architecture.md mục 5).

  kỳ vọng ĐẶT (expect)  -> kết quả MATCH hoặc DIFF (DIFF = ứng viên lỗi, phải xác minh thủ công + RCA)
  kỳ vọng None          -> chỉ QUAN SÁT (ghi lại hành vi, chưa có căn cứ để gọi là lỗi)

    python scripts/probe_boundaries.py [--only sc3,sc4,sc5]
Ghi: reports/probes/<thời điểm>.json và .md (key đã redact). Dọn bản ghi tạo ra sau khi chạy.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import uuid

import k05_common as c

MISSING_UUID = str(uuid.UUID(int=0x20202020_0000_4000_8000_000000000001))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--only", default="sc3,sc4,sc5")
    args = ap.parse_args()
    only = {s.strip().lower() for s in args.only.split(",")}
    c.load_env()
    c.assert_localhost(c.base_url())
    key = c.api_key()
    limited = c.api_key("TWENTY_API_KEY_LIMITED", required=False)
    created: list[str] = []
    rows: list[dict] = []

    def case(cid, sc, desc, method, path, expect, *, body=None, k=key, raw=None, headers=None):
        status, parsed, secs = c.http(method, path, body, k, raw_body=raw, headers=headers)
        if method == "POST" and 200 <= status < 300:
            recs = c.first_record(parsed)
            for rec in (recs if isinstance(recs, list) else [recs]):
                if isinstance(rec, dict) and "id" in rec:
                    created.append(rec["id"])
        verdict = "OBSERVE" if expect is None else ("MATCH" if status in expect else "DIFF")
        snippet = json.dumps(parsed, ensure_ascii=False)[:160] if parsed is not None else ""
        rows.append({"id": cid, "scenario": sc, "desc": desc, "request": f"{method} {path}",
                     "expect": sorted(expect) if expect else None, "status": status, "verdict": verdict,
                     "seconds": round(secs, 3), "response_head": snippet})
        print(f"{cid:<8}{verdict:<8}{status}  {method} {path[:70]}  — {desc}")
        return status, parsed

    def mk(n):
        return [{"name": f"K05-PROBE-{uuid.uuid4().hex[:8]}-{i}"} for i in range(n)]

    if "sc3" in only:
        # Kỳ vọng từ parse-limit-rest-request.util.ts: <0 hoặc NaN -> lỗi; >200 bị cắt về 200, không báo lỗi.
        for cid, v, exp, d in [
            ("P3-01", "0", None, "limit=0 (biên dưới)"), ("P3-02", "1", {200}, "limit=1"),
            ("P3-03", "60", {200}, "limit=60 (mặc định)"), ("P3-04", "200", {200}, "limit=200 (QUERY_MAX_RECORDS)"),
            ("P3-05", "201", None, "limit=201: mã nguồn cắt về 200 âm thầm (H1) -> quan sát"),
            ("P3-06", "100000", None, "limit rất lớn"), ("P3-07", "-1", {400}, "limit âm"),
            ("P3-08", "abc", {400}, "limit không phải số"), ("P3-09", "1.5", None, "limit thập phân"),
            ("P3-10", "", None, "limit rỗng"),
        ]:
            case(cid, "SC3", d, "GET", f"/companies?limit={v}", exp)
        case("P3-11", "SC3", "starting_after rác", "GET", "/companies?starting_after=khong-phai-cursor", None)
        case("P3-12", "SC3", "ending_before rác", "GET", "/companies?ending_before=%00", None)
        case("P3-13", "SC3", "order_by trường không tồn tại", "GET", "/companies?order_by=khongtontai", None)
        case("P3-14", "SC3", "filter sai cú pháp", "GET", "/companies?filter=name[eq", None)
        case("P3-15", "SC3", "depth ngoài khoảng", "GET", "/companies?depth=99", None)
        case("P3-16", "SC3", "id không phải UUID", "GET", "/companies/not-a-uuid", None)
        case("P3-17", "SC3", "id UUID hợp lệ nhưng không tồn tại", "GET", f"/companies/{MISSING_UUID}", {404})

    if "sc4" in only:
        case("P4-01", "SC4", "batch rỗng []", "POST", "/batch/companies", None, body=[])
        s, p = case("P4-02", "SC4", "batch 1 bản ghi", "POST", "/batch/companies", {200, 201}, body=mk(1))
        s, p = case("P4-03", "SC4", "batch 200 bản ghi (biên trên)", "POST", "/batch/companies", {200, 201}, body=mk(200))
        s, p = case("P4-04", "SC4", "batch 201 bản ghi: mã nguồn báo 'Maximum number of records to upsert is 200'",
                    "POST", "/batch/companies", {400, 413, 422}, body=mk(201))
        case("P4-05", "SC4", "batch 61 bản ghi (giá trị 60 trong ghi chú nhóm: kiểm tra có bị chặn không)",
             "POST", "/batch/companies", {200, 201}, body=mk(61))
        case("P4-06", "SC4", "body là object thay vì mảng", "POST", "/batch/companies", None, body={"name": "x"})
        case("P4-07", "SC4", "mảng chứa phần tử không hợp lệ", "POST", "/batch/companies", None, body=[{"name": 123}, None, "x"])
        case("P4-08", "SC4", "JSON hỏng", "POST", "/batch/companies", None, raw=b"{khong phai json")

    if "sc5" in only:
        case("P5-01", "SC5", "không gửi key", "GET", "/companies", {401}, k=None)
        case("P5-02", "SC5", "key sai", "GET", "/companies", {401}, k="k05-sai-key-000000")
        case("P5-03", "SC5", "scheme sai (Basic)", "GET", "/companies", {401}, k=None, headers={"Authorization": "Basic YTpi"})
        case("P5-04", "SC5", "Bearer rỗng", "GET", "/companies", {401}, k=None, headers={"Authorization": "Bearer "})
        case("P5-05", "SC5", "ghi không có key", "POST", "/companies", {401}, k=None, body={"name": "K05-PROBE-noauth"})
        case("P5-06", "SC5", "/open-api/core không key (endpoint công khai, kỳ vọng khung schema)", "GET", "/open-api/core", None, k=None)
        if limited:
            case("P5-07", "SC5", "key role giới hạn: đọc", "GET", "/companies?limit=1", {200}, k=limited)
            case("P5-08", "SC5", "key role giới hạn: ghi (nếu role chỉ đọc -> 403)", "POST", "/companies", {403}, k=limited,
                 body={"name": "K05-PROBE-limited"})
        else:
            print("(bỏ qua P5-07/08: chưa có TWENTY_API_KEY_LIMITED)")

    # Dọn dẹp mọi bản ghi đã tạo (ID lấy từ phản hồi POST)
    for rid in created:
        c.http("DELETE", f"/companies/{rid}", key=key)
    print(f"Dọn: đã xoá {len(created)} bản ghi K05-PROBE (nếu còn sót, xoá tay hoặc dùng seed.py --cleanup).")

    out_dir = c.ROOT / "reports" / "probes"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    secrets = [key, limited]
    (out_dir / f"{stamp}.json").write_text(c.redact_text(json.dumps(rows, ensure_ascii=False, indent=2), secrets), encoding="utf-8")
    md = ["# Kết quả thăm dò biên", "", "| ID | SC | Mô tả | Yêu cầu | Kỳ vọng | Thực tế | Kết luận |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['id']} | {r['scenario']} | {r['desc']} | `{r['request']}` | {r['expect'] or '—'} | {r['status']} | **{r['verdict']}** |")
    n_diff = sum(r["verdict"] == "DIFF" for r in rows)
    md += ["", f"Tổng {len(rows)} ca: MATCH {sum(r['verdict'] == 'MATCH' for r in rows)}, DIFF {n_diff}, "
               f"OBSERVE {sum(r['verdict'] == 'OBSERVE' for r in rows)}.",
           "DIFF/OBSERVE bất thường phải xác minh thủ công bằng curl rồi ghi vào bảng lỗi (mục G)."]
    (out_dir / f"{stamp}.md").write_text(c.redact_text("\n".join(md), secrets), encoding="utf-8")
    print(f"\nĐã ghi reports/probes/{stamp}.json và .md. DIFF = {n_diff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
