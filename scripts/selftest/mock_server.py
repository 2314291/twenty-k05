#!/usr/bin/env python3
"""MOCK — máy chủ giả để tự kiểm tra script K05. KHÔNG phải Twenty.

Mô phỏng tối thiểu: /rest/{companies,people,opportunities,notes,tasks} (GET/POST/PATCH/DELETE), /rest/batch/{...},
/open-api/core. Lỗi cố ý: GET /rest/companies?limit=200 -> 500.
Bản ghi có createdAt theo đồng hồ của máy chủ giả; MOCK_CLOCK_SKEW=<giây> làm đồng hồ đó chạy nhanh hơn máy thật
(mô phỏng container Docker lệch giờ với Windows). GET danh sách hiểu order_by=createdAt[Desc...] và limit.
"""
import datetime as dt
import json
import os
import re
import sys
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

KEY = "mock-key-123"
STORE = {"companies": {}, "people": {}, "opportunities": {}, "notes": {}, "tasks": {}}
SINGULAR = {"companies": "Company", "people": "Person", "opportunities": "Opportunity", "notes": "Note", "tasks": "Task"}
SKEW = float(os.environ.get("MOCK_CLOCK_SKEW", "0"))


def created_at() -> str:
    t = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=SKEW)
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"
BATCH_MAX = 200


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        raw = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(n) or b"null")
        except ValueError:
            return ValueError

    def _route(self, method):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query, keep_blank_values=True).items()}
        if u.path == "/open-api/core":
            return self._send(200, {"openapi": "3.0.3", "paths": {}})
        if self.headers.get("Authorization") != f"Bearer {KEY}":
            return self._send(401, {"statusCode": 401, "error": "Unauthorized"})
        m = re.fullmatch(r"/rest/(batch/)?(companies|people|opportunities|notes|tasks)(?:/([^/]+))?", u.path)
        if not m:
            return self._send(404, {"error": "NotFound"})
        batch, plural, rid = m.group(1), m.group(2), m.group(3)
        db = STORE[plural]
        if method == "GET" and not rid and not batch:
            if "limit" in q:
                try:
                    lim = int(q["limit"])
                except ValueError:
                    return self._send(400, {"error": "BadRequest"})
                if lim < 0:
                    return self._send(400, {"error": "BadRequest"})
                if lim == 200:
                    return self._send(500, {"error": "MOCK defect: limit=200"})
            rows = list(db.values())
            if q.get("order_by", "").startswith("createdAt[Desc"):
                rows.sort(key=lambda r: r.get("createdAt", ""), reverse=True)
            if "limit" in q:
                rows = rows[:lim]
            return self._send(200, {"data": {plural: rows}, "totalCount": len(db)})
        if method == "GET" and rid:
            return self._send(200, {"data": {SINGULAR[plural].lower(): db[rid]}}) if rid in db else self._send(404, {"error": "NotFound"})
        if method == "POST":
            body = self._body()
            if body is ValueError:
                return self._send(400, {"error": "BadRequest"})
            if batch:
                if not isinstance(body, list):
                    return self._send(400, {"error": "BadRequest"})
                if len(body) > BATCH_MAX:
                    return self._send(400, {"error": f"Maximum number of records to upsert is {BATCH_MAX}."})
                out = []
                for b in body:
                    if not isinstance(b, dict) or not isinstance(b.get("name", ""), (str, dict)):
                        return self._send(400, {"error": "BadRequest"})
                    r = {"id": str(uuid.uuid4()), "createdAt": created_at(), **b}
                    db[r["id"]] = r
                    out.append(r)
                return self._send(201, {"data": {"create" + plural.capitalize(): out}})
            if not isinstance(body, dict):
                return self._send(400, {"error": "BadRequest"})
            r = {"id": str(uuid.uuid4()), "createdAt": created_at(), **body}
            db[r["id"]] = r
            return self._send(201, {"data": {"create" + SINGULAR[plural]: r}})
        if method == "PATCH" and rid:
            body = self._body()
            if rid not in db:
                return self._send(404, {"error": "NotFound"})
            db[rid].update(body if isinstance(body, dict) else {})
            return self._send(200, {"data": {"update" + SINGULAR[plural]: db[rid]}})
        if method == "DELETE" and rid:
            return self._send(200, {"data": {"delete": db.pop(rid)}}) if rid in db else self._send(404, {"error": "NotFound"})
        self._send(405, {"error": "MethodNotAllowed"})

    do_GET = lambda self: self._route("GET")
    do_POST = lambda self: self._route("POST")
    do_PATCH = lambda self: self._route("PATCH")
    do_DELETE = lambda self: self._route("DELETE")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3001
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
