# dashboard/app.py
# Flask web server — serves the dashboard and API endpoints.
#
# Routes:
#   GET /               → dashboard HTML page
#   GET /api/events     → latest 100 events as JSON
#   GET /api/stats      → summary numbers as JSON
#   GET /api/top_ips    → top attacking IPs as JSON
#   GET /api/passwords  → most-tried passwords as JSON

from flask import Flask, render_template, jsonify
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_recent_events, get_stats, get_top_ips, get_top_passwords

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/events")
def events():
    return jsonify(get_recent_events(100))


@app.route("/api/stats")
def stats():
    return jsonify(get_stats())


@app.route("/api/top_ips")
def top_ips():
    return jsonify(get_top_ips(10))


@app.route("/api/passwords")
def passwords():
    return jsonify(get_top_passwords(10))


def start_dashboard(host="0.0.0.0", port=5000):
    print(f"[DASH] http://{host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)