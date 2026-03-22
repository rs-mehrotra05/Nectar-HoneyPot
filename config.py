 
SSH_HOST = "0.0.0.0"
SSH_PORT = 2222
HTTP_HOST = "0.0.0.0"
HTTP_PORT = 8080
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000
DB_PATH = "honeypot.db"
 
BAIT_CREDENTIALS = {
    ("root",  "password"),
    ("root",  "root123"),
    ("admin", "admin"),
    ("pi",    "raspberry"),
}
 
SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5"
 
FAKE_RESPONSES = {
    "whoami":            "root",
    "id":                "uid=0(root) gid=0(root) groups=0(root)",
    "uname -a":          "Linux ubuntu 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux",
    "hostname":          "ubuntu-server",
    "pwd":               "/root",
    "ls":                "snap  Desktop  Documents  Downloads",
    "ls /":              "bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  srv  sys  tmp  usr  var",
    "ls /home":          "ubuntu  deploy  backup",
    "ls /etc":           "apt  bash.bashrc  crontab  fstab  group  hostname  hosts  passwd  shadow  ssh",
    "cat /etc/hostname": "ubuntu-server",
    "cat /etc/hosts":    "127.0.0.1   localhost\n127.0.1.1   ubuntu-server",
    "cat /etc/passwd":   "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon\nubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash",
    "cat /etc/shadow":   "root:$6$xyz$fakehashabcdef1234567890:19000:0:99999:7:::",
    "cat /etc/os-release":"NAME=\"Ubuntu\"\nVERSION=\"22.04.3 LTS (Jammy Jellyfish)\"",
    "ps aux":            "USER  PID  COMMAND\nroot    1   /sbin/init\nroot  523   sshd: root@pts/0\nroot  612   -bash",
    "ps":                "  PID TTY   TIME CMD\n  523 pts/0 00:00:00 bash",
    "ifconfig":          "eth0: flags=4163<UP,BROADCAST,RUNNING>\n      inet 192.168.1.105  netmask 255.255.255.0",
    "ip a":              "2: eth0: <BROADCAST,MULTICAST,UP>\n    inet 192.168.1.105/24 brd 192.168.1.255",
    "netstat -an":       "Proto Recv-Q Local Address   State\ntcp   0      0.0.0.0:22      LISTEN",
    "df -h":             "Filesystem  Size  Used Avail\n/dev/sda1    50G   12G   36G",
    "free -m":           "       total  used  free\nMem:    7982  1204  5431",
    "env":               "SHELL=/bin/bash\nUSER=root\nHOME=/root",
    "history":           "    1  nmap -sV 192.168.1.0/24\n    2  ssh root@192.168.1.105\n    3  ls",
    "crontab -l":        "no crontab for root",
    "uptime":            " 14:32:01 up 3 days, 1 user, load average: 0.02",
    "date":              "Mon Jan 13 14:32:01 UTC 2025",
    "w":                 "USER  TTY  FROM           LOGIN@\nroot  pts/0 45.142.212.100 14:30",
    "last":              "root  pts/0  45.142.212.100  Mon Jan 13 14:30",
}