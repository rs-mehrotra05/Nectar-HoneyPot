import sqlite3, json, sys, os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, ip TEXT, username TEXT, password TEXT,
        command TEXT, country TEXT, city TEXT, isp TEXT,
        port INTEGER, timestamp TEXT, raw_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT, start_time TEXT, end_time TEXT,
        total_cmds INTEGER DEFAULT 0, got_shell INTEGER DEFAULT 0)''')
    conn.commit(); conn.close()
    print("[DB] Initialised at", DB_PATH)

def log_event(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO events
        (type,ip,username,password,command,country,city,isp,port,timestamp,raw_data)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (
        data.get("type",""), data.get("ip",""),
        data.get("username",""), data.get("password",""),
        data.get("command",""), data.get("country",""),
        data.get("city",""), data.get("isp",""),
        data.get("port",0),
        data.get("timestamp", datetime.utcnow().isoformat()),
        json.dumps(data)))
    conn.commit(); conn.close()

def get_recent_events(limit=100):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close(); return rows

def get_top_ips(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT ip,country,COUNT(*) as total FROM events GROUP BY ip ORDER BY total DESC LIMIT ?", (limit,))
    rows = [{"ip":r[0],"country":r[1],"count":r[2]} for r in c.fetchall()]
    conn.close(); return rows

def get_top_passwords(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password,COUNT(*) as total FROM events WHERE password!='' GROUP BY password ORDER BY total DESC LIMIT ?", (limit,))
    rows = [{"password":r[0],"count":r[1]} for r in c.fetchall()]
    conn.close(); return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM events"); total = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT ip) FROM events"); unique_ips = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM events WHERE type='ssh_attempt'"); logins = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM events WHERE type='ssh_command'"); cmds = c.fetchone()[0]
    conn.close()
    return {"total_events":total,"unique_ips":unique_ips,"login_attempts":logins,"commands":cmds}
