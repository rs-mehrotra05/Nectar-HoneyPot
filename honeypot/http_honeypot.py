# honeypot/http_honeypot.py
# Fake HTTP server that looks like a real admin panel.
# Logs every request attackers make (scanning, login attempts).

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HTTP_HOST, HTTP_PORT
from database.db import log_event
from analysis.geoip import get_geo

FAKE_LOGIN_PAGE = b"""<!DOCTYPE html>
<html><head><title>Admin Login</title>
<style>
body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
.box{background:white;padding:40px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.15);width:340px}
h2{color:#1a1a2e;text-align:center;margin-bottom:24px;font-size:22px}
input{width:100%;padding:11px;margin:7px 0;border:1px solid #ddd;border-radius:5px;box-sizing:border-box;font-size:14px}
button{width:100%;padding:12px;background:#0066cc;color:white;border:none;border-radius:5px;cursor:pointer;font-size:15px;margin-top:8px}
button:hover{background:#0052a3}
p{text-align:center;color:#888;font-size:12px;margin-top:16px}
</style></head>
<body><div class="box">
<h2>Administrator Login</h2>
<form method="POST" action="/login">
<input type="text"     name="username" placeholder="Username" required/>
<input type="password" name="password" placeholder="Password" required/>
<button type="submit">Sign In</button>
</form>
<p>Powered by Apache/2.4.41 (Ubuntu)</p>
</div></body></html>"""

FAKE_404 = b"""<!DOCTYPE html><html><head><title>404 Not Found</title></head>
<body><h1>Not Found</h1><p>The requested URL was not found on this server.</p>
<hr><address>Apache/2.4.41 (Ubuntu)</address></body></html>"""


class HoneypotHTTPHandler(BaseHTTPRequestHandler):

    def _log(self, method, body=""):
        ip = self.client_address[0]
        geo = get_geo(ip)
        print(f"[HTTP] {ip} {method} {self.path}")
        log_event({
            "type":       "http_request",
            "ip":         ip,
            "command":    f"{method} {self.path}",
            "port":       HTTP_PORT,
            "country":    geo.get("country", ""),
            "city":       geo.get("city",    ""),
            "isp":        geo.get("isp",     ""),
            "timestamp":  datetime.utcnow().isoformat(),
            "user_agent": self.headers.get("User-Agent", ""),
            "body":       body,
        })

    def do_GET(self):
        self._log("GET")
        admin_paths = ["/", "/admin", "/login", "/wp-admin",
                       "/phpmyadmin", "/panel", "/dashboard", "/manager"]
        if self.path.rstrip("/") in admin_paths or self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Server", "Apache/2.4.41 (Ubuntu)")
            self.end_headers()
            self.wfile.write(FAKE_LOGIN_PAGE)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(FAKE_404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="ignore")
        self._log("POST", body=body)
        self.send_response(302)
        self.send_header("Location", "/login")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress default output


def start_http_honeypot(host=HTTP_HOST, port=HTTP_PORT):
    server = HTTPServer((host, port), HoneypotHTTPHandler)
    print(f"[HTTP] Listening on {host}:{port}")
    server.serve_forever()