"""Fester HTTP-Gateway vom lokalen Browser zur isolierten Juice-Shop-Instanz."""

from __future__ import annotations

import os
import socket
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


UPSTREAM_HOST = os.environ.get("UPSTREAM_HOST", "juice-shop")
UPSTREAM_PORT = int(os.environ.get("UPSTREAM_PORT", "3000"))
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "8081"))
HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}


class BrowserGateway(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _health(self) -> None:
        try:
            with socket.create_connection((UPSTREAM_HOST, UPSTREAM_PORT), timeout=2):
                pass
        except OSError:
            self.send_error(503, "Juice Shop ist noch nicht erreichbar")
            return
        payload = b"ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _proxy(self) -> None:
        if self.path == "/healthz":
            self._health()
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length) if content_length else None
        headers = {
            name: value
            for name, value in self.headers.items()
            if name.lower() not in HOP_BY_HOP and name.lower() != "host"
        }
        headers["Host"] = f"{UPSTREAM_HOST}:{UPSTREAM_PORT}"

        connection = HTTPConnection(UPSTREAM_HOST, UPSTREAM_PORT, timeout=30)
        try:
            connection.request(self.command, self.path, body=body, headers=headers)
            response = connection.getresponse()
            payload = response.read()
            self.send_response(response.status, response.reason)
            for name, value in response.getheaders():
                if name.lower() not in HOP_BY_HOP and name.lower() != "content-length":
                    self.send_header(name, value)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(payload)
        except OSError as error:
            self.send_error(502, f"Juice Shop nicht erreichbar: {error}")
        finally:
            connection.close()

    do_GET = _proxy
    do_HEAD = _proxy
    do_OPTIONS = _proxy
    do_POST = _proxy
    do_PUT = _proxy
    do_PATCH = _proxy
    do_DELETE = _proxy

    def do_CONNECT(self) -> None:  # noqa: N802
        self.send_error(405, "CONNECT ist nicht erlaubt")


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", LISTEN_PORT), BrowserGateway).serve_forever()
