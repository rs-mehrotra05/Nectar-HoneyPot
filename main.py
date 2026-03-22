# main.py — Entry point. Starts everything.
#
# HOW IT WORKS:
# Python can only do one thing at a time normally.
# We use THREADS so SSH, HTTP, and the dashboard all run simultaneously.
# threading.Thread creates a separate "lane" for each service.

import threading
import sys
import os

# Add current directory to path so imports work
sys.path.insert(0, os.path.dirname(__file__))

from config import SSH_HOST, SSH_PORT, HTTP_HOST, HTTP_PORT, DASHBOARD_HOST, DASHBOARD_PORT
from database.db import init_db
from honeypot.ssh_honeypot import start_ssh_honeypot
from honeypot.http_honeypot import start_http_honeypot
from dashboard.app import start_dashboard


def main():
    print("""
    ██╗  ██╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗
    ██║  ██║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝
    ███████║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝
    ██╔══██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝
    ██║  ██║╚██████╔╝██║ ╚████║███████╗   ██║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝
         Nectar — SSH/HTTP Honeypot v1.0
    """)

    # Step 1: Initialize database (creates honeypot.db)
    init_db()

    # Step 2: Start SSH honeypot in background thread
    # daemon=True means the thread stops when main program stops
    t_ssh = threading.Thread(
        target=start_ssh_honeypot,
        args=(SSH_HOST, SSH_PORT),
        daemon=True
    )
    t_ssh.start()

    # Step 3: Start HTTP honeypot in background thread
    t_http = threading.Thread(
        target=start_http_honeypot,
        args=(HTTP_HOST, HTTP_PORT),
        daemon=True
    )
    t_http.start()

    # Step 4: Start dashboard (this blocks — runs in main thread)
    # Open http://localhost:5000 in your browser to see it
    print(f"\n[*] Dashboard → http://localhost:{DASHBOARD_PORT}")
    print(f"[*] SSH Honeypot → port {SSH_PORT}")
    print(f"[*] HTTP Honeypot → port {HTTP_PORT}")
    print("[*] Press Ctrl+C to stop\n")

    try:
        start_dashboard(DASHBOARD_HOST, DASHBOARD_PORT)
    except KeyboardInterrupt:
        print("\n[*] Shutting down HoneyShield...")


if __name__ == "__main__":
    main()