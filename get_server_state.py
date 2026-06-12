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
    ("=== shop.html ===", "cat /root/backend/shop.html"),
    ("=== payment.html ===", "cat /root/backend/payment.html"),
    ("=== login.html exists? ===", "ls -la /root/backend/login.html 2>/dev/null && cat /root/backend/login.html 2>/dev/null || echo 'NO LOGIN.HTML'"),
    ("=== frontend index.html ===", "cat /var/www/frontend/index.html"),
    ("=== routes dir ===", "ls -la /root/backend/routes/ 2>/dev/null"),
    ("=== auth route ===", "cat /root/backend/routes/auth.js 2>/dev/null || echo 'NO AUTH ROUTE'"),
    ("=== payment route ===", "cat /root/backend/routes/payment.js 2>/dev/null || echo 'NO PAYMENT ROUTE'"),
    ("=== data dir ===", "ls -la /root/backend/data/ 2>/dev/null"),
    ("=== Check auth/user routes ===", "grep -n 'login\\|register\\|auth\\|user\\|session\\|jwt\\|token\\|passport' /root/backend/server-v4.js 2>/dev/null"),
]

for label, cmd in cmds:
    print(label)
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out: print(out[:50000])  # Limit output
    if err: print("STDERR:", err)
    print()

client.close()
