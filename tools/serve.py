"""Dev server for cydniejocelyn-v2.

The preview sandbox cannot read ~/Desktop, so this serves a mirror that
sync.sh writes into the session scratchpad. No-store headers are deliberate:
without them the browser serves a stale site.js and you debug code that is no
longer on disk.

Copy this and sync.sh into the session scratchpad, point .claude/launch.json
entry "cj-v2" at this file, then preview_start.
"""
import functools, http.server, os, socketserver

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "preview")
PORT = int(os.environ.get("PORT", "8620"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def log_message(self, *a):
        pass


handler = functools.partial(Handler, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
print("serving %s on %d" % (ROOT, PORT), flush=True)
socketserver.TCPServer(("127.0.0.1", PORT), handler).serve_forever()
