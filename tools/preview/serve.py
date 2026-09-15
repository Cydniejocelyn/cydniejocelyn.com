import sys, os, http.server, socketserver
root = sys.argv[1]; port = int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=root, **k)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()
    def log_message(self, *a): pass
# THREADED, 14 September 2026. A single-threaded TCPServer answered one
# connection at a time, and headless Chrome's virtual clock stops while any
# request is outstanding. The rebuilt Gatlinburg page makes enough requests
# (plus the 375px probe iframe) that one idle keep-alive socket held the queue
# and the suite hung on that page for 12+ minutes with an empty dump. Threaded,
# it finishes in 4 seconds, 80 pass.
socketserver.ThreadingTCPServer.allow_reuse_address = True
socketserver.ThreadingTCPServer.daemon_threads = True
with socketserver.ThreadingTCPServer(("127.0.0.1", port), H) as httpd:
    print("serving", root, "on", port, flush=True); httpd.serve_forever()
