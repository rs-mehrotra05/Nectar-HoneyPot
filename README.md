# Nectar — SSH and HTTP HoneyPot
 
> A cybersecurity honeypot system that traps attackers in a fake server, silently logs every move they make, and displays it all on a live real-time dashboard.
 
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=flat-square&logo=flask)
![Paramiko](https://img.shields.io/badge/Paramiko-3.4.0-orange?style=flat-square)
![SQLite](https://img.shields.io/badge/Database-SQLite-green?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)
 
---
 
## Nectar — SSH and HTTP HoneyPot — What is this Project?
 
Nectar is a Python-based honeypot system built as a 3rd Year CSE Cybersecurity project. It creates two fake servers — a fake SSH server and a fake HTTP admin website — that look real to an attacker. When an attacker connects and tries to break in, every single action they take is silently captured and stored. A live web dashboard shows all attack events in real time including the attacker's IP address, the passwords they tried, the commands they ran, and their geographic location.
 
The attacker thinks they found a vulnerable server. In reality they walked into a trap.
 
---
 
## Nectar — SSH and HTTP HoneyPot — How it Works
 
```
Attacker scans the network
        ↓
Finds Nectar on port 2222 (SSH) or port 8080 (HTTP)
        ↓
Tries to brute force login — every attempt is logged
        ↓
Enters bait password (e.g. root:password) — accepted on purpose
        ↓
Gets a fake Ubuntu shell — looks completely real
        ↓
Runs commands (whoami, cat /etc/passwd, ls) — all logged
        ↓
Tries to download malware — silently blocked and logged
        ↓
Types exit — session ends — full report saved to database
        ↓
Live dashboard shows everything in real time
```
 
---
 
## Nectar — SSH and HTTP HoneyPot — Project Structure
 
```
Nectar/
├── config.py                      ← All settings in one place
├── main.py                        ← Entry point — starts everything
├── requirements.txt               ← Libraries to install
├── honeypot/
│   ├── __init__.py
│   ├── ssh_honeypot.py            ← Fake SSH server (Paramiko)
│   └── http_honeypot.py          ← Fake HTTP web server
├── database/
│   ├── __init__.py
│   └── db.py                      ← SQLite database operations
├── analysis/
│   ├── __init__.py
│   └── geoip.py                   ← IP geolocation lookup
└── dashboard/
    ├── __init__.py
    ├── app.py                     ← Flask API and web server
    └── templates/
        └── index.html             ← Live monitoring dashboard UI
```
 
---
 
## Nectar — SSH and HTTP HoneyPot — Tech Stack
 
| Technology | Purpose |
|---|---|
| Python 3.8+ | Core programming language |
| Paramiko | SSH server emulation — handles full SSH protocol |
| Flask | Web framework — serves dashboard and REST API |
| SQLite | File-based database — stores all attack events |
| Requests | HTTP calls to ip-api.com for geolocation |
| Threading | Runs SSH, HTTP, and dashboard simultaneously |
| HTML / CSS / JS | Dashboard frontend — live event feed |
| ip-api.com | Free geolocation API — country, city, ISP from IP |
 
---
 
## Nectar — SSH and HTTP HoneyPot — Installation
 
### Step 1 — Clone the repository
 
```bash
git clone https://github.com/yourusername/Nectar.git
cd Nectar
```
 
### Step 2 — Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### Step 3 — Run Nectar
 
```bash
python main.py
```
 
You will see this in the terminal:
 
```
[DB]   Ready → honeypot.db
[SSH]  Listening on 0.0.0.0:2222
[HTTP] Listening on 0.0.0.0:8080
[DASH] http://0.0.0.0:5000
[*]    Press Ctrl+C to stop
```
 
### Step 4 — Open the dashboard
 
Open your browser and go to:
 
```
http://localhost:5000
```
 
---
 
## Nectar — SSH and HTTP HoneyPot — Testing
 
### Test the SSH Honeypot
 
Open a second terminal window and run:
 
```bash
ssh root@localhost -p 2222
```
 
Try a wrong password first — it will appear as a LOGIN event on the dashboard:
 
```
password: wrongpass     →  FAILED  — logged to dashboard
password: 123456        →  FAILED  — logged to dashboard
password: password      →  SUCCESS — bait accepted — fake shell opens
```
 
Once inside the fake shell, run these commands and watch them appear live on the dashboard:
 
```bash
whoami
id
uname -a
cat /etc/passwd
cat /etc/shadow
ls /home
ls /etc
ps aux
ifconfig
df -h
free -m
history
uptime
exit
```
 
### Test the HTTP Honeypot
 
Open these URLs in your browser:
 
```
http://localhost:8080
http://localhost:8080/admin
http://localhost:8080/wp-admin
http://localhost:8080/phpmyadmin
http://localhost:8080/panel
```
 
Each one shows a fake admin login page. Enter any username and password and click submit — the credentials will be logged and appear as an HTTP event on the dashboard.
 
---
 
## Nectar — SSH and HTTP HoneyPot — Dashboard Features
 
| Feature | Description |
|---|---|
| Live Event Log | Every attack event appears in real time with color-coded badges |
| Total Events Card | Running count of all honeypot activity |
| Login Attempts Card | Count of SSH brute-force attempts |
| Commands Logged Card | Count of commands run inside fake shell |
| Unique IPs Card | Number of distinct attacking IP addresses |
| Top Attacker IPs | Table showing most active attackers with attack count bar |
| Most-Tried Passwords | List of passwords attackers commonly try |
| Geo Intelligence | Country, city, ISP of the last attacker |
 
The dashboard auto-refreshes every 3 seconds — no manual page reload needed.
 
---
 
## Nectar — SSH and HTTP HoneyPot — Bait Credentials
 
Bait credentials are passwords the honeypot deliberately accepts. When an attacker tries one, they are let into the fake shell. These are defined in `config.py`:
 
```python
BAIT_CREDENTIALS = {
    ("root",  "password"),
    ("root",  "root123"),
    ("admin", "admin"),
    ("root",  "toor"),
    ("pi",    "raspberry"),
}
```
 
You can add or remove any bait credential by editing this file. No other code needs to change.
 
---
 
## Nectar — SSH and HTTP HoneyPot — Demo on Another Device
 
### Step 1 — Find your IP address
 
```bash
# Windows
ipconfig
 
# Linux / Mac
ifconfig
```
 
Look for the IPv4 address under your WiFi adapter, for example `192.168.1.105`.
 
### Step 2 — Allow ports through Windows Firewall
 
Run PowerShell as Administrator:
 
```powershell
netsh advfirewall firewall add rule name="Nectar SSH"       dir=in action=allow protocol=TCP localport=2222
netsh advfirewall firewall add rule name="Nectar HTTP"      dir=in action=allow protocol=TCP localport=8080
netsh advfirewall firewall add rule name="Nectar Dashboard" dir=in action=allow protocol=TCP localport=5000
```
 
### Step 3 — Connect from another device on the same WiFi
 
| Action | Address |
|---|---|
| View dashboard | `http://192.168.1.105:5000` |
| SSH attack | `ssh root@192.168.1.105 -p 2222` |
| HTTP attack | `http://192.168.1.105:8080` |
 
Replace `192.168.1.105` with your actual IP address.
 
---
 
## Nectar — SSH and HTTP HoneyPot — MITRE ATT&CK Mapping
 
Every attack Nectar captures maps to a real MITRE ATT&CK technique:
 
| Technique ID | Name | How Nectar Captures It |
|---|---|---|
| T1046 | Network Service Scanning | Port scans on 2222 and 8080 logged |
| T1110.001 | Password Brute Force | All SSH login attempts logged with credentials |
| T1078 | Valid Accounts | Bait credential acceptance logged as bait_accepted |
| T1059 | Command and Scripting | All commands in fake shell logged |
| T1041 | Exfiltration over C2 | curl and wget attempts blocked and logged |
| T1083 | File and Directory Discovery | ls and cat commands logged |
| T1082 | System Information Discovery | whoami, uname, id commands logged |
| T1087 | Account Discovery | cat /etc/passwd, w, last, who logged |
 
---
 
## Nectar — SSH and HTTP HoneyPot — Database
 
All events are saved to `honeypot.db` (SQLite). You can view them directly:
 
```bash
sqlite3 honeypot.db
 
# Inside SQLite shell:
.tables
SELECT * FROM events ORDER BY id DESC LIMIT 20;
SELECT ip, COUNT(*) as total FROM events GROUP BY ip ORDER BY total DESC;
SELECT password, COUNT(*) as total FROM events WHERE password != '' GROUP BY password ORDER BY total DESC;
.quit
```
 
The events table stores:
 
```
id, type, ip, username, password, command,
country, city, isp, port, timestamp, raw_data
```
 
---
 
## Nectar — SSH and HTTP HoneyPot — Safety and Ethics
 
> This project is for educational and research purposes only.
 
- Run inside a **controlled local network** — not on public internet
- Use **port 2222** instead of 22 — avoids needing administrator privileges
- All outbound connections from the fake shell are **blocked** — attacker cannot download malware
- The fake shell **never executes real OS commands** — all responses are pre-programmed strings
- Never deploy on a **college or office network** without written permission from the network administrator
- The attacker **never touches your real operating system** at any point
---
 
## Nectar — SSH and HTTP HoneyPot — Future Enhancements
 
- [ ] Email or SMS alert when bait credential is accepted
- [ ] World map showing attack origins using Leaflet.js
- [ ] FTP honeypot on port 21
- [ ] MySQL honeypot on port 3306
- [ ] Machine learning threat level classification
- [ ] Docker containerization for safe isolated deployment
- [ ] Session recording and replay capability
- [ ] Offline geolocation using MaxMind GeoLite2 database
- [ ] Integration with Splunk or ELK Stack SIEM
- [ ] Distributed honeypot network on AWS or Azure
---
 
## Nectar — SSH and HTTP HoneyPot — Requirements
 
```
paramiko==3.4.0
flask==3.0.0
requests==2.31.0
```
 
Install all with:
 
```bash
pip install -r requirements.txt
```
 
---
 
## Nectar — SSH and HTTP HoneyPot — Quick Reference
 
| What | Command |
|---|---|
| Start Nectar | `python main.py` |
| Open dashboard | `http://localhost:5000` |
| SSH attack (same machine) | `ssh root@localhost -p 2222` |
| HTTP attack (same machine) | `http://localhost:8080` |
| View database | `sqlite3 honeypot.db` |
| Stop Nectar | `Ctrl + C` |
 
---
 
## Nectar — SSH and HTTP HoneyPot — Acknowledgements
 
- [Paramiko](https://www.paramiko.org/) — Python SSH library used to build the fake SSH server
- [Flask](https://flask.palletsprojects.com/) — Lightweight web framework for the dashboard
- [ip-api.com](http://ip-api.com/) — Free IP geolocation API
- [Cowrie](https://github.com/cowrie/cowrie) — Open source SSH honeypot that inspired the design
- [MITRE ATT&CK](https://attack.mitre.org/) — Framework used to classify captured attack techniques
---
 
## Nectar — SSH and HTTP HoneyPot — License
 
This project is licensed under the MIT License.
 
---
 
> **Built as a 3rd Year CSE Cybersecurity Project — 2025**
>
> *The attacker thinks they won. We planned it from the beginning.*
