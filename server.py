import http.server
import socketserver
import urllib.parse

PORT = 5000
DIRECTORY = "nadega_liquids_ready"

ROUTES = {
    "/liquids": "/liquids.html",
    "/disposables": "/disposables.html",
    "/pods": "/pods.html",
    "/admin": "/admin.html",
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def translate_path(self, path):
        parsed = urllib.parse.urlparse(path)
        clean = parsed.path.rstrip("/") or "/"
        if clean in ROUTES:
            path = ROUTES[clean]
        return super().translate_path(path)

    def log_message(self, format, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
