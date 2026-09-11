"""The BaseHTTPRequestHandler wrapper every endpoint subclasses.

Vercel's Python runtime looks for a class called `handler` in each file under
api/. Everything those four files have in common is here: the method guard,
the origin check, the honeypot, JSON in and JSON out, and turning a Rejected
into the right status code.
"""
import json
import sys
import pathlib
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _lib import http as H          # noqa: E402
from _lib.db import connect          # noqa: E402


class JsonPost(BaseHTTPRequestHandler):
    """Subclass and implement `act(self, data, conn, ip_hash)`."""

    # Set to False on endpoints reached by a link rather than a form post.
    requires_origin = True

    def act(self, data, conn, ip_hash):
        raise NotImplementedError

    # ---- plumbing --------------------------------------------------------

    def _send(self, status, body):
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        # This API is same origin only. Saying so explicitly stops a future
        # reader assuming the absence of a CORS header is an oversight.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        try:
            if self.requires_origin and not H.origin_ok(self.headers):
                raise H.Rejected(403, "This form can only be used on the site.")

            length = int(self.headers.get("content-length") or 0)
            data = H.read_json(self.rfile.read(length) if length else b"")

            # The honeypot is answered with success on purpose. A bot told it
            # failed will try again with the field left blank.
            if (data.get(H.HONEYPOT) or "").strip():
                return self._send(200, {"ok": True})

            ip_hash = H.hash_ip(H.client_ip(self.headers))

            with connect("SITE_DATABASE_URL") as conn:
                result = self.act(data, conn, ip_hash)
                conn.commit()
            self._send(200, result or {"ok": True})

        except H.Rejected as e:
            self._send(e.status, {"ok": False, "error": e.message})
        except Exception:
            # Never leak a database error to the browser: the text of one
            # names tables and columns. It goes to the Vercel log instead.
            import traceback
            traceback.print_exc()
            self._send(500, {"ok": False, "error": "Something went wrong. Please try again."})

    def do_GET(self):
        self._send(405, {"ok": False, "error": "Use POST."})
