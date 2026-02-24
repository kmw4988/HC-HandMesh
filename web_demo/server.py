"""Local HTTPS server with COOP/COEP headers for SharedArrayBuffer (WASM multi-threading)."""

import http.server
import ssl
import os
import sys


class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    script_dir = os.path.dirname(os.path.abspath(__file__))
    certfile = os.path.join(script_dir, "cert.pem")
    keyfile = os.path.join(script_dir, "key.pem")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile, keyfile)

    with http.server.HTTPServer(("0.0.0.0", port), CORSHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        import socket
        ip_addr = socket.gethostbyname(socket.gethostname())
        # Try to get the actual LAN IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_addr = s.getsockname()[0]
            s.close()
        except Exception:
            pass

        print(f"Serving on (HTTPS with COOP/COEP headers):")
        print(f"  Local:   https://localhost:{port}")
        print(f"  Network: https://{ip_addr}:{port}")
        httpd.serve_forever()
