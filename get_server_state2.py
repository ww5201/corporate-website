import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

cmds = [
    ("=== shop.html full ===", "cat /root/backend/shop.html"),
    ("=== login.html full ===", "cat /root/backend/login.html 2>/dev/null || echo 'NO LOGIN.HTML ON SERVER'"),
    ("=== login.html in frontend? ===", "ls -la /var/www/frontend/login.html 2>/dev/null || echo 'NO LOGIN IN FRONTEND'"),
    ("=== nginx login route ===", "grep -A3 'login' /etc/nginx/conf.d/site.conf 2>/dev/null"),
    ("=== curl login.html ===", "curl -sI http://localhost/login.html 2>/dev/null | head -5"),
    ("=== curl shop.html ===", "curl -sI http://localhost/shop.html 2>/dev/null | head -5"),
    ("=== backend shop.html route check ===", "curl -sI http://localhost:3000/shop.html 2>/dev/null | head -5"),
    ("=== backend login.html route check ===", "curl -sI http://localhost:3000/login.html 2>/dev/null | head -5"),
    ("=== Check if server serves login ===", "grep -n 'login' /root/backend/server-v4.js"),
]

for label, cmd in cmds:
    print(label)
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out: print(out[:30000])
    if err: print("STDERR:", err)
    print()

client.close()
