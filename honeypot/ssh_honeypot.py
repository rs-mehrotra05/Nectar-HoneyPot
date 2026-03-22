# honeypot/ssh_honeypot.py

import socket
import threading
import paramiko
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SSH_HOST, SSH_PORT, SSH_BANNER, BAIT_CREDENTIALS, FAKE_RESPONSES
from database.db import log_event
from analysis.geoip import get_geo

# Generate RSA host key — every SSH server needs this
HOST_KEY = paramiko.RSAKey.generate(2048)


class HoneypotServer(paramiko.ServerInterface):

    def __init__(self, client_ip):
        self.client_ip     = client_ip
        self.attempts      = 0
        self.shell_granted = False
        self.shell_event   = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        self.attempts += 1
        geo = get_geo(self.client_ip)
        ts  = datetime.utcnow().isoformat()

        print(f"[SSH] {self.client_ip} tried {username}:{password}")

        log_event({
            "type":      "ssh_attempt",
            "ip":        self.client_ip,
            "username":  username,
            "password":  password,
            "port":      SSH_PORT,
            "country":   geo.get("country", ""),
            "city":      geo.get("city",    ""),
            "isp":       geo.get("isp",     ""),
            "timestamp": ts,
        })

        if (username, password) in BAIT_CREDENTIALS:
            print(f"[SSH] *** BAIT ACCEPTED *** {username}:{password} from {self.client_ip}")
            log_event({
                "type":      "bait_accepted",
                "ip":        self.client_ip,
                "username":  username,
                "password":  password,
                "port":      SSH_PORT,
                "country":   geo.get("country", ""),
                "city":      geo.get("city",    ""),
                "isp":       geo.get("isp",     ""),
                "timestamp": ts,
            })
            self.shell_granted = True
            return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED

    def check_channel_shell_request(self, channel):
        self.shell_event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height,
                                   pixelwidth, pixelheight, modes):
        return True

    def get_allowed_auths(self, username):
        return "password"


def get_fake_response(cmd: str) -> str:
    if cmd in FAKE_RESPONSES:
        return FAKE_RESPONSES[cmd]

    for key in FAKE_RESPONSES:
        if cmd.startswith(key.split()[0]):
            return FAKE_RESPONSES[key]

    blocked = ["curl", "wget", "nc ", "netcat", "python -c", "bash -i", "perl"]
    if any(b in cmd for b in blocked):
        return ""

    return f"-bash: {cmd.split()[0]}: command not found"


def fake_shell(channel, client_ip):
    geo = get_geo(client_ip)

    channel.send(b"\r\nWelcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-91-generic x86_64)\r\n")
    channel.send(b"\r\n * Documentation:  https://help.ubuntu.com\r\n")
    channel.send(b"\r\nLast login: Mon Jan 13 09:12:44 2025 from 192.168.0.1\r\n")
    channel.send(b"root@ubuntu:~# ")

    cmd_buffer = ""

    while True:
        try:
            data = channel.recv(1024)
            if not data:
                break

            for char in data.decode("utf-8", errors="ignore"):
                if char in ("\r", "\n"):
                    cmd = cmd_buffer.strip()
                    cmd_buffer = ""
                    channel.send(b"\r\n")

                    if not cmd:
                        channel.send(b"root@ubuntu:~# ")
                        continue

                    print(f"[SSH] {client_ip} ran: {cmd}")
                    log_event({
                        "type":      "ssh_command",
                        "ip":        client_ip,
                        "command":   cmd,
                        "port":      SSH_PORT,
                        "country":   geo.get("country", ""),
                        "city":      geo.get("city",    ""),
                        "isp":       geo.get("isp",     ""),
                        "timestamp": datetime.utcnow().isoformat(),
                    })

                    if cmd in ("exit", "logout", "quit"):
                        channel.send(b"logout\r\n")
                        channel.close()
                        return

                    response = get_fake_response(cmd)
                    if response:
                        for line in response.split("\n"):
                            channel.send((line + "\r\n").encode())
                    channel.send(b"root@ubuntu:~# ")

                elif char in ("\x7f", "\x08"):
                    if cmd_buffer:
                        cmd_buffer = cmd_buffer[:-1]
                        channel.send(b"\x08 \x08")
                else:
                    cmd_buffer += char
                    channel.send(char.encode())

        except Exception as e:
            print(f"[SSH] Shell error {client_ip}: {e}")
            break

    channel.close()


def handle_connection(client_socket, client_addr):
    client_ip = client_addr[0]
    print(f"[SSH] Connection from {client_ip}")
    transport = None
    try:
        transport = paramiko.Transport(client_socket)
        transport.local_version = SSH_BANNER
        transport.add_server_key(HOST_KEY)
        server = HoneypotServer(client_ip)
        transport.start_server(server=server)
        channel = transport.accept(30)
        if channel is None:
            return
        if server.shell_granted:
            server.shell_event.wait(10)
            fake_shell(channel, client_ip)
        else:
            channel.close()
    except Exception as e:
        print(f"[SSH] Error {client_ip}: {e}")
    finally:
        if transport:
            transport.close()


def start_ssh_honeypot(host=SSH_HOST, port=SSH_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    print(f"[SSH] Listening on {host}:{port}")
    while True:
        try:
            client_sock, client_addr = sock.accept()
            t = threading.Thread(
                target=handle_connection,
                args=(client_sock, client_addr),
                daemon=True
            )
            t.start()
        except Exception as e:
            print(f"[SSH] Accept error: {e}")