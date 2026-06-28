#!/usr/bin/env python3
"""Dev server for engine.html.

The live love.js preview needs SharedArrayBuffer, which only exists in a
cross-origin-isolated page — so it cannot run from file://. This serves the
current folder with the required isolation headers and opens engine.html for
you. One command, no dependencies (Python 3 standard library only):

    python3 serve.py [port]      # default port 8000

COEP is set to `credentialless` so the CDN-loaded runtime (love.js, CodeMirror,
marked) still loads under isolation without needing per-resource CORP headers.
For a static host you don't control (e.g. GitHub Pages), use the bundled
coi-serviceworker.js instead — engine.html registers it automatically.
"""
import http.server
import socketserver
import sys
import threading
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass  # quiet


def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        url = "http://localhost:%d/engine.html" % PORT
        print("engine.html dev server  →  %s" % url)
        print("Cross-origin isolated (COOP/COEP) so the love.js preview works.")
        print("Ctrl+C to stop.")
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
